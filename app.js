async function loadPredictions() {
    try {
        const response = await fetch('./data/predictions.json');
        const data = await response.json();

        // Update race info
        const nextRace = data.next_race;
        document.getElementById('raceName').textContent = nextRace.race_name;
        document.getElementById('raceLocation').textContent = `🌍 ${nextRace.country} - ${nextRace.circuit}`;

        // Format date
        const raceDate = new Date(nextRace.date_start);
        const formattedDate = raceDate.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        document.getElementById('raceDate').textContent = `📅 ${formattedDate}`;

        // Update podium predictions
        const prediction = data.prediction;
        document.getElementById('driver1').textContent = prediction.podium['1st'];
        document.getElementById('driver2').textContent = prediction.podium['2nd'];
        document.getElementById('driver3').textContent = prediction.podium['3rd'];

        // Update reasoning
        document.getElementById('reasoning').textContent = prediction.reason;

        // Update prediction time
        const predictionDate = new Date(data.predicted_at);
        const formattedPredictionTime = predictionDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZone: 'UTC'
        });
        document.getElementById('predictionTime').textContent = `Prediction generated: ${formattedPredictionTime} UTC`;

    } catch (error) {
        console.error('Error loading predictions:', error);
        document.getElementById('reasoning').textContent = 'Error loading predictions. Please refresh the page.';
    }
}

// Load predictions when page loads
document.addEventListener('DOMContentLoaded', loadPredictions);
