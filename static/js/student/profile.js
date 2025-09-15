document.addEventListener("DOMContentLoaded", () => {
    const profileData = {
      name: "Ahmed Raza",
      studentId: "SL-2024-001",
      email: "ahmedraza@gmail.com",
      semester: "6",
      department: "Computer Science",
      subjects: "AI, Web Dev, Data Science",
      joinDate: "August 15, 2022"
    };
  
    const profileContainer = document.querySelector(".profile-card");
    renderProfile();
  
    function renderProfile() {
      profileContainer.innerHTML = `
        <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Profile Picture" class="profile-pic">
        <h2>${profileData.name}</h2>
        <p><strong>Student ID:</strong> ${profileData.studentId}</p>
        <p><strong>Email:</strong> ${profileData.email}</p>
        <p><strong>Semester:</strong> ${profileData.semester}</p>
        <p><strong>Department:</strong> ${profileData.department}</p>
        <p><strong>Subjects:</strong> ${profileData.subjects}</p>
        <p><strong>Join Date:</strong> ${profileData.joinDate}</p>
        <button onclick="downloadProfilePDF()">Download Profile</button>
        <button onclick="editProfile()">Edit Profile</button>
      `;
    }
  
    window.editProfile = function () {
      profileContainer.innerHTML = `
        <img src="https://randomuser.me/api/portraits/men/32.jpg" alt="Profile Picture" class="profile-pic">
        <input id="name" value="${profileData.name}" />
        <input id="studentId" value="${profileData.studentId}" />
        <input id="email" value="${profileData.email}" />
        <input id="semester" value="${profileData.semester}" />
        <input id="department" value="${profileData.department}" />
        <input id="subjects" value="${profileData.subjects}" />
        <input id="joinDate" value="${profileData.joinDate}" />
        <button onclick="saveProfile()">Save</button>
        <button onclick="renderProfile()">Cancel</button>
      `;
    };
  
    window.saveProfile = function () {
      profileData.name = document.getElementById("name").value;
      profileData.studentId = document.getElementById("studentId").value;
      profileData.email = document.getElementById("email").value;
      profileData.semester = document.getElementById("semester").value;
      profileData.department = document.getElementById("department").value;
      profileData.subjects = document.getElementById("subjects").value;
      profileData.joinDate = document.getElementById("joinDate").value;
      renderProfile();
    };
  });
  
  function downloadProfilePDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
  
    const profileData = document.querySelector(".profile-card");
    const name = document.querySelector(".profile-card h2").textContent;
    const details = profileData.querySelectorAll("p");
  
    doc.setFontSize(16);
    doc.text("Student Profile", 20, 20);
  
    doc.setFontSize(12);
    doc.text(`Name: ${name}`, 20, 30);
  
    details.forEach((item, index) => {
      doc.text(item.textContent, 20, 40 + index * 10);
    });
  
    doc.save("student_profile.pdf");
  }
  