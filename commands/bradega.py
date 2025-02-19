import a2s
from bot import bot
from discord.ext import commands

@bot.command()
async def bradega(ctx):
    try:
        ip = "45.81.254.160"
        port = 27015

        # Gauname serverio informaciją
        server_address = (ip, port)
        info = a2s.info(server_address)

        await ctx.send(f"🎮 **Bradega.lt Serverio informacija:**\n"
                       f"🔹 Žaidėjų skaičius: {info.player_count}/{info.max_players}\n"
                       f"🌍 Žemėlapis: {info.map_name}\n"
                       f"🏷️ Serverio pavadinimas: {info.server_name}")
    except Exception as e:
        await ctx.send("⚠️ Nepavyko gauti Bradega serverio informacijos!")
        print(e)
