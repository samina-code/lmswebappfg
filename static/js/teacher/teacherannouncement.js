document.addEventListener('DOMContentLoaded', function() {
    const semesterSelect = document.getElementById('semesterSelect');
    const subjectSelect = document.getElementById('subjectSelect');
    const form = document.getElementById('announcementForm');
    const announcementList = document.getElementById('announcementList');

    semesterSelect.addEventListener('change', function() {
        const semesterId = this.value;
        subjectSelect.innerHTML = '<option value="">Loading...</option>';

        if (!semesterId) {
            subjectSelect.innerHTML = '<option value="">--Select Subject--</option>';
            return;
        }

        fetch(`/get-subjects/${semesterId}/`)
            .then(response => response.json())
            .then(data => {
                subjectSelect.innerHTML = '<option value="">--Select Subject--</option>';
                data.forEach(subject => {
                    const option = document.createElement('option');
                    option.value = subject.id;
                    option.textContent = subject.title + " (" + (subject.code || "") + ")";
                    subjectSelect.appendChild(option);
                });
            })
            .catch(err => {
                console.error("Error fetching subjects:", err);
                subjectSelect.innerHTML = '<option value="">--Select Subject--</option>';
            });
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        fetch("", {
            method: "POST",
            headers: {"X-Requested-With": "XMLHttpRequest"},
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === "success"){
                announcementList.innerHTML = data.html;
                form.reset();
                subjectSelect.innerHTML = '<option value="">--Select Subject--</option>';
                alert("Announcement posted successfully!");
            } else {
                alert(data.message);
            }
        })
        .catch(err => console.error("Error submitting announcement:", err));
    });
});
