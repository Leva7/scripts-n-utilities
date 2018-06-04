#!/bin/bash

read TPdevice <<< $( xinput | sed -nre '/Touchpad/s/.*id=([0-9]*).*/\1/p' )
state=$( xinput list-props "$TPdevice" | grep "Device Enabled" | grep -o "[01]$" )
icon="/usr/share/icons/Numix-Circle/48/apps/touchpad-indicator.svg"

if [ "$state" -eq '1' ];then
    xinput disable "$TPdevice"
    notify-send "Touchpad disabled" "Press Ctrl+F12 to reenable" -i "$icon"
else
    xinput enable "$TPdevice"
    notify-send "Touchpad enabled" "Press Ctrl+F12 to disable" -i "$icon"
fi
