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

@app.route('/get_channels', methods=['GET'])
def get_channels():
    """Grąžina serverio kanalų sąrašą"""
    url = f"{BOT_API_URL}/guilds/{GUILD_ID}/channels"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        channels = response.json()
        
        # Filtruoti tik tekstinius kanalus
        text_channels = [
            {
                "id": channel["id"], 
                "name": channel["name"],
                "type": channel["type"],  # Kanalų tipas (pvz., 0 - tekstinis)
                "topic": channel.get("topic", "Nėra temos")  # Kanalo tema (jei yra)
            }
            for channel in channels if channel["type"] == 0  # Tik tekstiniai kanalai
        ]
        
        # Pridėkite papildomą informaciją apie kanalus
        additional_info = {
            "total_channels": len(text_channels),
            "message": "Kanalo sąrašas sėkmingai gautas."
        }
        
        return jsonify({
            "channels": text_channels,
            "additional_info": additional_info
        })
    else:
        return jsonify({"error": "Nepavyko gauti kanalų."}), response.status_code

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

@app.route('/send_embed', methods=['POST'])
def send_embed():
    """Siunčia embed į pasirinkto kanalo Discord"""
    try:
        data = request.json
        channel_id = data.get("channel_id")
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

        # Siųsti embed į pasirinkto kanalo Discord
        url = f"{BOT_API_URL}/channels/{channel_id}/messages"
        payload = {"embed": embed}
        
        response = requests.post(url, json=payload, headers=HEADERS)

        if response.status_code == 200:
            return jsonify({"message": "✅ Embed sėkmingai išsiųstas!"})
        else:
            return jsonify({"message": f"❌ Klaida: {response.status_code} - {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"message": f"❌ Klaida: {str(e)}"}), 500

# Paleidžiame Flask serverį atskirame threade
def start_dashboard():
    thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True, use_reloader=False))
    thread.daemon = True
    thread.start()
