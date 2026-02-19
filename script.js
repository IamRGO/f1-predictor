const BASE_URL = "https://ergast.com/api/f1";

// 2026 season (change if needed)
const SEASON = "2026";

async function fetchDrivers() {
    const response = await fetch(`${BASE_URL}/${SEASON}/drivers.json`);
    const data = await response.json();
    return data.MRData.DriverTable.Drivers;
}

async function fetchCareerStats(driverId) {
    let wins = 0;
    let podiums = 0;

    // Fetch all race results for driver
    const response = await fetch(`${BASE_URL}/drivers/${driverId}/results.json?limit=1000`);
    const data = await response.json();
    const races = data.MRData.RaceTable.Races;

    races.forEach(race => {
        race.Results.forEach(result => {
            const position = parseInt(result.position);

            if (position === 1) wins++;
            if (position <= 3) podiums++;
        });
    });

    return { wins, podiums };
}

function createDriverCard(driver, stats) {
    const container = document.getElementById("drivers-container");

    const card = document.createElement("div");
    card.classList.add("driver-card");

    card.innerHTML = `
        <h2>${driver.givenName} ${driver.familyName}</h2>
        <p class="stat"><strong>Nationality:</strong> ${driver.nationality}</p>
        <p class="stat"><strong>Date of Birth:</strong> ${driver.dateOfBirth}</p>
        <p class="stat"><strong>Career Wins:</strong> ${stats.wins}</p>
        <p class="stat"><strong>Career Podiums:</strong> ${stats.podiums}</p>
    `;

    container.appendChild(card);
}

async function loadDrivers() {
    const container = document.getElementById("drivers-container");
    container.innerHTML = "<p>Loading 2026 drivers...</p>";

    try {
        const drivers = await fetchDrivers();
        container.innerHTML = "";

        for (const driver of drivers) {
            const stats = await fetchCareerStats(driver.driverId);
            createDriverCard(driver, stats);
        }

    } catch (error) {
        container.innerHTML = "<p>Error loading data.</p>";
        console.error(error);
    }
}

loadDrivers();
