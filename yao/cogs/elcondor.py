import asyncio
import logging
from asyncio import gather

import youtube_dl
from discord import (
    Client,
    FFmpegPCMAudio,
    Member,
    PCMVolumeTransformer,
    Reaction,
    User,
    VoiceChannel,
    VoiceClient,
    VoiceState,
)
from discord.ext import commands
from discord.ext.commands import Context

from yao.settings import GIGUE_URL, TUDUDU_URL

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
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        filename = data['url']
        return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


async def connect_to_voice_channel(voice_channel: VoiceChannel, guild_name: str, client: Client) -> VoiceClient:
    for vc in client.voice_clients:
        if vc.guild.name == guild_name:
            await vc.disconnect(force=True)

    voice_client: VoiceClient = await voice_channel.connect()

    return voice_client


class ElCondor(commands.Cog):
    def __init__(self, bot) -> None:
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
        await reaction.message.add_reaction(f"{reaction.emoji}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, _: VoiceState, after: VoiceState) -> None:
        if member == self.bot.user or after.channel is None:
            return

        voice_client: VoiceClient = await connect_to_voice_channel(after.channel, member.guild.name, self.bot)
        player = await YTDLSource.from_url(TUDUDU_URL)
        voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        while voice_client.is_playing():
            await asyncio.sleep(1)

        await voice_client.disconnect(force=True)

