# Musical Keyboard

Use your computer's keyboard like a piano!
Just run this python3 script and press some keys of your keyboard to try it out.

You can also use it to play files, like this:

    cat samples/jingle.txt | ./music_kbd.py -q -t 0.2

### Advanced usage

Run `./music_kbd.py --help` to see the command-line arguments accepted by this program.

You can also pipe output of a program into this script and it will play it.
You can either control the timing yourself by flushing output at exactly the right times,
or you can dump all output together and the script will play characters one-by-one
if you pass it the `-q` switch.

You can control the duration for which a character is played by using the `-t` flag.
By default, underscores, uppercase characters and other characters which require the shift key to be typed
will be played for twice the duration. You can switch this behavior off by using the `--no-double-upper` flag.

### Map file

A map file is used to specify what frequency each key maps to.
By default `default_map.json` is used.
You can specify a custom map file by using the `-m` or `--mapfile` command-line argument.

The mapfile is a dictionary where keys are strings and values are frequencies.
All characters in a key will be mapped to the corresponding frequency.
Characters mapped to `null` will not be played, but will take up time when using the `-q` mode.
Characters which have not been mapped to anything will not be played and will not take up time in `-q` mode.

### How it works

This python 3 script uses ALSA's `speaker-test` to produce sound.
`speaker-test` comes pre-installed in Ubuntu 16.04.

`speaker-test` plays sound for either a very long time or indefinately.
Therefore, I kill it after waiting for the desired time.
This leads to bad sound quality (a tick sound at the end of keypress).

If you know of a better way to play sound, feel free to contribute!
