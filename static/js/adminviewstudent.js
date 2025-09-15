
  $(document).ready(function () {
    // Initialize DataTable
    $('#studentTable').DataTable({
      pageLength: 5,
      lengthChange: true,
      searching: true,
      ordering: true,
      language: {
        search: "Search:",
        lengthMenu: "Show _MENU_ entries",
        info: "Showing _START_ to _END_ of _TOTAL_ students",
        paginate: {
          previous: "Previous",
          next: "Next"
        }
      }
    });

    // DELETE button handler
    $('#studentTable').on('click', '.fa-trash-alt', function () {
      const confirmed = confirm("Are you sure you want to delete this row?");
      if (confirmed) {
        const row = $(this).closest('tr');
        $('#studentTable').DataTable().row(row).remove().draw();
        alert("Row deleted successfully.");
      }
    });

    // EDIT button handler
    $('#studentTable').on('click', '.fa-edit', function () {
      const studentId = $(this).closest('tr').data('id');
      if (studentId) {
        window.location.href = `adminupdatestudent.html?id=${studentId}`;
      }
    });

    // SEMESTER icon handler
    $('#studentTable').on('click', '.fa-calendar-alt', function () {
      const studentId = $(this).closest('tr').data('id');
      if (studentId) {
        window.location.href = `adminstudentsemester.html?id=${studentId}`;
      }
    });
  });

