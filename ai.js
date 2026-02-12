// ai.js
// PC / 모바일 / 태블릿 공통으로 동작하는 CLIP 연동 코드
// 현재 접속한 주소 기준으로 API 주소 자동 생성

const API_BASE = `${location.protocol}//${location.hostname}:8000`;

const AI = {
  init() {
    console.log("CLIP 서버 연동 AI 사용");
    console.log("API_BASE =", API_BASE);
  },

  async classify(canvas, callback) {
    try {
      // canvas → Blob
      const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/png")
      );

      if (!blob) {
        throw new Error("Canvas Blob 생성 실패");
      }

      // multipart/form-data 구성
      const formData = new FormData();
      formData.append("image", blob, "drawing.png");

      // CLIP 서버로 전송
      const res = await fetch(`${API_BASE}/clip-test`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`서버 응답 실패 (${res.status})`);
      }

      const data = await res.json();

      /**
       * 서버 응답 예시:
       * {
       *   category: "shape",
       *   guess: "triangle",
       *   confidence: 0.07,
       *   status: "unknown"
       * }
       */

      // game.js에서 쓰기 좋은 형태로 전달
      callback([
        {
          label: data.guess,
          confidence: data.confidence,
          category: data.category,
          status: data.status,
        },
      ]);
    } catch (e) {
      console.error("[AI classify error]", e);
      alert("AI 서버와 연결할 수 없어요 😢\n같은 Wi-Fi인지 확인해주세요.");
    }
  },
};
