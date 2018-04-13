import discord
from discord.ext import commands
from configparser import SafeConfigParser
import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from configparser import SafeConfigParser
import requests
from io import BytesIO
import time
import os

class Utils:
    '''
    User utilities. Anyone can use.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context="True",brief="Gets user information.")
    async def userinfo(self, ctx, user: discord.Member):
        """
        Allows you to get information on a user simply by tagging them.
        """
        member = user.id
        config = SafeConfigParser()
        config.read('wallet.ini')
        if(config.has_section(member)):
            balance = config.get(member, 'balance')
        else:
            balance = 'None'
        img = Image.open("infocard-original.png")
        avatar = requests.get(user.avatar_url)
        avatar = Image.open(BytesIO(avatar.content))
        basewidth = 90
        wpercent = (basewidth / float(avatar.size[0]))
        hsize = int((float(avatar.size[1]) * float(wpercent)))
        avatar = avatar.resize((basewidth, hsize), Image.ANTIALIAS)
        avatar.save('{}-avatar-ico.png'.format(user.name))
        avatar = Image.open('{}-avatar-ico.png'.format(user.name))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Archivo-Bold.ttf", 45)
        img.paste(avatar, (29, 29))
        draw.text((135, 60),'{}'.format(user.name),(255,255,255),font=font)
        font = ImageFont.truetype("Archivo-Bold.ttf", 30)
        draw.text((194, 132),'{}'.format(user.id),(255,255,255),font=font)
        draw.text((194, 164),'{}'.format(user.status),(255,255,255),font=font)
        draw.text((194, 196),'{}'.format(user.top_role),(255,255,255),font=font)
        draw.text((194, 228),'{}'.format(str(user.joined_at)[:10]),(255,255,255),font=font)
        draw.text((194, 260),'{}'.format(balance),(255,255,255),font=font)
        img.save('infocard-{}.png'.format(user.name))
        await self.bot.send_file(ctx.message.channel, 'infocard-{}.png'.format(user.name))
        time.sleep(10)
        os.remove('infocard-{}.png'.format(user.name))

    @commands.command(pass_context="True",brief="Adds 150 to your currency count. Can be used once every 24 hours.", aliases=['money','coin'])
    @commands.cooldown(1, 86400.0, commands.BucketType.user)
    async def daily(self, ctx):
        """
        This command adds 150 credits to your wallet. Can only be used once per day. This command is still a WIP.
        """
        config = SafeConfigParser()
        currenttime = datetime.datetime.now()
        user = ctx.message.author.id
        config.read('wallet.ini')
        if config.has_section('{}'.format(user)):
            balance = int(config.get('{}'.format(user), 'balance'))
            balance = balance + 150
            balance = str(balance)
            config.set('{}'.format(user), 'balance', "{}".format(balance))
            config.set('{}'.format(user), 'lastused', '{}'.format(currenttime))
            with open('wallet.ini', 'w') as f:
                config.write(f)

            embed = discord.Embed(title='Added Balance', description='Your balance has been updated successfully!', color=0xFFD000)
            embed.add_field(name='Balance', value='Your balance is now {}.'.format(balance), inline=True)

        else:
            config.add_section('{}'.format(user))
            config.set('{}'.format(user), 'lastused', '{}'.format(currenttime))
            config.set('{}'.format(user), 'balance', '150')
            with open('wallet.ini', 'w') as f:
                config.write(f)

            embed = discord.Embed(title='Created Wallet', description='Your wallet has been created successfully!', color=0xFFD000)
            embed.add_field(name='Balance', value='Your balance is now 150.', inline=True)
        embed.set_thumbnail(url='https://i.imgur.com/akZqYz8.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True,brief="Posts a reaction gif",aliases=["reaction","reactiongif","gif","jif"])
    async def react(self, ctx, arg):
        """
        Posts a reaction image or copypasta from a keyword specified.
        """
        config = SafeConfigParser()
        config.read('reactions.ini')
        if config.has_option('gifs','{}'.format(arg)):
            gif = config.get('gifs','{}'.format(arg))
            if gif.startswith('http'):
                embed = discord.Embed(title=None, description=None, color=0x00FF99)
                embed.set_image(url=gif)
            else:
                embed = discord.Embed(title=None, description=None, color=0x00FF99)
                embed.add_field(name=gif, value='Requested by {}'.format(ctx.message.author), inline=True)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(title='I could not find that reaction!', description='Please enter a valid reaction or try again.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='Lists reactions',aliases=['gifs','reactiongifs'])
    async def reactions(self):
        config = SafeConfigParser()
        config.read('reactions.ini')
        reactionlist = {k:v for k,v in config.items('gifs')}
        reactions = []
        bot_message='```'
        for x in reactionlist:
            reactions.append(str(x))
        for elem in reactions:
            bot_message += '{}\n'.format(elem)
        bot_message += '```'
        embed = discord.Embed(title='Gifs', description=bot_message, color=0x00FF99)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='Displays server information')
    async def serverinfo(self, ctx):
        embed = discord.Embed(name='Server Information Panel', description='Here you go!', color=0x00FF99)
        embed.set_author(name='{}'.format(ctx.message.author.name) + '\'s Info Request')
        embed.add_field(name='Name', value=ctx.message.server.name, inline=True)
        embed.add_field(name='ID', value=ctx.message.server.id, inline=True)
        embed.add_field(name='Roles', value=len(ctx.message.server.roles), inline=True)
        embed.add_field(name='Members', value=len(ctx.message.server.members), inline=True)
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='A Link to the Source')
    async def source(self, ctx):
        embed = discord.Embed(title='Bot Source Code', description='Have some spaghetti code!', color=0x00FF99)
        embed.set_thumbnail(url='https://opensource.org/files/osi_keyhole_600X600_90ppi.png')
        embed.add_field(name='GitHub Repository', value='https://github.com/dj505/MakiseKurisu', inline=True)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='Says something')
    async def say(self, ctx, *string):
        if '@' in str(ctx.message.content):
            embed = discord.Embed(title='Say command failed!', description='Please do not attempt to tag users with this command. \
                                                                            This results in either double tagging, or sending an `@everyone` tag \
                                                                            without permissions by using the bot as a loophole.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)

        else:
            await self.bot.say(message_string_parser(ctx.message.content))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, brief='Get user avatar')
    async def avatar(self, ctx, user: discord.Member):
        embed = discord.Embed(name='Avatar', description=None, color=0x000000)
        embed.set_image(url=user.avatar_url)
        await self.bot.say(embed=embed)

def message_string_parser(message):
    return(message[message.find(' ')+1:])

def setup(bot):
    bot.add_cog(Utils(bot))
