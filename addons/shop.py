import discord
from discord.ext import commands
import configparser
from configparser import SafeConfigParser
import os

if not os.path.isfile('./shop.ini'):
    print('Creating shop.ini...')
    with open('shop.ini','w+') as f:
        f.write('[Weapons]\nStarter Sword = [10, 100]\n')
        f.write('[Defense]\nStarter Armor = [10, 100]\n')
else:
    print('shop.ini exists, no need to create')

class Shop:
    '''
    WIP shop.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True, brief='Purchase a role for 100 credits or get the free Members role')
    async def role(self, ctx, role: discord.Role):
        assignable_roles = ['Blue','Turqoise','Green','Yellow','Orange','Pink','Purple','Grey','Black','DarkRed','DarkGreen','Magenta']
        member = ctx.message.author
        if str(role).lower() == 'moderator' or str(role).lower() == 'admin':
            embed = discord.Embed(title='Role assignment failed!', description='It looks like you tried to give yourself an admin or moderator role. ' \
                                                                               'This is not a publicly assignable role.', color=0xFF0000)
            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
            await self.bot.say(embed=embed)
        elif str(role).lower() == 'members' or str(role).lower() == 'spoilers':
            await self.bot.add_roles(member, role)
            embed = discord.Embed(title='Set role!', description='You have successfully been assigned the {} role!'.format(role), color=0x00FF99)
            await self.bot.say(embed=embed)
        elif str(role) in assignable_roles and get_balance(ctx.message.author.id) >= 100:
            config = SafeConfigParser()
            config.read('wallet.ini')
            user = ctx.message.author.id
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
        '''
        Prints out a list of roles that you can assign yourself.
        '''
        roles = ctx.message.server.roles
        assignable_roles = open('assignable_roles.txt', 'r')
        bot_message='```'
        for roles in assignable_roles:
            bot_message += '{}\n'.format(roles)
        bot_message += '```'
        embed = discord.Embed(title='Roles', description=bot_message, color=0x00FF99)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='The main shop.', aliases=['buy','store'])
    async def shop(self, ctx):
        '''
        This is where you buy most of the things.
        '''
        embed = discord.Embed(title='Work In Progress', description='This command is still a heavy WIP. Do not use it seriously yet.', color=0x00FF99)
        await self.bot.say(embed=embed)
        config = SafeConfigParser()
        config.read('shop.ini')
        weaponlist = {k:v for k,v in config.items('Weapons')}
        armorlist = {k:v for k,v in config.items('Defense')}
        heallist = {k:v for k,v in config.items('Healing')}
        weapons = []
        armors = []
        heal = []
        bot_message='```\nWeapons:\n'
        for x in weaponlist:
            weapons.append(str(x))
        for elem in weapons:
            bot_message += '    {}\n'.format(elem.title())
            bot_message += '      {} Damage\n'.format(get_weapon_power(elem))
            bot_message += '      {} Credits\n'.format(get_weapon_price(elem))
        bot_message += 'Defense:\n'
        for x in armorlist:
            armors.append(str(x))
        for elem in armors:
            bot_message += '    {}\n'.format(elem.title())
            bot_message += '      {} Damage\n'.format(get_armor_power(elem))
            bot_message += '      {} Credits\n'.format(get_armor_price(elem))
        bot_message += 'Healing:\n'
        for x in heallist:
            heal.append(str(x))
        for elem in heal:
            bot_message += '    {}\n'.format(elem.title())
            bot_message += '      Restores {} HP\n'.format(get_heal_power(elem))
            bot_message += '      {} Credits\n'.format(get_heal_price(elem))
        bot_message += '```'
        embed = discord.Embed(title='Shop List', description=bot_message, color=0x00FF99)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, brief='Purcahse armor')
    async def buyweapon(self, ctx, item):
        price = get_weapon_price(item)
        await self.bot.say('This item costs {} credits.'.format(price))

def get_weapon_price(item):
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get('Weapons', item)
    statlist = statlist.split(' ')
    return statlist[1]

def get_armor_price(item):
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get('Defense', item)
    statlist = statlist.split(' ')
    return statlist[1]

def get_heal_price(item):
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get('Healing', item)
    statlist = statlist.split(' ')
    return statlist[1]

def get_weapon_power(item):
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get('Weapons', item)
    statlist = statlist.split(' ')
    return statlist[0]

def get_armor_power(item):
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get('Defense', item)
    statlist = statlist.split(' ')
    return statlist[0]

def get_heal_power(item):
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get('Healing', item)
    statlist = statlist.split(' ')
    return statlist[0]

def get_balance(userid):
    config = SafeConfigParser()
    config.read('wallet.ini')
    balance = config.get(userid, 'balance')
    return int(balance)

def setup(bot):
    bot.add_cog(Shop(bot))
