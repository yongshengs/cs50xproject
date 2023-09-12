// Calculate age group real-time
document.getElementById("age").addEventListener("input", function() {
    const selectedAge = this.value;

    fetch("/calculate_age_group", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `age=${selectedAge}`,
    })

    .then(response => response.json())
    .then(data => {
        // Access 'age_group' property from JSON response
        const ageGroup = data.age_group;

        // Update age group display
        document.getElementById("age_group_display").textContent = ageGroup;
    })

    .catch(error => {
        console.error("Error:", error);
    });
});


// Calculate pushups score real-time
document.getElementById("push_ups").addEventListener("input", function() {
    const selectedAge = document.getElementById("age").value;
    const selectedPushUps = this.value;

    fetch("/calculate_pushup_score", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `age=${selectedAge}&push_ups=${selectedPushUps}`,
    })

    .then(response => response.json())
    .then(data => {
        // Access 'push_ups_score' and 'push_ups_to_next_point' properties from JSON response
        const pushUpsScore = data.push_ups_score;
        const pushUpsNextPoint = data.push_ups_to_next_point;

        // Update pushup score display
        document.getElementById("push_ups_score").textContent = pushUpsScore;
        // Update pushups reps to next point display
        document.getElementById("push_ups_to_next_point").textContent = pushUpsNextPoint > 0 ? pushUpsNextPoint + " reps" : "Reached max score";
    })

    .catch(error => {
        console.error("Error:", error);
    });
});


// Calculate situp score real-time
document.getElementById("sit_ups").addEventListener("input", function() {
    const selectedAge = document.getElementById("age").value;
    const selectedSitUps = this.value;

    fetch("/calculate_situp_score", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `age=${selectedAge}&sit_ups=${selectedSitUps}`,
    })

    .then(response => response.json())
    .then(data => {
        // Access 'sit_ups_score' and 'sit_ups_to_next_point' properties from JSON response
        const sitUpsScore = data.sit_ups_score;
        const sitUpsNextPoint = data.sit_ups_to_next_point;

        // Update situp score display
        document.getElementById("sit_ups_score").textContent = sitUpsScore;
        // Update situps reps to next point display
        document.getElementById("sit_ups_to_next_point").textContent = sitUpsNextPoint > 0 ? sitUpsNextPoint + " reps" : "Reached max score";
    })

    .catch(error => {
        console.error("Error:", error);
    });
});


// Dynamic seconds selection depending on minutes selected for 2.4km run station
document.getElementById("run_minutes").addEventListener("change", function() {
    const minutesSelect = document.getElementById("run_minutes");
    const secondsSelect = document.getElementById("run_seconds");

    // Define available seconds options based on the selected minutes
    const selectedMinutes = parseInt(minutesSelect.value);
    let secondsOptions = [];

    if (selectedMinutes === 8) {
        secondsOptions = [30, 40, 50];
    } else if (selectedMinutes === 18) {
        secondsOptions = [0, 10, 20];
    } else {
        // Default options for other minutes values
        secondsOptions = [0, 10, 20, 30, 40, 50];
    }

    // Clear existing options
    while (secondsSelect.options.length > 0) {
        secondsSelect.options.remove(0);
    }

    // Add new seconds options
    secondsOptions.forEach(seconds => {
        const option = document.createElement("option");
        option.value = seconds;
        option.text = seconds + " seconds";
        secondsSelect.appendChild(option);
    });
});


// Initialize seconds options based on the default selected minutes
document.getElementById("run_minutes").dispatchEvent(new Event("change"));


// Calculate run score real-time
function calculateRunScore() {
    const selectedAge = document.getElementById("age").value;
    const selectedMinutes = document.getElementById("run_minutes").value;
    const selectedSeconds = document.getElementById("run_seconds").value;

    // Ensure 'age' parameter is included in form data
    const formData = new FormData();
    formData.append("age", selectedAge);
    formData.append("run_minutes", selectedMinutes);
    formData.append("run_seconds", selectedSeconds);

    // Send request to server to calculate run score
    fetch("/calculate_run_score", {
        method: "POST",
        body: formData,
    })

    .then(response => response.json())
    .then(data => {
        // Access various properties from JSON response
        const runScore = data.run_score;
        const secsNextPoint = data.secs_to_next_point;
        const pace400m_min = data.pace_400m_minutes;
        const pace400m_sec = data.pace_400m_seconds;
        const pace1km_min = data.pace_1km_minutes;
        const pace1km_sec = data.pace_1km_seconds;

        // Update run score display
        document.getElementById("run_score").textContent = runScore;
        document.getElementById("secs_to_next_point").textContent = secsNextPoint < 0 ? secsNextPoint + " seconds" : "Reached max score";
        document.getElementById("pace400m_min").textContent = pace400m_min + " minutes";
        document.getElementById("pace400m_sec").textContent = pace400m_sec + " seconds";
        document.getElementById("pace1km_min").textContent = pace1km_min + " minutes";
        document.getElementById("pace1km_sec").textContent = pace1km_sec + " seconds";
    })

    .catch(error => {
        console.error("Error:", error);
    });
}


// Event listeners for run_minutes and run_seconds select elements
document.getElementById("run_minutes").addEventListener("change", calculateRunScore);
document.getElementById("run_seconds").addEventListener("input", calculateRunScore);


// Calculate total score and award type
function calculateTotalScore() {
    const selectedAge = document.getElementById("age").value;
    const selectedPushUps = document.getElementById("push_ups").value;
    const selectedSitUps = document.getElementById("sit_ups").value;
    const selectedMinutes = document.getElementById("run_minutes").value;
    const selectedSeconds = document.getElementById("run_seconds").value;

    // Send request to the server to calculate total score, award type, and incentive
    fetch("/calculate_total_score", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `age=${selectedAge}&push_ups=${selectedPushUps}&sit_ups=${selectedSitUps}&run_minutes=${selectedMinutes}&run_seconds=${selectedSeconds}`,
    })

    .then(response => response.json())
    .then(data => {
        // Access properties from JSON response
        const totalScore = data.total_score;
        const awardType = data.award_type;
        const incentiveAmount = data.incentive_amount;

        // Update total score, award type, and incentive amount displays
        document.getElementById("total_score").textContent = totalScore;
        document.getElementById("award_type").textContent = awardType;
        document.getElementById("incentive_amount").textContent = incentiveAmount > 0 ? `$${incentiveAmount}` : "N/A";
    })

    .catch(error => {
        console.error("Error:", error);
    });
}

// Event listeners for input fields to trigger total score calculation
document.getElementById("push_ups").addEventListener("input", calculateTotalScore);
document.getElementById("sit_ups").addEventListener("input", calculateTotalScore);
document.getElementById("run_minutes").addEventListener("change", calculateTotalScore);
document.getElementById("run_seconds").addEventListener("input", calculateTotalScore);


