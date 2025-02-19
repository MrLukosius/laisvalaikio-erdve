import discord
from discord.ext import commands
import a2s

class Bradega(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bradega(self, ctx):
        ip = "45.81.254.160"
        port = 27015
        server_address = (ip, port)

        try:
            # Bandom gauti serverio informaciją
            server_info = a2s.info(server_address)
            print(server_info)  # Išvedam terminale, kad patikrintume duomenis

            # Sukuriame atsakymą su serverio informacija
            embed = discord.Embed(title="🎮 Bradega.lt Serverio Informacija", color=discord.Color.green())
            embed.add_field(name="📛 Serverio Pavadinimas", value=server_info.server_name, inline=False)
            embed.add_field(name="🗺️ Žemėlapis", value=server_info.map, inline=True)
            embed.add_field(name="👥 Žaidėjai", value=f"{server_info.player_count}/{server_info.max_players}", inline=True)
            embed.add_field(name="🕹️ Žaidimas", value=server_info.game, inline=False)
            embed.set_footer(text="Informacija atnaujinta automatiškai.")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send("⚠️ Nepavyko gauti Bradega.lt serverio informacijos!")
            print(f"Klaida: {e}")

# Testuojame serverio informaciją terminale
if __name__ == "__main__":
    server_address = ("45.81.254.160", 27015)
    try:
        server_info = a2s.info(server_address)
        print(server_info)
    except Exception as e:
        print(f"Klaida: {e}")

async def setup(bot):
    await bot.add_cog(Bradega(bot))
