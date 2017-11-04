#!/usr/bin/env python3
# coding=utf-8

from pathlib import Path
import shutil

from . import imgtools

MODE_EXT = 1
MODE_CUT = 2
MODE_SAFECHECK = 3

class CardsManager:

    def getTypesFromProject(p):
        a = []
        cp = p.merged
        for tref in cp['types']:
            t = Type(p, tref, cp['types'][tref])
            a.append(t)
        return a

    def getCardsFromProject(p):
        a = []
        cp = p.merged
        for tref in cp['types']:
            t = Type(p, tref)
            for cref in cp['type_%s'%(tref)]:
                c = Card(p, t, cref)
                a.append(c)
        return a

    def build(dir, p, mode, dedup):
        path = Path(dir)/p.name/'cards'
        if path.exists():
            print('Deleting existing out dir: %s'%(path))
            shutil.rmtree(str(path))
        path.mkdir()
        
        cards = CardsManager.getCardsFromProject(p)
        n = 0
        for c in cards:
            fi = p.size.newImage()
            bi = p.size.newImage()
            c.paintFront(fi)
            c.paintBack(bi)
            if dedup:
                fi.save(path/('%s-%s-F-x%d.png'%(c.type.ref, c.ref, c.count)))
                bi.save(path/('%s-%s-B-x%d.png'%(c.type.ref, c.ref, c.count)))
                n+=1
            else:
                for num in range(c.count):
                    fi.save(path/('%s-%s-%02dF.png'%(c.type.ref, c.ref, num+1)))
                    bi.save(path/('%s-%s-%02dB.png'%(c.type.ref, c.ref, num+1)))
                    n+=1
                    
        print("Done! %d cards generated to: %s"%(n, path))

class Card:
    
    def __init__(self, project, type, ref):
        self.project = project
        self.type = type
        self.ref = ref
        self.name = project.merged['card_names'][ref]
        self.count = int(project.merged['type_%s'%(type.ref)][ref])
        
    def paintFront(self, i):
        return self.paint(i, 'front')
        
    def paintBack(self, i):
        return self.paint(i, 'back')
        
    def paint(self, i, side):
        cat = 'layers_%s'%(side)
        list = [x for x in self.project.config[cat]]
        list.sort(key=int)
        for id in list:
            l = self.project.config[cat][id]
            l = l.format(card=self.ref, type=self.type.ref, back=self.type.back)
            i.merge(self.project.dir/l)
    
class Type:

    def __init__(self, project, ref):
        self.project = project
        self.ref = ref
        self.name = project.merged['types'][ref]
        if ref in project.merged['backs']:
            self.back = project.merged['types_back'][ref]
        else:
            self.back = project.merged['types_back']['*']
