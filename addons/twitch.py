import argparse
from urllib.request import urlopen
from urllib.error import URLError
import json
import discord
from discord.ext import commands

def parse_args():
    """ parses commandline, returns args namespace object """
    desc = ('Check online status of twitch.tv user.\n'
            'Exit prints are 0: online, 1: offline, 2: not found, 3: error.')
    parser = argparse.ArgumentParser(description = desc,
             formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument('USER', nargs = 1, help = 'twitch.tv username')
    args = parser.parse_args()
    return args

def check_user(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    url = 'https://api.twitch.tv/dj505ITG/streams/' + user
    try:
        info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))
        if info['stream'] == None:
            status = 1
        else:
            status = 0
    except URLError as e:
        if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
            status = 2
        else:
            status = 3
    return status

class Twitch:
    '''
    Notifies when user it streaming on Twitch.
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    try:
        user = parse_args().USER[0]
        print(check_user(user))

def setup(bot):
    bot.add_cog(Twitch(bot))
