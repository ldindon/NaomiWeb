#!/usr/bin/env python

import sys
from time import sleep

def main():
    if len(sys.argv) != 2:
        return -1 # invalid arguments: python3 test.py game_size
    game_size = int(sys.argv[1])
    size = 0
    while size < game_size:
        sys.stderr.write("%08x\r" % size)
        size += int(game_size / 100)
        sleep(0.1)

if __name__ == "__main__":
    main()
