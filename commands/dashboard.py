from flask import Flask, request, jsonify, render_template
import requests
import os
import threading
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from datetime import datetime

load_dotenv()

app = Flask(__name__, template_folder="../templates")
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

BOT_API_URL = "https://discord.com/api/v10"
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

if not BOT_TOKEN or not GUILD_ID:
    raise ValueError("❌ DISCORD_TOKEN arba GUILD_ID nėra nustatyti .env faile!")

HEADERS = {"Authorization": f"Bot {BOT_TOKEN}"}

def hex_to_int(hex_color):
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    return int(hex_color, 16)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_channels', methods=['GET'])
def get_channels():
    url = f"{BOT_API_URL}/guilds/{GUILD_ID}/channels"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        channels = response.json()
        text_channels = [
            {
                "id": channel["id"],
                "name": channel["name"],
                "type": channel["type"],
                "topic": channel.get("topic", "Nėra temos")
            }
            for channel in channels if channel["type"] == 0
        ]
        return jsonify({
            "channels": text_channels,
            "additional_info": {
                "total_channels": len(text_channels),
                "message": "Kanalų sąrašas sėkmingai gautas."
            }
        })
    else:
        return jsonify({"error": "Nepavyko gauti kanalų."}), response.status_code

@app.route('/get_member_count', methods=['GET'])
def get_member_count():
    url = f"{BOT_API_URL}/guilds/{GUILD_ID}?with_counts=true"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "member_count": data.get("approximate_member_count", 0),
            "online_count": data.get("approximate_presence_count", 0)
        })
    else:
        return jsonify({"error": "Nepavyko gauti narių skaičiaus."}), response.status_code

@app.route('/send_embed', methods=['POST'])
def send_embed():
    try:
        channel_id = request.form.get("channel_id")
        title = request.form.get("title")
        description = request.form.get("description")
        color = request.form.get("color")
        image_url = request.form.get("image_url")

        embed = {}

        if title:
            embed["title"] = title
        if description:
            embed["description"] = description

        # Jei spalva pateikta – naudoti ją, kitaip naudoti Discord mėlyną
        if color:
            try:
                embed["color"] = hex_to_int(color)
            except ValueError:
                return jsonify({"message": "❌ Netinkama spalvos reikšmė"}), 400
        else:
            embed["color"] = 3447003  # Discord mėlyna (default)

        file = request.files.get("image_file")
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            with open(filepath, "rb") as f:
                upload_response = requests.post(
                    f"{BOT_API_URL}/channels/{channel_id}/messages",
                    headers={"Authorization": f"Bot {BOT_TOKEN}"},
                    files={"file": (filename, f)},
                    data={"payload_json": jsonify({"embeds": [embed]}).data.decode()}
                )
            os.remove(filepath)
            if upload_response.status_code in [200, 201]:
                return jsonify({
                    "message": "✅ Embed su paveikslėliu išsiųstas!",
                    "status": "success",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
            else:
                return jsonify({
                    "message": f"❌ Klaida siunčiant su paveikslėliu: {upload_response.text}",
                    "status": "error"
                }), upload_response.status_code

        elif image_url:
            embed["image"] = {"url": image_url}

        if not any(embed.values()):
            return jsonify({"message": "❌ Embed turi turėti bent vieną lauką!"}), 400

        response = requests.post(
            f"{BOT_API_URL}/channels/{channel_id}/messages",
            headers={**HEADERS, "Content-Type": "application/json"},
            json={"embeds": [embed]}
        )

        if response.status_code in [200, 201]:
            return jsonify({
                "message": "✅ Embed sėkmingai išsiųstas!",
                "status": "success",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        else:
            return jsonify({
                "message": f"❌ Klaida: {response.status_code} - {response.text}",
                "status": "error"
            }), response.status_code

    except Exception as e:
        return jsonify({
            "message": f"❌ Serverio klaida: {str(e)}",
            "status": "error"
        }), 500

def start_dashboard():
    thread = threading.Thread(target=lambda: app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=True,
        use_reloader=False
    ))
    thread.daemon = True
    thread.start()
