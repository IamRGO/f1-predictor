const API_URL = "https://live.f1api.dev";
const SEASON = "2026"; 

async function fetchStandings() {
    const response = await fetch(`${API_URL}/${SEASON}/standings/drivers`);

    if (!response.ok) {
        throw new Error("Failed to fetch standings");
    }

    const data = await response.json();
    return data;
}

function createDriverCard(driver) {
    const container = document.getElementById("drivers-container");

    const card = document.createElement("div");
    card.classList.add("driver-card");

    card.innerHTML = `
        <h2>#${driver.position} ${driver.driver}</h2>
        <p><strong>Team:</strong> ${driver.team}</p>
        <p><strong>Points:</strong> ${driver.points}</p>
    `;

    container.appendChild(card);
}

async function loadStandings() {
    const container = document.getElementById("drivers-container");
    container.textContent = "Loading season standings...";

    try {
        const standings = await fetchStandings();

        container.innerHTML = ""; // clear loading text

        if (!standings || standings.length === 0) {
            container.textContent = "No standings available for this season.";
            return;
        }

        standings.forEach(driver => {
            createDriverCard(driver);
        });

    } catch (error) {
        container.textContent = "Error loading standings.";
        console.error(error);
    }
}

loadStandings();
