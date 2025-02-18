import discord
from discord.ext import commands
from bot import bot

class Labas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def labas(self, ctx):
        await ctx.send("Labas! :)")

async def setup(bot):
    await bot.add_cog(Labas(bot))  # BŪTINAI su await!
