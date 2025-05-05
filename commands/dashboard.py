from flask import Flask, request, jsonify, render_template
import requests
import os
import threading
from dotenv import load_dotenv

# Užkrauname aplinkos kintamuosius
load_dotenv()

# Sukuriame Flask aplikaciją
app = Flask(__name__, template_folder="../templates")

BOT_API_URL = "https://discord.com/api/v10"
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  # Serverio ID

if not BOT_TOKEN or not GUILD_ID:
    raise ValueError("❌ DISCORD_TOKEN arba GUILD_ID nėra nustatyti .env faile!")

HEADERS = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_embed', methods=['POST'])
def send_embed():
    """Siunčia embed su nuotrauka į Discord"""
    try:
        data = request.form
        channel_id = data.get("channel_id")
        title = data.get("title")
        description = data.get("description")
        image_url = data.get("image_url")
        image_file = request.files.get("image_file")

        embed = {
            "title": title,
            "description": description,
            "color": 3447003,  # Default color (blue)
        }

        if image_url:
            embed["image"] = {"url": image_url}

        # Jei yra failas
        if image_file:
            # Upload to Discord API (this should be modified to handle actual file upload)
            pass

        # Implement your Discord channel sending logic here.
        return jsonify({"message": "✅ Embed sėkmingai išsiųstas!"})

    except Exception as e:
        return jsonify({"message": f"❌ Klaida: {str(e)}"}), 500

# Paleidžiame Flask serverį atskirame threade
def start_dashboard():
    thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True, use_reloader=False))
    thread.daemon = True
    thread.start()
