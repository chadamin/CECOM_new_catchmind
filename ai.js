// ai.js
const AI = {
  init() {
    console.log("CLIP 서버 연동 AI 사용");
  },

  async classify(canvas, callback) {
    try {
      // canvas → base64 이미지
      const imageBase64 = canvas.toDataURL("image/png");

      const res = await fetch("http://127.0.0.1:8000/clip-test", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          image: imageBase64
        })
      });

      if (!res.ok) {
        throw new Error("서버 응답 실패");
      }

      const data = await res.json();

      /**
       * 서버 응답 예시:
       * {
       *   "a cat": 0.72,
       *   "a dog": 0.12,
       *   ...
       * }
       */

      // 가장 높은 유사도 선택
      const best = Object.entries(data)
        .sort((a, b) => b[1] - a[1])[0];

      // game.js에서 기대하는 형식으로 변환
      callback([
        {
          label: best[0],
          confidence: best[1]
        }
      ]);

    } catch (e) {
      console.error(e);
      alert("AI 서버와 연결할 수 없어요 😢");
    }
  }
};
