document.addEventListener("DOMContentLoaded", () => {
  const burgerInput = document.querySelector(".burger input");
  const droppedList = document.querySelector(".droppedList");

  burgerInput.addEventListener("change", () => {
    if (burgerInput.checked) {
      droppedList.style.transform = "translateX(0)";
      document.body.style.overflow = "hidden";
    } else {
      droppedList.style.transform = "translateX(-100%)";
      document.body.style.overflow = "auto";
    }
  });
});
