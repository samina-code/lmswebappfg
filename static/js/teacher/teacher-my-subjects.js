document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector("input[name='q']");
  const semesterSelect = document.querySelector("select[name='semester']");
  const subjectCards = document.querySelectorAll(".subject-card");

  function filterSubjects() {
    const query = searchInput.value.toLowerCase().trim();
    const selectedSemester = semesterSelect.value.toLowerCase();

    subjectCards.forEach(card => {
      const name = card.querySelector(".subject-name").textContent.toLowerCase();
      const semester = card.querySelector(".subject-semester").textContent.toLowerCase();

      const matchesName = query === "" || name.includes(query);
      const matchesSemester = selectedSemester === "all" || semester.includes(selectedSemester);

      if (matchesName && matchesSemester) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  }

  searchInput.addEventListener("input", filterSubjects);
  semesterSelect.addEventListener("change", filterSubjects);
});
