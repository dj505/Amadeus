import discord
from discord.ext import commands
import datetime
import time

class Settings:
    '''
    Bot Configuration
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))    

def setup(bot):
    bot.add_cog(Settings(bot))