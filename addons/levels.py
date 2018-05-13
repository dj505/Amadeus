import discord
from discord.ext import commands
from configparser import SafeConfigParser

class Levels:
    '''
    Levek stats
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def xp(self, ctx):
        """
        Displays your xp.
        """
        user = ctx.message.author.id
        config = SafeConfigParser()
        config.read('xp.ini')
        xp = config.get('{}'.format(user), 'xp')
        await self.bot.say('You have {} xp.'.format(xp))

def setup(bot):
    bot.add_cog(Levels(bot))
