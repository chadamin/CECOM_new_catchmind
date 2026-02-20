const Timer = {
  duration: 20,
  time: 20,
  interval: null,

  start() {
    this.stop();
    this.time = this.duration;

    const bar = document.getElementById("chalk-bar");
    bar.style.width = "100%";
    bar.style.backgroundColor = "#f5f5f5"; // 고정 분필색

    this.interval = setInterval(() => {
      this.time--;

      const percent = (this.time / this.duration) * 100;
      bar.style.width = percent + "%";

      if (this.time <= 0) {
        this.stop();
        Game.submit();
      }

    }, 1000);
  },

  stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  },

  reset() {
    this.stop();
    this.time = this.duration;

    const bar = document.getElementById("chalk-bar");
    bar.style.width = "100%";
    bar.style.backgroundColor = "#f5f5f5";
  }
};