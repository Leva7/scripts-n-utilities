#!/usr/bin/python3
import argparse
import os
import shutil
from subprocess import run

bin_dir = '/usr/local/bin/'


def strip_ext(filename: str) -> str:
    '''Strip the extension from a filename'''
    return filename[:filename.rfind('.')]


def install_pip_upgrade():
    script = 'pip-upgrade.py'
    shutil.copy(script, bin_dir + strip_ext(script))


def install_take_break():
    script = 'take-break.py'
    take_break_assets = '/usr/local/share/take-break'

    shutil.copy(script, bin_dir + strip_ext(script))
    os.makedirs(take_break_assets, exist_ok=True)
    shutil.copy('assets/alert-image.jpg', take_break_assets)

    crontab = 'PATH={}\n\n*/20 * * * * DISPLAY=:0 take-break -a\n'
    run(['sudo', '-u', os.getlogin(), 'crontab'],
        input=crontab.format(os.getenv('PATH')).encode())


def install_toggle_alert():
    script = 'toggle-alert.sh'
    shutil.copy(script, bin_dir + strip_ext(script))
    print('Set a keybinding: Ctrl+F11 -> toggle-alert')


def install_toggle_touchpad():
    script = 'toggle-touchpad.sh'
    shutil.copy(script, bin_dir + strip_ext(script))
    print('Set a keybinding: Ctrl+F12 -> toggle-touchpad')


parser = argparse.ArgumentParser(description='Install the scripts')
parser.add_argument('-i', '--install',
                    help='list of scripts to install '
                         '(leave empty to install everything)',
                    choices=['pip-upgrade', 'take-break',
                             'toggle-alert', 'toggle-touchpad'],
                    nargs='+')

name_to_installer = {'pip-upgrade': install_pip_upgrade,
                     'take-break': install_take_break,
                     'toggle-alert': install_toggle_alert,
                     'toggle-touchpad': install_toggle_touchpad}

args = parser.parse_args()

for script in (args.install or name_to_installer):
    name_to_installer[script]()
