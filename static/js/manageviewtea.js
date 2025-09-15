$(document).ready(function () {
  //  Initialize DataTable only ONCE
  const table = $('#teachersTable').DataTable({
    pageLength: 5,
    lengthChange: true,
    searching: true,
    ordering: true,
    language: {
      search: "Search:",
      lengthMenu: "Show _MENU_ entries",
      info: "Showing _START_ to _END_ of _TOTAL_ teachers",
      paginate: {
        previous: "Previous",
        next: "Next"
      }
    }
  });

  //  DELETE button handler
  $('#teachersTable').on('click', '.fa-trash-alt', function () {
    if (confirm("Are you sure you want to delete this row?")) {
      const row = $(this).closest('tr');
      table.row(row).remove().draw();
      alert("Row deleted successfully.");
    }
  });

  //  EDIT button handler
  $('#teachersTable').on('click', '.fa-edit', function () {
    const teacherId = $(this).closest('tr').attr('data-id'); // Correct variable
    if (teacherId) {
      window.location.href = `mangeupdatetea.html?id=${teacherId}`;
    } else {
      alert("Teacher ID not found in this row.");
    }
  });

  //  ASSIGN SEMESTER button handler
  $('#teachersTable').on('click', '.fa-calendar-alt', function () {
    const teacherId = $(this).closest('tr').attr('data-id'); // Correct variable
    if (teacherId) {
      window.location.href = `manageassignsubject.html?id=${teacherId}`;
    } else {
      alert("Teacher ID not found in this row.");
    }
  });
});
