#!/usr/bin/python3
import argparse
import logging
import os
import sys
from subprocess import run, PIPE


class ColorFormatter(logging.Formatter):
    rest = ';1m[{levelname}]\033[0m {message}'

    def __init__(self):
        super().__init__(style='{')

    def format(self, record):
        if record.levelno > logging.INFO:
            self._style._fmt = '\033[31' + self.rest
        else:
            self._style._fmt = '\033[36' + self.rest
        return super().format(record)

    @staticmethod
    def bullet_list(items):
        return '\033[31;1m*\033[0m ' + '\n\033[31;1m*\033[0m '.join(items)


class SilenceableLogger(logging.Logger):
    def __init__(self, name, quiet=False, **kwargs):
        super().__init__(name, **kwargs)
        self.disabled = quiet

    def print(self, message):
        if not self.disabled:
            print(message)


parser = argparse.ArgumentParser(description='Upgrade all Python 3 packages at once')
parser.add_argument('-i', '--ignore',
                    help='list of packages to ignore',
                    nargs='+')
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose',
                   help='output the stdout and stderr of pip',
                   action='store_true')
group.add_argument('-q', '--quiet',
                   help='surpress the output of the script completely',
                   action='store_true')
parser.add_argument('-l', '--list-packages',
                    help='only list the outdated packages, do not upgrade',
                    action='store_true')
parser.add_argument('-I', '--ignore-forever',
                    help='write the ignored packages to $HOME/.config/'
                         'pip-upgrade/ignored to ignore them implicitly '
                         'in the future',
                    action='store_true')

args = parser.parse_args()

log = SilenceableLogger('pip-upgrade', quiet=args.quiet)

log_handler = logging.StreamHandler()
log_handler.setFormatter(ColorFormatter())
log.addHandler(log_handler)

current_user = os.getlogin()
ignored_filename = '/home/{}/.config/pip-upgrade/ignored'.format(current_user)
if os.path.exists(ignored_filename):
    with open(ignored_filename) as ignored:
        forever_ignored = set(ignored.read().splitlines())
else:
    os.makedirs(ignored_filename[:ignored_filename.rfind('/')], exist_ok=True)
    forever_ignored = set()

log.info('Listing outdated packages...')
list_outdated = run(['sudo', 'pip', 'list', '-o'], stdout=PIPE, stderr=PIPE)

try:
    columns, *packages_raw = list_outdated.stdout.decode().splitlines()[1:]
    type_length = len(columns.split()[3])
    currently_ignored = set() if args.ignore is None else set(args.ignore)
except ValueError:
    # if the stdout is empty, the unpacking will fail
    packages_raw = []

packages_parsed = []
packages_strings = []
for package_string in packages_raw:
    package = package_string.split()[0]
    if package in currently_ignored or package in forever_ignored:
        continue

    packages_parsed.append(package)
    packages_strings.append(package_string[:-type_length])

if not packages_parsed:
    log.info('All packages are up to date')
else:
    log.info('Packages to upgrade:')
    log.print(ColorFormatter.bullet_list(packages_strings))

    if args.list_packages:
        sys.exit(0)

    upgrader = run(['sudo', 'pip3', 'install', '--upgrade', *packages_parsed],
                   stdout=PIPE,
                   stderr=PIPE)

    if args.verbose:
        print('\n\033[31;1mSTDOUT:\033[0m')
        print(upgrader.stdout.decode())
        print('\033[31;1mSTDERR:\033[0m')
        print(upgrader.stderr.decode())

    if upgrader.returncode != 0:
        log.error('An error occured during the upgrade')
        if not args.verbose:
            log.print('\033[31;1mSTDERR:\033[0m')
            log.print(upgrader.stderr.decode())
        sys.exit(1)
    else:
        log.info('Done upgrading!')

if args.ignore_forever:
    with open(ignored_filename, 'w') as ignored:
        ignored.write('\n'.join(forever_ignored.union(currently_ignored)))
