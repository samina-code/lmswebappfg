document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const semesterSelect = document.getElementById("semesterSelect");
  const filterBtn = document.getElementById("filterBtn");
  const studentCards = document.querySelectorAll(".student-card");

  function filterStudents() {
    const query = searchInput.value.toLowerCase().trim();
    const selectedSemester = semesterSelect.value;

    studentCards.forEach(card => {
      const name = card.querySelector(".student-name").textContent.toLowerCase();
      const semester = card.querySelector(".student-semester").textContent.toLowerCase().replace("semester: ", "");

      const matchesName = query === "" || name.includes(query);
      const matchesSemester = selectedSemester === "all" || semester === selectedSemester.toLowerCase();

      if (matchesName && matchesSemester) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  }

  // Event listeners
  searchInput.addEventListener("input", filterStudents);
  semesterSelect.addEventListener("change", filterStudents);
  filterBtn.addEventListener("click", filterStudents);
});
