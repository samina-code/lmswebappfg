// Handle form submit
document.getElementById("teacherForm").addEventListener("submit", function (e) {
    e.preventDefault();
    alert("Teacher has been added successfully!");
    // You can handle backend submission via AJAX here
    this.reset(); // Reset form
  });
  
  // Optional: View button logic
  function viewTeachers() {
    alert("Redirecting to all teachers list...");
    // window.location.href = "view_teachers.html"; // optional navigation
  }
  document.getElementById("viewTeachersBtn").addEventListener("click", function () {
    window.location.href = "mangeviewtea.html";
  });

