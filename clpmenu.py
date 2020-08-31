# clpmenu.py



def gethelpmenu(message,commandchar):
    infomsg = ""
    if len(message.content)>5 and (message.content.startswith("!help") or message.content.startswith(commandchar+"help")):
        cutmsg = message.content[6:]
        if cutmsg.startswith("parse"):
            infomsg = "> **Yeah, this how I do the math**\n"
            infomsg+= "> I parse math expressions with only numbers and math ops\n"
            infomsg+= "> The result is infix notation. Supported math operations: + - * / %\n"
            infomsg+= "> Example: " + commandchar + "parse -4 + 5 + 5 * -1 - -4 / 5 % 2 + 20 * 4 - 5 * 8 + 2 - 10 % 6 - 4"
        elif cutmsg.startswith("solve"):
            infomsg = "> **Ah yes, I do math, of course I do**\n"
            infomsg+= "> I can solve math expressions with numbers and math ops\n"
            infomsg+= "> Supported math operations: + - * / %\n"
            infomsg+= "> Example: " + commandchar + "solve -4 + 5 + 5 * -1 - -4 / 5 % 2 + 20 * 4 - 5 * 8 + 2 - 10 % 6 - 4"
        elif cutmsg.startswith("make"):
            infomsg = "> **You don\'t like it here?**\n"
            infomsg+= "> I\'ll make a public or private channel for you\n"
            infomsg+= "> Usage: " + commandchar + "make [**public**/private] channel <name>\n"
            infomsg+= ">   For private rooms a new role is created with read/write access and the general role is disallowed this access\n"
            infomsg+= ">     Implicit **public** room: " + commandchar + "make channel pubchan\n"
            infomsg+= ">     Explicit **public** room: " + commandchar + "make public channel pubchan\n"
            infomsg+= ">     **Private** room: " + commandchar + "make private channel privchan\n"
            infomsg+= ">   You begin as the only user in the new group, manage other users with " + commandchar + "allow and " + commandchar + "revoke"
        elif cutmsg.startswith("delete"):
            infomsg = "> **We don\'t have time for that nonsense**\n"
            infomsg+= "> I can delete that channel you made with me\n"
            infomsg+= "> Example: " + commandchar + "delete channel MyUnnecessaryRoom"
        elif cutmsg.startswith("allow"):
            infomsg = "> **You could just have a private channel to yourself . . .**\n"
            infomsg+= "> You can allow other users to read and write in your private channels\n"
            infomsg+= "> Example: " + commandchar + "allow Hackler CoolKidsRoom"
        elif cutmsg.startswith("revoke"):
            infomsg = "> **Keep your secrets**\n"
            infomsg+= "> Remove a user\'s access to your private room\n"
            infomsg+= "> Example: " + commandchar + "revoke Hackler LameChatRoom"
    if infomsg=="":
        infomsg = "> **I say hello and tell jokes.**\n> \n"
        infomsg+= "> Commands: " + commandchar + "word [**default**/optional] <required>\n"
        infomsg+= ">   __math ops supported__  - + % / *\n"
        infomsg+= ">   " + commandchar + "parse <__math expr__>\n"
        infomsg+= ">   " + commandchar + "solve <__math expr__>\n"
        infomsg+= ">   " + commandchar + "make [**public**/private] channel <name>\n"
        infomsg+= ">   " + commandchar + "delete channel <name>\n"
        infomsg+= ">   " + commandchar + "allow <user> <your private channel>\n"
        infomsg+= ">   " + commandchar + "revoke <user> <your private channel>\n"
        infomsg+= ">   " + commandchar + "help [command]"
    return infomsg



