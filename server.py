from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
import clip
from PIL import Image
import io

app = FastAPI()

# ✅ CORS (웹 연동 필수)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 개발 단계
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "server alive"}

# 🔹 CLIP 모델은 서버 시작 시 1번만 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 🔹 게임에서 사용할 후보 단어들
CANDIDATES = [
    "cat",
    "dog",
    "car",
    "house",
    "tree",
    "person",
    "handwritten drawing"
]

@app.post("/clip-test")
async def clip_test(image: UploadFile = File(...)):
    # 이미지 로드
    image_bytes = await image.read()
    image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_input = preprocess(image_pil).unsqueeze(0).to(device)

    # CLIP 텍스트 프롬프트
    texts = [f"a drawing of a {c}" for c in CANDIDATES]
    text_tokens = clip.tokenize(texts).to(device)

    # CLIP 추론
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        text_features = model.encode_text(text_tokens)
        similarity = (image_features @ text_features.T).softmax(dim=-1)[0]

    best_idx = similarity.argmax().item()

    # ✅ 프론트에서 바로 쓰기 좋은 형태
    return {
        "guess": CANDIDATES[best_idx],
        "confidence": round(float(similarity[best_idx]), 2)
    }
