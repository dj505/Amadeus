# WonderlandBot by dj505. Version 3.0.0
# "The Great Refactoring"
# Now much more easily configureable, with fewer hardcoded variables!

import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import configparser
from configparser import SafeConfigParser
import os
import traceback
import random

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

config = configparser.SafeConfigParser()
config.read('settings.ini')

if config.has_section('main'):
    pass
else:
    config.add_section('main')
    config.set('main', 'token', 'TOKEN_HERE')
    config.set('main', 'prefix', 'PREFIX_HERE')
    config.set('main', 'desc', 'DESCRIPTION_HERE')
    with open('settings.ini', 'w') as f:
        config.write(f)

token = config.get('main', 'token')
prefix = config.get('main','prefix')
desc = config.get('main', 'desc')

bot = commands.Bot(command_prefix=prefix, description=desc)

@bot.event
async def on_message(message):
    message2 = str(message.content).lower()
    if message2.startswith('git gud'):
        await bot.send_message(message.channel, 'git: \'gud\' is not a git command. See \'git --help\'')

    await bot.process_commands(message)

@bot.event
async def on_ready():
        print("{} is running!".format(bot.user.name))

@bot.event
async def on_member_join(member):
    greetings = ['Hello there! You are a bold one, ','Hey there, welcome to the server ','Oh hi there! Welcome, ','Hey! welcome, ','Welcome to the server, ','Yo, welcome to the server, ']
    greeting = random.choice(greetings)
    await bot.send_message(bot.get_channel('429756378542768129'), '{}'.format(greeting) + '{0.mention}!'.format(member) + '\n\nIf you are unable to post in any other channels, ' \
                                                                  'please post a message here in #newcomers and we\'ll get you sorted.\nBut first, **please read through' \
                                                                  ' the rules!**')

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CommandNotFound):
        embed = discord.Embed(title='Error!', description='I cannot find that command!', color=0xFF0000)
        embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        await bot.send_message(ctx.message.channel, embed=embed)

    if isinstance(error, commands.errors.CheckFailure):
        embed = discord.Embed(title='Permissions error!', description='You do not have permission to use this command.', color=0xFF0000)
        embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        await bot.send_message(ctx.message.channel, embed=embed)

    elif isinstance(error, commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        # await bot.send_message(ctx.message.channel, "{} You are missing required arguments.\n{}".format(ctx.message.author.mention, formatter.format_help_for(ctx, ctx.command)[0]))
        embed = discord.Embed(title='Error!', description='You are missing required arguments.', color=0xFF0000)
        embed.add_field(name='Usage', value='{}'.format(ctx.message.author.mention, formatter.format_help_for(ctx, ctx.command)[0]))
        embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        await bot.send_message(ctx.message.channel, embed=embed)

    elif isinstance(error, commands.errors.CommandOnCooldown):
        try:
            await bot.delete_message(ctx.message)
        except discord.errors.NotFound:
            pass
        message = await bot.send_message(ctx.message.channel, "{} This command was used {:.2f}s ago and is on cooldown. Try again in {:.2f}s.".format(ctx.message.author.mention, error.cooldown.per - error.retry_after, error.retry_after))
        await asyncio.sleep(10)
        await bot.delete_message(message)

    else:
        # embed = discord.Embed(title='Error!', description='An error occured processing that command.', color=0xFF0000)
        # embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        print('Ignoring exception in command {0.command} in {0.message.channel}'.format(ctx))
        tb = traceback.format_exception(type(error), error, error.__traceback__)
        print(''.join(tb))
        # await bot.send_message(ctx.message.channel, embed=embed)

addons = [
    'addons.testing',
    'addons.load',
    'addons.utils',
    'addons.xkcdparse',
    'addons.doom',
    'addons.modutils',
    'addons.fun'
]

failed_addons = []

for extension in addons:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_addons.append([extension, type(e).__name__, e])

bot.run(token)
