import logging

import discord
from discord import Message
from discord.ext import commands

from yao.cogs.elcondor import ElCondor
from yao.cogs.legacy import Legacy
from yao.settings import CLIENT_SECRET

logger = logging.getLogger("discord")
intents = discord.Intents.default()
intents.message_content = True


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!", intents=intents, help_command=None,)

    async def setup_hook(self) -> None:
        await self.add_cog(ElCondor(bot))
        await self.add_cog(Legacy(bot))

    async def on_message(self, message: Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_ready(self) -> None:
        logger.info("Bot ready !")


if __name__ == "__main__":
    bot = DiscordBot()
    bot.run(CLIENT_SECRET)
