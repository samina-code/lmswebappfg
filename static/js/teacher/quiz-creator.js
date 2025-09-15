let questionCount = 0;

document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("questionsContainer");

    // Make function globally accessible for inline onclick
    window.addQuestion = function() {
        questionCount++;
        const block = document.createElement("div");
        block.className = "question-block";
        block.innerHTML = `
            <h4>Question ${questionCount}</h4>

            <label>Question:</label>
            <textarea name="questions[]" required></textarea>

            <label>Option A:</label>
            <input type="text" name="optionA[]" required>

            <label>Option B:</label>
            <input type="text" name="optionB[]" required>

            <label>Option C:</label>
            <input type="text" name="optionC[]" required>

            <label>Option D:</label>
            <input type="text" name="optionD[]" required>

            <label>Correct Answer:</label>
            <select name="correct[]" required>
              <option value="">--Select--</option>
              <option value="A">Option A</option>
              <option value="B">Option B</option>
              <option value="C">Option C</option>
              <option value="D">Option D</option>
            </select>

            <button type="button" class="remove-btn">❌ Remove</button>
        `;
        container.appendChild(block);

        // Attach remove listener
        block.querySelector(".remove-btn").addEventListener("click", function() {
            block.remove();
        });
    }
});
