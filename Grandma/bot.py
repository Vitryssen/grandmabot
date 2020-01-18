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
import reminders

lastChannelId = ""
bot = commands.Bot(command_prefix='.')

grandsons = {

}

async def background_checkReminders(self):
        await self.wait_until_ready()
        rem = ""
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

async def background_sendRandomReminder(self):
    await self.wait_until_ready()
    while not self.is_closed():
        if len(str(reminders.channelId)) > 0:
            randomReminder = random.randint(0, len(reminders.reminderValues)-1)
            channel = self.get_channel(reminders.channelId)
            print(randomReminder)
            await channel.send('{}'.format(reminders.reminderValues[randomReminder]))
        await asyncio.sleep(random.randint(1800, 3600))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name=".help for commands"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def reminderchannel(ctx):
    """Use this command on the channel where you want the reminders from Grandma"""
    reminders.channelId = ctx.message.channel.id
    await ctx.message.delete()

@bot.command()
async def addReminder(ctx, arg1):
    """Add a reminder to the list of reminders"""
    reminders.reminderValues.append(arg1)
    await ctx.message.delete()

@bot.command()
async def urban(ctx, arg1):
    """Returns Urbandictionary definition"""
    try:
        embed = getWebsite.getUrban(('https://www.urbandictionary.com/define.php?term={}').format(arg1))
        await ctx.send(embed=embed)
    except:
        await ctx.send(await ctx.send("Not enough love from my grandchildren to perform request :frowning:"))
    await ctx.message.delete()

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
async def reminder(ctx, arg1, arg2, arg3='m'):
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
            embed.set_footer(text=("Requested by "+ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
            grandsons[ctx.message.author.id] = userClasses.Grandson(ctx.message.author.name, ctx.message.author.id)
            if(arg3 == 's'):
                time = '{:%Y:%m:%d %H:%M:%S}'.format(datetime.now()+timedelta(seconds=arg2))
                embed.add_field(name="Set for", value=("{} seconds").format(arg2))
            elif(arg3 == 'h'):
                time = '{:%Y:%m:%d %H:%M:%S}'.format(datetime.now()+timedelta(hours=arg2))
                embed.add_field(name="Set for", value=("{} hours").format(arg2))
            elif(arg3 == 'm'):
                time = '{:%Y:%m:%d %H:%M:%S}'.format(datetime.now()+timedelta(minutes=arg2))
                embed.add_field(name="Set for", value=("{} minutes").format(arg2))
            grandsons[ctx.message.author.id].time = time
            grandsons[ctx.message.author.id].reminder = arg1
            grandsons[ctx.message.author.id].reminderChannel = ctx.message.channel.id
            await ctx.send(embed=embed)
    await ctx.message.delete()

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
    await ctx.message.delete()

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
    await ctx.message.delete()

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined, grab a cookie!'.format(member))

path = '../../token' #Set path where your file with token is
file = open(path, 'r')
token = file.readline().rstrip()

bot.loop.create_task(background_checkReminders(bot))
bot.loop.create_task(background_sendRandomReminder(bot))
bot.run(token)
