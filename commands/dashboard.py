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

@app.route('/preview_embed', methods=['POST'])
def preview_embed():
    """Grąžina embed peržiūrą"""
    try:
        data = request.json
        title = data.get("title")
        description = data.get("description")
        color = data.get("color", "#0000ff")  # Default color (blue)
        image_url = data.get("image_url")
        
        embed = {
            "title": title,
            "description": description,
            "color": color,
        }

        if image_url:
            embed["image"] = {"url": image_url}

        return jsonify({"embed": embed})

    except Exception as e:
        return jsonify({"message": f"❌ Klaida: {str(e)}"}), 500

# Paleidžiame Flask serverį atskirame threade
def start_dashboard():
    thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True, use_reloader=False))
    thread.daemon = True
    thread.start()
