#!/bin/bash

enabled="\(.*take-break -a\)"
disabled="#$enabled"
icon="/usr/share/icons/Numix-Circle/48/apps/userinfo.svg"

if crontab -l | grep -q "$disabled"; then
   crontab -l | sed "s/$disabled/\1/" | crontab
   notify-send "Alert enabled" "Press Ctrl+F11 to disable" -i "$icon"
else
   crontab -l | sed "s/$enabled/#\1/" | crontab
   notify-send "Alert disabled" "Press Ctrl+F11 to enable" -i "$icon"
fi
