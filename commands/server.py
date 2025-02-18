import discord
from discord.ext import commands
import a2s  # Patikrink, ar modulis įdiegtas!

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server(self, ctx):
        try:
            ip = '45.81.254.160'
            port = 27015  # CS 1.6 portas
            server = a2s.info((ip, port))  # NAUDOJAME `a2s.info()`
            
            await ctx.send(f"Serverio informacija: \n"
                           f"Žaidėjų skaičius: {server.player_count}/{server.max_players}\n"
                           f"Žemėlapis: {server.map_name}\n"
                           f"Serverio pavadinimas: {server.server_name}")
        except Exception as e:
            await ctx.send("⚠️ Nepavyko gauti serverio informacijos!")
            print(e)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
