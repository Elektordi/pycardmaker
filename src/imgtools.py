#!/usr/bin/env python3
# coding=utf-8

import logging
log = logging.getLogger("pycardmaker")

from pathlib import Path

from pgmagick import Image, Geometry, Color, CompositeOperator

class MyImage:
    def __init__(self, w, h):
        self.img = Image(Geometry(int(w), int(h)), 'transparent')
    
    def save(self, file):
        p = Path(file)
        if p.exists():
            return
        self.img.write(str(p))
    
    def merge(self, file):
        layer = Image(str(file))
        self.img.composite(layer, 0, 0, CompositeOperator.OverCompositeOp)
