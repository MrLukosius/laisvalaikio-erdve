import discord
from discord.ext import commands
import a2s
import asyncio

class Bradega(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bradega")
    async def bradega_info(self, ctx):
        """Gauti Bradega.lt serverio informaciją"""
        server_address = ("45.81.254.160", 27015)

        try:
            loop = asyncio.get_running_loop()
            server_info = await loop.run_in_executor(None, a2s.info, server_address)

            embed = discord.Embed(title="Bradega.lt Serverio Informacija", color=discord.Color.green())
            embed.add_field(name="🔹 Serveris", value=server_info.server_name, inline=False)
            embed.add_field(name="📍 Žemėlapis", value=server_info.map_name, inline=True)
            embed.add_field(name="👥 Žaidėjai", value=f"{server_info.player_count}/{server_info.max_players}", inline=True)
            embed.add_field(name="🛡️ VAC", value="Įjungtas" if server_info.vac_enabled else "Išjungtas", inline=False)
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("⚠️ Nepavyko gauti Bradega.lt serverio informacijos!")
            print(f"Klaida gaunant serverio info: {e}")

async def setup(bot):
    await bot.add_cog(Bradega(bot))
