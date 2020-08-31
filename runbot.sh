#!/bin/sh

nohup python3 hackler.py >> botout &

echo $! >> bot.pid
echo "launched the bot"
ls
