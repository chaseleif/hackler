#!/bin/bash
INPUT=./bot.pid

[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 0; }

while read line
	do
		kill -9 $line
done < $INPUT

echo "kill bots"
