import discord
from discord.ext import commands
import asyncio
import os
import threading
from dotenv import load_dotenv

# Užkrauname .env failą
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")  # Įsitikink, kad env faile yra DISCORD_TOKEN
if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN nėra nustatytas aplinkos kintamuosiuose!")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="#", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.listening, 
        name="Prižiūriu tvarką👀 Prefixas: # | Komandų sąrašas: #komandos"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ Prisijungta kaip {bot.user.name}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⌛ Palauk `{error.retry_after:.1f}` sekundžių prieš vėl naudojant šią komandą!", delete_after=3)

async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            extension = f"commands.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"✅ Įkelta komanda: {filename}")
            except commands.errors.ExtensionAlreadyLoaded:
                print(f"⚠️ Modulis {extension} jau įkeltas!")
            except Exception as e:
                print(f"❌ Klaida įkeliant {filename}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Paleidžiame bot'ą kaip atskirą "thread", kad Flask dashboard veiktų kartu
def run_discord_bot():
    asyncio.run(main())

# Jei šis failas paleidžiamas kaip pagrindinis, startuojame botą
if __name__ == "__main__":
    threading.Thread(target=run_discord_bot, daemon=True).start()
