#!/usr/bin/env python3
# coding=utf-8

import logging
log = logging.getLogger("pycardmaker")

from pathlib import Path
from pgmagick import Image, Geometry, Color, CompositeOperator, DrawableRoundRectangle

class MyImage:
    def __init__(self, w, h):
        self.img = Image(Geometry(int(w), int(h)), 'transparent')
    
    def save(self, file):
        p = Path(file)
        if p.exists():
            return
        self.img.write(str(p))
    
    def merge(self, file, modif=None):
        layer = Image(str(file))
        if modif:
            self.modif(layer, modif)
        self.img.composite(layer, 0, 0, CompositeOperator.OverCompositeOp)
        
    def drawRoundRect(self, w, h, color):
        x = int(self.img.size().width()/2)-int(w/2);
        y = int(self.img.size().height()/2)-int(h/2);
        r = DrawableRoundRectangle(x, y, x+w, y+h, 5, 5)
        self.img.strokeColor(color);
        self.img.fillColor('transparent');
        self.img.strokeWidth(5);
        self.img.draw(r)
        
    def modif(self, layer, modif):
        if modif=='mirror':
                layer.flip()
                layer.flop()
