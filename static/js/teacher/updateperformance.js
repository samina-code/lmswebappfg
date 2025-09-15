document.addEventListener('DOMContentLoaded', function() {
    const semesterSelect = document.getElementById('semester-select');
    const subjectSelect = document.getElementById('subject-select');

    semesterSelect.addEventListener('change', function() {
        const semesterId = this.value;
        subjectSelect.innerHTML = '<option value="">Loading...</option>';

        if (!semesterId) {
            subjectSelect.innerHTML = '<option value="">Select Subject</option>';
            return;
        }

        fetch(`/get_subjects/${semesterId}/`)
            .then(response => response.json())
            .then(data => {
                subjectSelect.innerHTML = '<option value="">Select Subject</option>';
                data.forEach(sub => {
                    const option = document.createElement('option');
                    option.value = sub.id;
                    option.text = sub.title;  // ya 'name', jo model me ho
                    subjectSelect.appendChild(option);
                });
            })
            .catch(err => {
                console.error("Error fetching subjects:", err);
                subjectSelect.innerHTML = '<option value="">Error loading subjects</option>';
            });
    });
});
