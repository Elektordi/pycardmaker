#!/usr/bin/env python3
# coding=utf-8

import logging
log = logging.getLogger("pycardmaker")

from pathlib import Path
from configparser import ConfigParser
from io import StringIO

from . import config

class ProjectsManager:

    def new(name, directory):
        dir = Path(directory)
        if dir.is_dir():
            log.error("Directory %s already exists."%(directory))
            return
        
        list = config.ConfigManager.getGames()
        print("Please choose a base game:")
        for i in sorted(list):
            print("\t'%s' : %s"%(i, list[i]))
        print()
        ref = input("Enter base game code: ")
        if not ref in list:
            print("Invalid game code: '%s'"%(ref))
            return
        game = list[ref]
        print()
        
        list = config.ConfigManager.getSizes()
        print("Please choose a card size:")
        for i in sorted(list):
            print("\t'%s' : %s"%(i, list[i]))
        print()
        ref = input("Enter size code: ")
        if not ref in list:
            print("Invalid size code: '%s'"%(ref))
            return
        size = list[ref]
        print()
        
        cp = ConfigParser()
        cp['pycardmaker'] = {'v':1, 'type':'Project'}
        cp['meta'] = {'name':"%s - %s edition"%(game.getName(), name)}
        cp['base'] = {'game':game.code, 'size':size.code}
        cp['layers_front'] = {2:'overlay.png', 1:'cards/{card}.png', 0:'background.png'}
        cp['layers_back'] = {1:'back_{back}.png', 0:'back.png'}
        
        dir.mkdir()
        f = (dir/'project.txt').open('w')
        cp.write(f)
        f.close()
        
        emptyimg = size.newImage()
        
        for f in ['overlay', 'background', 'back']:
            emptyimg.save(dir/("%s.png"%(f)))
        
        for f in game.getBacks():
            emptyimg.save(dir/("back_%s.png"%(f)))
        
        cards = dir/'cards'
        cards.mkdir()
        
        for f in game.getCards():
            emptyimg.save(cards/("%s.png"%(f)))
        
        print()
        print("Project '%s' created at '%s'. Enjoy!"%(name, directory))
    
    
class Project:

    def __init__(self, name, directory, game=None, size=None):
        self.name = name
        self.dir = Path(directory)
        self.game = game
        self.size = size
        
        if not self.dir.is_dir():
            raise InvalidProject("No project at directory %s"%(self.dir));
            
        configfile = self.dir/'project.txt'
        if not configfile.is_file():
            raise InvalidProject("No project config at %s"%(configfile));

        cp = ConfigParser()
        
        try:
            cp.read_file(configfile.open())
            
            if int(cp['pycardmaker']['v']) > 1:
                raise InvalidProject("Invalid project %s: Unknow config version %s"%(name, cp['pycardmaker']['v']))
            
            if cp['pycardmaker']['type'] != 'Project':
                raise InvalidProject("Invalid project %s: Invalid config type %s for project"
                            %(name, cp['pycardmaker']['type']))
                
            if not 'meta' in cp:
                raise InvalidProject("Invalid project %s: Missing meta section"%(name))
                
            if not 'name' in cp['meta'] or not cp['meta']['name']:
                raise InvalidProject("Invalid project %s: Missing meta name"%(name))        
        
            if self.game is None:
                self.game = config.ConfigManager.getGame(cp['base']['game'])
                if self.game is None:
                    raise MissingRessourceException("Missing game %s"%(cp['base']['game']));
                    
            if self.size is None:
                self.size = config.ConfigManager.getSize(cp['base']['size'])
                if self.size is None:
                    raise MissingRessourceException("Missing size %s"%(cp['base']['size']));
                    
            self.config = cp
            
                        
        except KeyError as e:
            raise InvalidProject("Invalid file %s: %s"%(name, e))
        
    def check(self):
        print("TODO CHECK")
        
    def getMergedGameConf(self):
        cp = ConfigParser()
        for c in [self.game.config, self.config]:
            io = StringIO()
            c.write(io)
            io.seek(0)
            cp.read_file(io)
            io.close()
        return cp



class InvalidProject(Exception):
    pass
    
class MissingRessourceException(Exception):
    pass
