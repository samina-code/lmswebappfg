// Semester-wise subjects
const semesterSubjects = {
  "2": ["Communication Skills", "Mathematics-I", "Intro to Programming"],
  "4": ["Data Structures", "Database Systems", "Web Development"],
  "6": ["Operating Systems", "Software Engineering", "Computer Networks"],
  "8": ["Artificial Intelligence", "Cloud Computing", "Final Year Project"]
};

// DOM elements
const semesterSelect = document.getElementById('semester');
const subjectSelect = document.getElementById('subject');
const form = document.getElementById('assignmentForm');
const messageBox = document.getElementById('message');
const tableBody = document.getElementById('assignmentTable').querySelector('tbody');

// Update subject options when semester changes
semesterSelect.addEventListener('change', () => {
  const selectedSemester = semesterSelect.value;
  subjectSelect.innerHTML = '<option value="">-- Choose Subject --</option>';

  if (semesterSubjects[selectedSemester]) {
    semesterSubjects[selectedSemester].forEach(subject => {
      const option = document.createElement('option');
      option.value = subject;
      option.textContent = subject;
      subjectSelect.appendChild(option);
    });
  }
});

// Handle form submission
form.addEventListener('submit', function (e) {
  e.preventDefault();

  const subject = subjectSelect.value;
  const title = document.getElementById('title').value;
  const fileInput = document.getElementById('fileUpload');
  const file = fileInput.files[0];

  // Validation
  if (!semesterSelect.value || !subject || !title || !file) {
    showMessage('Please fill in all fields.', 'red');
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    showMessage('File size exceeds 10MB!', 'red');
    return;
  }

  // Simulate file upload (demo purpose)
  const reader = new FileReader();
  reader.onload = function () {
    const uploadedDate = new Date().toLocaleString();

    const newRow = tableBody.insertRow();
    newRow.innerHTML = `
      <td>${subject}</td>
      <td>${title}</td>
      <td><a href="${URL.createObjectURL(file)}" target="_blank">${file.name}</a></td>
      <td>${uploadedDate}</td>
    `;

    showMessage('Assignment uploaded successfully!', 'green');
    form.reset();
    subjectSelect.innerHTML = '<option value="">-- Choose Subject --</option>';
  };

  reader.readAsDataURL(file);
});

// Show message helper
function showMessage(msg, color) {
  messageBox.textContent = msg;
  messageBox.style.color = color;
}
