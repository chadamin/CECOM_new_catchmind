from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
import clip
from PIL import Image
import io
import numpy as np
import cv2

# =========================
# App
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
# CLIP Model (1회 로드)
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# =========================
# 2단계 라벨 구조 (8 카테고리 / 50 세부)
# =========================
LABELS = {
    "animal": ["cat", "dog", "lion", "elephant", "rabbit", "fish", "whale"],
    "shape": ["triangle", "square", "circle", "star", "heart", "arrow", "crescent moon"],
    "vehicle": ["car", "bus", "airplane", "bicycle", "train", "rocket","ship"],
    "nature": ["tree", "flower", "sun", "cloud", "mountain", "snowman"],
    "human": ["face", "hand", "eye", "nose", "ear", "mouse", "feet"],
    "object": ["apple", "banana", "phone", "clock", "chair", "cup", "book"]
}

CATEGORY_LIST = list(LABELS.keys())

# =========================
# 🔥 Edge 기반 전처리 함수
# =========================
def extract_edges(image):
    img_np = np.array(image)

    # 1. grayscale
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

    # 2. blur (노이즈 제거)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Canny edge detection
    edges = cv2.Canny(blur, 50, 150)

    # 4. 선 두껍게
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # 5. 흰 배경 + 검은 선 재구성
    result = np.ones((edges.shape[0], edges.shape[1], 3), dtype=np.uint8) * 255
    result[edges != 0] = [0, 0, 0]

    return Image.fromarray(result)

# =========================
# 정사각 패딩
# =========================
def square_pad(image, fill_color=(255, 255, 255)):
    w, h = image.size
    max_dim = max(w, h)
    new_img = Image.new("RGB", (max_dim, max_dim), fill_color)
    new_img.paste(image, ((max_dim - w) // 2, (max_dim - h) // 2))
    return new_img

# =========================
# CLIP 추론 함수
# =========================
def clip_inference(image_input, labels):
    prompts = [f"a black outline drawing of a {l}" for l in labels]
    text_tokens = clip.tokenize(prompts).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_tokens)
        similarity = (image_features @ text_features.T).softmax(dim=-1)[0]

    best_idx = similarity.argmax().item()
    confidence = float(similarity[best_idx])

    return labels[best_idx], confidence


# =========================
# 2단계 분류 엔드포인트
# =========================
@app.post("/clip-test")
async def clip_test(image: UploadFile = File(...)):
    image_bytes = await image.read()
    image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # 🔥 Edge 전처리 적용
    image_pil = extract_edges(image_pil)

    # 🔥 정사각 패딩
    image_pil = square_pad(image_pil)

    image_input = preprocess(image_pil).unsqueeze(0).to(device)

    # =====================
    # 1️⃣ 카테고리 분류
    # =====================
    best_category, category_conf = clip_inference(image_input, CATEGORY_LIST)

    if category_conf < 0.20:
        return {
            "status": "unknown",
            "category": None,
            "guess": None,
            "confidence": round(category_conf, 2)
        }

    # =====================
    # 2️⃣ 세부 라벨 분류
    # =====================
    sub_labels = LABELS[best_category]
    best_label, label_conf = clip_inference(image_input, sub_labels)

    # =====================
    # Confidence 판단
    # =====================
    if label_conf >= 0.30:
        status = "strong"
    elif label_conf >= 0.18:
        status = "medium"
    elif label_conf >= 0.10:
        status = "weak"
    else:
        status = "unknown"

    print("DEBUG →", best_category, best_label, round(label_conf, 3))

    return {
        "status": status,
        "category": best_category,
        "guess": best_label,
        "confidence": round(label_conf, 2)
    }