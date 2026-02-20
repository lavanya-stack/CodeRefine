const analyzeBtn = document.getElementById("analyzeBtn");
const codeInput = document.getElementById("codeInput");
const resultSection = document.getElementById("resultSection");
const scoreDisplay = document.getElementById("score");
const issuesList = document.getElementById("issues");
const refinedCodeBox = document.getElementById("refinedCode");
const celebration = document.getElementById("celebration");
const toggleBtn = document.getElementById("themeToggle");

// 🌗 Dark / Light Toggle
toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        toggleBtn.innerText = "☀ Light Mode";
    } else {
        toggleBtn.innerText = "🌙 Dark Mode";
    }
});


// 🚀 Analyze Code
analyzeBtn.addEventListener("click", async () => {
    const code = codeInput.value.trim();

    if (!code) {
        alert("Please enter code to analyze.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code })
        });

        if (!response.ok) {
            throw new Error("Backend error");
        }

        const data = await response.json();

        // Show results section
        resultSection.style.display = "block";

        // 🎯 Score
        scoreDisplay.innerText = `Score: ${data.score}/100`;

        // 🛑 Issues (Red Color)
        issuesList.innerHTML = "";

        if (data.issues.length === 0) {
            issuesList.innerHTML = "<li style='color:green;'>No major issues found. Great job! 🎉</li>";
        } else {
            data.issues.forEach(issue => {
                const li = document.createElement("li");
                li.innerText = issue;
                li.style.color = "red";
                issuesList.appendChild(li);
            });
        }

        // ✨ Refined Code
        refinedCodeBox.textContent = data.refined_code;

        // 🎉 Celebration if 100 score
        if (data.score === 100) {
            celebration.style.display = "block";
            celebration.innerHTML = "👏👏 PERFECT SCORE! AMAZING CODE! 👏👏";

            setTimeout(() => {
                celebration.style.display = "none";
            }, 4000);
        }

    } catch (error) {
        resultSection.style.display = "block";
        scoreDisplay.innerText = "Error connecting to backend.";
        issuesList.innerHTML = "<li style='color:red;'>Make sure FastAPI server is running.</li>";
        refinedCodeBox.textContent = "";
    }
});