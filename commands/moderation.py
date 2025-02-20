import discord
from discord.ext import commands

# Administracijos rolių ID, kuriems negalima taikyti bausmių
ADMIN_ROLES = [
    1333731772285980703, 1333030957610963022, 1338599511324360704,
    1335641678031097997, 1334093147982008424, 1334093306669432833,
    1334535150310264953
]

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, member):
        """Patikrina, ar narys turi administracijos rolę."""
        return any(role.id in ADMIN_ROLES for role in member.roles)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Nenurodyta priežastis"):
        if self.is_admin(member):
            await ctx.send("⚠️ Negalite išmesti administracijos nario!")
            return
        if ctx.author.top_role <= member.top_role:
            await ctx.send("⚠️ Tu negali išmesti šio nario, nes jis turi aukštesnę arba lygiavertę rolę!")
            return
        await member.kick(reason=reason)
        await ctx.send(f"✅ {member.mention} buvo išmestas! Priežastis: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Nenurodyta priežastis"):
        if self.is_admin(member):
            await ctx.send("⚠️ Negalite užblokuoti administracijos nario!")
            return
        if ctx.author.top_role <= member.top_role:
            await ctx.send("⚠️ Tu negali užblokuoti šio nario, nes jis turi aukštesnę arba lygiavertę rolę!")
            return
        await member.ban(reason=reason)
        await ctx.send(f"✅ {member.mention} buvo užblokuotas! Priežastis: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="Nenurodyta priežastis"):
        mute_role = discord.utils.get(ctx.guild.roles, id=1333038923387113565)  # Mute rolės ID
        if not mute_role:
            await ctx.send("⚠️ Klaida: Nerasta 'Mute' rolė!")
            return
        if self.is_admin(member):
            await ctx.send("⚠️ Negalite užtildyti administracijos nario!")
            return
        if ctx.author.top_role <= member.top_role:
            await ctx.send("⚠️ Tu negali užtildyti šio nario, nes jis turi aukštesnę arba lygiavertę rolę!")
            return
        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} buvo užtildytas! Priežastis: {reason}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
