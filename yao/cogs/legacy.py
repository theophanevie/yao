import logging
import random

import cowsay
from discord import Message
from discord.ext import commands

from yao.settings import YAO_USER_ID

logger = logging.getLogger("discord.cogs.legacy")


class Legacy(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        logger.info("Legacy cog loaded")

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return

        if YAO_USER_ID in message.content:
            msg = cowsay.main.get_output_string(random.choice(list(cowsay.main.CHARS.keys())), "Woof")

            await message.channel.send(f"```{msg}```")

        elif "re mec" in message.content:
            if "valo" in message.content:
                await message.channel.send("Re mec ! ça tombe bien on vient de lancer le jeu !")
            else:
                await message.channel.send(
                    "Oohh re mec ! ça te dis une petite game de valo ? je viens de finir mon practice"
                )

        elif "tit valo" in message.content:
            await message.channel.send("Ouais allez, p'tit valo !")

        elif "jinxed" in message.content:
            await message.channel.send("https://www.youtube.com/watch?v=un9x-DjTMT0")

        elif "super" in message.content:
            await message.channel.send("C'est super !")

        elif "tit stream" in message.content:
            await message.channel.send(
                """Pour passer un bon moment avec les copains : https://www.twitch.tv/paulputier
                || --> N'hésitez pas à claquer votre prime :money_with_wings: ||""")
