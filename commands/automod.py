from datetime import datetime, timedelta
import discord
from discord.ext import commands
import asyncio

BAD_WORDS = ["blt", "blyat", "blet", "nahuj", "nx", "nahui", "krw", "kurva", "kurwa", "bybis", "bybys", "bybiai"]
RACIST_WORDS = ["nigga", "niggeris", "nyggeris", "nygeris", "nigeriukas", "pedikas", "pydaras", "pyderas", "pidaras", "pideras"]
BANNED_LINKS = ["youtube.com", "tiktok.com", "instagram.com", "facebook.com"]
ALLOWED_LINKS = ["tenor.com", "giphy.com", "ezgif.com", "bradega.lt", "discord.gg/laisvalaikioerdve", "imgur.com"]
INVITE_LINKS = ["discord.gg/", "discord.com/invite/"]

ADMIN_ROLES = [
    1333731772285980703, 1333030957610963022, 1338599511324360704,
    1335641678031097997, 1334093147982008424, 1334093306669432833,
    1334535150310264953
]  # Administracijos rolių ID

ALLOWED_STREAM_ROLE = 1341407147833032704  # Rolė, leidžianti kelti stream nuorodas
ALLOWED_STREAM_CHANNEL = 1335557698959441920  # Kanalo ID, kur leidžiama kelti stream nuorodas
STREAM_LINKS = ["youtube.com", "tiktok.com", "kick.com", "twitch.tv"]

MUTE_ROLE_ID = 1333038923387113565  # Mute rolė
LOG_CHANNEL_ID = 1333039387482525829  # Log kanalas
SPAM_LIMIT = 5
SPAM_TIMEFRAME = 10

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_users = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if any(role.id in ADMIN_ROLES for role in message.author.roles):
            return  # Administracijos nariams netikriname žinučių

        content_lower = message.content.lower()
        should_delete = False
        reason = None
        mute_time = 0

        # Leidžiame stream nuorodas tam tikrame kanale nariams su ALLOWED_STREAM_ROLE
        if any(link in content_lower for link in STREAM_LINKS):
            if message.channel.id == ALLOWED_STREAM_CHANNEL and any(role.id == ALLOWED_STREAM_ROLE for role in message.author.roles):
                return  # Leidžiame šią nuorodą

        # Tikriname blogus žodžius
        if any(word in content_lower for word in BAD_WORDS):
            reason = "Keiksmažodžiai"
            should_delete = True

        # Rasistiniai žodžiai → 15 min. mute
        elif any(word in content_lower for word in RACIST_WORDS):
            reason = "Rasistiniai žodžiai"
            should_delete = True
            mute_time = 15

        # Tikriname invite linkus → 5 min. mute
        elif any(invite in content_lower for invite in INVITE_LINKS):
            reason = "Discord kvietimo linkas"
            should_delete = True
            mute_time = 5

        # Tikriname neleistinus linkus → 5 min. mute
        elif any(link in content_lower for link in BANNED_LINKS):
            reason = "Draudžiamas linkas"
            should_delete = True
            mute_time = 5

        # Jei reikia, triname žinutę
        if should_delete:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, tavo žinutė buvo ištrinta. Priežastis: **{reason}**", delete_after=5)

        # Jei reikia mute, pridedame
        if mute_time > 0:
            await self.mute_member(message, reason, mute_time)

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
