# hackler.py

import os
import re
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from collections import deque
import random

import clpcalc
import textutils
import chanmod

random.seed()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
JOKETRIGGERS = ["dumb","whatever","stupid","funny","hard","what","joke","sad","kill"]
QUEUESIZE = 7 # how many outstanding requests to respond to
COMMANDCHAR = '\\'

class abot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='COMMANDCHAR') # catching all text ...
        self.messagequeue = deque()
        self.spamcounter=0 # incrementing counter for don't spam me messages
        self.spamflag=0 # incrementing flag for the serviceloop
        self.besilent=False

    async def serviceloop(self):
        onepause = False
        while True:
            waitcounter=0
            while len(self.messagequeue)<1:
                waitcounter+=1
                if self.spamflag>1:
                    await asyncio.sleep(5)
                    if self.spamchannel is not None:
                        try:
                            await self.spamchannel.send("Don\'t do that")
                        except:
                            pass
                    self.spamflag=1
                    self.spamcounter=0
                elif self.spamflag>0:
                    self.spamcounter=0
                    self.spamflag=0
                elif self.spamcounter>0:
                    self.spamcounter=0
                if len(self.messagequeue)<1:
                    if waitcounter<60:
                        await asyncio.sleep(1) # sleep for 1 sec, for 1 min
                    elif waitcounter<120:
                        await asyncio.sleep(2) # sleep for 2 sec, for 2 min
                    elif waitcounter<180:
                        await asyncio.sleep(5) # sleep for 5 sec, for 5 min
                    elif waitcounter<300:
                        await asyncio.sleep(10) # sleep for 10 sec, for 20 min
                    elif waitcounter%2==0:
                        await asyncio.sleep(30) # sleep for 30 seconds
                    else:
                        await asyncio.sleep(15) # sleep for 15 seconds
                    if waitcounter==179 or (waitcounter>279 and random.randint(0,2)==0 and waitcounter%20==0): # set an indication of idle-ness
                        nextname,nextdetails,nexturl = textutils.getvideo()
                        streamingnow = discord.Streaming(platform="YouTube",name=nextname,details=nextdetails,url=nexturl)
                        await self.change_presence(status=discord.Status.idle, activity=streamingnow)
                continue
            if self.spamflag>1: # getting spammed, drop our queue
                self.spamchannel = self.messagequeue.popleft().channel
                self.messagequeue = deque()
                await asyncio.sleep(15)
                continue
            if self.spamflag>0: # slow down response
                await asyncio.sleep(5)
                if onepause==False:
                    onepause=True
                    continue
            await self.change_presence() # ensure we are just online
            onepause=False
            message = self.messagequeue.popleft()
            # help and cmds
            if message.content.startswith("!help") or message.content==COMMANDCHAR+"commands" or message.content.startswith(COMMANDCHAR+"help"):
                await message.channel.trigger_typing()
                specialprint = ""
                if len(message.content)>5 and (message.content.startswith("!help") or message.content.startswith(COMMANDCHAR+"help")):
                    cutmsg = message.content[6:]
                    if cutmsg.startswith("parse"):
                        specialprint = "> I can parse math expressions with only numbers and math ops\n"
                        specialprint+= "> The result is infix notation. Supported math operations: + - * / %\n"
                        specialprint+= "> Example: " + COMMANDCHAR + "parse -4 + 5 + 5 * -1 - -4 / 5 % 2 + 20 * 4 - 5 * 8 + 2 - 10 % 6 - 4"
                    elif cutmsg.startswith("solve"):
                        specialprint = "> I can solve math expressions with only numbers and math ops\n"
                        specialprint+= "> Supported math operations: + - * / %\n"
                        specialprint+= "> Example: " + COMMANDCHAR + "solve -4 + 5 + 5 * -1 - -4 / 5 % 2 + 20 * 4 - 5 * 8 + 2 - 10 % 6 - 4"
                    elif cutmsg.startswith("make"):
                        specialprint = "> I can make public or private channels for you\n"
                        specialprint+= "> Example: " + COMMANDCHAR + "make [**public**/private] channel <name>\n"
                        specialprint+= ">   For private rooms a new role is created with read/write access and the general role is disallowed this access\n"
                        specialprint+= ">     Implicit **public** room: " + COMMANDCHAR + "make channel pubchan\n"
                        specialprint+= ">     Explicit **public** room: " + COMMANDCHAR + "make public channel pubchan\n"
                        specialprint+= ">     **Private** room: " + COMMANDCHAR + "make private channel privchan\n"
                        specialprint+= ">   You begin as the only user in the new group, manage other users with " + COMMANDCHAR + "allow and " + COMMANDCHAR + "revoke"
                    elif cutmsg.startswith("delete"):
                        specialprint = "> I can delete any channels that you have made with me\n"
                        specialprint+= "> Example: " + COMMANDCHAR + "delete channel MyUnnecessaryRoom"
                    elif cutmsg.startswith("allow"):
                        specialprint = "> Allow other users to read and write in your private channels\n"
                        specialprint+= "> Example: " + COMMANDCHAR + "allow Hackler CoolKidsRoom"
                    elif cutmsg.startswith("revoke"):
                        specialprint = "> Remove a user\'s access to your private room\n"
                        specialprint+= "> Example: " + COMMANDCHAR + "revoke Hackler LameChatRoom"
                if specialprint=="":
                    infomsg = "> I say hello and tell jokes.\n> \n"
                    infomsg+= "> Commands: " + COMMANDCHAR + "word [**default**/optional] <required>\n"
                    infomsg+= ">   __math ops supported__  - + % / *\n"
                    infomsg+= ">   " + COMMANDCHAR + "parse <__math expr__>\n"
                    infomsg+= ">   " + COMMANDCHAR + "solve <__math expr__>\n"
                    infomsg+= ">   " + COMMANDCHAR + "make [**public**/private] channel <name>\n"
                    infomsg+= ">   " + COMMANDCHAR + "delete channel <name>\n"
                    infomsg+= ">   " + COMMANDCHAR + "allow <user> <your private channel>\n"
                    infomsg+= ">   " + COMMANDCHAR + "revoke <user> <your private channel>"
                    await message.channel.send(infomsg)
                else:
                    await message.channel.send(specialprint)
            elif message.content.startswith(COMMANDCHAR):
                if message.content==COMMANDCHAR+"quit":
                    await message.channel.trigger_typing()
                    if await self.is_owner(message.author):
                        await message.channel.send(" . . . **ok** :(")
                        break
                    await asyncio.sleep(1)
                    await message.channel.send(f"ich will **doch nicht** gehen {message.author.mention}")
                elif message.content==COMMANDCHAR+"ruhe":
                    await message.channel.trigger_typing()
                    if await self.is_owner(message.author):
                        self.besilent=True
                        await message.channel.send(f"**:(**")
                        self.messagequeue = deque()
                        self.spamcounter=0
                        self.spamflag=0
                    else:
                        await message.channel.send("und **wer** bist du denn?")
                elif message.content.startswith(COMMANDCHAR+'make '): # and message.content.contains(' channel '):
                    await message.channel.trigger_typing()
                    newchannel = re.sub(r'\W+', '', str(message.content[6:]).replace(' ','_'))
                    returnmessage = await chanmod.makenewchannel(theguild=message.guild, channelname=newchannel, requser=message.author)
                    if returnmessage==newchannel:
                        if newchannel.startswith("private"):
                            await message.channel.send(f"{message.author.mention}, I created the **private channel** for you")
                        else:
                            await message.channel.send(f"{message.author.mention}, I created the **public channel** for you")
                    else:
                        await message.channel.send(f"{message.author.mention}, **Error:** {returnmessage}")
                elif message.content.startswith(COMMANDCHAR+'delete channel '):
                    await message.channel.trigger_typing()
                    delchannel = re.sub(r'\W+', '', message.content[16:].replace(' ','_'))
                    returnmessage = await chanmod.deleteuserchannel(theguild=message.guild, channelname=delchannel, requser=message.author)
                    try: # they could delete the channel that they are in . . .
                        if returnmessage==delchannel:
                            await message.channel.send(f"{message.author.mention}, I **deleted** your channel")
                        else:
                            await message.channel.send(f"{message.author.mention}, **Error:** {returnmessage}")
                    except:
                        pass
                elif message.content.startswith(COMMANDCHAR+'allow '):
                    await message.channel.trigger_typing()
                    userchan = re.sub(r'\W+', '', message.content[7:].replace(' ','_'))
                    returnstatus, returnmessage = await chanmod.updateuserchannelrole(message.guild, userchan, message.author,"add")
                    if returnstatus=="success":
                        await message.channel.send(f"**All set**, {returnmessage} can now participate in your channel {message.author.mention}")
                    else:
                        await message.channel.send(f"{message.author.mention} , **Error:** {returnmessage}")
                elif message.content.startswith(COMMANDCHAR+'revoke '):
                    await message.channel.trigger_typing()
                    userchan = re.sub(r'\W+', "", message.content[8:].replace(' ','_'))
                    returnstatus, returnmessage = await chanmod.updateuserchannelrole(message.guild, userchan, message.author,"delete")
                    if returnstatus=="success":
                        await message.channel.send(f"**All set**, {returnmessage} can no longer participate in your channel {message.author.mention}")
                    else:
                        await message.channel.send(f"{message.author.mention}, **Error:** {returnmessage}")
                elif message.content==COMMANDCHAR+"mach weiter":
                    await message.channel.trigger_typing()
                    if await self.is_owner(message.author):
                        self.besilent=False
                        await message.channel.send(f"**jawohl** {message.author.mention} !")
                    else:
                        await message.channel.send(f"mit **wem** redest du {message.author.mention}?")
                elif message.content.startswith(COMMANDCHAR+'solve'):
                    await message.channel.trigger_typing()
                    mathstring, retvalue, errormsg = clpcalc.domath(message.content[6:])
                    returnstring = "That\'s easy " + message.author.mention + ", " + mathstring + " = **" + str(retvalue) + "**"
                    if errormsg!="":
                        returnstring += " (" + errormsg + ")"
                    await message.channel.send(returnstring)
                elif message.content.startswith(COMMANDCHAR+'parse'):
                    await message.channel.trigger_typing()
                    parsestring = message.author.mention + ", I **think** you mean " + textutils.parsemathstring(message.content[6:])
                    await message.channel.send(parsestring)
            # misc prints
            elif 'hello' in message.content or 'Hello' in message.content or 'hallo' in message.content or 'Hallo' in message.content:
                await message.channel.trigger_typing()
                await message.channel.send(f"**Hallo** {message.author.mention}!")
            elif 'help' in message.content or 'HELP' in message.content or 'Help' in message.content:
                await message.channel.trigger_typing()
                await asyncio.sleep(0.2)
                if await self.is_owner(message.author)==True:
                    await message.channel.send(f"**How** may I help **you** {message.author.mention}?")
                else:
                    await message.channel.send("hat **jemand** was gesagt?")
            else:
                for atrigger in JOKETRIGGERS:
                    if atrigger in message.content:
                        await asyncio.sleep(1)
                        await message.channel.trigger_typing()
                        joke = textutils.get_joke()
                        await asyncio.sleep(2)
                        if joke != False:
                            await message.channel.send(f"**{joke['setup']}**")
                            await asyncio.sleep(5)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(2)
                            await message.channel.send(f"***{joke['punchline']}***")
                        break
        await self.change_presence(status=discord.Status.offline)
        await hackler.logout()
        await exit()

    async def on_ready(self):
        print(f"{self.user} connected to Discord")

    async def on_message(self,message):
        if self.spamflag>2: # 2 flags and we stop responding
            return
        if message.author.id == self.user.id:
            return
        if await self.is_owner(message.author)!=True and self.besilent==True:
            return
        if len(self.messagequeue)<QUEUESIZE:
            self.messagequeue.append(message)
            if self.spamcounter>0 and self.spamflag==0:
                self.spamcounter-=1
        else:
            self.spamcounter+=1 # increment it by one if the queue was full
            if self.spamcounter>QUEUESIZE:
                self.spamflag+=1
                if self.spamflag>1:
                    await message.channel.send(f"**I don\'t have time for this nonsense, {message.author.mention}.**")
                else:
                    self.spamcounter=0 # once spamflag is 2 we ignore
                    await message.channel.send(f"**Don\'t spam me {message.author.mention}.**")

hackler = abot()
try:
    hackler.loop.create_task(hackler.serviceloop())
    hackler.run(TOKEN)
except:
    pass
