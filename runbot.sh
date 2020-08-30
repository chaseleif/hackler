#!/bin/sh

nohup python3 hackler.py >> botout &

pidof python3 >> bot.pid
echo "launched the bot"
ls
