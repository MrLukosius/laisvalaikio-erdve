import discord
from discord.ext import commands
import asyncio

BAD_WORDS = ["blt", "blyat", "blet", "nahuj", "nx", "nahui", "krw", "kurva", "kurwa", "bybis", "bybys", "bybiai"]
RACIST_WORDS = ["nigga", "Nigga", "niggeris", "nyggeris", "nygeris", "nigeriukas", "pedikas", "pydaras", "pyderas", "pidaras", "pideras"]
BANNED_LINKS = ["youtube.com", "tiktok.com", "instagram.com", "facebook.com"]
ALLOWED_LINKS = ["tenor.com", "giphy.com", "ezgif.com", "bradega.lt", "discord.gg/laisvalaikioerdve", "imgur.com"]
INVITE_LINKS = ["discord.gg/", "discord.com/invite/"]

ADMIN_ROLES = [
    1333731772285980703, 1333030957610963022, 1338599511324360704,
    1335641678031097997, 1334093147982008424, 1334093306669432833,
    1334535150310264953
]

MUTE_ROLE_ID = 1333038923387113565  # Mute rolės ID
LOG_CHANNEL_ID = 1333039387482525829  # Log kanalo ID
SPAM_LIMIT = 5
SPAM_TIMEFRAME = 10  # Sekundėmis

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_users = {}
        self.muted_users = {}

    async def send_log(self, action, member, reason):
        """Siunčia log'ą į log kanalą"""
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(title=f"📌 {action}", color=discord.Color.red())
            embed.add_field(name="👤 Narys", value=member.mention, inline=False)
            embed.add_field(name="📄 Priežastis", value=reason, inline=False)
            await log_channel.send(embed=embed)

    async def mute_member(self, message, reason, duration):
        """Prideda mute rolę nariui"""
        if any(role.id in ADMIN_ROLES for role in message.author.roles):
            return  # Administratorių netildome

        mute_role = discord.utils.get(message.guild.roles, id=MUTE_ROLE_ID)
        if not mute_role:
            return

        if message.author.id in self.muted_users:
            return  # Jei jau mute, nieko nedarom

        await message.author.add_roles(mute_role, reason=reason)
        await message.channel.send(f"🔇 {message.author.mention}, gavai mute! Priežastis: **{reason}**")
        await self.send_log("🔇 Narys užtildytas", message.author, reason)

        self.muted_users[message.author.id] = True  
        await asyncio.sleep(duration * 60)

        if self.muted_users.get(message.author.id):
            await message.author.remove_roles(mute_role)
            await self.send_log("🔊 Narys atmutintas", message.author, "Baigėsi mute laikas")
            del self.muted_users[message.author.id]  

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or any(role.id in ADMIN_ROLES for role in message.author.roles):
            return  

        content_lower = message.content.lower()
        should_delete = False
        reason = None

        # Tikriname keiksmažodžius ir rasistinius žodžius
        if any(word in content_lower for word in BAD_WORDS):
            reason = "Keiksmažodžiai"
            should_delete = True
        elif any(word in content_lower for word in RACIST_WORDS):
            reason = "Rasistiniai žodžiai"
            should_delete = True
            await self.mute_member(message, reason, 15)  

        # Tikriname invite linkus
        elif any(invite in content_lower for invite in INVITE_LINKS):
            reason = "Discord kvietimo linkas"
            should_delete = True
            await self.mute_member(message, reason, 5)  

        # Tikriname neleistinus linkus
        elif any(link in content_lower for link in BANNED_LINKS) and not any(link in content_lower for link in ALLOWED_LINKS):
            reason = "Draudžiamas linkas"
            should_delete = True

        # SPAM tikrinimas
        author_id = message.author.id
        now = asyncio.get_event_loop().time()

        if author_id not in self.spam_users:
            self.spam_users[author_id] = []

        self.spam_users[author_id].append(now)
        self.spam_users[author_id] = [t for t in self.spam_users[author_id] if now - t < SPAM_TIMEFRAME]

        if len(self.spam_users[author_id]) >= SPAM_LIMIT:
            reason = "Spam"
            should_delete = True
            await self.mute_member(message, reason, 5)  
            self.spam_users[author_id] = []  

        # Jei reikia, triname žinutę ir siunčiame įspėjimą, bet tik vieną kartą
        if should_delete:
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, tavo žinutė buvo ištrinta. Priežastis: **{reason}**", delete_after=5)

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
