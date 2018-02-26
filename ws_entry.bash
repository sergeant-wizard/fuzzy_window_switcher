#!/bin/bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
CURRENT_WID=$(xprop -root _NET_ACTIVE_WINDOW | cut -d" " -f5)
USER_TEXT=$(zenity --entry --title='window selector' --text='win')
[[ !  -z  $USER_TEXT  ]] && echo $CURRENT_WID $USER_TEXT | $SCRIPTPATH/ws.py
