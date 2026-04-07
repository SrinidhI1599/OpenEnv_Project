const BASE_URL = window.location.origin;

async function resetEnv() {
    const res = await fetch(`${BASE_URL}/reset?task=easy`);
    const data = await res.json();

    document.getElementById("state").textContent = JSON.stringify(data, null, 2);
    document.getElementById("reward").textContent = "-";
    document.getElementById("done").textContent = "-";
}

async function stepEnv() {
    const thrust = parseFloat(document.getElementById("thrust").value);
    const rotate = parseFloat(document.getElementById("rotate").value);

    try {
        const res = await fetch(`/step`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ thrust, rotate })
        });

        const data = await res.json();

        console.log("STEP RESPONSE:", data);

        // ✅ Since backend returns flat state
        document.getElementById("state").textContent =
            JSON.stringify(data, null, 2);

        // ✅ Show derived info
        document.getElementById("reward").textContent =
            data.reward !== undefined ? data.reward : "N/A";

        document.getElementById("done").textContent =
            (data.landed || data.crashed) ? "Finished" : "Running";

    } catch (err) {
        console.error("Step error:", err);
    }
}