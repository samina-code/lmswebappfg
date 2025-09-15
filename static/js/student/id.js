//  Dark Mode & Theme
function toggleDarkMode() {
    document.body.classList.toggle("dark");
    localStorage.setItem("darkMode", document.body.classList.contains("dark") ? "on" : "off");
  }
  function setTheme(color) {
    document.body.classList.remove("theme-blue", "theme-green", "theme-red", "theme-purple");
    document.body.classList.add("theme-" + color);
    localStorage.setItem("themeColor", color);
  }
  //  Notifications
  function toggleNotifications() {
    const popup = document.getElementById("notificationsPopup");
    popup.style.display = popup.style.display === "block" ? "none" : "block";
  }
  function toggleProfileMenu() {
    const menu = document.getElementById("profileMenu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
  }
  function markAsRead(el) {
    el.innerHTML = "✔️ " + el.innerText.replace("🆕 ", "");
    el.style.opacity = 0.6;
  }
  
  //  Sticky Note
  function toggleStickyNote() {
    const note = document.getElementById("stickyNote");
    note.style.display = note.style.display === "block" ? "none" : "block";
  }
  
  //  Upload with Progress
  const uploadInput = document.getElementById("uploadFile");
  if (uploadInput) {
    uploadInput.addEventListener("change", () => {
      const progress = document.getElementById("uploadProgress");
      progress.value = 0;
      let i = 0;
      const interval = setInterval(() => {
        if (i >= 100) {
          clearInterval(interval);
          showToast(" Upload complete!");
        }
        progress.value = i++;
      }, 20);
    });
  }
  
  //  Countdown
  function startCountdown(targetDate) {
    const el = document.getElementById("countdownTimer");
    const end = new Date(targetDate).getTime();
    setInterval(() => {
      const now = new Date().getTime();
      const dist = end - now;
      if (dist < 0) {
        el.innerHTML = " Quiz Time!";
        return;
      }
      const d = Math.floor(dist / (1000 * 60 * 60 * 24));
      const h = Math.floor((dist % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const m = Math.floor((dist % (1000 * 60 * 60)) / (1000 * 60));
      const s = Math.floor((dist % (1000 * 60)) / 1000);
      el.innerHTML = `${d}d ${h}h ${m}m ${s}s`;
    }, 1000);
  }
  startCountdown("2025-04-15T09:00:00");
  
  //  Notes & Tasks Save
  const quickNote = document.getElementById("quickNote");
  if (quickNote) {
    quickNote.value = localStorage.getItem("quickNote") || "";
    quickNote.addEventListener("input", () => {
      localStorage.setItem("quickNote", quickNote.value);
    });
  }
  
  const checklist = document.querySelectorAll("#taskList input");
  checklist.forEach((box, idx) => {
    const key = `task-${idx}`;
    box.checked = localStorage.getItem(key) === "true";
    box.addEventListener("change", () => {
      localStorage.setItem(key, box.checked);
      showToast("✔️ Task updated!");
      if (box.checked) {
        triggerConfetti(3000); //  show for 3 sec only
      }
    });
  });
  
  // ✅ Drag & Drop To-Do
  const todoList = document.getElementById("dragTodo");
  if (todoList) {
    let dragItem;
    todoList.querySelectorAll("li").forEach(item => {
      item.addEventListener("dragstart", () => dragItem = item);
      item.addEventListener("dragover", e => e.preventDefault());
      item.addEventListener("drop", () => {
        if (dragItem !== item) {
          const temp = item.innerHTML;
          item.innerHTML = dragItem.innerHTML;
          dragItem.innerHTML = temp;
        }
      });
    });
  }
  
  //  Chart Filter
  function filterCharts() {
    const subject = document.getElementById("chartFilter").value;
    const progressCanvas = document.getElementById("progressChart");
    const subjectCanvas = document.getElementById("subjectChart");
  
    // Prevent error if canvases not found
    if (!progressCanvas || !subjectCanvas) return;
  
    const progressChart = progressCanvas.getContext("2d");
    const subjectChart = subjectCanvas.getContext("2d");
  
    if (window.progressInstance) window.progressInstance.destroy();
    if (window.subjectInstance) window.subjectInstance.destroy();
  
    window.progressInstance = new Chart(progressChart, {
      type: "doughnut",
      data: {
        datasets: [{
          data: subject === "OOP" ? [80, 20] : subject === "DSA" ? [60, 40] : [70, 30],
          backgroundColor: ["#007bff", "#e0e0e0"]
        }]
      },
      options: {
        cutout: "70%",
        plugins: { legend: { display: false } }
      }
    });
  
    window.subjectInstance = new Chart(subjectChart, {
      type: "bar",
      data: {
        labels: subject === "OOP" ? ["OOP"] : subject === "DSA" ? ["DSA"] : ["OOP", "DSA"],
        datasets: [{
          label: "Scores",
          data: subject === "OOP" ? [85] : subject === "DSA" ? [65] : [85, 65],
          backgroundColor: "#007bff"
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: true, max: 100 } },
        plugins: { legend: { display: false } }
      }
    });
  }
  
  //  Confetti
  function triggerConfetti(duration = 3000) {
    const canvas = document.getElementById("confettiCanvas");
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const pieces = Array.from({ length: 100 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 6 + 4,
      d: Math.random() * 10 + 10,
      color: `hsl(${Math.random() * 360}, 70%, 60%)`,
      tilt: Math.random() * 10 - 10
    }));
    let frame = 0;
    const interval = setInterval(() => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      pieces.forEach(p => {
        ctx.beginPath();
        ctx.fillStyle = p.color;
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fill();
        p.y += p.d * 0.2;
        p.x += Math.sin(frame + p.d);
      });
      frame++;
    }, 30);
    setTimeout(() => {
      clearInterval(interval);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }, duration);
  }
  
  //  Toast
  function showToast(msg) {
    const toast = document.getElementById("toast");
    toast.innerText = msg;
    toast.style.display = "block";
    setTimeout(() => toast.style.display = "none", 3000);
  }
  
  //  Load Theme on Startup + Charts only after DOM ready
  window.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("themeColor");
    const darkMode = localStorage.getItem("darkMode");
    if (savedTheme) setTheme(savedTheme);
    if (darkMode === "on") document.body.classList.add("dark");
  
    filterCharts(); //  Run when DOM is fully loaded
  });
  