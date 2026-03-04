// game.js
const Game = {
  isPlaying: false,

  start() {
    const startScreen = document.getElementById("start-screen");
    const gameScreen = document.getElementById("game-screen");

    startScreen.classList.remove("active");
    gameScreen.classList.add("active");

    this.isPlaying = true;
    Canvas.clear();
    Timer.start();
  },

  async submit() {
    if (!this.isPlaying) return;

    this.isPlaying = false;
    Timer.stop();

    const resultScreen = document.getElementById("result-screen");
    resultScreen.classList.add("active");

    // ✨ 아무것도 안 그림
    if (!Canvas.hasDrawn) {
      document.getElementById('result-text').innerText = '그림 없음';
      document.getElementById('ai-thought').innerText =
        '아직 아무것도 그리지 않았푸앙...';
      return;
    }

    document.getElementById('result-text').innerText = 'AI 생각 중...';
    document.getElementById('ai-thought').innerText = '';

    const canvas = Canvas.get();

    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append('image', blob, 'draw.png');

      try {
        const response = await fetch('http://127.0.0.1:8000/clip-test', {
          method: 'POST',
          body: formData, // ⚠️ Content-Type 직접 지정 ❌
        });

        if (!response.ok) {
          throw new Error('Server error');
        }

        const data = await response.json();
        this.showResult(data);

      } catch (error) {
        document.getElementById('result-text').innerText = '오류';
        document.getElementById('ai-thought').innerText =
          'AI 서버와 연결할 수 없어요 😢';
      }
    });
  },

  showResult(data) {
    const { guess, confidence } = data;

    document.getElementById('result-text').innerText = 'AI의 추측';

    if (confidence >= 0.8) {
      document.getElementById('ai-thought').innerText =
        `이건 거의 "${guess}" 같아요! 😄`;
    } else if (confidence >= 0.5) {
      document.getElementById('ai-thought').innerText =
        `혹시 "${guess}"을(를) 그렸나요? 🤔`;
    } else {
      document.getElementById('ai-thought').innerText =
        '음… 잘 모르겠어요 😅';
    }
  },

  reset() {
    if (!this.isPlaying) return;
    Canvas.clear();
  },

  restart() {
    const startScreen = document.getElementById("start-screen");
    const gameScreen = document.getElementById("game-screen");
    const resultScreen = document.getElementById("result-screen");

    resultScreen.classList.remove("active");
    gameScreen.classList.remove("active");
    startScreen.classList.add("active");

    this.isPlaying = false;
  } 
};
