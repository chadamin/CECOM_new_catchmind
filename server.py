from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
import clip
from PIL import Image
import io

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
# CLIP model (1회 로드)
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# =========================
# 🔹 2차원 라벨 구조
# =========================
LABELS = {
    "animal": ["cat", "dog"],
    "object": ["car", "house", "tree"],
    "human": ["person", "face", "hand"],
    "shape": ["triangle", "circle", "square"],
}

# 1차원으로 펼치기
ALL_LABELS = []
LABEL_TO_CATEGORY = {}

for category, labels in LABELS.items():
    for label in labels:
        ALL_LABELS.append(label)
        LABEL_TO_CATEGORY[label] = category

# =========================
# CLIP API
# =========================
@app.post("/clip-test")
async def clip_test(image: UploadFile = File(...)):
    # 이미지 로드
    image_bytes = await image.read()
    image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_input = preprocess(image_pil).unsqueeze(0).to(device)

    # CLIP 프롬프트 (drawing 최적화)
    texts = [f"a simple hand-drawn sketch of a {label}" for label in ALL_LABELS]
    text_tokens = clip.tokenize(texts).to(device)

    # 추론
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_tokens)
        similarity = (image_features @ text_features.T).softmax(dim=-1)[0]

    best_idx = similarity.argmax().item()
    best_label = ALL_LABELS[best_idx]
    confidence = float(similarity[best_idx])
    category = LABEL_TO_CATEGORY[best_label]

    # =========================
    # confidence 기반 상태
    # =========================
    if confidence >= 0.25:
        status = "strong"
    elif confidence >= 0.15:
        status = "medium"
    elif confidence >= 0.08:
        status = "weak"
    else:
        status = "unknown"

    # 🔍 디버그 로그 (중요)
    print("DEBUG →", category, best_label, round(confidence, 3))

    return {
        "category": category,
        "guess": best_label,
        "confidence": round(confidence, 2),
        "status": status
    }
