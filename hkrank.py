# chanmod.py

import discord
import time

def rankinghelpmenu(message,commandchar,author,managerankinggroup):
    isallowed=False
    for arole in author.roles:
        if arole.name==managerankinggroup:
            isallowed=True
            break
    infomsg = "> **Scoreboard system**\n"
    if isallowed==False:
        infomsg+= "> Usage: " + commandchar + "ranking\n"
        infomsg+= ">   Display scoreboard summary\n"
        return infomsg
    if message.startswith("ranking users"):
        infomsg+= "> *User options*\n"
        infomsg+= ">   Add a user:\n"
        infomsg+= ">   " + commandchar + "ranking adduser <name>\n"
        infomsg+= ">   Remove a user:\n"
        infomsg+= ">   " + commandchar + "ranking deluser <name>\n"
        return infomsg
    if message.startswith("ranking boards"):
        infomsg+= "> *Board options*\n"
        infomsg+= ">   Make a new leaderboard:\n"
        infomsg+= ">   " + commandchar + "ranking addboard <name> [opts]\n"
        infomsg+= ">   Delete a leaderboard:\n"
        infomsg+= ">   " + commandchar + "ranking delboard <name>\n"
        infomsg+= ">   Modify a board\'s attributes:\n"
        infomsg+= ">   " + commandchar + "ranking modboard <name>\n"
        return infomsg
    if message.startswith("ranking events"):
        infomsg+= "> *Event options*\n"
        infomsg+= ">   Make a new event:\n"
        infomsg+= ">   " + commandchar + "ranking addevent <name>\n"
        infomsg+= ">   Delete an event:\n"
        infomsg+= ">   " + commandchar + "ranking delevent <name>\n"
        infomsg+= ">   Modify an event\'s attributes:\n"
        infomsg+= ">   " + commandchar + "ranking modevent <name> [attribute=value], ...\n"
        return infomsg
    if message.startswith("ranking points"):
        infomsg+= "> *Scoring options*\n"
        infomsg+= ">   Delete an event:\n"
        infomsg+= ">   " + commandchar + "ranking delevent <name>\n"
        infomsg+= ">   Mark completion:\n"
        infomsg+= ">   " + commandchar + "ranking complete <eventname> <username>\n"
        infomsg+= ">   Modify user score:\n"
        infomsg+= ">   " + commandchar + "ranking setscore <eventname> <username> <value>\n"
        infomsg+= ">     *if the value is a number the user is assigned that value for the event*\n"
        infomsg+= ">     *the value can also be in the form +5 or -3 to do increment/decrement*\n"
        return infomsg
    infomsg+= "> Usage: " + commandchar + "ranking\n"
    infomsg+= ">   Display scoreboard summary\n"
    infomsg+= "> *Management options*\n"
    infomsg+= ">   More information:\n"
    infomsg+= ">   " + commandchar + "help ranking users\n"
    infomsg+= ">   " + commandchar + "help ranking boards\n"
    infomsg+= ">   " + commandchar + "help ranking events\n"
    infomsg+= ">   " + commandchar + "help ranking points\n"
    return infomsg

async def printranksummary(message):
    await message.channel.send("No summary yet")

# user validation happens before this call, user can manage ranking for the guild
async def rankingprocessor(message,trigger):
    request = message.content[len(trigger)+1:]
    # users, can add / remove
    if request.startswith('adduser '):
        await message.channel.send("No method yet")
    elif request.startswith('deluser '):
        await message.channel.send("No method yet")
    # boards, can add / remove / modify attributes
    elif request.startswith('addboard '):
        await message.channel.send("No method yet")
    elif request.startswith('delboard '):
        await message.channel.send("No method yet")
    elif request.startswith('modboard '):
        await message.channel.send("No method yet")
    ## merge boards?
    # events associate with boards and users can complete or get score from
    elif request.startswith('addevent '):
        await message.channel.send("No method yet")
    elif request.startswith('delevent '):
        await message.channel.send("No method yet")
    elif request.startswith('endevent '):
        await message.channel.send("No method yet")
    # a user's value associated with a board
    # setscore can assign value or do increment/decrement by operations
    elif request.startswith('setscore '):
        await message.channel.send("No method yet")
    # mark a user as having completed an activity
    elif request.startswith('complete '):
        await message.channel.send("No method yet")
    elif request.startswith('adduser '):
        await message.channel.send("No method yet")
    elif request.startswith('adduser '):
        await message.channel.send("No method yet")
    # detailed print functions
    elif request.startswith('print boards'):
        await message.channel.send("No method yet")
    elif request.startswith('print events'):
        await message.channel.send("No method yet")
    elif request.startswith('print users'):
        await message.channel.send("No method yet")
    else:
        await message.channel.send(f"{message.author.mention} get **!help**")

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
