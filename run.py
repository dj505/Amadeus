# Amadeus by dj505. Version 3.0.0
# "The Great Refactoring"
# Now much more easily configureable, with fewer hardcoded variables!

# Import all of the required modules/libraries that the script requires.
import discord # The Discord API wrapper for Python.
from discord.ext import commands # The cool command framework.
from discord.ext.commands import bot
import asyncio
import configparser
from configparser import SafeConfigParser
import os
import traceback
import random

# Change the directory to the bot's home directory to be able to access things.
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Read the settings configuration file
config = configparser.SafeConfigParser()
config.read('settings.ini')

# Check if the file has the [main] section, which stores the values.
# If not, create it.
if config.has_section('main'):
    pass
else:
    config.add_section('main')
    config.set('main', 'token', 'TOKEN_HERE')
    config.set('main', 'prefix', 'PREFIX_HERE')
    config.set('main', 'desc', 'DESCRIPTION_HERE')
    with open('settings.ini', 'w') as f:
        config.write(f)

token = config.get('main', 'token') # Set the bot token from the config
prefix = config.get('main','prefix') # Set the bot prefix from the config
desc = config.get('main', 'desc') # Set the bot description from the config

bot = commands.Bot(command_prefix=prefix, description=desc)

# This runs every time a message is sent. This one specifically checks to see
# if the message starts with "git gud" and sends a witty response.
@bot.event
async def on_message(message):
    message2 = str(message.content).lower()
    if message2.startswith('git gud'):
        await bot.send_message(message.channel, 'git: \'gud\' is not a git command. See \'git --help\'')

    await bot.process_commands(message) # Without this line, commands would no longer work as it just looks at message content instead.

# When the bot is ready, print "{bot name} is running!" to the command line.
@bot.event
async def on_ready():
    print("Creating server config directories if they don't exist...")
    for server in bot.servers:
        bot.server = server
        if not os.path.exists('./{}'.format(bot.server.id)):
            os.makedirs('./{}'.format(bot.server.id))
            with open('{}\\reactions.ini'.format(bot.server.id),'w+') as f:
                f.write('[gifs]\n')
            print("Directory {} created with default configs.".format(bot.server.id))
        else:
            print("No new directories to create!")
    print("{} is running!".format(bot.user.name))

# When a member joins, send a random greeting from the "greetings" array.
@bot.event
async def on_member_join(member):
    greetings = ['Hello there! You are a bold one, {0.mention}!'.format(member),
                 'Hey there, {0.mention}! Welcome to Future Studio!'.format(member),
                 'Oh hi {0.mention}! Welcome to Future Studio!'.format(member),
                 'Hey! Welcome, {0.mention}!'.format(member),
                 'Welcome to the server, {0.mention}'.format(member),
                 'Yo, welcome to Future Studio, {0.mention}!'.format(member),
                 'Thanks for popping in, {0.mention}! Welcome to Future Studio!'.format(member)]
    greeting = random.choice(greetings)
    welcome_message = '\n\nPlease feel free to introduce yourself! If none of the admins are around to assign the member role, ' \
                      'use the command `k!role Members` (case sensitive) in #bot-commands and it\'ll be automatically assigned.' \
                      ' If you\'d like a cool coloured role, use `k!daily` to get your daily 150 credits, and use `k!role colour' \
                      '` to give yourself the role. Keep in mind this costs 100 credits! With that out of the way, remember to ' \
                      'read the #rules! Enjoy your stay!'
    await bot.send_message(bot.get_channel('429756378542768129'), '{}'.format(greeting) + '{}'.format(welcome_message))

# When someone leaves (;-;) send a random goodbye.
@bot.event
async def on_member_remove(member):
    goodbyes = ['Goodbye, ','See ya, ','Bye, ','Sorry to see you go, ']
    bye = random.choice(goodbyes)
    await bot.send_message(bot.get_channel('429756378542768129'), '{}'.format(bye) + '{}!'.format(member))

# The currently very broken error handler. It only half works. Don't bother sacrificing your sanity to fix it.
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.errors.CommandNotFound):
        embed = discord.Embed(title='Error!', description='I cannot find that command!', color=0xFF0000)
        embed.set_thumbnail(url='https://i.imgur.com/z2xfrsH.png')
        await bot.send_message(ctx.message.channel, embed=embed)

    elif isinstance(error, commands.errors.CheckFailure):
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

# Queue the various addons in the "addons" folder to be loaded.
addons = [
    'addons.testing',
    'addons.load',
    'addons.utils',
    'addons.xkcdparse',
    'addons.modutils',
    'addons.fun',
    'addons.shop',
    'addons.settings',
    'addons.animelist'
]

failed_addons = []

# Actually attempt to load the addons.
for extension in addons:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
        failed_addons.append([extension, type(e).__name__, e])

# Start the bot.
bot.run(token)
