from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

BOT_API_URL = "http://127.0.0.1:5000"  # Įsitikink, kad botas klausosi šioje vietoje
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_embed', methods=['POST'])
def send_embed():
    data = request.json
    channel_id = data.get("channel_id")
    title = data.get("title")
    description = data.get("description")

    if not channel_id or not title:
        return jsonify({"message": "Trūksta duomenų"}), 400

    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
    embed_payload = {
        "content": None,
        "embeds": [{
            "title": title,
            "description": description,
            "color": 16711680
        }]
    }

    response = requests.post(
        f"https://discord.com/api/v10/channels/{channel_id}/messages",
        headers=headers,
        json=embed_payload
    )

    if response.status_code == 200 or response.status_code == 201:
        return jsonify({"message": "Embed išsiųstas!"})
    else:
        return jsonify({"message": f"Klaida: {response.text}"}), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
