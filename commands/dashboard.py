from flask import Flask, request, jsonify, render_template, session, redirect
import requests
import os
import threading
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="../templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "labai_slaptas")

# Bot parametrai
BOT_API_URL = "https://discord.com/api/v10"
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
HEADERS = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}

# OAuth2 parametrai
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_API_BASE = "https://discord.com/api"

if not BOT_TOKEN or not GUILD_ID:
    raise ValueError("❌ DISCORD_TOKEN arba GUILD_ID nėra nustatyti .env faile!")

# ===================== 🌐 OAUTH2 RUTINOS =======================

@app.route('/login')
def login():
    return redirect(f"{DISCORD_API_BASE}/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify")

@app.route('/callback')
def callback():
    code = request.args.get("code")
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": "identify"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(f"{DISCORD_API_BASE}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    token_json = r.json()
    session["access_token"] = token_json["access_token"]

    user = requests.get(f"{DISCORD_API_BASE}/users/@me", headers={
        "Authorization": f"Bearer {session['access_token']}"
    }).json()

    session["user"] = user
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/user")
def user_info():
    if "user" not in session:
        return jsonify({"logged_in": False})
    return jsonify({
        "logged_in": True,
        "user": session["user"]
    })

# ===================== 🔧 DASHBOARD IR BOT =======================

@app.route('/')
def home():
    return render_template('index.html')

def hex_to_int(hex_color):
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    return int(hex_color, 16)

@app.route('/get_channels', methods=['GET'])
def get_channels():
    url = f"{BOT_API_URL}/guilds/{GUILD_ID}/channels"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        channels = response.json()
        text_channels = [
            {"id": c["id"], "name": c["name"], "type": c["type"], "topic": c.get("topic", "Nėra temos")}
            for c in channels if c["type"] == 0
        ]
        return jsonify({
            "channels": text_channels,
            "additional_info": {
                "total_channels": len(text_channels),
                "message": "Kanalo sąrašas sėkmingai gautas."
            }
        })
    else:
        return jsonify({"error": "Nepavyko gauti kanalų."}), response.status_code

@app.route('/preview_embed', methods=['POST'])
def preview_embed():
    try:
        data = request.json
        embed = {
            "title": data.get("title"),
            "description": data.get("description")
        }
        if data.get("color"):
            embed["color"] = hex_to_int(data["color"])
        if data.get("image_url"):
            embed["image"] = {"url": data["image_url"]}
        return jsonify({"embed": embed})
    except Exception as e:
        return jsonify({"message": f"Klaida: {str(e)}"}), 500

@app.route('/send_embed', methods=['POST'])
def send_embed():
    try:
        data = request.json
        embed = {
            "title": data.get("title"),
            "description": data.get("description")
        }
        if data.get("color"):
            embed["color"] = hex_to_int(data["color"])
        if data.get("image_url"):
            embed["image"] = {"url": data["image_url"]}

        if not any([embed.get("title"), embed.get("description"), embed.get("image")]):
            return jsonify({"message": "Embed turi turėti bent vieną lauką."}), 400

        response = requests.post(
            f"{BOT_API_URL}/channels/{data['channel_id']}/messages",
            headers=HEADERS,
            json={"embed": embed}
        )

        if response.status_code == 200:
            return jsonify({"message": "✅ Embed sėkmingai išsiųstas!"})
        else:
            return jsonify({"message": f"Klaida: {response.status_code} - {response.text}"}), response.status_code
    except Exception as e:
        return jsonify({"message": f"Klaida: {str(e)}"}), 500

# ===================== 🚀 SERVER START =======================

def start_dashboard():
    thread = threading.Thread(target=lambda: app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=True,
        use_reloader=False
    ))
    thread.daemon = True
    thread.start()
