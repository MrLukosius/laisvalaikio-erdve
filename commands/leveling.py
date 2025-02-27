import discord
from discord.ext import commands
import json
import random

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
    return int(100 * (level ** 1.2))

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.XP_FILE = XP_FILE
        self.xp_data = self.load_xp_data()

    def load_xp_data(self):
        try:
            with open(self.XP_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_xp_data(self):
        with open(self.XP_FILE, "w") as f:
            json.dump(self.xp_data, f, indent=4)
        print(f"XP duomenys išsaugoti! ({len(self.xp_data)} nariai)")

    def get_level(self, xp):
        level = 1
        while xp >= xp_needed_for_level(level):
            level += 1
        return min(level, 500)

    async def update_member_roles(self, member):
        user_id = str(member.id)
        new_level = self.get_level(self.xp_data[user_id]["xp"])

        roles_to_give = [member.guild.get_role(role_id) for lvl, role_id in LEVEL_ROLES.items() if lvl <= new_level]
        roles_to_give = [role for role in roles_to_give if role and role not in member.roles]

        roles_to_remove = [member.guild.get_role(role_id) for lvl, role_id in LEVEL_ROLES.items() if lvl > new_level]
        roles_to_remove = [role for role in roles_to_remove if role and role in member.roles]

        if roles_to_give:
            await member.add_roles(*roles_to_give)

        if roles_to_remove:
            await member.remove_roles(*roles_to_remove)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        if user_id not in self.xp_data:
            self.xp_data[user_id] = {"xp": 0, "level": 1}

        gained_xp = random.randint(1, 5)
        self.xp_data[user_id]["xp"] += gained_xp
        self.save_xp_data()

        new_level = self.get_level(self.xp_data[user_id]["xp"])

        if self.xp_data[user_id]["level"] < new_level:
            self.xp_data[user_id]["level"] = new_level
            self.save_xp_data()
            await self.update_member_roles(message.author)

            channel = self.bot.get_channel(1333044850450239518)
            if channel is not None:
                await channel.send(f"🎉 {message.author.mention} pasiekė **{new_level}** lygį!")

    @commands.command(name="xpinfo")
    async def xp_info(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)
        if user_id in self.xp_data:
            xp = self.xp_data[user_id]["xp"]
            level = self.get_level(xp)
            await ctx.send(f"{member.mention} turi {xp} XP ir yra {level} lygyje.")
        else:
            await ctx.send(f"{member.mention} dar neturi XP duomenų.")

    @commands.command(name="update_roles", hidden=True)
    @commands.has_permissions(administrator=True)
    async def update_roles(self, ctx):
        guild = ctx.guild
        updated_members = 0

        for user_id, data in self.xp_data.items():
            member = guild.get_member(int(user_id))
            if not member:
                continue

            await self.update_member_roles(member)
            updated_members += 1

        await ctx.send(f"✅ Atnaujintos **{updated_members}** narių roles pagal jų XP!")

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))