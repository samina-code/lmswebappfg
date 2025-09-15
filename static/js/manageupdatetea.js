function updateTeacher() {
    const confirmation = confirm("Are you sure? Previous data will be permanently deleted!");
  
    if (confirmation) {
      const name = document.getElementById("teacherName").value;
      const email = document.getElementById("teacherEmail").value;
      const contact = document.getElementById("teacherContact").value;
      const qualification = document.getElementById("teacherQualification").value;
  
      showToast("Teacher data updated successfully!");
    } else {
      alert("Update cancelled.");
    }
  }
  
  function showToast(message) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerText = message;
    document.body.appendChild(toast);
  
    setTimeout(() => {
      toast.classList.add("show");
    }, 100);
  
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
  
 
  