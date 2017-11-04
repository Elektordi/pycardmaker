#!/usr/bin/env python3
# coding=utf-8

import logging
log = logging.getLogger("pycardmaker")

from pathlib import Path

from pgmagick import Image, DrawableCircle, DrawableText, Geometry, Color


class MyImage:
    def __init__(self, w, h):
        self.img = Image(Geometry(int(w), int(h)), 'transparent')
    
    def save(self, file):
        p = Path(file)
        if p.exists():
            return
        self.img.write(str(p))
    
