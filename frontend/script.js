// ---------------- PAGE NAVIGATION ----------------

function showPage(pageId) {
    document.querySelectorAll(".page").forEach(page => {
        page.classList.remove("active");
    });
    document.getElementById(pageId).classList.add("active");
}

// ---------------- IMAGE PREVIEW ----------------

document.getElementById("veg-input").addEventListener("change", (e) => {
    previewImage(e, "veg-preview");
});

document.getElementById("soil-input").addEventListener("change", (e) => {
    previewImage(e, "soil-preview");
});

function previewImage(event, previewId) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
        const img = document.getElementById(previewId);
        img.src = reader.result;
        img.style.display = "block";
    };
    reader.readAsDataURL(file);
}

// ---------------- BACKEND CONFIG ----------------
const API_BASE = "http://127.0.0.1:10000";
//const API_BASE = "https://YOUR-REAL-BACKEND.onrender.com";

// ---------------- AI PROCESSING ----------------

async function processAI(type) {
    const input =
        type === "vegetation"
            ? document.getElementById("veg-input")
            : document.getElementById("soil-input");

    const resultDiv =
        type === "vegetation"
            ? document.getElementById("veg-result")
            : document.getElementById("soil-result");

    if (!input.files.length) {
        resultDiv.style.color = "red";
        resultDiv.innerHTML = "❌ Please upload an image first.";
        return;
    }

    resultDiv.style.color = "#121212";
    resultDiv.innerHTML = "⏳ Processing with AI model...";

    const formData = new FormData();
    formData.append("file", input.files[0]);

    const endpoint =
        type === "vegetation"
            ? "/predict/vegetation"
            : "/predict/soil";

    try {
        const response = await fetch(API_BASE + endpoint, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Backend error");
        }

        resultDiv.style.color = "#2e7d32";

        if (type === "vegetation") {
            resultDiv.innerHTML =
                `✅ Green Coverage: <b>${data.coverage}%</b>`;
        } else {
            resultDiv.innerHTML =
                `✅ Soil Type: <b>${data.label}</b><br>
                 Confidence: ${(data.confidence * 100).toFixed(2)}%`;
        }

    } catch (err) {
        console.error("AI ERROR:", err);
        resultDiv.style.color = "red";
        resultDiv.innerHTML =
            "❌ Backend not reachable or model error.<br>Check Render logs.";
    }
}
