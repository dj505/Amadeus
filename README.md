# MakiseKurisu
Another version of my Discord bot, with extra features, meant for the server [Future Studio](https://discord.gg/HbmunrE)!

## What can it do?
A lot! There's a variety of moderator commands such as:

- `addgif`: adds a reaction gif to be used with the `gif` or `react` command
- `kick`: kicks a user from the server
- `ban`: bans a user from the server
- `givecredit`: adds a specified balance to a specified user's wallet
- `prune`: deletes previous bot messages, all if no amount specified

Here are some standard user commands;

- `ping`: checks the bot's response time
- `userinfo`: brings up an information card on the specified user
- `daily`: adds 150 to the user's wallet, can be used once per day
- `avatar`: gets the avatar of a specified user
- `react`: posts a reaction gif set with the `addgif` command
- `say`: a fun command to make the bot say things
- `serverinfo`: lists some server information
- `reactions`: lists available reactions to be used with the `react` command
- `source`: links to this GitHub page
- `xkcd`: grabs a specified, random, or keyword-based xkcd

## How do I set it up?
You'll need to make a few configuration files. Since I'm lazy and configparser is a thing, they're all `.ini` files. here's what they should look like.

settings.ini
```
[main]
token = your bot token here
prefix = k! (or hyour prefix)
desc = MakiseKurisu, a Future Studio server utility bot by dj505! (or your description)
```

reactions.ini (this one may not be necessary)
```
[gifs]
```
(Note: this might not be necessary unless the command throws an error when attempting to add a gif and the `[gif]` section does not exist.)

Once those are made, make sure you have the following **prerequisites**:
- Python3
- Discord.py
- xkcd
- bs4
- requests
- any others it may prompt for (these are all from memory)

Then simply run `run.py`!
