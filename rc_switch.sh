#!/bin/bash
DEV=/dev/elrostick
#echo cmd
echo "$@"
#fix arduino serial
stty -F "$DEV" cs8 9600  ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts
#start cat to read from serial line (required as arduino resets on each serial connection)
cat "$DEV" &
bgpid=$!
sleep 2
echo "$@" > "$DEV"
#kill cat(oh poor kitty)
kill $bgpid
