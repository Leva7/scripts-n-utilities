#!/usr/bin/python3
import argparse
import os
import shutil
from subprocess import run


bin_dir = '/usr/local/bin/'

try:
    from gi.repository import Gio
except ImportError:
    print('\033[31;1mWARNING\033[0m: GSettings not available')
    Gio = None


def strip_ext(filename: str) -> str:
    '''Strip the extension from a filename'''
    return filename[:filename.rfind('.')]


def set_keybinding(name: str, command: str, keys: str) -> str:
    '''Set a new keybinding'''
    schema = 'org.gnome.settings-daemon.plugins.media-keys'
    template = '/{}/custom-keybindings/custom'.format(schema.replace('.', '/'))

    gsettings = Gio.Settings.new(schema)
    keybindings = gsettings.get_strv('custom-keybindings')
    if keybindings:
        new_index = int(keybindings[-1][len(template):-1]) + 1
    else:
        new_index = 0

    keybindings.append(template + str(new_index) + '/')

    gsettings.set_strv('custom-keybindings', keybindings)
    gsettings.apply()

    key = Gio.Settings.new(
        '{}.custom-keybinding:{}{}/'.format(schema, template, new_index)
    )

    key.set_string('name', name)
    key.set_string('command', command)
    key.set_string('binding', keys)
    key.apply()


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
    run('crontab', input=crontab.format(os.getenv('PATH')).encode())


def install_toggle_alert():
    script = 'toggle-alert.sh'
    shutil.copy(script, bin_dir + strip_ext(script))
    if Gio is not None:
        set_keybinding('Toggle alert', 'toggle-alert', '<Primary>F11')


def install_toggle_touchpad():
    script = 'toggle-touchpad.sh'
    shutil.copy(script, bin_dir + strip_ext(script))
    if Gio is not None:
        set_keybinding('Toggle touchpad', 'toggle-touchpad', '<Primary>F12')


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
