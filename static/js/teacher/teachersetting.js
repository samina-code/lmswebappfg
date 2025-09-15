// Live profile picture preview
const uploadInput = document.getElementById("uploadPic");
const previewImg = document.getElementById("profilePreview");

if (uploadInput && previewImg) {
  uploadInput.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        previewImg.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
}

