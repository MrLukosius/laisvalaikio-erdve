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
    activity = discord.Activity(type=discord.ActivityType.listening, name="Prižiūrių tvarką👀 Prefixas: # Komandų sąrašas: !komandos")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ Prisijungta kaip {bot.user.name}")

    # Užregistruojamos visos komandos
    for command in bot.commands:
        print(f"🔹 Užregistruota komanda: {command.name}")

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
        
        # Patikriname, ar `serveris` ir `bradega` tikrai užkrauti
        if "commands.serveris" not in bot.extensions:
            print("⚠️ Komanda `#serveris` nebuvo užkrautas!")
        else:
            print("✅ Komanda `#serveris` sėkmingai užkrautas!")

        if "commands.bradega" not in bot.extensions:
            print("⚠️ Komanda `#bradega` nebuvo užkrauta!")
        else:
            print("✅ Komanda `#bradega` sėkmingai užkrauta!")
        if "commands.moderation" not in bot.extensions:
            print("⚠️ Moderavimo komandos nebuvo užkrautos")
        else:
            print("✅ Moderavimo komandos sėkmingai užkrautos!")
        if "commands.komandos" not in bot.extensions:
            print("⚠️ Komanda #komandos nebuvo užkrauta")
        else:
            print("✅ Komanda #komandos sėkmingai užkrauta!")
        if "commands.nario-info" not in bot.extensions:
            print("⚠️ Komanda #nario-info nebuvo užkrauta")
        else:
            print("✅ Komanda #nario-info sėkmingai užkrauta!")
        if "commands.kick_notifier" not in bot.extensions:
            print("⚠️ Kick pranesejas nebuvo užkrauta")
        else:
            print("✅ Kick pranesejas sėkmingai užkrauta!")
        if "commands.tiktok_notifier" not in bot.extensions:
            print("⚠️ Tiktok pranesejas nebuvo užkrauta")
        else:
            print("✅ Tiktok pranesejas sėkmingai užkrauta!")
        if "commands.automod" not in bot.extensions:
            print("⚠️ Auto-moderavimas nebuvo užkrauta")
        else:
            print("✅ Auto-moderavimas sėkmingai užkrauta!")
        if "commands.isvalyti" not in bot.extensions:
            print("⚠️ Isvalymas nebuvo užkrauta")
        else:
            print("✅ Isvalymas sėkmingai užkrauta!")
        if "commands.muzika" not in bot.extensions:
            print("⚠️ Muzika nebuvo užkrauta")
        else:
            print("✅ Muzika sėkmingai užkrauta!")
        if "commands.leveling" not in bot.extensions:
            print("⚠️ Lygiai nebuvo užkrauti")
        else:
            print("✅ Lygiai sėkmingai užkrauti!")
        if "commands.member_logger" not in bot.extensions:
            print("⚠️ Nariu pranesejas nebuvo užkrautas")
        else:
            print("✅ Nariu pranesejas sėkmingai užkrautas!")
        if "commands.reaction_verify" not in bot.extensions:
            print("⚠️ Reakcijos patvirtinimas nebuvo užkrautas")
        else:
            print("✅ Reakcijos patvirtinimas sėkmingai užkrautas!")
        

        

        await bot.start(os.getenv("DISCORD_TOKEN"))

# Startuojame bot'ą
asyncio.run(main())
