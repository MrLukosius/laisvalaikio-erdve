import discord
from discord.ext import commands, tasks
import asyncio
import re

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_count = {}
        self.warning_count = {}
        self.muted_users = {}
        self.banned_words = ["blt", "blyat", "blet", "nahuj", "nx", "nahui", "krw", "kurva", "kurwa", "bybis", "bybys", "bybiai"]
        self.racist_words = ["nigga", "Nigga", "niggeris", "nyggeris", "nygeris", "nigeriukas", "pedikas", "pydaras", "pyderas", "pidaras", "pideras"]
        self.banned_links = ["youtube.com", "tiktok.com", "instagram.com", "facebook.com"]
        self.allowed_links = ["tenor.com", "giphy.com", "ezgif.com", "bradega.lt", "discord.gg/laisvalaikioerdve", "imgur.com"]
        self.discord_invite_link_pattern = r"discord\.gg|discord\.com\/invite"
        self.log_channel_id = 1333039387482525829
        self.mute_role_id = 1333038923387113565
        self.admin_roles = [1333731772285980703, 1333030957610963022, 1338599511324360704, 1335641678031097997, 1334093147982008424, 1334093306669432833, 1334535150310264953]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # Neleisti administracijos mute'inimo
        if any(role.id in self.admin_roles for role in message.author.roles):
            return
        
        user_id = message.author.id
        channel = message.channel
        
        # Keiksmažodžiai – 3 kartai iš eilės → mute
        if any(word in message.content.lower() for word in self.banned_words):
            self.warning_count[user_id] = self.warning_count.get(user_id, 0) + 1
            if self.warning_count[user_id] >= 3:
                await self.apply_mute(message.author, 10, "Per dažni keiksmažodžiai", channel)
                self.warning_count[user_id] = 0  # Resetinam skaičiavimą
            else:
                await channel.send(f"⚠️ {message.author.mention}, tai {self.warning_count[user_id]}/3 įspėjimai dėl keiksmažodžių!")

        # Rasistiniai žodžiai – iškart mute
        elif any(word in message.content.lower() for word in self.racist_words):
            await self.apply_mute(message.author, 15, "Rasistinis turinys", channel)

        # Discord kvietimo linkai – mute
        elif re.search(self.discord_invite_link_pattern, message.content):
            await self.apply_mute(message.author, 5, "Discord kvietimo linkas", channel)

        # Spam – 5 kartai iš eilės → mute
        else:
            self.spam_count[user_id] = self.spam_count.get(user_id, 0) + 1
            if self.spam_count[user_id] >= 5:
                await self.apply_mute(message.author, 5, "Spam", channel)
                self.spam_count[user_id] = 0  # Resetinam skaičiavimą

    async def apply_mute(self, user, mute_time, reason, channel):
        """Uždeda mute rolę ir praneša į log kanalą"""
        role = discord.utils.get(user.guild.roles, id=self.mute_role_id)
        if role:
            await user.add_roles(role)
            await channel.send(f"🔇 {user.mention}, gavai mute {mute_time} minutėms! Priežastis: **{reason}**")
            
            # Log'ai administratoriams
            log_channel = self.bot.get_channel(self.log_channel_id)
            embed = discord.Embed(
                title="⚠️ Bausmė skirta",
                description=f"**Vartotojas:** {user.mention}\n"
                            f"**Priežastis:** {reason}\n"
                            f"**Bausmė:** Nutildymas\n"
                            f"**Laikas:** {mute_time} min\n",
                color=discord.Color.red()
            )
            await log_channel.send(embed=embed)

            await asyncio.sleep(mute_time * 60)
            await user.remove_roles(role)
            await channel.send(f"✅ {user.mention}, tavo mute baigėsi.")
        else:
            print("Mute rolė nerasta!")

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
