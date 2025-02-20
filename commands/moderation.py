import discord
from discord.ext import commands

# Administracijos rolių ID (jų negalima mute/kick/ban)
ADMIN_ROLES = [
    1333731772285980703, 1333030957610963022, 1338599511324360704,
    1335641678031097997, 1334093147982008424, 1334093306669432833,
    1334535150310264953
]

# Log kanalo ID
LOG_CHANNEL_ID = 1333039387482525829

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, member):
        """Patikrina, ar narys turi administracijos rolę."""
        return any(role.id in ADMIN_ROLES for role in member.roles)

    async def send_log(self, ctx, action, member, reason):
        """Siunčia log pranešimą į log kanalą."""
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(title=f"📌 {action}", color=discord.Color.red())
            embed.add_field(name="👤 Narys", value=member.mention, inline=False)
            embed.add_field(name="⚖️ Atsakingas administratorius", value=ctx.author.mention, inline=False)
            embed.add_field(name="📄 Priežastis", value=reason, inline=False)
            await log_channel.send(embed=embed)

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
        await self.send_log(ctx, "🚪 Narys išmestas", member, reason)

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
        await self.send_log(ctx, "⛔ Narys užblokuotas", member, reason)

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
        await self.send_log(ctx, "🔇 Narys užtildytas", member, reason)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Nuima mute nuo nario."""
        mute_role = discord.utils.get(ctx.guild.roles, id=1333038923387113565)  # Mute rolės ID
        if not mute_role:
            await ctx.send("⚠️ Klaida: Nerasta 'Mute' rolė!")
            return
        if mute_role not in member.roles:
            await ctx.send(f"ℹ️ {member.mention} nėra užtildytas.")
            return
        await member.remove_roles(mute_role)
        await ctx.send(f"🔊 {member.mention} buvo atmutintas!")
        await self.send_log(ctx, "🔊 Narys atmutintas", member, "Mute nuimtas")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
