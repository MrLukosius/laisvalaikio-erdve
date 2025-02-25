import discord
from discord.ext import commands
import random
import json
import os

# JSON failas XP duomenų saugojimui
XP_FILE = "xp_data.json"

# Kanalai ir rolių ID
LEVEL_UP_CHANNEL_ID = 1333044850450239518
LEVEL_ROLES = {
    1: 1337543319173206066,
    10: 1337543634261774556,
    20: 1337543867586707467,
    35: 1337544232373714997,
    50: 1333899221417595020
}
TOP_COMMAND = "#topas"

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_xp_data()

    def load_xp_data(self):
        """Įkelia XP duomenis iš failo arba sukuria naują"""
        if os.path.exists(XP_FILE):
            with open(XP_FILE, "r") as f:
                self.xp_data = json.load(f)
        else:
            self.xp_data = {}

    def save_xp_data(self):
        """Išsaugo XP duomenis į failą"""
        with open(XP_FILE, "w") as f:
            json.dump(self.xp_data, f, indent=4)

    def get_level_xp(self, level):
        """Apskaičiuoja, kiek XP reikia lygiui pasiekti"""
        return 100 + (level * 50)  # Kiekvienas lygis vis sunkesnis

    def get_level(self, xp):
        """Apskaičiuoja lygį pagal XP"""
        level = 1
        while xp >= self.get_level_xp(level):
            xp -= self.get_level_xp(level)
            level += 1
        return level

    @commands.Cog.listener()
    async def on_message(self, message):
        """Kai narys parašo žinutę – gauna XP"""
        if message.author.bot:
            return

        user_id = str(message.author.id)
        guild = message.guild

        if user_id not in self.xp_data:
            self.xp_data[user_id] = {"xp": 0, "level": 0}

        # Suteikiamas XP (random nuo 5 iki 15)
        xp_gained = random.randint(5, 15)
        self.xp_data[user_id]["xp"] += xp_gained

        # Apskaičiuojamas naujas lygis
        new_level = self.get_level(self.xp_data[user_id]["xp"])

        if new_level > self.xp_data[user_id]["level"]:  # Jei lygis pakilo
            self.xp_data[user_id]["level"] = new_level
            await self.level_up(message.author, guild, new_level)

        self.save_xp_data()  # Išsaugo duomenis

        # Tikrinama, ar tai komanda #topas
        if message.content.strip().lower() == TOP_COMMAND:
            await self.show_leaderboard(message.channel)

    async def level_up(self, member, guild, level):
        """Suteikia naują rolę ir praneša apie lygio pakilimą"""
        channel = self.bot.get_channel(LEVEL_UP_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="🎉 Lygio pakilimas!",
                description=f"{member.mention} pasiekė **{level} lygį**!",
                color=discord.Color.gold()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await channel.send(embed=embed)

        # Suteikiama nauja rolė, jei ji egzistuoja
        if level in LEVEL_ROLES:
            new_role = guild.get_role(LEVEL_ROLES[level])
            if new_role:
                await member.add_roles(new_role)

                # Pašalinamos senos rolės
                for lvl, role_id in LEVEL_ROLES.items():
                    if lvl < level:
                        old_role = guild.get_role(role_id)
                        if old_role in member.roles:
                            await member.remove_roles(old_role)

    async def show_leaderboard(self, channel):
        """Generuoja TOP lentelę ir siunčia embed'ą"""
        sorted_users = sorted(self.xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)
        leaderboard = ""

        for idx, (user_id, data) in enumerate(sorted_users[:10], start=1):
            user = self.bot.get_user(int(user_id))
            leaderboard += f"**{idx}.** {user.mention if user else user_id} - **{data['xp']} XP** (🆙 {data['level']} lygis)\n"

        embed = discord.Embed(
            title="🏆 Lygių TOP lentelė",
            description=leaderboard or "Nėra duomenų.",
            color=discord.Color.blue()
        )

        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))
