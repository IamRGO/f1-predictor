const drivers = [
    "Max Verstappen",
    "Lewis Hamilton",
    "Charles Leclerc",
    "Lando Norris",
    "George Russell",
];

const wikiApiBase =
    "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&prop=revisions&rvprop=content&rvslots=main&titles=";

async function fetchWikiInfobox(name) {
    const url = wikiApiBase + encodeURIComponent(name);
    const res = await fetch(url);
    const data = await res.json();
    const pages = data.query.pages;
    const page = pages[Object.keys(pages)[0]];

    if (!page.revisions) return null;

    const wikitext = page.revisions[0].slots.main["*"];
    return wikitext;
}

function parseStat(wikitext, fieldNames) {
    for (let field of fieldNames) {
        const regex = new RegExp("\\|" + field + "\\s*=\\s*(\\d+)", "i");
        const match = wikitext.match(regex);
        if (match) {
            return parseInt(match[1]);
        }
    }
    return 0;
}

async function fetchDriverData(name) {
    const wikitext = await fetchWikiInfobox(name);

    if (!wikitext) {
        return {
            name,
            wins: "N/A",
            podiums: "N/A",
            championships: "N/A",
        };
    }

    // Common infobox fields in F1 pages
    const wins = parseStat(wikitext, ["wins", "race_wins", "win"]);
    const podiums = parseStat(wikitext, ["podiums", "race_podiums"]);
    const championships = parseStat(wikitext, [
        "championships",
        "drivers_championships",
        "world_championships",
    ]);

    return {
        name,
        wins,
        podiums,
        championships,
    };
}

function createDriverCard(driver) {
    const container = document.getElementById("drivers-container");
    container.innerHTML = "";

    const card = document.createElement("div");
    card.classList.add("driver-card");
    card.innerHTML = `
        <h2>${driver.name}</h2>
        <p><strong>Career Wins:</strong> ${driver.wins}</p>
        <p><strong>Career Podiums:</strong> ${driver.podiums}</p>
        <p><strong>Championships:</strong> ${driver.championships}</p>
    `;
    container.appendChild(card);
}

async function loadDrivers() {
    const container = document.getElementById("drivers-container");
    container.innerHTML = "Fetching Wikipedia data...";

    try {
        for (let name of drivers) {
            const data = await fetchDriverData(name);
            createDriverCard(data);
        }
    } catch (err) {
        container.innerHTML = "Error loading data.";
        console.error(err);
    }
}

loadDrivers();