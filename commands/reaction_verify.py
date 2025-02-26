import discord
import random
import string
import asyncio
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

# Kanalas, kuriame nariai turi paspausti reakciją
VERIFY_CHANNEL_ID = 1333458652828536832
LOG_CHANNEL_ID = 1333039387482525829  # Logų kanalas
# Emoji, kurį reikia paspausti
VERIFY_EMOJI = "✅"
# Rolės
VERIFIED_ROLE_ID = 1344063403668406335
UNVERIFIED_ROLE_ID = 1344063479312814080

class ReactionVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != VERIFY_CHANNEL_ID or str(payload.emoji) != VERIFY_EMOJI:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member or member.bot:
            return
        
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        captcha_image = self.generate_captcha(captcha_text)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        verification_channel = await guild.create_text_channel(f'verifikacija-{member.name}', overwrites=overwrites)
        
        with open("captcha.png", "wb") as f:
            captcha_image.save(f, format='PNG')
        
        await verification_channel.send(file=discord.File("captcha.png"))
        await verification_channel.send(f"{member.mention}, įrašyk kodą iš paveikslėlio!")
        
        def check(msg):
            return msg.channel == verification_channel and msg.author == member
        
        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            if msg.content.strip().upper() == captcha_text:
                verified_role = guild.get_role(VERIFIED_ROLE_ID)
                unverified_role = guild.get_role(UNVERIFIED_ROLE_ID)
                if verified_role:
                    await member.add_roles(verified_role)
                if unverified_role and unverified_role in member.roles:
                    await member.remove_roles(unverified_role)
                await verification_channel.delete()
                log_channel = guild.get_channel(LOG_CHANNEL_ID)
                if log_channel:
                    await log_channel.send(f"✅ {member.mention} sėkmingai perėjo patvirtinimą!")
            else:
                await verification_channel.send("❌ Neteisingas kodas! Bandyk iš naujo paspaudęs reakciją.")
                await asyncio.sleep(5)
                await verification_channel.delete()
        except asyncio.TimeoutError:
            await verification_channel.send("⏳ Laikas baigėsi! Bandyk iš naujo paspaudęs reakciją.")
            await asyncio.sleep(5)
            await verification_channel.delete()

    def generate_captcha(self, text):
        image = Image.new('RGB', (200, 100), color=(255, 255, 255))
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(image)
        draw.text((50, 40), text, fill=(0, 0, 0), font=font)
        return image

async def setup(bot):
    await bot.add_cog(ReactionVerification(bot))
