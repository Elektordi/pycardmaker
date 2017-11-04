#!/usr/bin/env python3
# coding=utf-8

import logging
log = logging.getLogger("pycardmaker")

from pathlib import Path
from configparser import ConfigParser

from . import config

class ProjectsManager:

    def new(name, directory, configdir):
        dir = Path(directory)
        if dir.is_dir():
            log.error("Directory %s already exists."%(directory))
            return
        
        list = config.ConfigManager.getGames(configdir)
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
        
        list = config.ConfigManager.getSizes(configdir)
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
        
        dir.mkdir()
        f = (dir/'project.ini').open('w')
        cp.write(f)
        f.close()
        
        p = Project(name, directory)
        p.generateMissingAssets()
        
        print()
        print("Project '%s' created at %s. Enjoy!"%(name, directory))
    
    
class Project:

    def __init__(self, name, directory):
        self.name = name
        self.directory = directory
        
    def generateMissingAssets(self):
        print("TODO GENERATE")

