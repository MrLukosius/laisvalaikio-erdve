import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from commands.dashboard import start_dashboard  # Importuojame start_dashboard

# Užkrauname .env failą
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True  # Įjungiam reakcijų aptikimą

bot = commands.Bot(command_prefix="#", intents=intents)

# Žinutės ID ir su jomis susietos rolės
reaction_roles = {}  # {message_id: {emoji: role_id}}

@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.listening, 
        name="Prižiūriu tvarką👀 #komandos"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ Prisijungta kaip {bot.user.name}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⌛ Palauk `{error.retry_after:.1f}` sekundžių prieš vėl naudojant šią komandą!", delete_after=3)

@bot.event
async def on_raw_reaction_add(payload):
    """Kai vartotojas prideda reakciją, priskiria jam rolę"""
    if payload.guild_id is None:
        return  # DM reakcijos ignoruojamos

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    if payload.message_id in reaction_roles:
        role_id = reaction_roles[payload.message_id].get(payload.emoji.name)
        if role_id:
            role = guild.get_role(role_id)
            if role:
                member = guild.get_member(payload.user_id)
                if member and not member.bot:
                    await member.add_roles(role)
                    print(f'✅ Pridėta rolė {role.name} {member.name}')
    
@bot.event
async def on_raw_reaction_remove(payload):
    """Kai vartotojas pašalina reakciją, pašalina jam rolę"""
    if payload.guild_id is None:
        return  

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    if payload.message_id in reaction_roles:
        role_id = reaction_roles[payload.message_id].get(payload.emoji.name)
        if role_id:
            role = guild.get_role(role_id)
            if role:
                member = guild.get_member(payload.user_id)
                if member and not member.bot:
                    await member.remove_roles(role)
                    print(f'❌ Pašalinta rolė {role.name} iš {member.name}')

@bot.command()
async def add_reaction_role(ctx, message_id: int, emoji: str, role_id: int):
    """Rankiniu būdu prideda reakcijos-rolės susiejimą (admins only)"""
    if ctx.author.guild_permissions.administrator:
        if message_id not in reaction_roles:
            reaction_roles[message_id] = {}
        reaction_roles[message_id][emoji] = role_id
        await ctx.send(f'✅ Reakcijos {emoji} priskirta rolei <@&{role_id}> prie žinutės {message_id}')
    else:
        await ctx.send("❌ Tik administratoriai gali naudoti šią komandą!")

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
    start_dashboard()  # Paleidžiame Flask dashboard'ą atskiroje gijoje
    await load_extensions()
    await bot.start(os.getenv("DISCORD_TOKEN"))

# Startuojame bot'ą
asyncio.run(main())
