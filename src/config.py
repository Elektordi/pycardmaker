#!/usr/bin/env python3
# coding=utf-8

import logging
log = logging.getLogger("pycardmaker")

from pathlib import Path
from configparser import ConfigParser


class ConfigManager:
    def getGames(configdir):
        return ConfigManager._getList(configdir, Game)
    
    def getSizes(configdir):
        return ConfigManager._getList(configdir, Size)
        
    def getGame(configdir, name):
        return ConfigManager._getOne(configdir, Game, name)
    
    def getSize(configdir, name):
        return ConfigManager._getOne(configdir, Size, name)
        
    def _getList(configdir, t):
        p = Path("%s/%s"%(configdir, t.dirname()))
        list = [x for x in p.iterdir() if x.is_file() and x.suffix=='.txt']
        list = [t(x.stem, x.open()) for x in list]
        return dict([(x.code, x) for x in list])
        
    def _getOne(configdir, t, name):
        return [name]
    
    
class Generic(object):
    def dirname():
        raise NotImplementedError();
        
    def __init__(self, code, configfile):
        self.code = code
        
        cp = ConfigParser()
        cp.read_file(configfile)
        try:
            if int(cp['pycardmaker']['v']) > 1:
                log.error("Invalid file %s: Unknow config version %s"%(configfile.name, cp['pycardmaker']['v']))
                return
                
            cname = self.__class__.__name__
            if cp['pycardmaker']['type'] != cname:
                log.error("Invalid file %s: Invalid config type %s instead of %s"
                            %(configfile.name, cp['pycardmaker']['type'], cname))
                return
                
            if not 'meta' in cp:
                log.error("Invalid file %s: Missing meta section"%(configfile.name))
                return
                
            if not 'name' in cp['meta'] or not cp['meta']['name']:
                log.error("Invalid file %s: Missing meta name"%(configfile.name))
                return
                
            self.config = cp
            
        except KeyError as e:
            log.error("Invalid file %s: %s"%(configfile.name, e))
            return

    def __str__(self):
        if 'source' in self.config['meta']:
            return "%s (%s)"%(self.config['meta']['name'], self.config['meta']['source'])
        return self.config['meta']['name']
        
    def getName(self):
        return self.config['meta']['name']

    
class Game(Generic):
    def dirname():
        return 'games'          

class Size(Generic):
    def dirname():
        return 'sizes'
        

        
