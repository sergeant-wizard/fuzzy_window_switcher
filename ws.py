#!/usr/bin/env python3

import subprocess
from fuzzywuzzy import process


def call_sh(cmd):
    return subprocess.check_output(['/bin/bash', '-c', cmd]).decode("utf-8")


def is_normal_window(wid):
    w_type = call_sh("xprop -id " + wid)
    return " _NET_WM_WINDOW_TYPE_NORMAL" in w_type


def str_to_hex(string):
    return int(string, 16)


def is_active_window(wid):
    active_id = call_sh("xprop -root _NET_ACTIVE_WINDOW").rsplit(maxsplit=1)[1]
    return str_to_hex(wid) == str_to_hex(active_id)


class WindowSelector(object):
    def __init__(self):
        keys = ['wid', 'desktop', 'app', 'win']
        window_list = [
            dict(zip(keys, wl.split(maxsplit=3)))
            for wl in call_sh('wmctrl -lx').split('\n')[:-1]
        ]

        # filter out windows that are active or aren't normal
        window_list = [
            wl for wl in window_list
            if is_normal_window(wl['wid']) and not is_active_window(wl['wid'])]
        # remove hostname from win
        for wl in window_list:
            wl.update(win=wl['win'].split(maxsplit=1)[1])

        self.text_wid_pair = [
            {
                'text': wl['win'] + ' ' + wl['app'],
                'wid': wl['wid']
            } for wl in window_list
        ]

    def get_best_wid(self, user_input):
        match, _ = process.extractOne(
            user_input,
            [wl['text'] for wl in self.text_wid_pair])
        return next(
            twp['wid'] for twp in self.text_wid_pair
            if twp['text'] == match)


if __name__ == '__main__':
    ws = WindowSelector()

    user_input = call_sh("""
    zenity --entry --title='window selector' --text=win
    """)

    wid = ws.get_best_wid(user_input)
    call_sh('wmctrl -ia ' + wid)
