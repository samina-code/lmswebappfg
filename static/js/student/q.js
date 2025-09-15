function openResultModal() {
    document.getElementById("resultModal").style.display = "block";
  }
  
  function closeResultModal() {
    document.getElementById("resultModal").style.display = "none";
  }
  
  async function downloadResultPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
  
    const title = document.getElementById("quizTitle").textContent;
    const score = document.getElementById("quizScore").textContent;
    const questions = document.querySelectorAll("#questionResults li");
  
    doc.setFontSize(16);
    doc.text("Quiz Result: " + title, 20, 20);
    doc.setFontSize(12);
    doc.text("Score: " + score, 20, 30);
  
    questions.forEach((item, index) => {
      doc.text(item.textContent, 20, 40 + index * 10);
    });
  
    doc.save("Quiz_Result.pdf");
  }
  