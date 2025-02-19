import discord
from discord.ext import commands, tasks
import asyncio
import re

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_count = {}  # Laikysime kiekvieno nario žinučių skaičių
        self.muted_users = {}  # Laikysime narius, kurie buvo nutildyti
        self.banned_words = ["blt", "blyat", "blet", "nahuj", "nx", "nahui", "krw", "kurva", "kurwa", "bybis", "bybys", "bybiai"]  # Įrašyk neleistinus žodžius
        self.racist_words = ["nigga", "Nigga", "niggeris", "nyggeris", "nygeris", "nigeriukas", "pedikas", "pydaras", "pyderas", "pidaras", "pideras"]  # Rasistiniai žodžiai
        self.banned_links = ["youtube.com", "tiktok.com", "instagram.com", "facebook.com"]  # Neleistini link'ai
        self.allowed_links = ["tenor.com", "giphy.com", "ezgif.com", "bradega.lt", "discord.gg/laisvalaikioerdve", "imgur.com"]  # Leidžiami link'ai
        self.discord_invite_link_pattern = r"discord\.gg|discord\.com\/invite"
        self.check_spam.start()  # Tikrina spam'ą kas minutę
        self.log_channel_id = 1333039387482525829  # Administratoriams skirtas log kanalas

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Ignoruojame botų žinutes
        
        # Neleistini žodžiai
        if any(word in message.content.lower() for word in self.banned_words):
            await self.handle_mute(message.author, 10, "Neleistinas žodis")  # Nutildymas 10min
            await message.delete()  # Ištrinama žinutė
            await message.channel.send(f"⚠️ {message.author.mention}, tavo žinutė/-ės buvo pašalinta/-os už neleistiną žodį/-ius!")

        # Rasistiniai žodžiai
        elif any(word in message.content.lower() for word in self.racist_words):
            await self.handle_mute(message.author, 15, "Rasistinis žodis")  # Nutildymas 15min
            await message.delete()  # Ištrinama žinutė
            await message.channel.send(f"⚠️ {message.author.mention}, tavo žinutė/-ės buvo pašalinta/-os už rasistinį žodį/-ius!")

        # Neleistini link'ai
        elif any(link in message.content.lower() for link in self.banned_links):
            await self.handle_mute(message.author, 20, "Neleistinas linkas")  # Nutildymas 20min
            await message.delete()  # Ištrinama žinutė
            await message.channel.send(f"⚠️ {message.author.mention}, tavo žinutė buvo pašalinta už neleistiną linką!")

        # Leidžiami link'ai
        elif any(link in message.content.lower() for link in self.allowed_links):
            pass  # Jei leidžiamas linkas, nieko nedarome

        # Discord invite link'ai
        elif re.search(self.discord_invite_link_pattern, message.content):
            await self.handle_mute(message.author, 5, "Discord kvietimo linkas")  # Nutildymas 5min
            await message.delete()  # Ištrinama žinutė
            await message.channel.send(f"⚠️ {message.author.mention}, tavo žinutė buvo pašalinta už Discord kvietimą!")

        # Spam‘as
        elif message.author.id not in self.spam_count:
            self.spam_count[message.author.id] = 1
        else:
            self.spam_count[message.author.id] += 1

        # Jei pasikartoja 5 žinutės per minutę
        if self.spam_count.get(message.author.id, 0) >= 5:
            await self.handle_mute(message.author, 5, "Spam'as")  # Nutildymas 5min
            await message.delete()  # Ištrinama žinutė
            await message.channel.send(f"⚠️ {message.author.mention}, tavo žinutė buvo pašalinta už spam'ą!")
            self.spam_count[message.author.id] = 0  # Išvalome skaičiavimus

    async def handle_mute(self, user, mute_time, reason):
        """Nutildo vartotoją ir suteikia jam rolių su nutildymu"""
        role = discord.utils.get(user.guild.roles, id=1341145232485646387)  # Rolės ID
        if role:
            await user.add_roles(role)
            await user.send(f"Tu buvai nutildytas {mute_time} minutėms! Priežastis: {reason}")
            await asyncio.sleep(mute_time * 60)  # Laikinas mute
            await user.remove_roles(role)  # Pašalinama rolė po nutildymo
            await user.send(f"Tavo nutildymas baigėsi.")
            
            # Log'ai administratoriams
            log_channel = self.bot.get_channel(self.log_channel_id)
            embed = discord.Embed(
                title="⚠️ Bausmė skirta",
                description=f"**Vartotojas:** {user.mention}\n"
                            f"**Priežastis:** {reason}\n"
                            f"**Bausmė:** Nutildymas\n"
                            f"**Laikinas nutildymas:** {mute_time} minutės\n",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)
        else:
            print(f"Nutildymo rolė nerasta serveryje!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Resetina žinučių skaičiavimus kai naujas narys prisijungia."""
        if member.id in self.spam_count:
            del self.spam_count[member.id]

    @tasks.loop(seconds=60)  # Tikriname kas minutę
    async def check_spam(self):
        """Išvalome spam skaičiavimus po 1 minutės."""
        self.spam_count.clear()

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
