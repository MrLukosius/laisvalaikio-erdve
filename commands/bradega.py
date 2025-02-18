import a2s
from discord.ext import commands

class Bradega(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bradega")
    async def bradega(self, ctx):
        try:
            ip = '45.81.254.160'
            port = 27015  

            server = a2s.ServerQuerier((ip, port))
            info = server.info()

            await ctx.send(f"🎮 **Bradega serveris:**\n"
                           f"👥 Žaidėjų skaičius: {info['players']}/{info['max_players']}\n"
                           f"🗺️ Žemėlapis: {info['map']}\n"
                           f"📢 Pavadinimas: {info['server_name']}")
        except Exception as e:
            await ctx.send("⚠️ Nepavyko gauti Bradega serverio informacijos!")
            print(e)

async def setup(bot):
    await bot.add_cog(Bradega(bot))
