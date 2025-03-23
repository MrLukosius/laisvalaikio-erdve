from flask import Flask, jsonify, request
import discord
from discord.ext import commands
from flask_cors import CORS
import os

# Flask App
app = Flask(__name__)
CORS(app)

# Sukuriame botą
TOKEN = os.getenv("TOKEN")  # Bot tokenas iš Railway
bot = commands.Bot(command_prefix="#", intents=discord.Intents.all())

@app.route('/')
def home():
    return "Sveikas! Laisvalaikio erdvė BOTO Dashboard API!"

@app.route('/send_embed', methods=['POST'])
async def send_embed():
    data = request.json
    channel_id = int(data["channel_id"])
    title = data["title"]
    description = data["description"]
    
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(embed=embed)
        return jsonify({"status": "success", "message": "Embed išsiųstas!"})
    else:
        return jsonify({"status": "error", "message": "Kanalas nerastas!"})

# Paleidžiame botą
@bot.event
async def on_ready():
    print(f"{bot.user} prisijungė!")

if __name__ == '__main__':
    bot.run(TOKEN)
