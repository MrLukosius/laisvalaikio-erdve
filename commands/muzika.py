import discord
import asyncio
import yt_dlp as youtube_dl
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.current_song = {}

    async def ensure_queue(self, ctx):
        """Sukuria dainų eilę konkrečiam gildijai"""
        if ctx.guild.id not in self.song_queue:
            self.song_queue[ctx.guild.id] = []

    async def join_voice_channel(self, ctx):
        """Botas prisijungia į balso kanalą"""
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
        """Prideda dainą į eilę arba pradeda groti"""
        if not await self.join_voice_channel(ctx):
            return
        await self.ensure_queue(ctx)

        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "default_search": "ytsearch",
            "extract_flat": "in_playlist",
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search, download=False)
            if "entries" in info:
                info = info["entries"][0]
            url = info["url"]
            title = info["title"]

        self.song_queue[ctx.guild.id].append((url, title))

        if ctx.voice_client.is_playing():
            await ctx.send(f"🎵 **Pridėta į eilę:** `{title}`")
        else:
            await self.play_next(ctx)

    

        url, title = self.song_queue[ctx.guild.id].pop(0)
        self.current_song[ctx.guild.id] = title

        ctx.voice_client.stop()
        ctx.voice_client.play(discord.FFmpegPCMAudio(url, executable="ffmpeg"), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))

        await ctx.send(f"🎶 **Dabar groja:** `{title}`")

    @commands.command(name="pause")
    async def pause(self, ctx):
        """Sustabdo dabartinę dainą"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸ **Daina sustabdyta.**")

    @commands.command(name="unpause")
    async def unpause(self, ctx):
        """Atstato sustabdytą dainą"""
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ **Daina atstabdyta.**")

    @commands.command(name="skip")
    async def skip(self, ctx):
        """Praleidžia dabartinę dainą"""
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭ **Daina praleista.**")
            await self.play_next(ctx)

    @commands.command(name="queue")
    async def queue(self, ctx):
        """Parodo dainų eilę"""
        if ctx.guild.id not in self.song_queue or not self.song_queue[ctx.guild.id]:
            await ctx.send("📭 **Dainų eilė tuščia.**")
        else:
            queue_list = "\n".join([f"🎵 {song[1]}" for song in self.song_queue[ctx.guild.id]])
            await ctx.send(f"📜 **Dainų eilė:**\n{queue_list}")

    @commands.command(name="leave")
    async def leave(self, ctx):
        """Botas palieka balso kanalą"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("👋 **Botas paliko kanalą.**")

async def setup(bot):
    await bot.add_cog(Music(bot))
