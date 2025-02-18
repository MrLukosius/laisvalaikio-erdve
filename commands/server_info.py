import discord
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def server_info(self, ctx):
        guild = ctx.guild  # Gauname serverio informaciją

        # Serverio savininkas
        owner = guild.owner

        # Serverio sukūrimo data
        created_at = guild.created_at.strftime("%Y-%m-%d %H:%M:%S")

        # Narių skaičius
        member_count = guild.member_count

        # Serverio pavadinimas ir ID
        server_name = guild.name
        server_id = guild.id

        # Serverio ikona (jei yra)
        icon_url = guild.icon.url if guild.icon else None

        embed = discord.Embed(
            title=f"📌 {server_name} Serverio Informacija",
            color=discord.Color.blue()
        )
        embed.add_field(name="📌 Serverio ID", value=server_id, inline=False)
        embed.add_field(name="👑 Savininkas", value=owner, inline=False)
        embed.add_field(name="📅 Sukurta", value=created_at, inline=False)
        embed.add_field(name="👥 Narių skaičius", value=member_count, inline=False)

        # Pridedame serverio ikoną (jei yra)
        if icon_url:
            embed.set_thumbnail(url=icon_url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
