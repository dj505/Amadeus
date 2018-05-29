import discord
from discord.ext import commands
import configparser
from configparser import SafeConfigParser
import os
import time
import json

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

##### The following command is no longer needed, uncomment if you plan to use it #####
#
#    async def role(self, ctx, role: discord.Role):
#    @commands.command(pass_context=True, brief='Purchase a role for 100 credits or get the free Members role')
#        assignable_roles = ['Blue','Turqoise','Green','Yellow','Orange','Pink','Purple','Grey','Black','DarkRed','DarkGreen','Magenta']
#        member = ctx.message.author
#        if str(role).lower() == 'moderator' or str(role).lower() == 'admin':
#            embed = discord.Embed(title='Role assignment failed!', description='It looks like you tried to give yourself an admin or moderator role. ' \
#                                                                               'This is not a publicly assignable role.', color=0xFF0000)
#            embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
#            await self.bot.say(embed=embed)
#        elif str(role).lower() == 'members' or str(role).lower() == 'spoilers':
#            await self.bot.add_roles(member, role)
#            embed = discord.Embed(title='Set role!', description='You have successfully been assigned the {} role!'.format(role), color=0x00FF99)
#            await self.bot.say(embed=embed)
#        elif str(role) in assignable_roles and get_balance(ctx.message.author.id) >= 100:
#            config.read('wallet.ini')
#            user = ctx.message.author.id
#            if config.has_section('{}'.format(user)):
#                balance = int(config.get('{}'.format(user), 'balance'))
#                balance = balance - 100
#                config.set('{}'.format(user), 'balance', "{}".format(balance))
#                with open('wallet.ini','w') as f:
#                    config.write(f)
#                await self.bot.add_roles(member, role)
#                embed = discord.Embed(title='Set role!', description='You have successfully been assigned the {} role for 100 credits!'.format(role), color=0x00FF99)
#                await self.bot.say(embed=embed)
#            else:
#                embed = discord.Embed(title='No Wallet', description='You do not have an existing wallet or balance! Please run the `daily` command.', color=0xFF0000)
#                await self.bot.say(embed=embed)
#
######################################################################################

    @commands.command(pass_context=True, brief='Check your wallet balance')
    async def wallet(self, ctx, user: discord.Member=None):
        if user == None:
            balance = get_balance(str(ctx.message.author.id))
            embed = discord.Embed(title='Wallet', description=None, color=0xFFD000)
            embed.add_field(name='Balance', value='Your balance is {}.'.format(balance), inline=True)
            embed.set_thumbnail(url='https://i.imgur.com/akZqYz8.png')
            await self.bot.say(embed=embed)
        else:
            balance = get_balance(str(user.id))
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
        See what's for sale!
        '''
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

    @commands.command(pass_context=True, brief='TESTING: Purchase')
    async def purchase(self, ctx, category, item):
        await self.bot.say('This command is incomplete and does not work properly yet. Do not try to buy anything.')
        id = ctx.message.author.id
        file = open('players.json')
        players = file.read()
        data = json.loads(players)
        try:
            if category.lower() == 'weapon':
                try:
                    price = get_price('weapons', item)
                    weapons = data[id]['weapons']
                    weapons.append(item)
                    data[id]['weapons'] = weapons
                    data = json.dumps(data, indent=2, separators=(',',': '))
                    with open('players.json','w') as f:
                        f.write(data)
                    subtract_balance(id, price)
                    await self.bot.say('Purchase succeeded!')
                except Exception as e:
                    await self.bot.say('Something went wrong. Is that an available item?')
                    print(e)
            elif category.lower() == 'defense':
                try:
                    price = get_price('defense', item)
                    armor = data[id]['defense']
                    armor.append(item)
                    data[id]['weapons'] = armor
                    data = json.dumps(data, indent=2, separators=(',',': '))
                    with open('players.json','w') as f:
                        f.write(data)
                    await self.bot.say('Purchase succeeded!')
                except:
                    await self.bot.say('Something went wrong. Is that an available item?')
            elif category.lower() == 'health' or category.lower() == 'healing':
                try:
                    price = get_price('healing', item)
                    items = data[id]['healing']
                    items.append(item)
                    data[id]['weapons'] = items
                    data = json.dumps(data, indent=2, separators=(',',': '))
                    with open('players.json','w') as f:
                        f.write(data)
                    await self.bot.say('Purchase succeeded!')
                except:
                    await self.bot.say('Something went wrong. Is that an available item?')
            else:
                await self.bot.say('Please enter a valid category and item.')
        except Exception as e:
            await self.bot.say('Something went wrong! Make sure you created an inventory with the `mkinv` command first.')
            print(e)

    @commands.command(pass_context=True, brief="WIP - Display inv")
    async def mkinv(self, ctx):
        file = open('players.json')
        players = file.read()
        inv = json.loads(players)
        id = str(ctx.message.author.id)
        inv[id] = {
            'health': 100,
            'weapons': [],
            'defense': [],
            'healing': [],
            'equipped_weapon': '',
            'equipped_defense': '',
        }
        invs = json.dumps(inv, indent=2, separators=(',',': '))
        with open('players.json','w') as f:
            f.write(invs)
        await self.bot.say('Inventory created!')

    @commands.command(pass_context=True, brief='WIP - Display inv')
    async def inv(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.message.author
        file = open('players.json')
        players = file.read()
        invs = json.loads(players)
        player = invs['{}'.format(ctx.message.author.id)]
        weapons = ', '.join(player['weapons'])
        defense = ', '.join(player['defense'])
        healing = ', '.join(player['healing'])
        embed = discord.Embed(title='Inventory/Info for {}'.format(user), description=None)
        embed.add_field(name='Health', value=player['health'])
        embed.add_field(name='Weapons', value=weapons)
        embed.add_field(name='Defense', value=defense)
        embed.add_field(name='Healing Items', value=healing)
        embed.add_field(name='Equipped Weapon', value=player['equipped_weapon'])
        embed.add_field(name='Equipped Armor', value=player['equipped_defense'])
        await self.bot.say(embed=embed)

def get_price(category, item):
    category = category.title()
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get(category, item)
    statlist = statlist.split(' ')
    return statlist[1]

def get_power(category, item):
    category = category.title()
    config = SafeConfigParser()
    config.read('shop.ini')
    statlist = config.get(category, item)
    statlist = statlist.split(' ')
    return statlist[0]

def subtract_balance(user, amount):
    amount = int(amount)
    config = SafeConfigParser()
    config.read('wallet.ini')
    balance = config.get(user, 'balance')
    balance = int(balance)
    balance = balance - amount
    config.set(user, 'balance', str(balance))
    with open('wallet.ini', 'w') as f:
        config.write(f)

def get_balance(userid):
    config = SafeConfigParser()
    config.read('wallet.ini')
    balance = config.get(userid, 'balance')
    return int(balance)

def setup(bot):
    bot.add_cog(Shop(bot))
