import discord
from discord.ext import commands
import configparser
from configparser import SafeConfigParser
import os
import time

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
        You can but healing items, armor, and weapons here.
        '''
        embed = discord.Embed(title='Work In Progress', description='This command is still a heavy WIP. Do not use it seriously yet. There\'s no way to buy anything.', color=0x00FF99)
        await self.bot.say(embed=embed)
        config = SafeConfigParser()
        config.read('shop.ini')
        weaponlist = {k:v for k,v in config.items('Weapons')}
        armorlist = {k:v for k,v in config.items('Defense')}
        heallist = {k:v for k,v in config.items('Healing')}
        weapons = []
        armors = []
        heal = []
        bot_message = 'Welcome to {}\'s shop!'.format(self.bot.server.name)
        bot_message += '```\n-Weapons-\n'
        for x in weaponlist:
            weapons.append(str(x))
        for elem in weapons:
            bot_message += '  {}\n'.format(elem.title())
            bot_message += '    {} Damage\n'.format(get_power('Weapons', elem))
            bot_message += '    {} Credits\n'.format(get_price('Weapons', elem))
        bot_message += '\n-Defense-\n'
        for x in armorlist:
            armors.append(str(x))
        for elem in armors:
            bot_message += '  {}\n'.format(elem.title())
            bot_message += '    {} Defense\n'.format(get_power('Defense', elem))
            bot_message += '    {} Credits\n'.format(get_price('Defense', elem))
        bot_message += '\n-Healing-\n'
        for x in heallist:
            heal.append(str(x))
        for elem in heal:
            bot_message += '  {}\n'.format(elem.title())
            bot_message += '    Restores {} HP\n'.format(get_power('Healing', elem))
            bot_message += '    {} Credits\n'.format(get_price('Healing', elem))
        bot_message += '```'
        embed = discord.Embed(title='The Shop', description=bot_message, color=0x00FF99)
        await self.bot.say(embed=embed)

    # Fair warning. The following code is an absolute mess. I have no idea what I'm doing.
    # configparser is definitely not the best for this. Idk how to use the json module tho.
    # I apologize in advance. You have been warned. Carry on.
    # Dear future me: fix this dammit
    @commands.command(pass_context=True, brief='Purchase a thing')
    async def purchase(self, ctx, category, item):
        await self.bot.say('This command is incomplete. Do not purchase anything yet.')
        config = SafeConfigParser()
        if not os.path.isfile('./{}_inv.ini'.format(str(ctx.message.author.id))):
            message = await self.bot.say('Creating inventory...')
            with open('./{}_inv.ini'.format(str(ctx.message.author.id)),'w+') as f:
                f.write('[Weapons]\ninv = \nequipped = \n')
                f.write('[Defense]\ninv = \nequipped = \n')
                f.write('[Healing]\ninv = \n')
            time.sleep(0.5)
            message = await self.bot.edit_message(message, 'Inventory created! Please run the command again.')
        else:
            price = get_price(category, item)
            price = int(price)
            user = ctx.message.author.id
            config.read('wallet.ini')
            if config.has_section('{}'.format(user)):
                balance = int(config.get('{}'.format(user), 'balance'))
                if balance >= price:
                    balance = balance - price
                    config.set('{}'.format(user), 'balance', "{}".format(balance))
                    with open('wallet.ini','w') as f:
                        config.write(f)
                    confirmation = await self.bot.say('Balance subtracted...')
                    handle_purchase(ctx.message.author.id, item)
                    confirmation.edit('Purchased!')
                else:
                    await self.bot.say('You can\'t afford this!')
            else:
                await self.bot.say('You don\'t have a wallet!')

def get_price(category, item):
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get(category, item)
    statlist = statlist.split(' ')
    return statlist[1]

def get_power(category, item):
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get(category, item)
    statlist = statlist.split(' ')
    return statlist[0]

def get_balance(userid):
    config = SafeConfigParser()
    config.read('wallet.ini')
    balance = config.get(userid, 'balance')
    return int(balance)

def handle_purchase(id, item):
    config = SafeConfigParser()
    config.read('{}_inv.ini'.format(id))

def setup(bot):
    bot.add_cog(Shop(bot))
