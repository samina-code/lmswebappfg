const semesterTitleInput = document.getElementById("semesterTitle");
const addSemesterBtn = document.getElementById("addSemesterBtn");
const viewAllBtn = document.getElementById("viewAllBtn");
const tableSection = document.getElementById("semesterTableSection");
const tableBody = document.getElementById("semesterTableBody");

const subjectModal = document.getElementById("subjectModal");
const subjectTitleInput = document.getElementById("subjectTitle");
const subjectCodeInput = document.getElementById("subjectCode");
const addSubjectBtn = document.getElementById("addSubjectBtn");
const modalTitle = document.getElementById("modalTitle");
const subjectList = document.getElementById("subjectList");

let semesters = [];
let currentSemester = null;

// Add new semester
addSemesterBtn.addEventListener("click", () => {
  const title = semesterTitleInput.value.trim();
  if (title === "") {
    alert("Please enter semester title.");
    return;
  }

  semesters.push({
    id: semesters.length + 1,
    title,
    subjects: [],
  });

  semesterTitleInput.value = "";
  alert("Semester added successfully!");
  renderTable();
});

// Toggle semester list
viewAllBtn.addEventListener("click", () => {
  tableSection.classList.toggle("hidden");
  viewAllBtn.textContent = tableSection.classList.contains("hidden")
    ? "View All Semesters"
    : "Hide Semesters";
  renderTable();
});

// Render semester table
function renderTable() {
  tableBody.innerHTML = "";
  semesters.forEach((sem, index) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${sem.title}</td>
      <td>
        <i 
          class="fas fa-book-open" 
          title="View Subjects" 
          onclick="openSubjectModal(${sem.id})"
          style="cursor: pointer; color: #007bff;"
        ></i>
      </td>
    `;
    tableBody.appendChild(tr);
  });
}

// Open subject modal
function openSubjectModal(semesterId) {
  currentSemester = semesters.find((s) => s.id === semesterId);
  modalTitle.textContent = `Manage ${currentSemester.title} Subjects`;
  subjectModal.classList.remove("hidden");
  updateSubjectList();
}

// Close subject modal
function closeModal() {
  subjectModal.classList.add("hidden");
  subjectTitleInput.value = "";
  subjectCodeInput.value = "";
  subjectList.innerHTML = "";
}

// Add new subject
addSubjectBtn.addEventListener("click", () => {
  const title = subjectTitleInput.value.trim();
  const code = subjectCodeInput.value.trim();

  if (title === "" || code === "") {
    alert("Please enter subject title and code.");
    return;
  }

  currentSemester.subjects.push({ title, code });
  alert("Subject added!");
  subjectTitleInput.value = "";
  subjectCodeInput.value = "";
  updateSubjectList();
});

// Update subject list in modal
function updateSubjectList() {
  subjectList.innerHTML = "";
  currentSemester.subjects.forEach((sub, i) => {
    const item = document.createElement("div");
    item.className = "subject-item";
    item.innerHTML = `
      <span>${i + 1}. ${sub.title} (${sub.code})</span>
      <i 
        class="fas fa-trash delete-icon" 
        title="Delete Subject" 
        onclick="deleteSubject(${i})"
      ></i>
    `;
    subjectList.appendChild(item);
  });
}

// Delete subject from semester
function deleteSubject(index) {
  if (confirm("Are you sure you want to delete this subject?")) {
    currentSemester.subjects.splice(index, 1);
    updateSubjectList();
  }
}
