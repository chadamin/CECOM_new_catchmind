const Canvas = {
  hasDrawn: false,   // ✨ 그림을 그렸는지 여부

  draw() {
    if (!Game.isPlaying) return;

    // 캔버스 안에서만 그림 허용
    if (
      mouseIsPressed &&
      mouseX >= 0 && mouseX <= width &&
      mouseY >= 0 && mouseY <= height
    ) {
      stroke(255);
      strokeWeight(7);
      line(mouseX, mouseY, pmouseX, pmouseY);
      this.hasDrawn = true; // ✨ 그림이 하나라도 그려졌음
    }
  },

  clear() {
    clear();
    this.hasDrawn = false; // ✨ 다시 그리기 시 그림 상태만 초기화
  },

  get() {
    return document.querySelector('canvas');
  }
};
ad