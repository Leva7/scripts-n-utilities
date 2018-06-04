#!/bin/bash

job_config="$HOME/.gnome/gnome-schedule/crontab/1"
disabled="command_d=#"
enabled="command_d="
icon="/usr/share/icons/Numix-Circle/48/apps/userinfo.svg"

if grep -qF "$disabled" "$job_config"; then
   sed -i "s/$disabled/$enabled/g" "$job_config"
   notify-send "Alert enabled" "Press Ctrl+F11 to disable" -i "$icon"
else
   sed -i "s/$enabled/$disabled/g" "$job_config"
   notify-send "Alert disabled" "Press Ctrl+F11 to enable" -i "$icon"
fi
