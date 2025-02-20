import discord
from discord.ext import commands

ADMIN_ROLES = [
    1333731772285980703, 1333030957610963022, 1338599511324360704,
    1335641678031097997, 1334093147982008424, 1334093306669432833,
    1334535150310264953
]  # Administracijos rolių ID

LOG_CHANNEL_ID = 1333039387482525829  # Log kanalas

class CleanMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, ctx, amount):
        """Siunčia log'ą apie ištrintas žinutes"""
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(title="🧹 Kanale ištrintos žinutės", color=discord.Color.orange())
            embed.add_field(name="👤 Administracijos narys", value=ctx.author.mention, inline=False)
            embed.add_field(name="📄 Kiekis", value=f"{amount} žinutės(-čių)", inline=False)
            embed.add_field(name="📌 Kanale", value=ctx.channel.mention, inline=False)
            await log_channel.send(embed=embed)

    @commands.command(name="isvalyti")
    @commands.has_permissions(manage_messages=True)
    async def isvalyti(self, ctx, amount: int):
        """Ištrina žinutes iš kanalo. Tik administracija gali naudoti"""
        if not any(role.id in ADMIN_ROLES for role in ctx.author.roles):
            await ctx.send("❌ **Neturi leidimo naudoti šios komandos!**", delete_after=5)
            return

        if amount > 500:
            await ctx.send("⚠️ **Negali ištrinti daugiau nei 500 žinučių vienu metu!**", delete_after=5)
            return
        if amount < 1:
            await ctx.send("⚠️ **Turi nurodyti bent 1 žinutę!**", delete_after=5)
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"✅ **Ištrintos {len(deleted) - 1} žinutės!**", delete_after=5)
        await self.send_log(ctx, len(deleted) - 1)

async def setup(bot):
    await bot.add_cog(CleanMessages(bot))
