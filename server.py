from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
import clip
from PIL import Image
import io
import numpy as np
import cv2

# =========================
# FastAPI
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "server alive"}

# =========================
# CLIP MODEL
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# =========================
# LABELS
# =========================
LABELS = {
    "animal": ["cat", "dog", "lion", "elephant", "rabbit", "fish", "bird"],
    "vehicle": ["car", "bus", "bicycle", "train", "airplane"],
    "object": ["chair", "clock", "book", "cup", "scissors", "key"],
    "food": ["pizza", "hamburger", "ice cream", "banana"]
}

CATEGORY_LIST = list(LABELS.keys())

LABELS_KO = {
    "animal": "동물",
    "vehicle": "탈것",
    "object": "사물",
    "food": "음식",

    "cat": "고양이",
    "dog": "강아지",
    "lion": "사자",
    "elephant": "코끼리",
    "rabbit": "토끼",
    "fish": "물고기",
    "whale": "고래",

    "car": "자동차",
    "bus": "버스",
    "airplane": "비행기",
    "bicycle": "자전거",
    "train": "기차",
    "rocket": "로켓",
    "ship": "배",

    "pizza": "피자",
    "hamburger": "햄버거",
    "cake": "케이크",
    "ice cream": "아이스크림",
    "donut": "도넛",
    "banana": "바나나",
    "sandwich": "샌드위치",

    "apple": "사과",
    "chair": "의자",
    "clock": "시계",
    "book": "책",
    "phone": "휴대폰",
    "cup": "컵"
}

# =========================
# Edge preprocessing (완화)
# =========================
def extract_edges(image):

    img_np = np.array(image)

    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    edges = cv2.Canny(gray, 80, 180)

    result = np.ones((edges.shape[0], edges.shape[1], 3), dtype=np.uint8) * 255
    result[edges != 0] = [0, 0, 0]

    return Image.fromarray(result)

# =========================
# Square padding
# =========================
def square_pad(image, fill_color=(255,255,255)):

    w,h = image.size
    max_dim = max(w,h)

    new_img = Image.new("RGB",(max_dim,max_dim),fill_color)
    new_img.paste(image,((max_dim-w)//2,(max_dim-h)//2))

    return new_img

# =========================
# Prompt templates (CLIP sketch 최적)
# =========================
PROMPT_TEMPLATES = [
    "a simple sketch of a {}",
    "a doodle of a {}",
    "a line drawing of a {}"
]

# =========================
# TEXT FEATURE CACHE
# =========================
TEXT_FEATURE_CACHE = {}

def get_text_features(labels):

    key = tuple(labels)

    if key in TEXT_FEATURE_CACHE:
        return TEXT_FEATURE_CACHE[key]

    prompts = []

    for label in labels:
        for template in PROMPT_TEMPLATES:
            prompts.append(template.format(label))

    tokens = clip.tokenize(prompts).to(device)

    with torch.no_grad():
        text_features = model.encode_text(tokens)

        text_features /= text_features.norm(dim=-1, keepdim=True)

    TEXT_FEATURE_CACHE[key] = text_features

    return text_features

# =========================
# CLIP inference
# =========================
def clip_inference(image_input, labels):

    text_features = get_text_features(labels)

    with torch.no_grad():

        image_features = model.encode_image(image_input)

        image_features /= image_features.norm(dim=-1, keepdim=True)

        logit_scale = model.logit_scale.exp()

        similarity = logit_scale * (image_features @ text_features.T)

        similarity = similarity.reshape(len(labels), len(PROMPT_TEMPLATES))

        similarity = similarity.mean(dim=1)

        probs = similarity.softmax(dim=0)

    best_idx = probs.argmax().item()

    return labels[best_idx], probs[best_idx].item()

# =========================
# API
# =========================
@app.post("/clip-test")
async def clip_test(image: UploadFile = File(...)):

    image_bytes = await image.read()

    image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # edge
    image_pil = extract_edges(image_pil)

    # padding
    image_pil = square_pad(image_pil)

    image_input = preprocess(image_pil).unsqueeze(0).to(device)

    # =====================
    # 1️⃣ CATEGORY
    # =====================
    best_category, category_conf = clip_inference(image_input, CATEGORY_LIST)

    if category_conf < 0.20:
        return {
            "status":"unknown",
            "category":None,
            "category_ko":None,
            "guess":None,
            "guess_ko":None,
            "confidence":round(category_conf,2)
        }

    # =====================
    # 2️⃣ SUB LABEL
    # =====================
    sub_labels = LABELS[best_category]

    best_label, label_conf = clip_inference(image_input, sub_labels)

    # =====================
    # confidence level
    # =====================
    if label_conf >= 0.30:
        status = "strong"
    elif label_conf >= 0.18:
        status = "medium"
    elif label_conf >= 0.10:
        status = "weak"
    else:
        status = "unknown"

    print("DEBUG →", best_category, best_label, round(label_conf,3))

    return {
        "status":status,
        "category":best_category,
        "category_ko":LABELS_KO.get(best_category,best_category),
        "guess":best_label,
        "guess_ko":LABELS_KO.get(best_label,best_label),
        "confidence":round(label_conf,2)
    }