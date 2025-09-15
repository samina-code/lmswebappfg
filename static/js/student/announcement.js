const announcements = [
    {
      title: "Midterm Postponed",
      message: "The AI midterm has been moved to April 25.",
      teacher: "Dr. Sarah Khan",
      date: "2025-04-18",
      category: "exam",
      pinned: true
    },
    {
      title: "Assignment 2 Deadline",
      message: "Submit assignment 2 by April 20 on the portal.",
      teacher: "Mr. Ahmed Raza",
      date: "2025-04-15",
      category: "assignment",
      pinned: false
    },
    {
      title: "Group Study Session",
      message: "Optional group study this Friday at 2PM.",
      teacher: "Miss Hira",
      date: "2025-04-12",
      category: "general",
      pinned: false
    }
  ];
  
  function isNew(dateStr) {
    const today = new Date();
    const posted = new Date(dateStr);
    const diff = (today - posted) / (1000 * 3600 * 24);
    return diff <= 2;
  }
  
  function renderAnnouncements(list) {
    const container = document.getElementById("announcementList");
    container.innerHTML = "";
  
    // Pinned first
    list.sort((a, b) => b.pinned - a.pinned);
  
    list.forEach((a, index) => {
      const card = document.createElement("div");
      card.className = "announcement-card";
  
      const title = document.createElement("h3");
      title.innerHTML = `${a.title}${isNew(a.date) ? ' <span class="badge-new">NEW</span>' : ''}`;
      title.onclick = () => {
        const msg = card.querySelector(".announcement-message");
        msg.style.display = msg.style.display === "none" ? "block" : "none";
      };
  
      const meta = document.createElement("div");
      meta.className = "announcement-meta";
      meta.innerHTML = `🗓️ ${a.date} — 👨‍🏫 ${a.teacher}
        <span class="read-toggle" onclick="markRead(this)">Mark as Read</span>`;
  
      const msg = document.createElement("div");
      msg.className = "announcement-message";
      msg.innerText = a.message;
  
      card.appendChild(title);
      card.appendChild(meta);
      card.appendChild(msg);
      container.appendChild(card);
    });
  }
  
  function markRead(elem) {
    const card = elem.closest(".announcement-card");
    card.classList.add("read");
    elem.style.display = "none";
  }
  
  // Filter logic
  document.getElementById("filterCategory").addEventListener("change", function () {
    filterAndSearch();
  });
  
  document.getElementById("searchAnnouncement").addEventListener("input", function () {
    filterAndSearch();
  });
  
  function filterAndSearch() {
    const category = document.getElementById("filterCategory").value;
    const keyword = document.getElementById("searchAnnouncement").value.toLowerCase();
  
    const filtered = announcements.filter(a =>
      (category === "all" || a.category === category) &&
      (a.title.toLowerCase().includes(keyword) || a.teacher.toLowerCase().includes(keyword))
    );
  
    renderAnnouncements(filtered);
  }
  
  // Initial render
  renderAnnouncements(announcements);
  