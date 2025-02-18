import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Užkrauname .env failą (jei naudojamas)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="Prižiūrių tvarką👀")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"Prisijungta kaip {bot.user.name}")
    for command in bot.commands:
        print(f"Užregistruota komanda: {command.name}")

@bot.event
async def on_ready():
    print(f"✅ Prisijungta kaip {bot.user}")
    await load_extensions()  # UŽKRAUNAME KOMANDAS!

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(f"✅ Įkelta komanda: {filename}")
            except Exception as e:
                print(f"⚠️ Klaida įkeliant {filename}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_TOKEN"))

# Startuojame bot'ą
asyncio.run(main())
