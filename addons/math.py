import discord
from discord.ext import commands

class Math:
    '''
    Just some math stuff.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def add(self, ctx):
        '''
        Add some numbers together
        '''
        message = message_string_parser(ctx.message.content)
        numbers = message.split(' ')
        sum = 0
        for num in numbers:
            num = int(num)
            sum += num
        await self.bot.say(str(sum))

def setup(bot):
    bot.add_cog(Math(bot))

def message_string_parser(message):
    return(message[message.find(' ')+1:])
