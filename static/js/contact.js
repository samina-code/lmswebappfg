// contact.js
// Wait until DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {

  // Form Element
  const contactForm = document.getElementById('contactForm');

  // Confirmation message element
  const confirmationMessage = document.getElementById('confirmation');

  // Form Submit Event
  contactForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Stop page reload

    // Getting values from input fields
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();

    // Basic Validation
    if (name === '' || email === '' || message === '') {
      alert('⚠️ Please fill out all fields.');
      return;
    }

    if (!validateEmail(email)) {
      alert('⚠️ Please enter a valid email address.');
      return;
    }

    // If everything is fine
    contactForm.reset(); // Clear form fields
    confirmationMessage.style.display = 'block'; // Show thank you message

    // Hide message after 4 seconds
    setTimeout(function () {
      confirmationMessage.style.display = 'none';
    }, 4000);
  });

});

// Email Validation Function
function validateEmail(email) {
  // Simple Regex for basic email pattern
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
