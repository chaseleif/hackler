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

class abot(commands.Bot):#discord.Client):
    def __init__(self):
        super().__init__(command_prefix='!')
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
                else:
                    onepause=False
            await self.change_presence() # ensure we are just online
            onepause=False
            message = self.messagequeue.popleft()
            # system cmds
            if message.content.startswith('!'):
                if message.content=="!quit":
                    await message.channel.trigger_typing()
                    if await self.is_owner(message.author):
                        await message.channel.send(" . . . ok :(")
                        break
                    await asyncio.sleep(1)
                    await message.channel.send(f"ich will doch nicht gehen {message.author.name}")
                elif message.content=="!ruhe":
                    await message.channel.trigger_typing()
                    if await self.is_owner(message.author):
                        self.besilent=True
                        await message.channel.send(":(")
                        self.messagequeue = deque()
                        self.spamcounter=0
                        self.spamflag=0
                    else:
                        await message.channel.send("wie bitte?")
                elif message.content.startswith('!make '): # and message.content.contains(' channel '):
                    await message.channel.trigger_typing()
                    newchannel = re.sub(r'\W+', '', str(message.content[6:]).replace(' ','_'))
                    returnmessage = await chanmod.makenewchannel(theguild=message.guild, channelname=newchannel, requser=message.author)
                    if returnmessage==newchannel:
                        if newchannel.startswith("private"):
                            await message.channel.send("I created a private channel for you")
                        else:
                            await message.channel.send("I created a public channel for you")
                    else:
                        await message.channel.send("Error: " + returnmessage)
                elif message.content.startswith('!delete channel '):
                    await message.channel.trigger_typing()
                    delchannel = re.sub(r'\W+', '', message.content[16:].replace(' ','_'))
                    returnmessage = await chanmod.deleteuserchannel(theguild=message.guild, channelname=delchannel, requser=message.author)
                    try: # they could delete the channel that they are in . . .
                        if returnmessage==delchannel:
                            await message.channel.send("I deleted your channel")
                        else:
                            await message.channel.send("Error: " + returnmessage)
                    except:
                        pass
                elif message.content.startswith('!allow '):
                    await message.channel.trigger_typing()
                    userchan = message.content[7:]
                    returnstatus, returnmessage = await chanmod.allowuserchannel(message.guild, userchan, message.author)
                    if returnstatus=="success":
                        await message.channel.send("All set, "+returnmessage+" can now participate in your channel")
                    else:
                        await message.channel.send("Error: " + returnmessage)
                elif message.content.startswith('!revoke '):
                    await message.channel.trigger_typing()
                    userchan = message.content[8:]
                    returnstatus, returnmessage = await chanmod.revokeuserchannel(message.guild, userchan, message.author)
                    if returnstatus=="success":
                        await message.channel.send("All set, "+returnmessage+" can no longer participate in your channel")
                    else:
                        await message.channel.send("Error: " + returnmessage)
                elif message.content=="!mach weiter":
                    await message.channel.trigger_typing()
                    if await self.is_owner(message.author):
                        self.besilent=False
                        await message.channel.send("jawohl!")
                    else:
                        await message.channel.send("wie bitte?")
                elif message.content=="!commands" or message.content=="!help":
                    await message.channel.trigger_typing()
                    infomsg = "> I say hello and tell jokes.\n> \n"
                    infomsg+= "> Commands: !keyword [optional/**default**] <required value>\n"
                    infomsg+= ">   __math ops supported__  - + % / *\n"
                    infomsg+= ">   !parse <__math expr__>\n"
                    infomsg+= ">   !solve <__math expr__>\n"
                    infomsg+= ">   !make [**public**/private] channel <name>\n"
                    infomsg+= ">   !delete channel <name>\n"
                    infomsg+= ">   !allow <other user> <your private channel>\n"
                    infomsg+= ">   !revoke <other user> <your private channel>"
                    await message.channel.send(infomsg)
                elif message.content.startswith('!solve'):
                    await message.channel.trigger_typing()
                    mathstring, retvalue, errormsg = clpcalc.domath(message.content[6:])
                    returnstring = "That\'s easy, " + mathstring + " = " + str(retvalue)
                    if errormsg!="":
                        returnstring += " (" + errormsg + ")"
                    await message.channel.send(returnstring)
                elif message.content.startswith('!parse'):
                    await message.channel.trigger_typing()
                    parsestring = "I think you mean " + textutils.parsemathstring(message.content[6:])
                    await message.channel.send(parsestring)
            elif 'hello' in message.content or 'Hello' in message.content or 'hallo' in message.content or 'Hallo' in message.content:
                await message.channel.trigger_typing()
                await message.channel.send("Hallo {0.author.mention}!".format(message))
            elif 'help' in message.content or 'HELP' in message.content or 'Help' in message.content:
                await message.channel.trigger_typing()
                await asyncio.sleep(0.2)
                if await self.is_owner(message.author)==True:
                    await message.channel.send("How may I help you {0.author.mention}?".format(message))
                else:
                    await message.channel.send("what?")
            else:
                for atrigger in JOKETRIGGERS:
                    if atrigger in message.content:
                        await asyncio.sleep(1)
                        await message.channel.trigger_typing()
                        joke = textutils.get_joke()
                        await asyncio.sleep(2)
                        if joke != False:
                            await message.channel.send(joke['setup'])
                            await asyncio.sleep(5)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(2)
                            await message.channel.send(joke['punchline'])
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
                    await message.channel.send("I don\'t have time for this nonsense.")
                else:
                    self.spamcounter=0 # once spamflag is 2 we ignore
                    await message.channel.send("Don\'t spam me.")

hackler = abot()
try:
    hackler.loop.create_task(hackler.serviceloop())
    hackler.run(TOKEN)
except:
    pass