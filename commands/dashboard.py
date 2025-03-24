from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Užkrauname aplinkos kintamuosius
load_dotenv()

# Sukuriame Flask aplikaciją
app = Flask(__name__, template_folder="../templates")

# Nustatome Discord API adresą ir bot tokeną
BOT_API_URL = "https://discord.com/api/v10"
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN nėra nustatytas .env faile!")

# Pagrindinis puslapis
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint embed žinutės siuntimui į Discord
@app.route('/send_embed', methods=['POST'])
def send_embed():
    try:
        data = request.json
        channel_id = data.get("channel_id")
        title = data.get("title")
        description = data.get("description")

        if not channel_id or not title or not description:
            return jsonify({"message": "❌ Trūksta reikalingų duomenų!"}), 400

        headers = {
            "Authorization": f"Bot {BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        embed_payload = {
            "content": None,
            "embeds": [{
                "title": title,
                "description": description,
                "color": 16711680  # Raudona spalva
            }]
        }

        response = requests.post(
            f"{BOT_API_URL}/channels/{channel_id}/messages",
            headers=headers,
            json=embed_payload
        )

        if response.status_code in [200, 201]:
            return jsonify({"message": "✅ Embed išsiųstas!"})
        else:
            return jsonify({"message": f"❌ Klaida: {response.status_code} - {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"message": f"❌ Serverio klaida: {str(e)}"}), 500

# Paleidžiame Flask serverį
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
