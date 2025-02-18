import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Užkrauk aplinkos kintamuosius (jei naudojate .env failą)
load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="Prižiūrių tvarką👀")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Prisijungta kaip {bot.user.name}")

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(f"✅ Įkelta komanda: {filename}")
            except Exception as e:
                print(f"⚠️ Klaida įkeliant {filename}: {e}")

# Šalinti asyncio.run(), nes bot.run() tai padarys už jus.
bot.run(os.getenv("DISCORD_TOKEN"))
