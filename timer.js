const Timer = {
  duration: 20, // 총 시간
  time: 20,
  interval: null,

  start() {
    this.stop();
    this.time = this.duration;

    const bar = document.getElementById("timer-bar");
    bar.style.width = "100%";
    bar.style.background = "#38ff78"; // 초록 시작

    this.interval = setInterval(() => {
      this.time--;

      const percent = (this.time / this.duration) * 100;
      bar.style.width = percent + "%";

      // 색 변화
      if (this.time <= 10 && this.time > 5) {
        bar.style.background = "#f1c40f"; // 노랑
      } else if (this.time <= 5) {
        bar.style.background = "#e74c3c"; // 빨강
      } else {
        bar.style.background = "#38ff78"; // 초록
      }

      if (this.time <= 0) {
        this.stop();
        Game.submit();
      }
    }, 1000);
  },

  stop() {
    if (this.interval) clearInterval(this.interval);
  },

  reset() {
    this.stop();
    this.time = this.duration;
    const bar = document.getElementById("timer-bar");
    bar.style.width = "100%";
    bar.style.background = "#38ff78";
  }
};
