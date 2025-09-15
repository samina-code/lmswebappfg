//  Form validation function
function validateForm() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    // Email validation regex
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

    if (!email.match(emailPattern)) {
        alert("Please enter a valid email address.");
        return false; // prevent form submit
    }

    if (password === "") {
        alert("Password cannot be empty.");
        return false; // prevent form submit
    }

    //  Allow form to be submitted to Django backend
    return true;
}
