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
    async def userinfo(self, ctx, user: discord.Member=None):
        # I will try and explain this monstrosity of spaghetti
        # Probably many better ways to do this but I'm lazy and it works well enough
        """
        Allows you to get information on a user simply by tagging them.
        """
        if user == None:
            user = ctx.message.author
        else:
            user = user
        member = user.id
        config = SafeConfigParser()
        config.read('wallet.ini')
        if(config.has_section(member)):
            balance = config.get(member, 'balance')
        else:
            balance = 'No Wallet'
        img = Image.open("infocard-original.png") # Open original infocard image
        avatar = requests.get(user.avatar_url) # Get the contents of the user avatar URL
        avatar = Image.open(BytesIO(avatar.content)) # Open the avatar URL contents as an image with BytesIO
        basewidth = 90 # Set the image base width to be used with the following math things
        wpercent = (basewidth / float(avatar.size[0])) # Quick maths
        hsize = int((float(avatar.size[1]) * float(wpercent)))
        avatar = avatar.resize((basewidth, hsize), Image.ANTIALIAS)
        avatar.save('{}-avatar-ico.png'.format(user.name)) # Save the avatar as a 90x90px PNG file
        avatar = Image.open('{}-avatar-ico.png'.format(user.name)) # Open the image again
        font = ImageFont.truetype("Archivo-Bold.ttf", 45) # Set the font
        draw = ImageDraw.Draw(img) # Initialize drawing things over top of the blank info card
        img.paste(avatar, (29, 29)) # Paste the avatar icon in the right poisition
        draw.text((135, 60),'{}'.format(user.name),(255,255,255),font=font) # Draw the username text
        font = ImageFont.truetype("Archivo-Bold.ttf", 30) # Set a smaller font for the following text
        draw.text((194, 132),'{}'.format(user.id),(255,255,255),font=font) # Draw the user ID
        draw.text((194, 164),'{}'.format(user.status),(255,255,255),font=font) # Draw the user status
        draw.text((194, 196),'{}'.format(user.top_role),(255,255,255),font=font) # Draw the user's top role
        draw.text((194, 228),'{}'.format(str(user.joined_at)[:10]),(255,255,255),font=font) # Draw the user join date
        draw.text((194, 260),'{}'.format(balance),(255,255,255),font=font) # Draw the user's current waller balance if applicable
        img.save('infocard-{}.png'.format(user.name)) # Save the info card as a PNG separate from the original
        await self.bot.send_file(ctx.message.channel, 'infocard-{}.png'.format(user.name)) # Send the new PNG
        time.sleep(10) # Wait 10 seconds
        os.remove('infocard-{}.png'.format(user.name)) # Delete the user info card
        os.remove('{}-avatar-ico.png'.format(user.name)) # Delete the user avatar icon
        # If you have an actual sane way of doing this feel free to create a merger request or something
        # Nobody should have to rely on this spaghetti

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

    @commands.command(pass_context=True, brief='A Link to the Source', aliases=['sauce'])
    async def source(self, ctx):
        embed = discord.Embed(title='Bot Source Code', description='Have some spaghetti!', color=0x00FF99)
        embed.set_thumbnail(url='https://opensource.org/files/osi_keyhole_600X600_90ppi.png')
        embed.add_field(name='GitHub Repository', value='https://github.com/dj505/Amadeus', inline=True)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='Says something')
    async def say(self, ctx, *string):
        if '@' in str(ctx.message.content): # literally just check if the message contains an @ anywhere because I'm lazy
            embed = discord.Embed(title='Say command failed!', description='Please do not attempt to tag users with this command. \
                                                                            This results in either double tagging, or sending an `@everyone` tag \
                                                                            without permissions by using the bot as a loophole.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)
        else:
            await self.bot.say(message_string_parser(ctx.message.content))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, brief='Get user avatar')
    async def avatar(self, ctx, user: discord.Member=None):
        if user != None:
            embed = discord.Embed(name='Avatar', description=None, color=0x000000)
            embed.set_image(url=user.avatar_url)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(name='Avatar', description=None, color=0x000000)
            embed.set_image(url=ctx.message.author.avatar_url)
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='Leaderboard!')
    async def leaderboard(self, ctx):
        await self.bot.say("This is still a WIP.")

def message_string_parser(message):
    return(message[message.find(' ')+1:])
    # chucknorify17's biggest contribution to this repo
    # Literally just gets the contents of the message after the prefix/command
    # by finding the first space and returning everything after it
    # I think the only thing that uses it is the say command
    # Yet it's stilly surprisingly useful

def setup(bot):
    bot.add_cog(Utils(bot))
