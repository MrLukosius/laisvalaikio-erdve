import discord
from discord.ext import commands

# Kanalas, kuriame nariai turi paspausti reakciją
VERIFY_CHANNEL_ID = 1333458652828536832
# Emoji, kurį reikia paspausti
VERIFY_EMOJI = "✅"
# Rolė, kuri suteikiama paspaudus reakciją
VERIFIED_ROLE_ID = 1344063403668406335
# Rolė, kuri pašalinama paspaudus reakciją
UNVERIFIED_ROLE_ID = 1344063479312814080

class ReactionVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Kai narys paspaudžia reakciją"""
        if payload.channel_id != VERIFY_CHANNEL_ID or str(payload.emoji) != VERIFY_EMOJI:
            return  # Tikriname, ar reakcija buvo teisingame kanale ir su teisingu emoji

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return

        verified_role = guild.get_role(VERIFIED_ROLE_ID)
        unverified_role = guild.get_role(UNVERIFIED_ROLE_ID)

        if verified_role:
            await member.add_roles(verified_role)

        if unverified_role and unverified_role in member.roles:
            await member.remove_roles(unverified_role)

        try:
            await member.send("✅ Sveikas atvykęs į **Laisvalaikio Erdvė** serverį! Tu patvirtinai savo paskyrą ir gavai prieigą prie serverio!")
        except discord.Forbidden:
            pass  # Jei negalima išsiųsti žinutės, tiesiog praleidžiame

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Kai narys nuima reakciją, pašaliname jam patvirtinimo rolę"""
        if payload.channel_id != VERIFY_CHANNEL_ID or str(payload.emoji) != VERIFY_EMOJI:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member:
            return

        verified_role = guild.get_role(VERIFIED_ROLE_ID)
        if verified_role and verified_role in member.roles:
            await member.remove_roles(verified_role)

async def setup(bot):
    await bot.add_cog(ReactionVerification(bot))
