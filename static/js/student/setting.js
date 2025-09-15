function toggleSection(id) {
    const section = document.getElementById(id);
    const isVisible = section.style.display === 'block';
  
    document.getElementById("profilePicSection").style.display = "none";
    document.getElementById("changePasswordSection").style.display = "none";
  
    if (!isVisible) {
      section.style.display = "block";
    }
  }
  
  // Profile Picture Preview
  const profileUpload = document.getElementById("profileUpload");
  const profilePreview = document.getElementById("profilePreview");
  
  if (profileUpload && profilePreview) {
    profileUpload.addEventListener("change", function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          profilePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }
  
  // Password Change Validation
  document.getElementById("passwordForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const current = document.getElementById("currentPass").value;
    const newPass = document.getElementById("newPass").value;
    const confirm = document.getElementById("confirmPass").value;
    const msg = document.getElementById("passMsg");
  
    if (newPass !== confirm) {
      msg.style.color = "red";
      msg.textContent = "New passwords do not match.";
      return;
    }
  
    msg.style.color = "green";
    msg.textContent = "Password changed successfully.";
    this.reset();
  });
  