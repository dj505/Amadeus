import discord
from discord.ext import commands
import configparser
from configparser import SafeConfigParser

class Settings:
    '''
    Bot Configuration commands; admins only
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, brief='Changes bot description. Admins only.')
    async def setdesc(self, ctx, desc):
        '''
        Sets the bot's description, which is shown within the `help` command.
        '''
        config = SafeConfigParser()
        config.read('settings.ini')
        original_desc = config.get('main', 'desc')
        if desc == '':
            config.set('main', 'desc', '{}'.format(original_desc))
            with open('settings.ini', 'w') as f:
                config.write(f)
            embed = discord.Embed(title='Settings Not Updated', description=None, color=0x99FF00)
            embed.add_field(name='Description', value='The description you entered was blank and not changed.', inline=True)
            await self.bot.say(embed=embed)
        else:
            config.set('main', 'desc', '{}'.format(desc))
            with open('settings.ini', 'w') as f:
                config.write(f)
            embed = discord.Embed(title='Updated settings', description=None, color=0x00FF99)
            embed.add_field(name='Description', value='New description: {}'.format(desc), inline=True)
            await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Settings(bot))