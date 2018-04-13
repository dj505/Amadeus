import discord
from discord.ext import commands
import configparser
from configparser import SafeConfigParser

class Shop:
    '''
    Making sure things actually work using one handy module
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True, brief='Purchase a role for 100 credits, or assign yorself the free Members role')
    async def role(self, ctx, role: discord.Role):
        if str(role).lower() == 'moderator' or 'admin':
            embed = discord.Embed(title='Role assignment failed!', description='It looks like you tried to give yourself an admin or moderator role. ' \
                                                                               'This is not a publicly assignable role.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)
        elif str(role).lower() == 'members':
            await self.bot.add_roles(member, role)
            embed = discord.Embed(title='Set role!', description='You have successfully been assigned the {} role!'.format(role), color=0x00FF99)
            await self.bot.say(embed=embed)
#        elif str(role).lower()

    @commands.command(pass_context=True, brief='Check your wallet balance')
    async def wallet(self, ctx):
        member = ctx.message.author.id
        balance = get_balance(str(ctx.message.author.id))
        embed = discord.Embed(title='Wallet', description=None, color=0xFFD000)
        embed.add_field(name='Balance', value='Your balance is {}.'.format(balance), inline=True)
        embed.set_thumbnail(url='https://i.imgur.com/akZqYz8.png')
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='List assignable roles.')
    async def listroles(self, ctx):
        roles = get_roles(ctx.message.server.roles)
        assignable_roles = open('assignable_roles.txt', 'r')
        bot_message='```'
        for assignable_roles in roles:
            bot_message += '{}\n'.format(assignable_roles)
        bot_message += '```'
        embed = discord.Embed(title='Roles', description=bot_message, color=0x00FF99)
        await self.bot.say(embed=embed)

def get_balance(userid):
    config = SafeConfigParser()
    config.read('wallet.ini')
    balance = config.get(userid, 'balance')
    return int(balance)

def get_roles(server):
    x = server.roles
    roles = []
    for role in x:
        roles.append(str(role))
    return roles

def setup(bot):
    bot.add_cog(Shop(bot))
