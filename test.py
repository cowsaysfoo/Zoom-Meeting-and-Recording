#!/usr/bin/env python3
import sys

with open('args.txt', 'w') as f:
    f.write(' '.join(sys.argv))
