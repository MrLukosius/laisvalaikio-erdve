import discord
from discord.ext import commands

# Logų kanalo ID
LOG_CHANNEL_ID = 1333039387482525829

# Rolės, kurias naujas narys turėtų gauti
ROLE_IDS = [
    1341145400505274509,
    1338601212785721464,
    1333034068207603836,
    1338601474812416110,
    1338600863274631220,
]

class MemberLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Kai narys prisijungia į serverį"""
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="📥 Naujas narys prisijungė!",
                description=f"👤 **{member.name}**#{member.discriminator} ({member.mention}) prisijungė prie serverio!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await log_channel.send(embed=embed)

        # Priskiria roles
        for role_id in ROLE_IDS:
            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Kai narys išeina iš serverio"""
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="📤 Narys išėjo",
                description=f"🚪 **{member.name}**#{member.discriminator} paliko serverį.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MemberLogger(bot))
