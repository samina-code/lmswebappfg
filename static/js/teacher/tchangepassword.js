document.getElementById("passwordForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    const current = document.getElementById("currentPass").value;
    const newPass = document.getElementById("newPass").value;
    const confirm = document.getElementById("confirmPass").value;
    const msg = document.getElementById("passMsg");
  
    if (newPass !== confirm) {
      msg.style.color = "red";
      msg.textContent = " New passwords do not match.";
      return;
    }
  
    // Dummy check (in real backend, validate currentPass)
    if (current === newPass) {
      msg.style.color = "orange";
      msg.textContent = "⚠️ New password cannot be same as current.";
      return;
    }
  
    msg.style.color = "green";
    msg.textContent = " Password changed successfully.";
  
    this.reset();
  });
  