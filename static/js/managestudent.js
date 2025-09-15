document.addEventListener("DOMContentLoaded", function() {
  // Get the View All Students button element
  const viewAllBtn = document.getElementById("viewAllBtn");

  // Log the button element to make sure it's selected correctly
  console.log(viewAllBtn); // This will log the button element to the console
  
  // Attach a single click event listener
  viewAllBtn.addEventListener("click", function () {
    // Log when the button is clicked
    console.log("Button Clicked!");

    // Redirect to the adminviewstudent.html page
    window.location.href = 'adminviewstudent.html'; 
  });
});
