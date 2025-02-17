import discord
from discord.ext import commands
import a2s  # Atsiųsti serverio duomenis

# CS 1.6 serverio adresas ir portas
SERVER_IP = "45.81.254.160"
SERVER_PORT = 27015  # Pakeisk į savo serverio portą

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server(self, ctx):
        """Gauti CS 1.6 serverio informaciją"""
        server_address = (SERVER_IP, SERVER_PORT)

        try:
            server_info = a2s.info(server_address)
            players = a2s.players(server_address)

            player_names = "\n".join([player.name for player in players]) if players else "Nėra žaidėjų"

            embed = discord.Embed(title="🎮 Bradega.lt Serverio Informacija", color=discord.Color.green())
            embed.add_field(name="📌 Serveris", value=server_info.server_name, inline=False)
            embed.add_field(name="🗺️ Žemėlapis", value=server_info.map_name, inline=True)
            embed.add_field(name="👥 Žaidėjai", value=f"{server_info.player_count}/{server_info.max_players}", inline=True)
            embed.add_field(name="🎮 Modas", value=server_info.game, inline=True)
            embed.add_field(name="🔹 Žaidėjų sąrašas", value=player_names, inline=False)
            embed.set_footer(text=f"IP: {SERVER_IP}:{SERVER_PORT}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Nepavyko gauti serverio informacijos!\n```{e}```")

async def setup(bot):
    await bot.add_cog(Server(bot))
