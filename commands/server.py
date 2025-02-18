import a2s
from bot import bot #boto importas is bot.py

@bot.command()
async def server(ctx):
    try:
        # Serverio IP ir portas
        ip = '45.81.254.160'
        port = 27015  # Paprastai Counter Strike 1.6 naudojamas šis portas

        # Sujungimas su serveriu
        server = a2s.ServerQuerier((ip, port))

        # Gauti serverio informaciją
        info = server.info()

        # Pateikite serverio informaciją
        await ctx.send(f"Serverio informacija: \n"
                       f"Žaidėjų skaičius: {info['players']}/{info['max_players']}\n"
                       f"Žemėlapis: {info['map']}\n"
                       f"Serverio pavadinimas: {info['server_name']}")
    except Exception as e:
        await ctx.send("⚠️ Nepavyko gauti serverio informacijos!")
        print(e)
