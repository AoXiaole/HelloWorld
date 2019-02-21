#!/usr/bin/python3

import sys

from pyquery import PyQuery as pq

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("failed! param : [url]")
    url = sys.argv[1]
    doc = pq(url)
    title_targ = doc("#download_top").find("h3")
    print('success:',title_targ.text())

