import discord
from discord.ext import commands

class Serveris(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serveris(self, ctx):
        guild = ctx.guild  # Gauname serverio objektą
        owner = guild.owner  # Gauname serverio savininką

        embed = discord.Embed(title=f"📜 {guild.name} informacija", color=discord.Color.blue())
        embed.add_field(name="👑 Savininkas", value=owner.mention if owner else "Justelis", inline=False)
        embed.add_field(name="👥 Narių skaičius", value=guild.member_count, inline=False)
        embed.add_field(name="📅 Serveris sukurtas", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Serveris(bot))
