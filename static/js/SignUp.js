
document.getElementById("signupForm").addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent form from submitting

  const name = document.getElementById("fullName").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  // Name validation: only letters and spaces, minimum 3 characters
  const namePattern = /^[A-Za-z\s]{3,}$/;
  if (!name.match(namePattern)) {
    alert("Please enter a valid full name (letters and spaces only, minimum 3 characters).");
    return;
  }

  // Email validation
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}$/;
  if (!email.match(emailPattern)) {
    alert("Please enter a valid email address.");
    return;
  }

  // Password validation: 8-16 characters, at least one letter, one digit, one special char
  const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$/;
  if (!password.match(passwordPattern)) {
    alert("Password must be 8–16 characters, include a letter, number, and special character.");
    return;
  }

  alert("Sign up successful!");
  // e.target.submit(); // Uncomment if you want to proceed with submission
});


function validateSignUp() {
  const fullName = document.getElementById("fullname").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  // Check if fields are empty
  if (!fullName || !email || !password) {
      alert("Please fill in all fields.");
      return false;
  }

  // Email validation
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  if (!email.match(emailPattern)) {
      alert("Please enter a valid email address.");
      return false;
  }

  // Full name should not match password
  if (fullName.toLowerCase() === password.toLowerCase()) {
      alert("Name and password cannot be the same.");
      return false;
  }

  // Success
  alert("Sign up successful!");
  window.location.href = "SignIn.html"; // Optional redirect to login page
  return false; // Prevent actual form submission
}

