function openImg(src) {
  document.getElementById("openedImageDiv").style.display = "block";
  document.getElementById("openedImage").src = src;
}

function closeImg() {
  document.getElementById("openedImageDiv").style.display = "none";
}
