import discord
from discord.ext import commands

class Serveris(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serveris")
    async def serveris(self, ctx):
        guild = ctx.guild  # Gauname serverio informaciją
        
        # Paimame duomenis
        server_name = guild.name
        server_owner = guild.owner
        member_count = guild.member_count
        created_at = guild.created_at.strftime("%Y-%m-%d")
        server_description = guild.description if guild.description else "Nėra aprašymo"

        # Sukuriame įterptą (embed) pranešimą
        embed = discord.Embed(title=f"📢 {server_name} informacija", color=discord.Color.blue())
        embed.add_field(name="👑 Savininkas", value=server_owner, inline=True)
        embed.add_field(name="👥 Narių skaičius", value=member_count, inline=True)
        embed.add_field(name="📆 Sukurta", value=created_at, inline=True)
        embed.add_field(name="📜 Aprašymas", value=server_description, inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)  # Serverio ikona, jei yra
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Serveris(bot))
