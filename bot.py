import discord
import os
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True  # Užtikrina, kad botui leidžiama skaityti žinutes
intents.guilds = True # Leidzia matyti serverius
intents.message_content = True # Leidzia matyti pranesimu turini (butina komandoms!)

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
    print(f"✅ Prisijungta kaip: {bot.user}")
    print("🚀 Botas sėkmingai paleistas!")
    for command in bot.commands:
        print(f"🔹 Užregistruota komanda: {command}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start("TAVO BOT_TOKENAS")

asyncio.run(main())
