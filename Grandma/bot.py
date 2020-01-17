import discord
from discord.ext import commands
import random
import getWebsite
import sys
import getUrls
import userClasses
import datetime
from datetime import datetime, timedelta
import asyncio

lastChannelId = ""
bot = commands.Bot(command_prefix='.')

grandsons = {

}

async def background_checkReminders(self):
        await self.wait_until_ready()
        rem = ""
        global lastChannelId
        while not self.is_closed():
            time = '{:%Y:%m:%d %H:%M:%S}'.format(datetime.now())
            for users in grandsons:
                if grandsons[users].time == time:
                    rem = grandsons[users].reminder
                    if(len(rem) > 0):
                        channel = self.get_channel(grandsons[users].reminderChannel)
                        await channel.send("Reminder for user {}, {}".format(grandsons[users].name,rem))
                        rem = ""
            await asyncio.sleep(1)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name=".help for commands"))

@bot.event
async def on_message(message):
    global lastChannelId
    if message.author == bot.user:
        return
    lastChannelId = message.channel.id
    await bot.process_commands(message)

@bot.command()
async def urban(ctx, arg1):
    """Returns Urbandictionary definition"""
    try:
        embed = getWebsite.getUrban(('https://www.urbandictionary.com/define.php?term={}').format(arg1))
        await ctx.send(embed=embed)
    except:
        await ctx.send(await ctx.send("Not enough love from my grandchildren to perform request :frowning:"))

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def reminder(ctx, arg1, arg2):
    """Sets a reminder for a given amount of time"""
    try:
        arg2 = int(arg2)
    except:
        await ctx.send("Invalid value for time")
    else:
        if isinstance(arg2, int):
            embed = discord.Embed()
            embed.title = "Reminder set"
            embed.add_field(name="Reminder", value=arg1)
            embed.add_field(name="Set for", value=("{} minutes").format(arg2))
            embed.set_footer(text=("Requested by "+ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
            grandsons[ctx.message.author.id] = userClasses.Grandson(ctx.message.author.name, ctx.message.author.id)
            time = '{:%Y:%m:%d %H:%M:%S}'.format(datetime.now()+timedelta(minutes=arg2))
            grandsons[ctx.message.author.id].time = time
            grandsons[ctx.message.author.id].reminder = arg1
            grandsons[ctx.message.author.id].reminderChannel = ctx.message.channel.id
            await ctx.send(embed=embed)

@bot.command()
async def users(ctx):
    for users in grandsons:
        time = '{:%Y:%m:%d} '.format(grandsons[users].time)+' {:%H:%M:%S}'.format(grandsons[users].time)
        await ctx.send(time)

@bot.command()
async def img(ctx, arg1):
    """Searches for an image"""
    page = random.randint(0, 5)
    resp = getUrls.extract_images(arg1, page, 'photo')
    if resp != False:
        embed = discord.Embed()
        embed.set_image(url=resp)
        embed.title = "Result for "+arg1
        embed.set_footer(text=("Requested by "+ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Not enough love from my grandchildren to perform request :frowning:")

@bot.command()
async def gif(ctx, arg1):
    """Searches for a gif"""
    page = random.randint(0, 5)
    resp = getUrls.extract_images(arg1, page, 'animated')
    embed = discord.Embed()
    if resp != False:
        embed.set_image(url=resp)
        embed.title = "Result for "+arg1
        embed.set_footer(text=("Requested by "+ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = "Not enough love from my grandchildren to perform request frowning"
        await ctx.send(embed=embed)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined, grab a cookie!'.format(member))

path = '../../token' #Set path where your file with token is
file = open(path, 'r')
token = file.readline().rstrip()

bot.loop.create_task(background_checkReminders(bot))
bot.run(token)
