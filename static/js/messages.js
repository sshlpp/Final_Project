window.onload = function () {
  const popup = document.getElementById("success-popup-message");
  if (popup) {
    setTimeout(() => {
      popup.style.opacity = 0;
      this.setTimeout(() => popup.remove(), 500);
    }, 5000);
  }
};
