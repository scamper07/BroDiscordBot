from asyncio import sleep

import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

from base_logger import logger
from utility import send_embed


class Music(commands.Cog):
    """
    Cog to handle music playback in voice channels
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        self.is_playing = False
        # queue of [song, voice_channel] entries
        self.music_queue = []
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
        self.FFMPEG_OPTIONS = {
            "before_options": (
                "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            ),
            "options": "-vn",
        }

        self.vc = ""
        self.current_song = ""

    def search_yt(self, item):
        """Searches youtube for the given query and returns the first result"""
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                full = ydl.extract_info(f"ytsearch:{item}", download=False)
                logger.debug(full)
                info = full["entries"][0]
            except Exception:
                return False

        return {"source": info["formats"][0]["url"], "title": info["title"]}

    def play_next(self, ctx):
        """Plays the next song in the queue (callback after a song finishes)"""
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]
            self.current_song = self.music_queue[0][0]["title"]
            self.music_queue.pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx),
            )
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        """Connects to the voice channel and plays through the queue"""
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]["source"]

            if self.vc == "" or not self.vc.is_connected() or self.vc is None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            await send_embed(
                ctx=ctx,
                title="Now Playing",
                description=self.music_queue[0][0]["title"],
            )
            self.current_song = self.music_queue[0][0]["title"]
            self.music_queue.pop(0)

            self.vc.play(
                discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx),
            )

            while self.vc.is_playing():
                await sleep(10)

            if len(self.music_queue) == 0:
                # wait before leaving the voice channel
                await sleep(120)
                if not self.vc.is_playing():
                    await send_embed(ctx=ctx, title="Bye!")
                    await self.vc.disconnect()
        else:
            self.is_playing = False

    @commands.command(aliases=["pl"], help="Plays a selected song from youtube")
    async def play(self, ctx: commands.Context, *args) -> None:
        """Plays a selected song from youtube"""
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if voice_channel is None:
            await send_embed(ctx=ctx, title="Join voice channel and try again")
            return

        song = self.search_yt(query)
        if song is False:
            await send_embed(
                ctx=ctx, title="Could not play song, try different keyword"
            )
            return

        if self.music_queue:
            await send_embed(ctx=ctx, title="Song added to the queue")
        self.music_queue.append([song, voice_channel])

        if not self.is_playing:
            await self.play_music(ctx)

    @commands.command(aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx: commands.Context) -> None:
        """Displays the current songs in the queue"""
        retval = ""
        for index, entry in enumerate(self.music_queue, start=1):
            retval += f"{index}. {entry[0]['title']}\n\n"

        if retval:
            await send_embed(ctx=ctx, title="Playing Next", description=retval)
        else:
            await send_embed(ctx=ctx, title="No music in queue")

    @commands.command(aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx: commands.Context) -> None:
        """Skips the current song being played"""
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(aliases=["np"], help="Displays the current playing song")
    async def nowplaying(self, ctx: commands.Context) -> None:
        """Displays the currently playing song"""
        if self.vc and self.vc.is_playing():
            await send_embed(
                ctx=ctx, title="Now Playing", description=self.current_song
            )
        else:
            await send_embed(ctx=ctx, title="No music is playing")

    @commands.command(aliases=["pp"], help="Pauses song being played")
    async def pause(self, ctx: commands.Context) -> None:
        """Pauses the song being played"""
        if self.vc and self.vc.is_playing():
            self.vc.pause()
            await send_embed(ctx=ctx, title="Paused", description=self.current_song)
        else:
            await send_embed(ctx=ctx, title="No music is playing")

    @commands.command(aliases=["r"], help="Resumes paused song")
    async def resume(self, ctx: commands.Context) -> None:
        """Resumes the paused song"""
        if self.vc and self.vc.is_paused():
            self.vc.resume()
            await send_embed(ctx=ctx, title="Resumed", description=self.current_song)
        else:
            await send_embed(ctx=ctx, title="No music is paused")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))
