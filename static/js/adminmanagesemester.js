// Array to hold semester data
let semesters = [];

// Function to display toast messages
function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

// Function to render all semester cards
function renderSemesters() {
  const container = document.getElementById("semesterCards");
  container.innerHTML = "";

  semesters.forEach((semester, index) => {
    const card = document.createElement("div");
    card.className = "semester-card";

    const statusText = semester.active ? "Active" : "Inactive";

    card.innerHTML = `
      <h3>${semester.name}</h3>
      <p><strong>Description:</strong> ${semester.description}</p>
      <p><strong>Start Date:</strong> ${semester.startDate}</p>
      <p><strong>End Date:</strong> ${semester.endDate}</p>
      <p><strong>Status:</strong> ${statusText}</p>
      <div class="actions">
        <button class="edit-btn" onclick="editSemester(${index})">Edit</button>
        <button class="delete-btn" onclick="deleteSemester(${index})">Delete</button>
      </div>
    `;

    container.appendChild(card);
  });
}

// Function to add a new semester
function addSemester() {
  const name = document.getElementById("semesterInput").value.trim();
  const description = document.getElementById("descriptionInput").value.trim();
  const startDate = document.getElementById("startDateInput").value;
  const endDate = document.getElementById("endDateInput").value;
  const active = document.getElementById("statusInput").checked;

  if (!name || !description || !startDate || !endDate) {
    showToast("Please fill in all fields.");
    return;
  }

  semesters.push({ name, description, startDate, endDate, active });
  renderSemesters();
  showToast("Semester added successfully.");

  // Clear input fields
  document.getElementById("semesterInput").value = "";
  document.getElementById("descriptionInput").value = "";
  document.getElementById("startDateInput").value = "";
  document.getElementById("endDateInput").value = "";
  document.getElementById("statusInput").checked = true;
}

// Function to edit an existing semester
function editSemester(index) {
  const semester = semesters[index];

  // Populate input fields with existing data
  document.getElementById("semesterInput").value = semester.name;
  document.getElementById("descriptionInput").value = semester.description;
  document.getElementById("startDateInput").value = semester.startDate;
  document.getElementById("endDateInput").value = semester.endDate;
  document.getElementById("statusInput").checked = semester.active;

  // Remove the semester from the array
  semesters.splice(index, 1);
  renderSemesters();
  showToast("Edit the semester details and click 'Add Semester' to save changes.");
}

// Function to delete a semester
function deleteSemester(index) {
  semesters.splice(index, 1);
  renderSemesters();
  showToast("Semester deleted successfully.");
}
