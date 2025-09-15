// Remove preventDefault so Django can handle form submission
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("quizForm");
  if (form) {
    form.addEventListener("submit", function () {
      // Optional: show a quick message before server reloads
      const msg = document.getElementById("resultMessage");
      if (msg) {
        msg.textContent = " Submitting your quiz...";
      }
    });
  }
});
