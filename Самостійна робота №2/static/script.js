// script.js

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/players')
    .then(response => response.json())
    .then(players => displayPlayers(players))
    .catch(error => console.error('Error fetching players:', error));
});

function displayPlayers(players) {
    var playerListDiv = document.getElementById("playerList");
    playerListDiv.innerHTML = "<h2>Player List</h2>";

    players.forEach(function(player) {
        var playerInfo = document.createElement("div");
        playerInfo.innerHTML = "<strong>Name:</strong> " + player.name +
                               ", <strong>Score:</strong> " + player.score +
                               ", <strong>Level:</strong> " + player.level +
                               " <button onclick=\"deletePlayer(" + player.id + ")\">Delete</button>";
        playerListDiv.appendChild(playerInfo);
    });
}

function addPlayer() {
    var playerName = document.getElementById("playerName").value;
    var playerScore = document.getElementById("playerScore").value;
    var playerLevel = document.getElementById("playerLevel").value;

    fetch('/api/players', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: playerName,
            score: parseInt(playerScore),
            level: parseInt(playerLevel)
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Player added successfully!');
        console.log(data);

        fetch('/api/players')
        .then(response => response.json())
        .then(players => displayPlayers(players))
        .catch(error => console.error('Error fetching players:', error));
    })
    .catch(error => {
        alert('Failed to add player. Please try again.');
        console.error('Error:', error);
    });
}

function deletePlayer(playerId) {
    fetch('/api/players/' + playerId, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.status === 200) {
            alert('Player deleted successfully!');
        } else {
            alert('Failed to delete player. Please try again.');
        }

        fetch('/api/players')
        .then(response => response.json())
        .then(players => displayPlayers(players))
        .catch(error => console.error('Error fetching players:', error));
    })
    .catch(error => console.error('Error deleting player:', error));
}
