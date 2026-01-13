const Timer = {
  time: 20,
  interval: null,

  start() {
    this.stop();
    this.time = 20;
    const timerEl = document.getElementById('timer');
    timerEl.innerText = this.time;
    timerEl.classList.remove('danger', 'blink'); // 🔥 추가

    this.interval = setInterval(() => {
      this.time--;

      const timerEl = document.getElementById('timer');
      timerEl.innerText = this.time;

      // 🔥 5초 이하 UI 변경
      if (this.time <= 5) {
        timerEl.classList.add('danger');
        timerEl.classList.add('blink');
      }

      if (this.time <= 0) {
        this.stop();          // 안전하게 인터벌 정지
        Game.submit();
      }
    }, 1000);

  },

  stop() {
    if (this.interval) clearInterval(this.interval);
  },

  reset() {
    this.stop();
    this.time = 20;
    
    const timerEl = document.getElementById('timer');
    timerEl.innerText = this.time;
    timerEl.classList.remove('danger', 'blink'); // 🔥 추가
  }
};
