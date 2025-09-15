//  Dark Mode Toggle

 async function loadChartData(apiUrl, canvasId, chartType, labelText, colors) {
  try {
    const res = await fetch(apiUrl);
    const data = await res.json();

    if (chartInstances[canvasId]) {
      chartInstances[canvasId].destroy();
      const canvas = document.getElementById(canvasId);
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    const ctx = document.getElementById(canvasId).getContext("2d");

    chartInstances[canvasId] = new Chart(ctx, {
      type: chartType,
      data: {
        labels: data.labels,
        datasets: [{
          label: labelText,
          data: data.data,
          backgroundColor: Array.isArray(colors) ? colors : [colors],
          borderColor: Array.isArray(colors) ? colors : [colors],
          fill: chartType === "line" ? false : true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { position: "bottom" } },
        interaction: { mode: "index", intersect: false },
        scales: chartType === "bar" || chartType === "line"
          ? { y: { beginAtZero: true } } : {}
      }
    });
  } catch (error) {
    console.error(`Error loading chart data for ${canvasId}:`, error);
  }
}

  const toggleBtn = document.getElementById("darkModeToggle");
toggleBtn.addEventListener("click", function () {
  document.body.classList.toggle("dark-mode");

  // icon switch
  const icon = toggleBtn.querySelector("i");
  if (document.body.classList.contains("dark-mode")) {
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
  } else {
    icon.classList.remove("fa-sun");
    icon.classList.add("fa-moon");
  }

  // save preference in localStorage
  localStorage.setItem("darkMode", document.body.classList.contains("dark-mode"));
});

// Load saved theme on page refresh
window.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("darkMode") === "true") {
    document.body.classList.add("dark-mode");
    toggleBtn.querySelector("i").classList.remove("fa-moon");
    toggleBtn.querySelector("i").classList.add("fa-sun");
  }
});



// Load all charts
loadChartData("/api/chart/students/", "studentChart", "bar", "Students", "rgba(75,192,192,0.6)");
loadChartData("/api/chart/teachers/", "teacherChart", "bar", "Teachers", "rgba(54,162,235,0.6)");
loadChartData("/api/chart/activity/", "semesterChart", "line", "Subjects", "rgba(255,99,132,0.6)");
