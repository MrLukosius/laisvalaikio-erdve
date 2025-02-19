import discord
from discord.ext import commands
import a2s

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.command()
async def bradega(ctx):
    server_address = ("45.81.254.160", 27015)
    try:
        server_info = await a2s.async_info(server_address)  # NAUDOJAME await!!!
        embed = discord.Embed(title="Bradega.lt Serverio Informacija", color=discord.Color.green())
        embed.add_field(name="Serverio Pavadinimas", value=server_info.server_name, inline=False)
        embed.add_field(name="Žemėlapis", value=server_info.map_name, inline=True)
        embed.add_field(name="Žaidėjai", value=f"{server_info.player_count}/{server_info.max_players}", inline=True)
        embed.add_field(name="Versija", value=server_info.version, inline=True)
        embed.set_footer(text="Serverio informacija atnaujinta realiu laiku!")

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"⚠️ Nepavyko gauti Bradega.lt serverio informacijos!\n```{e}```")

