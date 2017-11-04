#!/usr/bin/env python3
# coding=utf-8

import logging
log = logging.getLogger("pycardmaker")

from pathlib import Path
from configparser import ConfigParser

from . import imgtools


class ConfigManager:
    def setConfigDir(configdir):
        ConfigManager.configdir = configdir

    def getGames():
        return ConfigManager._getList(Game)
    
    def getSizes():
        return ConfigManager._getList(Size)
        
    def getGame(name):
        return ConfigManager._getOne(Game, name)
    
    def getSize(name):
        return ConfigManager._getOne(Size, name)
        
    def _getList(t):
        p = Path("%s/%s"%(ConfigManager.configdir, t.dirname()))
        list = [x for x in p.iterdir() if x.is_file() and x.suffix=='.txt']
        list = [t(x.stem, x.open()) for x in list]
        return dict([(x.code, x) for x in list])
        
    def _getOne(t, name):
        p = Path("%s/%s/%s.txt"%(ConfigManager.configdir, t.dirname(), name))
        if not p.is_file():
            return None
        return t(p.stem, p.open())
    
    
class Generic(object):
    def dirname():
        raise NotImplementedError();
        
    def __init__(self, code, configfile):
        self.code = code
        
        cp = ConfigParser()
        cp.read_file(configfile)
        try:
            if int(cp['pycardmaker']['v']) > 1:
                raise InvalidConfig("Invalid file %s: Unknow config version %s"%(configfile.name, cp['pycardmaker']['v']))
                
            cname = self.__class__.__name__
            if cp['pycardmaker']['type'] != cname:
                raise InvalidConfig("Invalid file %s: Invalid config type %s instead of %s"
                            %(configfile.name, cp['pycardmaker']['type'], cname))
                
            if not 'meta' in cp:
                raise InvalidConfig("Invalid file %s: Missing meta section"%(configfile.name))
                
            if not 'name' in cp['meta'] or not cp['meta']['name']:
                raise InvalidConfig("Invalid file %s: Missing meta name"%(configfile.name))
                
            self.config = cp
            
        except KeyError as e:
            raise InvalidConfig("Invalid file %s: %s"%(configfile.name, e))

    def __str__(self):
        if 'source' in self.config['meta']:
            return "%s (%s)"%(self.config['meta']['name'], self.config['meta']['source'])
        return self.config['meta']['name']
        
    def getName(self):
        return self.config['meta']['name']

    
class Game(Generic):
    def dirname():
        return 'games'     
        
    def getCards(self):
        # HACK
        return [str(x) for x in self.config['card_names']]
        
    def getBacks(self):
        # HACK
        return [str(x) for x in self.config['backs']]

class Size(Generic):
    def dirname():
        return 'sizes'
        
    def createPlaceholder(self, file):
        wh = self.config['size']['bleedsize'].split('x')
        i = imgtools.MyImage(wh[0], wh[1])
        i.save(file)
        

class InvalidConfig(Exception):
    pass
