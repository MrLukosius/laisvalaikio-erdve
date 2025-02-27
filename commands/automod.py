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

STREAMER_ROLE_ID = 1341407147833032704  # Streamer rolės ID
STREAMER_CHANNEL_ID = 1335557698959441920  # Kanalas, kuriame leidžiamos transliacijų nuorodos
MUTE_ROLE_ID = 1333038923387113565  # Mute rolė
LOG_CHANNEL_ID = 1333039387482525829  # Log kanalas
SPAM_LIMIT = 5
SPAM_TIMEFRAME = 10

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_users = {}

    async def send_log(self, ctx, action, member, reason):
        """Siunčia log'ą į log kanalą"""
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(title=f"📌 {action}", color=discord.Color.red())
            embed.add_field(name="👤 Narys", value=member.mention, inline=False)
            embed.add_field(name="📄 Priežastis", value=reason, inline=False)
            await log_channel.send(embed=embed)

    async def mute_member(self, message, reason, duration):
        """Skiria mute tik jei narys dar nėra užtildytas"""
        if any(role.id in ADMIN_ROLES for role in message.author.roles):
            return  # Administracijos nariams netaikome mute

        mute_role = discord.utils.get(message.guild.roles, id=MUTE_ROLE_ID)
        if not mute_role:
            return

        if mute_role in message.author.roles:
            return  # Jei jau turi mute, nebeduodam dar kartą

        msg = await message.channel.send(f"🔇 {message.author.mention}, gavai mute {duration} minutėms! Priežastis: **{reason}**")
        await asyncio.sleep(5)
        await msg.delete()

        await self.send_log(message, "🔇 Narys užtildytas", message.author, reason)

        await message.author.add_roles(mute_role, reason=reason)
        await asyncio.sleep(duration * 60)
        
        if mute_role in message.author.roles:
            await message.author.remove_roles(mute_role)
            await self.send_log(message, "🔊 Narys atmutintas", message.author, "Baigėsi mute laikas")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if any(role.id in ADMIN_ROLES for role in message.author.roles):
            return  # Jei narys turi administracijos rolę, netikriname jo žinučių

        content_lower = message.content.lower()
        should_delete = False
        reason = None
        mute_time = 0

        # Streamer rolės tikrinimas
        if message.channel.id == STREAMER_CHANNEL_ID and any(role.id == STREAMER_ROLE_ID for role in message.author.roles):
            return  # Jei turi streamer rolę ir rašo live kanale, leidžiame nuorodas

        # Tikriname blogus žodžius
        if any(word in content_lower for word in BAD_WORDS):
            reason = "Keiksmažodžiai"
            should_delete = True

        # Rasistiniai žodžiai → 15 min. mute
        elif any(word in content_lower for word in RACIST_WORDS):
            reason = "Rasistiniai žodžiai"
            should_delete = True
            mute_time = 15  # Mute 15 min

        # Tikriname invite linkus → 5 min. mute
        elif any(invite in content_lower for invite in INVITE_LINKS):
            reason = "Discord kvietimo linkas"
            should_delete = True
            mute_time = 5  # Mute 5 min

        # Tikriname neleistinus linkus → 5 min. mute
        elif any(link in content_lower for link in BANNED_LINKS):
            reason = "Draudžiamas linkas"
            should_delete = True
            mute_time = 5  # Mute 5 min

        # SPAM tikrinimas → 5 min. mute
        author_id = message.author.id
        now = asyncio.get_event_loop().time()

        if author_id not in self.spam_users:
            self.spam_users[author_id] = []

        self.spam_users[author_id].append(now)
        self.spam_users[author_id] = [t for t in self.spam_users[author_id] if now - t < SPAM_TIMEFRAME]

        if len(self.spam_users[author_id]) >= SPAM_LIMIT:
            reason = "Spam"
            should_delete = True
            mute_time = 5  # Mute 5 min
            self.spam_users[author_id] = []  # Resetinam spam counter

        # **N18 turinio tikrinimas** (NSFW)
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith(("image/", "video/")):
                if not message.channel.is_nsfw():
                    reason = "N-18 turinys neleistiname kanale"
                    should_delete = True
                    mute_time = 30  # Mute 30 min
                    break  # Sustabdome tikrinimą po pirmos rastos N-18 medijos

        # Jei reikia, triname žinutę ir siunčiame įspėjimą
        if should_delete:
            warn_msg = await message.channel.send(f"⚠️ {message.author.mention}, tavo žinutė buvo ištrinta. Priežastis: **{reason}**", delete_after=5)
            await asyncio.sleep(5)
            await warn_msg.delete()
            await message.delete()

        # Jei reikia mute, pridedame
        if mute_time > 0:
            await self.mute_member(message, reason, mute_time)

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
