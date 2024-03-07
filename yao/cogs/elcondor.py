import asyncio
import logging
from asyncio import gather
from typing import Any

import youtube_dl
from discord import (
    FFmpegPCMAudio,
    Member,
    PCMVolumeTransformer,
    Reaction,
    User,
    VoiceClient,
    VoiceState,
)
from discord.ext import commands
from discord.ext.commands import Context

from yao.settings import GIGUE_URL, TUDUDU_URL, EAZHI_USER_ID

youtube_dl.utils.bug_reports_message = lambda: ''
logger = logging.getLogger("discord.cogs.elcondor")

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(PCMVolumeTransformer):
    """
    from: https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
    """

    def __init__(self, source: Any, *, data: dict[Any, Any], volume: float = 0.45) -> None:
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url: str) -> 'YTDLSource':
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        filename = data['url']
        return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class ElCondor(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        logger.info("ElCondor cog loaded")

    @commands.command(name="gigue", description="Petit gigue de bon matin")
    async def gigue(self, ctx: Context) -> None:
        await gather(
            ctx.message.delete(),
            ctx.channel.send(GIGUE_URL)
        )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, _: User) -> None:
        if reaction.me:
            return
        # Because I mean, you can control your individuality, right ?
        if reaction.message.author.id == EAZHI_USER_ID:
            await reaction.message.add_reaction(reaction.emoji)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, _: VoiceState, after: VoiceState) -> None:
        if member == self.bot.user or after.channel is None:
            return

        for vc in self.bot.voice_clients:
            if vc.guild.name == member.guild.name:
                await vc.disconnect(force=False)

        voice_client: VoiceClient = await after.channel.connect()

        player = await YTDLSource.from_url(TUDUDU_URL)
        voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        while voice_client.is_playing():
            await asyncio.sleep(1)

        await voice_client.disconnect(force=False)
