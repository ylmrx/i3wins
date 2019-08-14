# i3wins

As the name might suggest, this is a wrapper to rofi acting as a window-switcher.

I found `-show window` option to be quite slow, and would often get in the way. On another topic, I use i3 in an XFCE environment (for the PM and such)… and the virtual desktops would conflicts, and be generally weird.

i3wins is fast and won't get in the way.

# Pre-requisites

- i3
- rofi
- a working python3 environment can help
- libi3ipc (`libi3ipc-glib` on ubuntu/debian)

# Installation

I recommand using some virtual environments.

```bash
python3 -m venv new_folder
source new_folder/bin/activate
pip install i3wins
deactivate
```

If you're a more yolo-oriented person : `pip install --user i3wins`

You can now run : `new_folder/bin/i3wins`

# Help !

No help. All options you give to i3wins are directly sent to rofi. 

Check rofi manpage.

# Settings

Here's a snippet from my i3 config:

```
bindsym Mod1+space exec "/home/fuzzy/.local/share/virtualenvs/i3switch/bin/i3wins -kb-row-down 'Down,Control+n,Alt+space,space' -kb-accept-entry '!Alt+space,!Alt_L,!Alt+Alt_L,Return'"
bindsym Mod1+Tab exec "/home/fuzzy/.local/share/virtualenvs/i3switch/bin/i3wins -kb-row-down 'Down,Control+n,Alt+Tab' -kb-accept-entry '!Alt+Tab,!Alt_L,!Alt+Alt_L,Return'"
```

Feel free to use it as-is. Or modify it into oblivion.

# Some explanation on the i3 config

Long story made short :
- Faster mode : Hold Alt, then press Tab as many times as needed, when you're where you want : release Tab *then* Alt.
- Not so fast : Hold Alt, then press Tab and release Alt while still holding Tab : the window will stay there, you can search text, scroll, validate with a single press on Alt, or the good'ol Enter key

You'll get used to it.

# More swag

## Keys

Have you noticed desktops are displayed with d1, d2, d3, … And that windows are numbered in the relevant order with 'w' ?

Have you noticed how close d and w are close to the tab key ?

… just saying.

## Eyes

- Current desk is pink
- Current window is yellow
- I think you're cool
- Have a mojito.

Colors are hardcoded and were set by yours truly for ecstatic co-workers' high-fives and maximum swaginess in every situation. But they're still designed for darker themes of rofi.

# Todo

Handles URGENCY, Fullscreen, vim-marks and more i3-specific concepts (tree depth for examples).

