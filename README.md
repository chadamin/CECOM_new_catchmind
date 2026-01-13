# 🎨 AI 캐치마인드 (AI Catchmind)
사용자가 제한 시간 안에 그림을 그리면,
AI가 해당 그림을 분석하여 무엇을 그렸는지 추측하는 체험형 웹 게임 프로젝트

## 🧠 프로젝트 개요
제한 시간 내 캔버스에 그림 그리기
그림을 AI 모델로 분석
AI가 추측한 결과를 즉시 피드백
단순 예측이 아닌, *“AI가 어떻게 생각하는지”*를 체험하는 데 초점

## 🛠️ 사용 기술 (Tech Stack)
### 🔹 Frontend
HTML5
CSS3
JavaScript (Vanilla JS)
### 🔹 Libraries
p5.js
→ Canvas 기반 자유 드로잉 구현
ml5.js
→ (초기 버전) 브라우저 기반 머신러닝 실험용
### 🔹 AI Model / Backend
CLIP (Contrastive Language–Image Pretraining)
→ 이미지와 텍스트의 의미적 유사도를 비교하는 멀티모달 모델
FastAPI (Python)
→ AI 추론 서버
PyTorch
Pillow (PIL)

## 🧩 시스템 구조
[ Browser ]
   └─ p5.js Canvas
        └─ 그림 제출 (UploadFile)
             ↓
[ FastAPI Server ]
   └─ CLIP 모델 추론
        └─ 결과(JSON) 반환
             ↓
[ Browser ]
   └─ AI 추측 결과 출력
