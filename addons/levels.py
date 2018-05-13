import discord
from discord.ext import commands
import datetime
import time

class Levels:
    '''
    Levek stats
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def leaderboard(self, ctx):
        """
        Displays the leaderboard. Does not work yet.
        """
        await self.bot.say("This command does not work yet.")

def setup(bot):
    bot.add_cog(Levels(bot))
