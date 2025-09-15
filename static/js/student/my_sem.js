// semester.js

     
     // semester.js
// semester.js
document.addEventListener('DOMContentLoaded', function () {
  const semesterData = {
    6: {
      semester: "6th Semester",
      start: "2025-03-01",
      end: "2025-07-20",
      midterm: "2025-05-01",
      final: "2025-07-10",
      notes: "AI, web dev, and mini project.",
    }
  };

  const data = semesterData[assignedSemester];
  if (!data) return;

  document.getElementById("semesterNumber").textContent = data.semester;
  document.getElementById("startDate").textContent = data.start;
  document.getElementById("endDate").textContent = data.end;
  document.getElementById("midterm").textContent = data.midterm;
  document.getElementById("final").textContent = data.final;
  document.getElementById("notes").textContent = data.notes;
  document.getElementById("semesterDetails").classList.remove("hidden");

  // Debugging calendar
  const calendarEl = document.getElementById('calendar');
  console.log("Calendar element:", calendarEl);

  // Calendar
});
