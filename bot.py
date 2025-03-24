import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Užkrauname .env failą (jei naudojamas)
load_dotenv()

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
        if filename.endswith(".py") and filename != "dashboard.py":
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
        await bot.start(os.getenv("DISCORD_TOKEN"))

# Startuojame bot'ą
asyncio.run(main())
