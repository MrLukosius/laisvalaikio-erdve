import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput, Select


class EmbedBuilder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed")
    async def embed_command(self, ctx):
        """Pradeda embed kūrimo procesą"""
        await ctx.send("🛠️ Įveskite informaciją apie embed:", ephemeral=True)
        await ctx.author.send_modal(EmbedModal())  # Modal siunčiamas DM arba kaip interakcija


class EmbedModal(Modal, title="Sukurti Embed"):
    title_input = TextInput(label="Pavadinimas", required=True)
    description_input = TextInput(label="Aprašymas", style=discord.TextStyle.long, required=True)
    color_input = TextInput(label="Spalva (hex, pvz., #ff0000)", required=False)
    image_input = TextInput(label="Paveikslėlio URL", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        """Kai vartotojas pateikia informaciją"""
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.description_input.value,
            color=discord.Color.from_str(self.color_input.value) if self.color_input.value else discord.Color.blue()
        )
        if self.image_input.value:
            embed.set_image(url=self.image_input.value)

        await interaction.response.send_message(
            "🔍 Peržiūrėkite savo embed:",
            embed=embed,
            view=EmbedView(embed),
            ephemeral=True
        )


class EmbedView(View):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed

        send_button = Button(label="Išsiųsti", style=discord.ButtonStyle.green)
        send_button.callback = self.send_embed
        self.add_item(send_button)

        cancel_button = Button(label="Atšaukti", style=discord.ButtonStyle.red)
        cancel_button.callback = self.cancel_embed
        self.add_item(cancel_button)

    async def send_embed(self, interaction: discord.Interaction):
        """Kai paspaudžiamas 'Išsiųsti' mygtukas"""
        await interaction.response.send_message("📩 Pasirinkite kanalą:", view=ChannelSelectView(self.embed), ephemeral=True)

    async def cancel_embed(self, interaction: discord.Interaction):
        """Kai paspaudžiamas 'Atšaukti' mygtukas"""
        await interaction.response.send_message("❌ Embed kūrimas atšauktas.", ephemeral=True)
        self.stop()


class ChannelSelectView(View):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed

        channels = [
            discord.SelectOption(label=channel.name, value=str(channel.id))
            for channel in embed.guild.text_channels if channel.permissions_for(embed.guild.me).send_messages
        ]

        self.select = Select(placeholder="Pasirinkite kanalą", options=channels)
        self.select.callback = self.channel_selected
        self.add_item(self.select)

    async def channel_selected(self, interaction: discord.Interaction):
        """Kai vartotojas pasirenka kanalą"""
        channel_id = int(self.select.values[0])
        channel = interaction.guild.get_channel(channel_id)

        if channel:
            await channel.send(embed=self.embed)
            await interaction.response.send_message("✅ Embed sėkmingai išsiųstas!", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ Nepavyko rasti kanalo.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(EmbedBuilder(bot))
