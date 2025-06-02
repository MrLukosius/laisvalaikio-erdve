import discord
import asyncio
import yt_dlp as youtube_dl
from discord.ext import commands

class Muzika(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.current_song = {}

    async def ensure_queue(self, ctx):
        if ctx.guild.id not in self.song_queue:
            self.song_queue[ctx.guild.id] = []

    async def join_voice_channel(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("❌ **Turi būti prisijungęs prie balso kanalo!**")
            return False
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        elif ctx.voice_client.channel != voice_channel:
            await ctx.voice_client.move_to(voice_channel)
        return True

    @commands.command(name="play")
    async def play(self, ctx, *, search: str):
        print(f"Komanda gauta: {search}")
        await ctx.send(f"🔎 Ieškoma: `{search}`")

        if not await self.join_voice_channel(ctx):
            return
        await self.ensure_queue(ctx)

        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "default_search": "ytsearch",
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search, download=False)
            if "entries" in info and len(info["entries"]) > 0:
                info = info["entries"][0]

            url = info["url"]
            title = info.get("title", "Nežinomas pavadinimas")

            if url is None:
                await ctx.send("❌ **Nepavyko gauti dainos URL.**")
                return

        self.song_queue[ctx.guild.id].append((url, title))

        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            await ctx.send(f"🎵 **Pridėta į eilę:** `{title}`")
        else:
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if not self.song_queue[ctx.guild.id]:
            await ctx.send("🎶 **Dainų eilė baigėsi. Botas palieka kanalą.**")
            await ctx.voice_client.disconnect()
            return

        url, title = self.song_queue[ctx.guild.id].pop(0)
        self.current_song[ctx.guild.id] = title

        def after_play(err):
            if err:
                print(f"Klaida grojant dainą: {err}")
            fut = asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Klaida po dainos: {e}")

        ctx.voice_client.stop()
        ctx.voice_client.play(
            discord.FFmpegPCMAudio(url),  # Jei reikia, pridėk path prie ffmpeg: executable="C:/ffmpeg/bin/ffmpeg.exe"
            after=after_play
        )

        await ctx.send(f"🎶 **Dabar groja:** `{title}`")

    @commands.command(name="pause")
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸ **Daina sustabdyta.**")

    @commands.command(name="unpause")
    async def unpause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ **Daina atstatyta.**")

    @commands.command(name="skip")
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭ **Daina praleista.**")
            await self.play_next(ctx)

    @commands.command(name="queue")
    async def queue(self, ctx):
        if ctx.guild.id not in self.song_queue or not self.song_queue[ctx.guild.id]:
            await ctx.send("📭 **Dainų eilė tuščia.**")
        else:
            queue_list = "\n".join([f"🎵 {song[1]}" for song in self.song_queue[ctx.guild.id]])
            await ctx.send(f"📜 **Dainų eilė:**\n{queue_list}")

    @commands.command(name="leave")
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 **Botas paliko kanalą.**")

async def setup(bot):
    await bot.add_cog(Muzika(bot))
