# chanmod.py

import discord
import time

async def makenewchannel(theguild, channelname, requser: discord.Member):
    # use time as a counter to prevent name clashes
    newname = ""
    makepublic = True
    startpos = -1
    if channelname.startswith('public_channel_'): # String pre-formatted a bit, spaces are underscores and all valid characters
        startpos=15
    elif channelname.startswith('private_channel_'):
        startpos=16
        makepublic = False
    elif channelname.startswith('channel_'): # public/private not specified. make public
        startpos=8
    else:
        return "**invalid format, get !help**"
    if len(channelname)<startpos+1:
        return "**no channel name specified**"
    newname = channelname[startpos:]
    uniqkey = int(time.time())
    newrolename = requser.name + "-" + newname + "-" + str(uniqkey)
    if makepublic==False:
        # new role to make channel private, restrict read/write
        try:
            await theguild.create_role(name=newrolename,mentionable=False)
            newrole = discord.utils.get(theguild.roles, name=newrolename)
            await requser.add_roles(newrole,reason="private channel",atomic=True)
        except BaseException as e:
            return str(e)
        noaccess = discord.PermissionOverwrite()
        noaccess.send_messages = False
        noaccess.read_messages = False
        noaccess.view_channel = False
        noaccess.stream = False
        noaccess.embed_links = False
        noaccess.attach_files = False
        noaccess.read_message_history = False
        noaccess.mention_everyone = False
        yesaccess = discord.PermissionOverwrite()
        yesaccess.send_messages = True
        yesaccess.read_messages = True
        yesaccess.view_channel = True
        yesaccess.stream = True
        yesaccess.embed_links = True
        yesaccess.attach_files = True
        yesaccess.read_message_history = True
        specrules = { newrole: yesaccess, theguild.default_role: noaccess }
        try:
            await theguild.create_text_channel(name=newrolename,overwrites=specrules,reason=requser.name+" private channel")
        except BaseException as e:
            return str(e)
    else:
        try:
            await theguild.create_text_channel(name=newrolename,reason=requser.name+" public channel")
        except BaseException as e:
            return str(e)
    return channelname

async def deleteuserchannel(theguild, channelname, requser):
    fullchannelname = ""
    for chan in theguild.channels:
        if chan.name.startswith(requser.name):
            if chan.name[len(requser.name)+1:len(requser.name)+len(channelname)+1]==channelname:
                try:
                    await chan.delete(reason="Deleting user channel")
                except BaseException as e:
                    return str(e)
                fullchannelname = chan.name
                break
    if fullchannelname=="":
        return "**Couldn\'t find your channel** \"" + channelname + "\""
    rolelist = await theguild.fetch_roles()
    for arole in rolelist:
        if arole.name==fullchannelname:
            try:
                await arole.delete(reason="Deleting role for private channel")
            except BaseException as e:
                return str(e)
            break
    return channelname

async def updateuserchannelrole(theguild, userchan, requser, userop):
    addinguser = False
    if userop=="add":
        addinguser=True
    elif userop!="delete":
        print(f"chanmod.updateuserchannelrole called with userop=\"{userop}\"\n")
    theusername = ""
    thechannel = ""
    donewithuser = False
    for c in userchan:
        if c=='_' and theguild.get_member_named(theusername)!=None:
            donewithuser=True
        elif donewithuser==False:
            theusername+=c
        else:
            thechannel+=c
    if donewithuser==False:
        return "failure", "Couldn\'t find the user in \"" + userchan + "\""
    if thechannel=="":
        return "failure", "No channel to add \"" + theusername + "\" to"
    fullchannelname = ""
    for chan in theguild.channels:
        if chan.name.startswith(requser.name):
            if chan.name[len(requser.name)+1:len(requser.name)+len(thechannel)+1]==thechannel:
                fullchannelname = chan.name
                break
    if fullchannelname=="":
        return "failure", "Couldn\'t find your channel \"" + thechannel + "\""
    otheruser = theguild.get_member_named(theusername)
    if otheruser is None:
        return "failure", "Couldn\'t find the user " + theusername
    existingrole = discord.utils.get(theguild.roles, name=fullchannelname)
    try:
        if addinguser==True:
            await otheruser.add_roles(existingrole,reason="added to private channel",atomic=True)
        else:
            await otheruser.remove_roles(existingrole,reason="removed from private channel",atomic=True)
    except BaseException as e:
        return "failure", str(e)
    return "success", theusername

'''
  discord.abc.Snowflake { .id,.created_at } # abstract, almost all Discord models are this
  discord.abc.GuildChannel { .name,.guild

  discord.Role {
  id=(int) id for this role, name=(str),mentionable=False
  coroutine .delete(*,reason=None) # deletes the role

  discord.Member() {
  .display_name
  coroutine .remove_roles(roles=[abc.Snowlake,*],reason="private channel",atomic=True)
  coroutine .add_roles(roles=[abc.Snowlake,*],reason="private channel",atomic=True) # raises Forbidden / HTTP

 overwritesdict = { (Member or Role) : PermissionOverwrite , * }
  discord.Guild() {
  .channels = [abc.GuildChannel, TextChannel, VoiceChannel, ...]
  .me # like Client.user
  .text_channels = [TextChannel,...]
  .default_role
  .get_member_named(name) # returns discord.Member
  coroutine create_text_channel(name=,overwrites=dict,reason=)

  discord.TextChannel { (discord.VoiceChannel)
  coroutine.delete(*,reason=None) # deletes the channel
  coroutine.set_permissions(target=discord.Role,read_messages=False,send_messages=False,reason=)
'''
