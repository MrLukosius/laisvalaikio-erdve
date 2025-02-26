import discord
from discord.ext import commands
import json
import random
import asyncio

# XP failo pavadinimas
XP_FILE = "xp_data.json"

# Lygių rolės
LEVEL_ROLES = {
    1: 1337543319173206066,   # 1 lygis
    10: 1337543634261774556,  # 10 lygis
    20: 1337543867586707467,  # 20 lygis
    35: 1337544232373714997,  # 35 lygis
    50: 1333899221417595020   # 50 lygis
}

# XP reikalingas pasiekti lygį
def xp_needed_for_level(level):
    return int(100 * (level ** 1.2))  # Didėjantis XP kiekis

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_data = self.load_xp_data()

    def load_xp_data(self):
        """Įkelia XP duomenis iš failo"""
        try:
            with open(XP_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_xp_data(self):
        """Išsaugo XP duomenis į failą"""
        with open(XP_FILE, "w") as f:
            json.dump(self.xp_data, f, indent=4)

    def get_level(self, xp):
        """Apskaičiuoja nario lygį pagal XP"""
        level = 1
        while xp >= xp_needed_for_level(level):
            level += 1
        return min(level, 500)  # Maksimalus lygis 500

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        if user_id not in self.xp_data:
            self.xp_data[user_id] = {"xp": 0}

        # Pridedame atsitiktinį XP nuo 1 iki 5
        gained_xp = random.randint(1, 5)
        self.xp_data[user_id]["xp"] += gained_xp
        self.save_xp_data()

        new_level = self.get_level(self.xp_data[user_id]["xp"])

        # Tikriname, ar narys pakilo lygiu
        if "level" not in self.xp_data[user_id] or self.xp_data[user_id]["level"] < new_level:
            self.xp_data[user_id]["level"] = new_level
            self.save_xp_data()
            await self.handle_level_up(message.author, new_level)

    async def handle_level_up(self, member, new_level):
        """Suteikia naują rolę ir pašalina seną pasiekus naują lygį"""
        guild = member.guild
        role_to_give = LEVEL_ROLES.get(new_level)
        role_to_remove = LEVEL_ROLES.get(new_level - 1)

        if role_to_give:
            role = guild.get_role(role_to_give)
            if role and role not in member.roles:
                await member.add_roles(role)

        if role_to_remove:
            old_role = guild.get_role(role_to_remove)
            if old_role and old_role in member.roles:
                await member.remove_roles(old_role)

        # Pranešimas apie lygio pakėlimą
        channel = self.bot.get_channel(1333044850450239518)  # Lygio pasikėlimo kanalas
        if channel:
            await channel.send(f"🎉 {member.mention} pasiekė **{new_level}** lygį!")

    @commands.command(name="topas")
    async def leaderboard(self, ctx):
        """Rodo TOP 10 narių su daugiausiai XP"""
        sorted_users = sorted(self.xp_data.items(), key=lambda x: x[1]["xp"], reverse=True)[:10]
        embed = discord.Embed(title="🏆 Lygių TOP lentelė", color=discord.Color.gold())

        for index, (user_id, data) in enumerate(sorted_users, start=1):
            user = self.bot.get_user(int(user_id))
            if user:
                embed.add_field(name=f"**{index}. {user.name}**", value=f"{data['xp']} XP (🆙 {data.get('level', 1)} lygis)", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="update_roles", hidden=True)
    @commands.has_permissions(administrator=True)
    async def update_roles(self, ctx):
        """Atnaujina visų narių roles pagal jų XP"""
        guild = ctx.guild
        updated_members = 0

        for user_id, data in self.xp_data.items():
            member = guild.get_member(int(user_id))
            if not member:
                continue

            new_level = self.get_level(data["xp"])
            role_to_give = discord.utils.get(guild.roles, id=LEVEL_ROLES.get(new_level))
            role_to_remove = discord.utils.get(guild.roles, id=LEVEL_ROLES.get(new_level - 1))

            if role_to_remove and role_to_remove in member.roles:
                await member.remove_roles(role_to_remove)

            if role_to_give and role_to_give not in member.roles:
                await member.add_roles(role_to_give)
                updated_members += 1

        await ctx.send(f"✅ Atnaujintos **{updated_members}** narių roles pagal jų XP!")

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))
