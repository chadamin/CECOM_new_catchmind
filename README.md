# 🎨 AI 캐치마인드 (AI Catch-Mind)

## 📌 프로젝트 소개
AI 캐치마인드는 사용자가 웹 캔버스에 그림을 그리면 인공지능이 해당 그림을 분석하여 무엇을 그렸는지 추론하는 AI 기반 그림 인식 게임이다.
사용자는 브라우저에서 자유롭게 그림을 그리고, 시스템은 CLIP 기반 이미지-텍스트 유사도 모델을 활용하여 그림의 의미를 추론한다.

## ⚙️ 주요 기능
### 🖌 웹 캔버스 드로잉
p5.js 기반 실시간 그림 그리기
### 🤖 AI 그림 인식
CLIP 모델을 활용한 이미지 의미 분석
### 🧠 텍스트-이미지 유사도 계산
cosine similarity 기반 분류
### 🎮 게임 인터페이스
시작 화면 / 그림 화면 / 결과 화면 구성

## 🧠 사용 기술 (Tech Stack)
### Frontend
- HTML
- CSS
- JavaScript
- p5.js (Canvas drawing)
### AI / ML
- CLIP (Contrastive Language–Image Pretraining)
- Image preprocessing
- Cosine similarity 기반 분류

## 🧩 시스템 구조
User Drawing
      ↓
Canvas (p5.js)
      ↓
Image Capture
      ↓
Image Preprocessing
      ↓
CLIP Model
      ↓
Text Similarity Calculation
      ↓
Prediction Result

## 🤖 CLIP 모델 설명
CLIP은 OpenAI에서 개발한 멀티모달 AI 모델로,
이미지와 텍스트를 동일한 의미 공간에 임베딩하여 두 데이터 간의 의미적 유사도를 계산할 수 있다.
본 프로젝트에서는
- 사용자가 그린 이미지
- 사전에 정의된 텍스트 라벨
을 벡터로 변환한 후 cosine similarity를 계산하여 가장 유사한 객체를 예측한다.

## 🎯 프로젝트 목적
웹 기반 AI 인터랙티브 서비스 구현
멀티모달 AI 모델(CLIP)의 실제 응용
사용자 참여형 AI 게임 시스템 개발