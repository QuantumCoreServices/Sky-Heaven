#! /usr/bin/env /usr/bin/python3

import sys
import os.path

if len(sys.argv) < 2:
    sys.stderr.write("Usage: realpath path\n")
    exit(2)

sys.stdout.write(os.path.realpath(sys.argv[1]) + "\n")
