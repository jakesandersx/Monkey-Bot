from discord.ext import commands, tasks
from discord.ext.commands import MissingPermissions
import discord
import random as rand
import asyncio
import datetime
import sosa
import os
from datetime import datetime
import traceback
from bs4 import BeautifulSoup
import time
import schedule
import ast
import string
import random
import requests
from fake_useragent import UserAgent
import json
import unidecode
import pandas as pd
import lxml
from io import BytesIO
from PIL import Image, ImageEnhance



clash_api_token = '[REDACTED]'

intents = discord.Intents.all()
intents.members = True
intents.presences = True

client = commands.Bot(command_prefix='%', intents=intents)
client.launch_time = datetime.now()
client.remove_command('help')

error_channel = client.get_channel(1080940745864773764)
join_leave_channel = client.get_channel(1080940790316015738)
commands_channel = client.get_channel(1080940827523682364)
edited_messages_channel = client.get_channel(1080940862554509432)
deleted_messages_channel = client.get_channel(1080940877716922428)
launches_channel = client.get_channel(1080940957744238674)


@client.command()
async def coinflip(ctx):
    determine_flip = [1, 0]
    if rand.choice(determine_flip) == 1:
        await ctx.reply('Heads. Needs a better catchphrase'.format(ctx.author))

    else:
        await ctx.reply('Tails. That shit NEVA fails'.format(ctx.author))
    print('coinflip command finished')


@client.command()
async def av(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    memberAvatar = member.avatar_url

    avatarEmbed = discord.Embed(title=f"{member.name}'s Avatar")
    avatarEmbed.set_image(url=memberAvatar)
    avatarEmbed.set_footer(text=f"Requested by {ctx.author}",
                           icon_url=ctx.author.avatar_url)

    await ctx.send(embed=avatarEmbed)
    print('pfp command finished')


@client.command()
async def history(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

        counter = 0

        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                async for message in channel.history(limit=999999999999):
                    if message.author == member:
                        counter += 1

    await ctx.reply(f'{member} has sent {counter} messages in this server.')
    print('history command finished')


@client.command()
async def profile(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    profileEmbed = discord.Embed(title=f"{member.name}'s Profile")

    fields = [('Name', str(member), True),
              ('Top Role', member.top_role.mention, True),
              ('Status', str(member.status).title(), True),
              ('Account Created',
               member.created_at.strftime('%m/%d/%Y %H:%M:%S'), True),
              ('Joined Server', member.joined_at.strftime('%m/%d/%Y %H:%M:%S'),
               True), ('Messages Sent', 'Use %history', True)]

    for name, value, inline in fields:
        profileEmbed.add_field(name=name, value=value, inline=inline)
    profileEmbed.set_thumbnail(url=member.avatar_url)
    profileEmbed.set_footer(text=f"Requested by {ctx.author}",
                            icon_url=ctx.author.avatar_url)

    await ctx.send(embed=profileEmbed)
    print('profile command finished')

@client.event
async def on_member_join(member: discord.Member):
    embed = discord.Embed(description=f"{member} has joined the server",
                          color=0x2ecc71)
    join_leave_channel = client.get_channel(1080940790316015738)
    await join_leave_channel.send(f"{member} has joined the server")


@client.event
async def on_member_remove(member: discord.Member):
    embed = discord.Embed(description=f"{member} has left the server",
                          color=0xe74c3c)
    join_leave_channel = client.get_channel(1080940790316015738)
    await join_leave_channel.send(f"{member} has left the server")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name='%help'))
    for i in range(100):
        print(chr(27) + "[2J")
    print('Connected')
    print('Successful login as {0.user}'.format(client))
    print('\n')
    log_server_update = client.get_channel(990275272261648454)
    time = datetime.now()
    await log_server_update.send('monkey bot is back online at {}'.format(time))
    launches_channel = client.get_channel(1080940957744238674)
    await launches_channel.send(f'monkey bot got back online at {time}')


@client.event
async def on_message_edit(before, after):
    edit_embed = discord.Embed(title=f'{before.author} edited their message')
    edit_embed.add_field(name='Original Message',
                         value=f'{before.content}',
                         inline=False)
    edit_embed.add_field(name='Edited Message',
                         value=f'{after.content}',
                         inline=False)
    jammo_log = client.get_channel(990291989905948672)
    edited_messages_channel = client.get_channel(1080940862554509432)
    await jammo_log.send(embed=edit_embed)
    await edited_messages_channel.send(embed=edit_embed)
    


@client.event
async def on_message_delete(message):
    embed = discord.Embed(
        description=
        f"Message from {message.author} deleted in {message.channel.mention}",
        color=0x3498db)
    deleted_messages_channel = client.get_channel(1080940877716922428)
    jammo_logs = client.get_channel(990281292878852176)
    embed.add_field(name="Message: ", value=message.content)
    embed.timestamp = message.created_at
    await deleted_messages_channel.send(embed=embed)
    await jammo_logs.send(embed=embed)


@client.command()
async def credits(ctx):
    await ctx.send('`Made by Jammo`')
    await ctx.send('`With help from Tekno and tiaanvanniekerk`')
    print('credits command finished')


@client.command()
async def jr(ctx):
    await ctx.send(sosa.jolly_text)
    print('jolly rage command finished')



@client.command()
async def help(ctx, args=None):
    if args == None:
        await ctx.send(sosa.help_text)
    else:
        arg = args.lower()
        if arg == 'av':
            await ctx.reply(
                "%av @User replies with the mentioned user's avatar picture")
        elif arg == 'ban':
            await ctx.reply(
                'Admin Only: %ban @User will ban a user from the server')
        elif arg == 'clear':
            await ctx.reply(
                'Admin Only: %clear # will delete a specified number of messages from chat'
            )
        elif arg == 'coinflip':
            await ctx.reply('%coinflip flips a coin')
        elif arg == 'claninfo':
            await ctx.reply('%claninfo #clantag provides clan information on any given clan')
        elif arg == 'data':
            await ctx.reply(
                'Admin Only: %data will send a download link for admins to view logs'
            )
        elif arg == 'deck':
            await ctx.reply(
                '%deck {trophies} {name} retrives a players deck using their in game name and trophy count'
            )
        elif arg == 'eightball':
            await ctx.reply(
                '%eightball {question} will ask the 8ball a question')
        elif arg == 'help':
            await ctx.reply('U r here rn')
        elif arg == 'history':
            await ctx.reply(
                '%history @User will return how many messages a user has sent in the current server'
            )
        elif arg == 'jr':
            await ctx.reply(':smirk:')
        elif arg == 'stats':
            await ctx.reply('%stats {trophies} {name} will return some basic stats about any given player')
        elif arg == 'kick':
            await ctx.reply(
                'Admin Only: %kick @User will kick a user from the server')
        elif arg == 'mute':
            await ctx.reply(
                'Admin Only: %mute @User time will mute a user from chatting for a specified amount of time'
            )
        elif arg == 'profile':
            await ctx.reply(
                "%profile @User will display a user's server profile")
        elif arg == 'random':
            await ctx.reply('%random will send something random to the chat')
        elif arg == 'timeout':
            await ctx.reply(
                'Admin Only: %timeout @User time will not let a user speak in voice chat for a specified amount of time'
            )
        elif arg == 'rps':
            await ctx.reply('%rps will play rock paper scissors')
        elif arg == 'server':
            await ctx.reply(
                '%serverinfo will display information about the current server'
            )
        elif arg == 'song':
            await ctx.reply('%song will send a random song to the chat')
        elif arg == 'unban':
            await ctx.reply(
                'Admin Only: %unban USERID will unban a user from the server')
        elif arg == 'unmute':
            await ctx.reply(
                'Admin Only: %unmute @User will unmute a user from the server')
        elif arg == 'uptime':
            await ctx.reply(
                '%uptime shows how long the bot has currently been online')
        else:
            await ctx.reply('i dont have that command moron')
        print('help command finished')


@client.command()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - client.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if minutes == 0:
        await ctx.reply(f"bot has currently been online for {seconds} seconds")
    elif hours == 0:
        await ctx.reply(
            f"bot has currently been online for {minutes} minutes, {seconds} seconds"
        )
    elif days == 0:
        await ctx.reply(
            f"bot has currently been online for {hours} hours, {minutes} minutes, {seconds} seconds"
        )
    else:
        await ctx.reply(
            f"bot has currently been online for {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
        )
    print('uptime command done')

@client.command(aliases=['8ball'])
async def eightball(ctx, *, question):
    responses = [
        'Fo sho', 'Dawg. Fuck no.', 'Idk fam. Ask someone else',
        "Yes but only if you're drunk as fuck", 'Do what Jesus would do',
        'Who the fuck cares about that', 'No doubt niggy', 'Dont sweat it fam',
        'Awh Hell nah', 'Aint no way bruh', 'I mean shiii its possible',
        'Probably but like I aint bettin on that shi',
        'Fuck it. You got this shi', 'Nah. Try again later fam',
        'Ion feel like answering that dumbass shit rn', 'Ya. Go away',
        'Nah. Leave me alone', 'My reply is stfu',
        'My sources say no. Sources: Yo momma'
    ]
    response = rand.choice(responses)
    await ctx.reply(response)
    print('8ball command finished')


VC = '%Vee See'
jit = '%Jit'
nigga = '%Nigga'
chink = '%Chink'
jew = '%Jew'
chinese = '%Chinese'
dari = '%Dariotic'
white = '%White'
asian = '%Asian'
Jolly = '%Jolly'
Axcel = '%Axcel'
Shayah = '%Shayah'
GFK = '%GFK'
RG = '%RageGhost'
Jam = '%Jammo'
vaz = '%Vaz'
Sheath = '%Sheath'
Milo = '%Milo'
Swiggy = '%Swiggy'
Chuck = '%Chuck'
Kappa = '%Kappa'
Chimney = '%Chimney'
Japanese = '%Japanese'


@client.event
async def on_message(message):
    msg = message
    content = msg.content
    
    if message.guild == client.get_guild(846859389104554046):
        with open("data.txt", "a") as n:
            n.write("\n" + 'Text: ' + msg.content + " ||||| " + 'Author: ' +
                    str(msg.author) + " ||||| " + str(msg.created_at) +
                    ' ||||| ' + 'Jump Link: ' + str(msg.jump_url))
     
    rageghost_id = 695003930660306945
    jolly_id = 493196157867130919
    jammo_id = 819749600205733989
    author = message.author
    if author == client.get_user(695003930660306945): #Rageghost id
        if 'david' in content.lower():
            await message.delete()
            await message.channel.send(f'Deleted a message from {msg.author}')
            await message.channel.send(f'{message.author.mention} shut up cunt')

    await client.process_commands(message)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.reply(f'{member} has been kicked')
        print('kick command finished')
    except discord.ext.commands.errors.MissingPermissions as deceMP:
        await ctx.reply('you do not have permission to do that')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.reply('you cannot kick people')
        error_channel = client.get_channel(1080940745864773764)
        await error_channel.send(f"{ctx.author} tried to kick someone")


@client.command()
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.reply(f'{member} has been banned')
    print('ban command finished')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.reply('you cannot ban people')
        error_channel = client.get_channel(1080940745864773764)
        await error_channel.send(f"{ctx.author} tried to ban someone")


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    print('clear command finished')


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.reply('you dont have permissions to use that')
        error_channel = client.get_channel(1080940745864773764)
        await error_channel.send(f"{ctx.author} tried to use clear")


async def timeout_user(*, user_id: int, guild_id: int, until):
    headers = {"Authorization": f"Bot {client.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() +
               datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}
    async with client.session.patch(url, json=json,
                                    headers=headers) as session:
        if session.status in range(200, 299):
            return True
        return False
    
@client.command()
async def say(ctx, message: str):
    channel_id = client.get_channel(980718334309957652)
    await channel_id.send(message)

@client.command()
async def random():
    channel_id = client.get_channel(980718334309957652)
    random_list = [
        'https://cdn.discordapp.com/attachments/632633970969935873/991079032269459456/IMG_6021.jpg',
        'https://i.imgur.com/rfMjAjs.png',
        'https://imgur.com/a/ZMZkbkU',
        'https://www.youtube.com/watch?v=pEm_rve9bv8',
        'https://www.youtube.com/watch?v=ltfOdj1Yc44',
        'https://media.discordapp.net/attachments/820396616585314344/980982245126967316/MbPZSKOG.gif',
        'https://tenor.com/view/aesthetic-egirl-egirl-aesthetic-gif-18233199?',
        'https://cdn.discordapp.com/attachments/632633970969935873/988890062462795806/IMG_3124.jpg',
        'https://cdn.discordapp.com/attachments/623686691076571137/640389866802118656/image0.png',
        'https://imgur.com/XmtIE5V',
        'https://tenor.com/view/taeyong-nct-127-concerned-dog-gif-23191321',
        'https://cdn.discordapp.com/attachments/632633970969935873/988582402475589669/1643252839842-1-1.gif',
        'https://tenor.com/view/yes-correct-nodding-right-agree-gif-21291190',
        'https://cdn.discordapp.com/attachments/632633970969935873/987590525832011857/bennyRIP.mp4',
        'https://cdn.discordapp.com/attachments/632633970969935873/987580431396388924/image0.jpg',
        'https://cdn.discordapp.com/attachments/632633970969935873/986857006721822790/unknown.png',
        'https://www.youtube.com/watch?v=JjtsYUibg5I',
        'https://tenor.com/view/elfontheshelf-elfonmyself-thesquad-blackmama-god-i-wish-this-were-me-gif-19220612',
        'bind o host_timescale 0; host_framerate 900; mirv_streams record start',
        'https://www.youtube.com/watch?v=coj8SGedees',
        'https://cdn.discordapp.com/attachments/632633970969935873/984179159238606858/image0.jpg',
        'https://cdn.discordapp.com/attachments/632633970969935873/984086409751183390/47B50172-692D-4211-93EA-F017A7F5F4B5.jpg',
        'https://tenor.com/view/monkey-mojothemonkey-zzsoobn-monkey-sleep-sleepy-gif-22926696',
        'https://tenor.com/view/drink-shot-glass-whiskey-pour-pouring-gif-15196770',
        'https://cdn.discordapp.com/attachments/632633970969935873/983169813268545566/FPto7poX0AABGuI.jpg',
        'https://cdn.discordapp.com/attachments/632633970969935873/983169621110702222/image0.jpg',
        'https://youtu.be/nwQpuxJovCw',
        'https://cdn.discordapp.com/attachments/732856988014346241/983098131837227128/3271640820.mp4',
        'https://pbs.twimg.com/media/FUWSuggWQAEeTBR.jpg',
        'https://cdn.discordapp.com/attachments/632633970969935873/982415851598778388/unknown.png',
        'https://cdn.discordapp.com/attachments/632633970969935873/981855643143143444/4C6FEB08-C85A-49C2-8130-033EDFB9CEC8.png',
        'offline — 06/01/2022 Im have Covat 19',
        'https://cdn.discordapp.com/attachments/632633970969935873/981694879530889246/unknown.png',
        'https://cdn.discordapp.com/attachments/632633970969935873/981691926556315748/IMG_7812.png',
        'https://streamable.com/8i1j0',
        'https://tenor.com/view/get-beamed-beamed-roblox-beam-gif-22785144',
        'https://tenor.com/view/terry-crews-muscle-chest-pecs-move-gif-4754376',
        'https://cdn.discordapp.com/attachments/632633970969935873/980988944755855410/IMG_7778.jpg',
        'https://cdn.discordapp.com/attachments/632633970969935873/980921329320611880/unknown.png',
        'https://cdn.discordapp.com/attachments/632633970969935873/980183451082821632/image0.jpg',
        'https://cdn.discordapp.com/attachments/632633970969935873/980156679607951440/Media-Player-Classic.png',
        'https://cdn.discordapp.com/attachments/632633970969935873/979988653621268500/unknown.png',
        'https://twitter.com/FaZeClan/status/1528782779936231424?',
        'champ — 05/26/2022 I want u to play with this dick',
        'https://cdn.discordapp.com/attachments/632633970969935873/979481374757093466/unknown.png',
        'https://cdn.discordapp.com/attachments/632633970969935873/979476806585434172/1B53952A-3CA1-48A5-9502-6448B5B3B37A.jpg',
        'https://open.spotify.com/track/5DHGRUo4zU3fgbSXlkv724?si=60e5e52b45ac4e22',
        'https://cdn.discordapp.com/attachments/632633970969935873/977640982092845126/cm-chat-media-video-1a55c1bb7-8ee3-5710-abf3-8575f5c278bf247200.MOV',
        'https://tenor.com/view/carl-grimes-cute-edit-gif-21326062',
        'https://i.imgur.com/AUrejaS.png',
        'https://cdn.discordapp.com/attachments/632633970969935873/977625779028508732/image0.jpg',
        'https://cdn.discordapp.com/attachments/632633970969935873/977613224579043398/IMG_7460.jpg',
        'https://cdn.discordapp.com/attachments/607237844901298217/608317621112274964/image0.jpg',
        'https://cdn.discordapp.com/attachments/603378080387432459/608561882332135424/fresh_fade_1.mp4',
        'https://cdn.discordapp.com/attachments/607237844901298217/609473289093382163/image0.jpg',
        'https://cdn.discordapp.com/attachments/607237844901298217/609550441260515358/image0.png',
        'https://cdn.discordapp.com/attachments/607237844901298217/609550777597558785/image0.png',
        'https://cdn.discordapp.com/attachments/607237844901298217/609835404224364545/be_nice_2_me.mp4',
        'https://cdn.discordapp.com/attachments/607237844901298217/609879571617021982/carticong.mp4',
        'https://cdn.discordapp.com/attachments/607237844901298217/610910504361394236/IMG-20190812-WA0110.jpg',
        'https://cdn.discordapp.com/attachments/607237844901298217/611357414389710869/unknown-157.png',
        'луJesuscrhriat',
        'https://cdn.discordapp.com/attachments/607237844901298217/612779113308094558/unknown.png',
        '.', 'https://tinyurl.com/snyvhd7h',
        'https://cdn.discordapp.com/attachments/607213585030184981/957817760094765146/video0_17.mp4',
        'Refresher pls.',
        'https://tenor.com/view/kunar-flu-sneeze-sick-tissue-gif-14001136',
        'Just outcycle', 'God I hate beatdown players',
        'Graveyard players deserve hell', 'Where did my dad go',
        'Todays Wordle: Fuck you',
        'https://cdn.discordapp.com/attachments/889269647315177552/954407995100512366/redditsave.com_lond-evb5w8m3ryn81.mp4',
        'https://cdn.discordapp.com/attachments/889269647315177552/954497799439925368/IMG_2082.png',
        'Por que??????????',
        'ᛁ ᚺᚨᛏᛖ ᛖᚡᛖᚱᚤᛟᚾᛖ. ᛞᛟᚾᛏ ᚹᛟᚱᚱᚤ ᚨᛒᛟᚢᛏ ᛗᛖ. ᛃᚢᛋᛏ ᚠᚨᛚᛚᛁᚾᚷ ᛏᚺᚱᛟᚢᚷᚺ ᚨᚾ ᛖᛪᛁᛋᛏᛖᚾᛏᛁᚨᛚ ᚲᚱᛁᛋᛁᛋ.',
        'WW91J3JlIHByZXR0eSBnb29kIGF0IGNvbXB1dGluZyBpZiB5b3UgY2FuIHRyYW5zbGF0ZSB0aGlzLiBKYW1tbyBpcyB0aGUga2luZy4gTW9ua2V5IGJvdCBvbiB0b3AhIQ==',
        'i, crying, dear sir i ripected for you', 'watching. Fanily Guy!',
        'i, mark, BALLS', 'LOVE ROCKET CYCLE', 'Yoooo???',
        'Them bitches got some saggy ahhh tiddies',
        'Goofy ahh nigggaaaaaaa :skull: :skull:',
        'https://tenor.com/view/deception-apple-logo-obey-gif-13713054',
        'https://cdn.discordapp.com/attachments/932405338991378485/943887845528068147/impact.png',
        'Sick.', 'Thoughts??',
        'https://media.discordapp.neFt/attachments/815510648179130380/900465310799388732/image0.gif',
        'https://media.discordapp.net/attachments/932713481629737020/940063365873684500/ezgif.com-gif-maker_4.gif',
        'https://gfycat.com/fancynippyachillestang',
        'https://media.discordapp.net/attachments/932405338991378485/936457999059390484/960D4F3E-7218-4156-87CA-2C0DBD760526.gif',
        'https://media.discordapp.net/attachments/733212765866426440/742981220786241566/ezgif-1-ef9bd3712598.gif',
        'https://tenor.com/view/segsy-guy-hot-terox-yes-ghadad-gif-18021808',
        'https://tenor.com/view/dr-nefario-fart-gun-gif-20054143',
        'Proud member of Yeeter Gang TM',
        'AHHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAH', '2022!',
        'sTUPID fuckign Ping', '@all Stfu!', 'Shame on You',
        'https://cdn.discordapp.com/attachments/703922373535072308/949576169114726420/video0_5-1-1.mp4',
        'QUIT',
        'https://tenor.com/view/sushichaeng-golozer-golozer42-ritchie-golozer-ritchie-gif-22225591',
        'Axcel Erp', 'Bald ahh head', 'Twitter is for losers',
        'The Alamo was fraud', 'art is like play', 'Smoki.', 'Yup.', 'kk',
        'Hoi', 'Can we ban this kid', '@Jammy!', 'cl_allowdownload 1?',
        'Just throw a night witch behind it', 'Check twitter. Life good.',
        'Fax.', 'Form?', '(everyone liked that)', '(nobody liked that)',
        'Twizzy Gang', 'I miss the old kanye', 'MO LIGHT REDDIT', '6k PB talk',
        'Faggoit', 'LAOO',
        'https://www.youtube.com/watch?v=5tIiRvl-064&ab_channel=bride',
        'http://astronaut.io/#',
        'https://cdn.discordapp.com/attachments/632633970969935873/934980157263974450/IMG_2936.jpg',
        'Bro ill eat ur dead moms ashes like fun dip',
        'Croak weak ahh nigggaaaa',
        'On this big ass wap i actually got hacked',
        'one time i fapped so long i got a vruise on my arm',
        'https://cdn.discordapp.com/attachments/632633970969935873/653804884381925387/video0.mp4',
        'https://cdn.discordapp.com/attachments/703922224599531588/851532563738394624/How_could_you_hate_from_outside_of_the_club.mp4',
        'L role L life L dad L discord L name L pfp ratio boso my respect for you sheesh my glizzy gobbler menace to society Lgtb',
        'I love poo so much', 'Shut the fu k',
        'https://cdn.discordapp.com/attachments/607233923528916996/791999143853555752/video0.mp4',
        'https://cdn.discordapp.com/attachments/607233923528916996/788239000510398474/video0.mp4',
        'https://cdn.discordapp.com/attachments/607233923528916996/788114639673491456/video0.mov',
        'https://cdn.discordapp.com/attachments/607233923528916996/787874111409881138/video0.mov',
        'https://media.discordapp.net/attachments/771469683916275722/781708784447258664/image0.jpg',
        'ALVAN!!!!',
        'https://tenor.com/view/pokelawls-turkish-kiss-turkish-fat-kiss-love-gif-16694934',
        'https://tenor.com/view/coke-spill-shocked-funny-gif-13744709',
        'https://media.discordapp.net/attachments/718265073889574913/749344795326939197/image0.gif',
        'https://cdn.discordapp.com/attachments/592969234389401601/676650055666499595/583.JPG',
        'https://cdn.discordapp.com/attachments/607233923528916996/674900642044575744/1x.mp4',
        'https://www.youtube.com/watch?v=i9_40Tcu_nc',
        'https://cdn.discordapp.com/attachments/607233923528916996/617629477459197954/image0.png',
        'Nirvana 4 dropping tonight.... stay tuned',
        "I can't take Baig dick But i can Suck on it..... - Tupac",
        'https://www.youtube.com/watch?v=blkeIqivVnQ',
        'https://cdn.discordapp.com/attachments/623686691076571137/652313827920314398/image0.jpg',
        'https://images-ext-1.discordapp.net/external/y4R-q0sRBjFT5UknzqzMkID2tBEtPFIGfB9c-M9eNKk/https/media.discordapp.net/attachments/518215403152080896/649304178660999194/9LCsmPq-iHaNq4IT.mp4',
        'https://cdn.discordapp.com/attachments/448512638851481611/644926997520318482/received_442122210017553.mp4',
        "I’m going to Run over Ur Ballz",
        'the partey never stops when u r in melter',
        'jeb get home from work in 20 min if u r not in vc ready for cards against jeb u are being executed 1944 style',
        'https://media.discordapp.net/attachments/418922126938996737/745715801784451282/GIF4zQIFSL9C9B2kA3vU0.gif',
        'smh-shakingmyhead-nope-steveharvey gif',
        'https://cdn.discordapp.com/attachments/623686691076571137/640389866802118656/image0.png',
        'https://youtu.be/AMHSjHWSDvo',
        'https://cdn.discordapp.com/attachments/623690352594780160/626831994122141696/image1.gif',
        'https://cdn.discordapp.com/attachments/623690352594780160/626831994973847583/image0.gif',
        'https://cdn.discordapp.com/attachments/623690352594780160/624997939965591562/image0.jpg',
        'https://cdn.discordapp.com/attachments/623690352594780160/625670327279550484/image0.jpg',
        'There are 360 days in a year. Like the degres in a circle',
        'If im ever a virigin when im in my 30s Bich im fuckin a chicken',
        'Man whenever i see cute dogs i justr want to bite it',
        'Lmfaoooo stay broke boy',
        'Bich its national sex day every day for my meat',
        'U niggaz in trouble',
        'Idk what bitches mean When black penis feels better. I tried it out myself it feels the same',
        'I told one of the strippers poggers when she whipped her titties out',
        'U rly think Im dumb i Have a 2.6 Gpa',
        '@janmio im@ go. a fuckibg cry if u fuckibg leave me',
        'https://media.discordapp.net/attachments/846859389565534240/943304849532022784/2b9c2ea18bffcdf3ec4442f258811ae1.png?width=400&height=107',
        'https://cdn.discordapp.com/attachments/846859389565534240/942871162336186368/IMG_3442.png',
        'https://media.discordapp.net/attachments/921645273342689300/928166645875216444/IMG_4005.png?width=400&height=178',
        'https://media.discordapp.net/attachments/921645273342689300/921648935574048768/BF07D871-1841-4B7A-93A1-56605EE1C617.jpg?width=400&height=91',
        'Jolly cant win a CC',
        'https://www.youtube.com/watch?v=J6rY1RncyOM&ab_channel=Axcel',
        'アンドラーシュあなたがこれを読んでいるなら、私はあなたの内臓が嫌いです', ':farmer:',
        'https://tenor.com/view/praying-pray-snoop-dogg-begging-please-gif-12502205',
        'https://open.spotify.com/track/5mCPDVBb16L4XQwDdbRUpz?si=384acf3ba38545d7',
        'lololol', 'Vaz was here, inside the code'
    ]

    reply = rand.choice(random_list)
    await channel_id.send(reply)
    print('random command finished')


@client.command()
async def timeout(ctx: commands.Context, member: discord.Member, until: int):
    handshake = await timeout_user(user_id=member.id,
                                   guild_id=ctx.guild.id,
                                   until=until)
    if handshake:
        return await ctx.send(
            f"Successfully timed out user for {until} minutes.")
        print('timeout command finished')
    await ctx.send("Something went wrong")



@client.command()
async def serverinfo(ctx):
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    role_count = len(ctx.guild.roles)

    embed2 = discord.Embed(color=ctx.author.color)

    embed2.add_field(name='Name', value=f"{ctx.guild.name}", inline=True)
    embed2.add_field(name='Owner', value=f'{ctx.guild.owner}', inline=True)
    embed2.add_field(name='Highest role',
                     value=ctx.guild.roles[-1],
                     inline=True)
    embed2.add_field(name='Number of Roles',
                     value=str(role_count),
                     inline=True)
    embed2.add_field(name='Number Of Members',
                     value=ctx.guild.member_count,
                     inline=True)
    embed2.add_field(name='Text Channels', value=text_channels, inline=True)
    embed2.add_field(name='Voice Channels', value=voice_channels, inline=True)
    embed2.add_field(name='Categories', value=categories, inline=True)

    embed2.set_thumbnail(url=ctx.guild.icon_url)
    embed2.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    embed2.set_footer(
        text=
        f'Requested by {ctx.author} | Server Created: {ctx.guild.created_at.__format__("%m/%d/%Y")}',
        icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed2)
    print('serverinfo command finished')

@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, num: int, time: str):
    if not member:
        await ctx.send("who do u want me to mute")
        return
    mod = discord.utils.get(ctx.guild.roles, name='Mod')
    leader = discord.utils.get(ctx.guild.roles, name='DK Leader')

    if time == 'seconds':
        num = num
    elif time == 'minutes':
        num = num * 60
    elif time == 'hours':
        num = num * 3600
    elif time == 'days':
        num = num * 84600

    if mod in member.roles:
        await ctx.reply('i cant do that. he is a mod')
    elif leader in member.roles:
        await ctx.reply('i cant do that. he is a leader')
    else:
        role = discord.utils.get(ctx.guild.roles, name="muted")
        await member.add_roles(role)
        await ctx.reply(f'{member} has been muted for {num} {time}')

        await asyncio.sleep(num)
        await member.remove_roles(role)
        await ctx.send(f'{member}, you are now muted')
        print('mute command finished')
        


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.reply('you cant mute people')
        error_channel = client.get_channel(1080940745864773764)
        await error_channel.send(f"{ctx.author} tried to mute someone")


@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
    if not member:
        ctx.send("who do u want me to unmute")
        return

    muted = discord.utils.get(ctx.guild.roles, name='muted')
    author = ctx.author
    await member.remove_roles(muted)
    await ctx.send(f'{member}, you have been unmuted by {author}')
    print('unmute command finished')


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.reply('you cant unmute people')
        error_channel = client.get_channel(1080940745864773764)
        await error_channel.send(f"{ctx.author} tried to unmute someone")


@client.command()
@commands.has_permissions(kick_members=True)
async def unban(ctx, id: int):
    author = ctx.author
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f'{user} has been unbanned by {author}')
    print('unban command finished')


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.reply('you cant unban people')
        error_channel = client.get_channel(1080940745864773764)
        await error_channel.send(f"{ctx.author} tried to unban someone")


@client.event
async def on_command(ctx):
    user = ctx.author
    command = ctx.command

    jammo_log_channel = client.get_channel(990275229110636574)
    commands_channel = client.get_channel(1080940827523682364)
    await jammo_log_channel.send(f'{user} used -> {command}')
    await commands_channel.send(f'{user} used -> {command}')
    
@client.command()
@commands.has_permissions(administrator=True)
async def data(message):
    await message.author.send(file=discord.File('data.txt'))
    print('data command finished')


@data.error
async def logs_error(ctx, error):
    if isinstance(error, MissingPermissions):
        error_channel = client.get_channel(1080940745864773764)
        await error_channel.send('log error')
        
@client.command()
async def claninfo(ctx, clan_tag):
    ua = UserAgent(verify_ssl=False, fallback_cache_timeout=300)
    user_agent = ua.random
    api_token = clash_api_token
    headers = {
        'Accept': 'application/json',
        'authorization': api_token,
        'User-Agent': user_agent
    }

    r = requests.get(f"https://api.clashroyale.com/v1/clans/%23{clan_tag.replace('#', '')}", headers=headers)
    print(r.content)
    if int(r.status_code) == 200:
        clan_data = r.json()
        clan_name = clan_data['name']
        description = clan_data['description']
        score = clan_data['clanScore']
        war_trophies = clan_data['clanWarTrophies']
        required_trophies = clan_data['requiredTrophies']
        member_count = clan_data['members']
        await ctx.send(f"Data for {clan_name}\n\nDescription: {description}\nClan Score: {score}\nClan War Trophies: {war_trophies}\nRequired Trophies: {required_trophies}\nMember Count: {member_count}")
    else:
        await ctx.send('api error')


def get_player_tag(player_name):
    url = f"https://api.royaleapi.com/search"
    querystring = {"name": player_name}

    headers = {
        "Accept": "application/json",
        "auth": "your-royaleapi-token"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        if data:
            print(data[0]["tag"])
            return data[0]["tag"]
        else:
            return None
    else:
        return None


def get_player_tag(player_name, trophies):
        for i in range(5):
            ua = UserAgent()
            user_agent = ua.random
            headers = {"User-Agent": user_agent}

            print("Starting Trophy player matching...")
            response = requests.get(
                f'https://royaleapi.com/player/search/results?lang=en&q={player_name}',
                headers=headers)
            page_soup = BeautifulSoup(response.content, "html.parser")

            entire_table = page_soup.find(
                'table', class_='ui selection unstackable attached table')
            if "player_tag" in str(entire_table):
                all_tags = entire_table.find_all('div', class_='player_tag')
            else:
                continue
            if len(all_tags) >= 1:
                all_clean_tags = [single_tag.text for single_tag in all_tags]
                return all_clean_tags
            else:
                continue
        return ("No user were found by that name")

@client.command()
async def deck(ctx, player_name: str, trophies: int):
    # Get the player's tag from their name and trophies
    player_tag = get_player_tag(player_name, trophies)
    if player_tag is None:
        await ctx.send(f"Could not find a player named '{player_name}' with {trophies} trophies.")
        return
    
    # Make API request to get the player's battle log
    response = requests.get(f'https://api.clashroyale.com/v1/players/{player_tag}/battlelog',
                            headers={'Authorization': clash_api_token})
    data = response.json()
    
    # Find the player's most recent battle where they had the given trophy count
    battle = None
    for b in data:
        if 'team' in b:
            for p in b['team']:
                if p['tag'] == player_tag and p['startingTrophies'] == trophies:
                    battle = b
                    break
        if battle is not None:
            break
    
    # Extract the player's deck from the battle data
    deck = None
    if battle is not None:
        for p in battle['team']:
            if p['tag'] == player_tag:
                deck = p['cards']
                break
    
    # Send the player's deck as a message
    if deck is not None:
        deck_str = ', '.join(deck)
        await ctx.send(f"{player_name}'s current deck at {trophies} trophies: {deck_str}")
    else:
        await ctx.send(f"Could not find a battle where {player_name} had {trophies} trophies.")





@client.command()
async def stats(ctx, required_trophies, player_name):
    ua = UserAgent()

    def player_deck_retrieve(player_tags, required_trophies):
        if len(player_tags) != 0:
            user_agent = ua.random
            api_token = clash_api_token
            headers = {
                "Accept": "application/json",
                "authorization": api_token,
                "User-Agent": user_agent
            }

            for single_tag in player_tags:
                all_card_names = str()
                r = requests.get(
                    f"https://api.clashroyale.com/v1/players/%23{single_tag.replace('#', '')}",
                    headers=headers)
                print(r.content)
                if int(r.status_code) == 200:
                    all_player_data = r.json()
                    trophies = all_player_data['trophies']
                    if str(trophies) == str(required_trophies):
                        pb = all_player_data['bestTrophies']
                        all_battles = all_player_data['battleCount']
                        wins = all_player_data['wins']
                        losses = all_player_data['losses']
                        fav = all_player_data['currentFavouriteCard']['name']
                        current_deck = all_player_data['currentDeck']
                        card_names = [cn['name'] for cn in current_deck]
                        player_deck = f"Deck: {',  '.join(card_names)}"
                        current_season_high = all_player_data['leagueStatistics']['currentSeason']['bestTrophies']
                        best_season = all_player_data['leagueStatistics']['bestSeason']['trophies']
                        previous_season = all_player_data['leagueStatistics']['previousSeason']['trophies']
                        stats = f"Statistics on {all_player_data['name']} \n\nPersonal Best: {pb}" \
                                f"\nWins: {wins}\nLosses: {losses}\nFavorite Card: {fav}\nCurrent Season High: {current_season_high}\n" \
                                f"Previous Season: {previous_season}\nBest Season: {best_season}\n{player_deck}"
                        return stats
            return ("No user found with that amount of trophies")

    def user_name_receive(player_name):
        for i in range(5):
            user_agent = ua.random
            headers = {"User-Agent": user_agent}

            print("Starting Trophy player matching...")
            response = requests.get(
                f'https://royaleapi.com/player/search/results?lang=en&q={player_name}',
                headers=headers)
            page_soup = BeautifulSoup(response.content, "html.parser")

            entire_table = page_soup.find(
                'table', class_='ui selection unstackable attached table')
            if "player_tag" in str(entire_table):
                all_tags = entire_table.find_all('div', class_='player_tag')
            else:
                continue
            if len(all_tags) >= 1:
                all_clean_tags = [single_tag.text for single_tag in all_tags]
                return all_clean_tags
            else:
                continue
        return ("No user were found by that name")

    user_name = user_name_receive(player_name)
    if type(user_name) == list:
        await ctx.send(player_deck_retrieve(user_name, required_trophies))
    else:
        await ctx.send(user_name)



    
@client.command()
async def leaderboard(ctx):
    headers = {"Accept":"application/json", "authorization":clash_api_token}

    r=requests.get(f"https://api.clashroyale.com/v1/clans/%23JC0YVU/currentriverrace", headers=headers)

    clean_data = json.loads(r.content)
    await ctx.reply(clean_data)
    own_clan = clean_data['clan']

    all_participants = own_clan['participants']
    ranking_data = {}
    for single_participant in all_participants:
        if single_participant['decksUsed'] != 0:
            if str(single_participant['fame']) not in ranking_data.keys():
                ranking_data[str(single_participant['fame'])] = [{'name': single_participant['name'], 'fame': single_participant['fame']}]
            else:
                ranking_data[str(single_participant['fame'])].append({'name': single_participant['name'], 'fame': single_participant['fame']})

    all_rank_int = [int(ri) for ri in ranking_data.keys()]
    all_rank_int.sort(reverse=True)


    main_data = {'Rank':[], 'Name':[], 'Fame':[]}
    main_counter = 1
    for single_fame in all_rank_int:
        for single_player in ranking_data[str(single_fame)]:
            new_name = ''.join(ch for ch in single_player['name'] if ch.isalpha())
            new_name = unidecode.unidecode(new_name)

            main_data['Rank'].append(main_counter)
            main_data['Name'].append(new_name)
            main_data['Fame'].append(single_player['fame'])

            main_counter += 1

    print(main_data)
    array = pd.DataFrame(main_data)
    embed = discord.Embed(description='```' + array.to_markdown(index=False) + '```') 
    await ctx.send(embed=embed)
    
    

    
    
@client.command()
async def attacks(ctx):
    headers = {"Accept":"application/json", "authorization":clash_api_token}

    r=requests.get(f"https://api.clashroyale.com/v1/clans/%23JC0YVU/currentriverrace", headers=headers)

    clean_data = json.loads(r.content)
    #print(clean_data)
    own_clan = clean_data['clan']

    all_participants = own_clan['participants']
    attacks_data = {}
    for single_participant in all_participants:
        if single_participant['decksUsed'] != 0:
            attacks_left = 4-int(single_participant['decksUsedToday'])
            if attacks_left != 0:
                if str(attacks_left) in attacks_data.keys():
                    attacks_data[str(attacks_left)].append(single_participant['name'])
                else:
                    attacks_data[str(attacks_left)] = [single_participant['name']]
                
    main_attack = []
    for single_attack in attacks_data.keys():
        main_attack.append(f'{single_attack} Attacks Left')
        main_attack.append(f'-'*15)
        for single_player in attacks_data[single_attack]:
            main_attack.append(single_player)
        main_attack.append("   ")
    array = {'Attacks Left': main_attack}
    array = pd.DataFrame(array)
    embed = discord.Embed(description='```' + array.to_markdown(index=False) + '```') 
    await ctx.send(embed=embed)

    
    
@client.command()
async def link(ctx, clash_account_tag):
    try:
        player_data = open('player_data.txt', 'a')
    except:
        player_data = open('player_data.txt', 'w')
    player_data_read = open('player_data.txt', 'r').read().split("\n")
    if len(player_data_read) >= 1:
        all_discord_saved = []
        for pdr in player_data_read:
            if len(pdr.split('; ')) >= 1:
                all_discord_saved.append(pdr.split('; ')[0])
        if str(ctx.author.id) not in all_discord_saved:
            player_data.write(f"{str(ctx.author.id)}; {str(clash_account_tag)}\n") 
            await ctx.send(f"{str(clash_account_tag)} Clash Account linked to <@{str(ctx.author.id)}>")
        else:
            await ctx.send(f'{str(ctx.author.display_name)} is already linked to {str(clash_account_tag)}')
    
    
@client.command(pass_context=True)
async def ping(ctx):
    try:
        player_data = open('player_data.txt', 'r')
    except:
        print("player_data.txt not found")
        player_data = False
    if player_data != False:
        player_data = player_data.read()
        players = [player.split('; ') for player in player_data.split('\n')]
        clean_players = [player for player in players if len(player) >= 2]
        all_clash_accounts = []
        all_discord_accounts = []
        for single_player in clean_players:
            all_clash_accounts.append(single_player[1])
            all_discord_accounts.append(single_player[0])

        headers = {"Accept":"application/json", "authorization":clash_api_token}
        r=requests.get(f"https://api.clashroyale.com/v1/clans/%23JC0YVU/currentriverrace", headers=headers)

        clean_data = json.loads(r.content)
        own_clan = clean_data['clan']
        all_participants = own_clan['participants']
        all_player_tags = [player_tag['tag'] for player_tag in all_participants]
        all_player_names = [player_tag['name'] for player_tag in all_participants]
        
        all_attacks_left = []
        for single_clash in all_clash_accounts:
            try:
                player_index = all_player_tags.index(single_clash)
            except:
                await ctx.send(f"{str(single_clash)} could not be found in clan")
                continue

            decks_used = all_participants[player_index]['decksUsedToday']
            if (4 - int(decks_used)) != 0:
                player_discord = all_discord_accounts[all_clash_accounts.index(single_clash)]
                all_attacks_left.append(f"<@{str(player_discord)}>, you have {int(4 - int(decks_used))} attacks left")
        await ctx.send("\n".join(all_attacks_left))
        print("ping command finished")

@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        error_channel = client.get_channel(1080940745864773764)
        await ctx.reply('you dont have authority to do that') 
        await error_channel.send(f"{ctx.author} tried to use ping")
        



    
@client.command()
async def image(ctx, search_query, text_on_image):
    def text_to_image(image_file_list, required_text):
        if len(image_file_list) == 0:
            return "No images found"
        font_choice = rand.choice(list(range(1, 9)))
        
        all_fonts = open('all_fonts.txt', 'r').read()
        font_sections = all_fonts.split("---")
        selected_font = font_sections[font_choice-1]
        font_lines_split = selected_font.split('\n')
        font_lines_split.pop(0)
        font_lines_split.pop()
        
        font_using = {}
        for single_line in font_lines_split:
            splitted = single_line.split(' = ')
            font_using[str(splitted[0])] = ast.literal_eval(splitted[1])
        
        def text_image_generator():
            list_im = [rt for rt in required_text.replace(" ", "^").replace("+", "^").replace("-", "^").replace("_", "^").replace(".", "^").lower()]
            new_text_images = []
            image_dict = {}
            
            counter = 0
            for single_letter_image in list_im:
                cur_img = Image.new("RGBA", font_using[str(single_letter_image+"_size")])
                cur_img.putdata(font_using[single_letter_image])
                
                image_dict[counter] = cur_img
                counter += 1

            widths, heights = zip(*(i.size for i in image_dict.values()))

            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new('RGBA', (total_width, max_height))

            x_offset = 0
            for im in image_dict.values():
                new_im.paste(im, (x_offset,0))
                x_offset += im.size[0]

            return new_im
        
        text_created = text_image_generator()
        new_text_image_size = text_created.size
        
        image_chosen = rand.choice(image_file_list)
        image_size = image_chosen.size
        
        new_final_image = Image.new('RGBA', image_size)
        new_final_image.paste(image_chosen)
        
        threshhold = 0.95
        try1 = image_size[0] / new_text_image_size[0]
        if try1 >= 1:
            if int(try1 - 1) <= 1:
                new_resize = (int((new_text_image_size[0]*try1)*threshhold), int((new_text_image_size[1]*try1-0.2)*threshhold))
            else:
                new_resize = (int((new_text_image_size[0]*int(try1))*threshhold), int((new_text_image_size[1]*int(try1-0.2))*threshhold))
        else:
            change_threshhold = (image_size[0]*threshhold)/new_text_image_size[0]
            new_resize = ((int(new_text_image_size[0]*change_threshhold), int(new_text_image_size[1]*change_threshhold)))

        final_text = text_created.resize(new_resize)
        
        x_cords, y_cords = int(int(image_size[0]-int(final_text.size[0]))/2), int(image_size[1]/15)
        new_final_image.paste(final_text, (x_cords, y_cords), final_text)
        new_final_image.save('image.png')
        return 'image.png'


    def image_find_save(search_query, on_image_text):
        ua = UserAgent()
        
        query = str(search_query.strip()).replace(" ", '+').replace(".", '+').replace("-", '+').replace("_", '+')
        search_page = requests.get(f"https://www.google.com/search?q={query}&source=lnms&tbm=isch&sa=X&tbs=il:ol", allow_redirects=True, headers={'User-Agent' : UserAgent().random})

        soup = BeautifulSoup(search_page.content, 'lxml')
        main_table = soup.find('table', class_='GpQGbf')

        all_links = []
        for single_row in main_table.find_all('tr'):
            for single_image in single_row.find_all('td', class_='e3goi'):
                for valid_link in single_image.find_all('img'):
                    try:
                        a_url = valid_link['src']
                    except:
                        continue

                    all_links.append(a_url)
        all_found_Images = []
        for single_main_link in all_links:
            query = search_query.replace(" ", '+').replace(".", '+').replace("-", '+').replace("_", '+')
            search_page = requests.get(f"https://www.google.com/search?q={query}&source=lnms&tbm=isch&sa=X", allow_redirects=True, headers={'User-Agent' : UserAgent().random})

            soup = BeautifulSoup(search_page.content, 'lxml')
            main_table = soup.find('table', class_='GpQGbf')

            all_links = []
            for single_row in main_table.find_all('tr'):
                for single_image in single_row.find_all('td', class_='e3goi'):
                    for valid_link in single_image.find_all('img'):
                        try:
                            a_url = valid_link['src']
                        except:
                            continue

                        all_links.append(a_url)
        tries = 0
        while True:
            tries += 1
            if tries >= 5:
                break
            parameters = {'url': rand.choice(all_links)}
            image_request = requests.post('https://tineye.com/result_json/', params=parameters, headers={'User-Agent' : UserAgent().random})
            json_data = image_request.json()

            all_images = []
            all_images_names = []


            for single_match in json_data['matches']:
                image_url = single_match['domains'][0]['backlinks'][0]['url']

                try:
                    img_request = requests.get(image_url, stream=True, headers={'User-Agent' : UserAgent().random}, timeout=10, verify=False)
                    with open(f"temp_images/test{len(all_images_names)+1}.jpg", 'wb') as test_image:
                        test_image.write(img_request.content)
                    all_images_names.append(f'temp_images/test{len(all_images_names)+1}.jpg')
                except:
                    continue


            if len(all_images_names) == 0:
                continue

            for single_image in all_images_names:
                try:
                    img = Image.open(single_image)
                except:
                    continue
                all_images.append(img)
            
            time.sleep(1)
            if len(all_images) != 0:
                return text_to_image(all_images, on_image_text)
        return "Could not find image"
	
    final_image_out = image_find_save(search_query, text_on_image)
    if not final_image_out.endswith('.png'):
        await ctx.reply(final_image_out)
    final_image = Image.open("image.png")
    sharpness = ImageEnhance.Sharpness(final_image)
    factor = 50
    final_image_edit = sharpness.enhance(factor)
    final_image_edit.save('image.png')
    
    if final_image_out.endswith('.png'):
        await ctx.reply(file=discord.File("image.png"))
    else:
        await ctx.send(file=discord.File('image.png'))

        
@client.command(pass_context=True)
@commands.has_role('DK Leader')
async def accounts(ctx):
    try:
        player_data = open('player_data.txt', 'r')
    except:
        print("player_data.txt not found")
        player_data = False
    if player_data != False:
        player_data = player_data.read()
        players = [player.split('; ') for player in player_data.split('\n')]
        clean_players = [player for player in players if len(player) >= 2]
        all_clash_accounts = []
        all_discord_accounts = []
        for single_player in clean_players:
            all_clash_accounts.append(single_player[1])
            all_discord_accounts.append(single_player[0])

        headers = {"Accept":"application/json", "authorization":clash_api_token}
        r=requests.get(f"https://api.clashroyale.com/v1/clans/%23JC0YVU/currentriverrace", headers=headers)

        clean_data = json.loads(r.content)
        own_clan = clean_data['clan']
        all_participants = own_clan['participants']
        all_player_tags = [player_tag['tag'] for player_tag in all_participants]
        all_player_names = [player_tag['name'] for player_tag in all_participants]
        
        all_attacks_left = []
        for single_clash in all_clash_accounts:
            try:
                player_index = all_player_tags.index(single_clash)
            except:
                await ctx.send(f"{str(single_clash)} could not be found in clan")
                continue
            
            decks_used = all_participants[player_index]['decksUsedToday']
            player_discord = all_discord_accounts[all_clash_accounts.index(single_clash)]
            all_attacks_left.append(f"<@{str(player_discord)}> is linked to {single_clash}")
        await ctx.send(f'we currently have {len(all_attacks_left)} accounts linked: \n\n' + "\n".join(all_attacks_left))
        

        
@client.event
async def on_error(event, *args, **kwargs):
    embed = discord.Embed(title=':x: Event Error', colour=0xe74c3c) #Red
    embed.add_field(name='Event', value=event)
    embed.description = '```py\n%s\n```' % traceback.format_exc()
    embed.timestamp = datetime.utcnow()
    error_channel = client.get_channel(1080940745864773764)
    await error_channel.send(embed=embed)        
        
    
    
monkey_token = '[REDACTED]'
cool_token = '[REDACTED]'

client.run('[REDACTED]')