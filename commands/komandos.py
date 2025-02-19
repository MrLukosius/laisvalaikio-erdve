import discord
from discord.ext import commands

class Komandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="komandos", help="Parodo visų komandų sąrašą")
    async def komandos(self, ctx):
        embed = discord.Embed(
            title="📜 Komandų sąrašas",
            description="Laisvalaikio Erdvės Bot'o komandų sąrašas.",
            color=discord.Color.blue()
        )

        # Pagrindinės komandos (visi gali naudoti)
        pagrindines = """
        **#komandos** – Boto komandų sąrašas
        **#serveris** – Parodo serverio informaciją
        **#bradega** – Bradega.lt serverio informacija (tvarkoma)
        **labas, sveikas, sveiki** – Botas pasisveikins su jumis
        **#nario-info arba #nario-info @vnarys** – parodo informaciją apie jus ar apie kitą narį
        """
        embed.add_field(name="✅ Pagrindinės komandos", value=pagrindines, inline=False)

        # Administracijos komandos (tik su leidimais)
        administracija = """
        **#kick @narys [priežastis]** – Išspiria vartotoją iš serverio
        **#ban @narys [priežastis]** – Užblokuoja vartotoją
        **#mute @narys [trukmė]** – Nutildo vartotoją (uždeda rolę)
        **#unmute @narys** – Nuima mute nuo vartotojo
        """
        embed.add_field(name="🛠 Administracijos komandos", value=administracija, inline=False)

        embed.set_footer(text="Naudokite komandas atsakingai!")

        await ctx.send(embed=embed)

# Pridedame šį Cog prie boto
async def setup(bot):
    await bot.add_cog(Komandos(bot))
