import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Užkrauk aplinkos kintamuosius (jei naudojate .env failą)
load_dotenv()

intents = discord.Intents.default()
intents.messages = True  # Užtikrina, kad botui leidžiama skaityti žinutes
intents.guilds = True # Leidžia matyti serverius
intents.message_content = True # Leidžia matyti pranešimų turinį (būtina komandoms!)

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(f"✅ Įkelta komanda: {filename}")
            except Exception as e:
                print(f"⚠️ Klaida įkeliant {filename}: {e}")

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="Prižiūriu Laisvalaikio Erdvė serverį:P")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ Prisijungta kaip: {bot.user}")
    print("🚀 Botas sėkmingai paleistas!")
    for command in bot.commands:
        print(f"🔹 Užregistruota komanda: {command}")

async def main():
    async with bot:
        await load_extensions()
        # Naudok DISCORD_TOKEN iš aplinkos kintamųjų
        token = os.getenv("DISCORD_TOKEN")
        if token is None:
            print("❌ Nustatytas neteisingas tokenas! Patikrink savo Railway aplinkos kintamuosius.")
            return
        await bot.start(token)

asyncio.run(main())
