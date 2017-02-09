#!/usr/bin/env python3

import sys
import os
import json
import time
import subprocess
import argparse
from threading import Thread

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_KEY_TIME = 0.3
DEFAULT_KEYMAP_FILE = os.path.join(BASE_DIR, "map2.json")

class Console(object):

    @staticmethod
    def init():
        Console.isatty = sys.stdin.isatty()
        if not Console.isatty:
            Console.getch = lambda: sys.stdin.read(1)
        else:
            try:
                import termios
                Console.is_unix = True
                Console.getch = lambda: sys.stdin.read(1)
                # Disable buffering
                Console.fd = sys.stdin.fileno()
                Console.oldattr = termios.tcgetattr(Console.fd)
                newattr = termios.tcgetattr(Console.fd)
                newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
                termios.tcsetattr(Console.fd, termios.TCSANOW, newattr)
            except ImportError:
                Console.is_unix = False
                import msvcrt
                if sys.version_info.major == 2:
                    Console.getch = msvcrt.getch
                else:
                    Console.getch = lambda: msvcrt.getch().decode('utf-8')

    @staticmethod
    def reset():
        if Console.isatty and Console.is_unix:
            import termios
            termios.tcsetattr(Console.fd, termios.TCSANOW, Console.oldattr)

def print_char(ch):
    if ch == '\x7f':
        ch = '\b \b'
    elif ch in ('', '\x04'):
        raise EOFError
    print(ch, end='', flush=True)

def make_keymap(mapfile):
    mydict = json.load(open(mapfile))
    keymap = {}
    for k, v in mydict.items():
        for ch in k:
            keymap[ch] = v
    return keymap

def play_sound(freq, time):
    proc = subprocess.Popen(['speaker-test', '--frequency', str(freq), '--test', 'sine'],
                            stdout=subprocess.DEVNULL)
    try:
        proc.wait(timeout=time)
    except subprocess.TimeoutExpired:
        pass
    finally:
        proc.kill()

def play_char(ch, keymap, key_time, queue):
    try:
        freq = keymap[ch]
    except KeyError:
        return
    if queue:
        if freq is None:
            time.sleep(key_time)
        else:
            play_sound(freq, key_time)
    elif freq is not None:
        Thread(target=(lambda: play_sound(freq, key_time))).start()

def main():
    parser = argparse.ArgumentParser(description="Play piano using your computer's keyboard")
    parser.add_argument('-m', '--mapfile',
        help='Path to file mapping keyboard keys to frequencies')
    parser.add_argument('-t', '--key-time', type=float, default=DEFAULT_KEY_TIME,
        help='Time for which a key will stay pressed')
    parser.add_argument('-q', '--queue', action='store_true', default=False,
        help='Queue multiple keys instead of playing simultaneously')
    args = parser.parse_args()
    keymap = make_keymap(args.mapfile or DEFAULT_KEYMAP_FILE)

    Console.init()
    try:
        while(True):
            ch = Console.getch()
            print_char(ch)
            play_char(ch, keymap, args.key_time, args.queue)
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        Console.reset()

if __name__ == '__main__':
    main()
