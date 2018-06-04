# Scripts 'n' Utilities

This repository contains my scripts, previously residing in Gists.

## Installation

Clone this repository and execute:

```bash
$ ./configure.py
```

You can also install only specific scripts by listing their names with `-i` option:

```bash
$ ./configure.py -i pip-upgrade take-break
```

The script names are available in the overview or by using the `-h` option.

## Overview

* `pip-upgrade` - upgrades all available Python packages
* `take-break` - reminds you to take a break every 20 minutes
* `toggle-alert` - allows toggling `take-break` through the command line or a keybinding (Ctrl+F11)
* `toggle-touchpad` - allows toggling the touchpad through the command line or a keybinding (Ctrl+F12)

## System requirements

These scripts are built for Ubuntu but will work on other Linux flavors.

The limitations:  
* Automatically setting keybindings is only available if GSettings is present (GNOME-based DEs)

## Credits

`assets/alert-image.jpg` is a photo by Daniil Kuželev on [Unsplash](https://unsplash.com/photos/KaVPZvzlLhs).

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](https://github.com/Leva7/scripts-n-utilities/blob/master/LICENSE) file for details.
