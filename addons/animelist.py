import discord
from discord.ext import commands
from configparser import SafeConfigParser
import datetime
import os

if not os.path.isfile('./anime.ini'):
    print('Creating anime.ini...')
    with open('anime.ini','w+') as f:
        f.write('[anime]\n')
else:
    print('anime.ini exists, no need to create')

class AnimeList:
    '''
    Community curated anime suggestion list
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context="True",brief="Displays a list of suggested anime",aliases=['anime'])
    async def animelist(self, ctx):
        config = SafeConfigParser()
        config.read('anime.ini')
        animelist = {k:v for k,v in config.items('anime')}
        anime = []
        bot_message='```'
        for x in animelist:
            anime.append(str(x))
        for elem in anime:
            bot_message += '{}\n'.format(elem)
        bot_message += '```'
        embed = discord.Embed(title='Anime', description=bot_message, color=0x00FF99)
        await self.bot.say(embed=embed)

    @commands.command(pass_context="True",brief="Gets information on a given anime in the list")
    async def animedesc(self, ctx, *anime):
        config = SafeConfigParser()
        config.read('anime.ini')
        if config.has_option('anime','{}'.format(anime)):
            desc = config.get('anime','{}'.format(anime))
            embed = discord.Embed(title=anime, description=desc, color=0x00FF99)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(title='I could not find that anime in the list!', description='Please enter a valid anime or try again.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)

    @commands.command(pass_context="true",brief="Adds an anime to the list",aliases=['addanime'])
    async def animeadd(self, ctx, *anime):
        """
        Adds an anime to the list.
        """
        anime = anime.lower()
        config = SafeConfigParser()
        config.read('anime.ini')
        if config.has_option('anime', anime):
            await self.bot.say('This anime is already in the list!')
        else:
            config.set('anime', '{}'.format(anime), 'No descripton set. Use `animedescset "{}" "description"` to set a description.'.format(anime))
            with open('anime.ini', 'w') as f:
                config.write(f)
            embed = discord.Embed(title='Added anime!', description='Your suggestion has been successfully recorded. Remember to add a description!', color=0x00FF99)
            await self.bot.say(embed=embed)

    @commands.command(pass_context="true",brief="Adds an anime to the list")
    async def animedescset(self, ctx, anime, desc):
        """
        Adds a description to an anime.
        """
        anime = anime.lower()
        config = SafeConfigParser()
        config.read('anime.ini')
        config.set('anime', anime, desc)
        with open('anime.ini', 'w') as f:
            config.write(f)
        embed = discord.Embed(title='Added anime description!', description='Your description has been successfully set.', color=0x00FF99)
        await self.bot.say(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, brief='Removes an anime entry from the list (admin only)')
    async def animedelete(self, ctx, anime):
        '''
        Removes a reaction gif or entry from the list.
        '''
        config = SafeConfigParser()
        config.read('anime.ini')
        if config.has_option('anime','{}'.format(anime)):
            config.remove_option('anime','{}'.format(anime))
            with open('anime.ini','w') as f:
                config.write(f)
            embed = discord.Embed(title='Removed anime!', description='The specified listing has been successfully removed.', color=0x00FF99)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(title='I could not find that anime in the list!', description='Please enter a valid anime or try again.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(AnimeList(bot))
