// ai.js
const AI = {
  init() {
    console.log("CLIP 서버 연동 AI 사용");
  },

  async classify(canvas, callback) {
    try {
      // canvas → Blob
      const blob = await new Promise(resolve =>
        canvas.toBlob(resolve, "image/png")
      );

      // multipart/form-data 구성
      const formData = new FormData();
      formData.append("image", blob, "drawing.png");

      const res = await fetch("http://127.0.0.1:8000/clip-test", {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        throw new Error("서버 응답 실패");
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
          status: data.status
        }
      ]);

    } catch (e) {
      console.error(e);
      alert("AI 서버와 연결할 수 없어요 😢");
    }
  }
};
