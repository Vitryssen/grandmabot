import discord
from discord.ext import commands
import random
import getWebsite
import sys
import getUrls
import userClasses
import datetime
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix='.')

grandsons = {

}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name=".help for commands"))

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
            grandsons[ctx.message.author.id].time = datetime.now()+timedelta(minutes=arg2)
            await ctx.send(embed=embed)

@bot.command()
async def users(ctx):
    for users in grandsons:
        time = '{:%Y:%m:%d} '.format(grandsons[users].time)+' {:%H:%M:%S}'.format(grandsons[users].time)
        await ctx.send(time)

@bot.command() #Change img and gif to use urls instead of downloading
async def img(ctx, arg1):
    """Searches for an image"""
    page = random.randint(0, 10)
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
    page = random.randint(0, 10)
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

file = open('token', 'r')
token = file.readline().rstrip()
bot.run(token)
