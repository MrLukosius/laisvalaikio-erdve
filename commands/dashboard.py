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

@app.route('/get_roles', methods=['GET'])
def get_roles():
    """Grąžina serverio roles."""
    url = f"{BOT_API_URL}/guilds/{GUILD_ID}/roles"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        roles = response.json()
        return jsonify(roles)
    else:
        return jsonify({"error": f"Klaida gaunant roles: {response.status_code}"}), response.status_code

@app.route('/assign_role_reaction', methods=['POST'])
def assign_role_reaction():
    """Priskiria reakciją rolei prie nurodytos žinutės."""
    try:
        data = request.json
        channel_id = data.get("channel_id")
        message_id = data.get("message_id")
        role_id = data.get("role_id")
        emoji = data.get("emoji")

        if not all([channel_id, message_id, role_id, emoji]):
            return jsonify({"message": "❌ Trūksta reikalingų duomenų!"}), 400

        # Pridedame reakciją prie žinutės
        emoji_encoded = emoji if emoji.isascii() else requests.utils.quote(emoji)
        url = f"{BOT_API_URL}/channels/{channel_id}/messages/{message_id}/reactions/{emoji_encoded}/@me"
        
        response = requests.put(url, headers=HEADERS)

        if response.status_code in [200, 201, 204]:
            return jsonify({"message": "✅ Reakcija pridėta!"})
        else:
            return jsonify({"message": f"❌ Klaida: {response.status_code} - {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"message": f"❌ Serverio klaida: {str(e)}"}), 500

# Paleidžiame Flask serverį atskirame threade
def start_dashboard():
    thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True, use_reloader=False))
    thread.daemon = True
    thread.start()
