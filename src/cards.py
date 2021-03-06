#!/usr/bin/env python3
# coding=utf-8

from pathlib import Path
import shutil

from . import imgtools

MODE_EXT = 1 # Full extend
MODE_CUT = 2 # White outside cut zone
MODE_SAFECHECK = 3 # Full with lines for cut (black) and safe (red)

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

    def build(dir, p, mode, dedup, nofront, noback):
        path = Path(dir)/p.name/'cards'
        if path.exists():
            print('Deleting existing out dir: %s'%(path))
            shutil.rmtree(str(path))
        path.mkdir(0o777, True)
        
        print("Generating cards...")
        cards = CardsManager.getCardsFromProject(p)
        n = 0
        for c in cards:           
            fi = p.size.newImage()
            bi = p.size.newImage()
            c.paintFront(fi)
            c.paintBack(bi)
            c.applyMode(fi, mode)
            c.applyMode(bi, mode)
            if dedup:
                if not nofront:
                    fi.save(path/('%s-%s-F-x%d.png'%(c.type.ref, c.ref, c.count)))
                if not noback:
                    bi.save(path/('%s-%s-B-x%d.png'%(c.type.ref, c.ref, c.count)))
                n+=1
            else:
                for num in range(c.count):
                    if not nofront:                
                        fi.save(path/('%03d-%s-%s-%02dF.png'%(n, c.type.ref, c.ref, num+1)))
                    if not noback:
                        bi.save(path/('%03d-%s-%s-%02dB.png'%(n, c.type.ref, c.ref, num+1)))
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
            modif = None
            if '|' in l:
                (l, modif) = l.split('|')
            i.merge(self.project.dir/l, modif)
            
    def applyMode(self, i, mode):
        if mode==MODE_EXT:
            pass
            
        elif mode==MODE_CUT:
            # TODO
            cut = self.project.size.getCutWH()
            i.drawRoundRect(cut[0], cut[1], 'black')
            pass
            
        elif mode==MODE_SAFECHECK:
            cut = self.project.size.getCutWH()
            i.drawRoundRect(cut[0], cut[1], 'black')
            safe = self.project.size.getSafeWH()
            i.drawRoundRect(safe[0], safe[1], 'red')

        else:
            raise AttributeError('Invalid card mode %r'%(mode))
    
class Type:

    def __init__(self, project, ref):
        self.project = project
        self.ref = ref
        self.name = project.merged['types'][ref]
        if ref in project.merged['backs']:
            self.back = project.merged['types_back'][ref]
        else:
            self.back = project.merged['types_back']['*']
