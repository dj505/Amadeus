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
        member = ctx.message.author
        if str(role).lower() == 'admins' or str(role).lower() == 'moderators':
            embed = discord.Embed(title='Role assignment failed!', description='It looks like you tried to give yourself an admin or moderator role. ' \
                                                                               'This is not a publicly assignable role.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)
        elif str(role).lower() == 'members':
            await self.bot.add_roles(member, role)
            embed = discord.Embed(title='Set role!', description='You have successfully been assigned the {} role!'.format(role), color=0x00FF99)
            await self.bot.say(embed=embed)
        elif str(role).lower() != 'members' and get_balance('{}'.format(member.id)) > 100:
            user = ctx.message.author.id
            config = SafeConfigParser()
            config.read('wallet.ini')
            if config.has_section('{}'.format(user)):
                balance = int(config.get('{}'.format(user), 'balance'))
                balance = balance - 100
                config.set('{}'.format(user), 'balance', "{}".format(balance))
                with open('wallet.ini','w') as f:
                    config.write(f)
                await self.bot.add_roles(member, role)
                embed = discord.Embed(title='Set role!', description='You have successfully been assigned the {} role for 100 credits!'.format(role), color=0x00FF99)
                await self.bot.say(embed=embed)
            else:
                embed = discord.Embed(title='No Wallet', description='You do not have an existing wallet or balance! Please run the `daily` command.', color=0xFF0000)
                await self.bot.say(embed=embed)
        else:
            await self.bot.say('You cannot afford this role.')

    @commands.command(pass_context=True, brief='Check your wallet balance')
    async def wallet(self, ctx):
        member = ctx.message.author.id
        config = SafeConfigParser()
        config.read('wallet.ini')
        balance = config.get(member, 'balance')
        embed = discord.Embed(title='Wallet', description=None, color=0xFFD000)
        embed.add_field(name='Balance', value='Your balance is {}.'.format(balance), inline=True)
        embed.set_thumbnail(url='https://i.imgur.com/akZqYz8.png')
        await self.bot.say(embed=embed)

def get_balance(userid):
    config = SafeConfigParser()
    config.read('wallet.ini')
    balance = config.get(userid, 'balance')
    return int(balance)

    
def setup(bot):
    bot.add_cog(Shop(bot))
