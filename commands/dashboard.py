from flask import Flask, request, jsonify, render_template
import requests
import os
import threading
from bot import run_discord_bot  # Importuojame boto paleidimą

# Sukuriame Flask aplikaciją
app = Flask(__name__)

TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_API = "https://discord.com/api/v10"

@app.route("/")
def index():
    return render_template("index.html")  # Užkrauna index.html

@app.route("/send_embed", methods=["POST"])
def send_embed():
    data = request.json
    channel_id = data.get("channel_id")
    embed = {
        "title": data.get("title"),
        "description": data.get("description"),
        "color": 5814783
    }

    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{DISCORD_API}/channels/{channel_id}/messages",
        headers=headers,
        json={"embeds": [embed]}
    )

    if response.status_code == 200:
        return jsonify({"message": "✅ Embed išsiųstas!"}), 200
    else:
        return jsonify({"error": "❌ Nepavyko išsiųsti"}), response.status_code

if __name__ == "__main__":
    # Paleidžiame botą lygiagrečiai su Flask
    threading.Thread(target=run_discord_bot, daemon=True).start()
    
    # Startuojame Flask serverį
    app.run(host="0.0.0.0", port=8080, debug=True)
