#!/usr/bin/env python3
# coding=utf-8

import sys
import os
import logging

from argparse import ArgumentParser

from . import projects
from . import config
from . import cards
from . import pdf

commandlist = {
    'help': 'This help.',
    'new': 'Create project and base files in it.',
    'build': 'Build project output images',
    'pdf': 'Build project output PDF',
    'safecheck': 'Build project output images with safe area check',
    'pdfsafecheck': 'Build project output PDF with safe area check',
    'check': 'Check project data without building',
    'config': 'Show all available config',
}

def argv_parse_check():

    basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    parser = ArgumentParser(description="Run specified command from the PyCardMaker engine.\n"
                            "Use command 'help' for list of available commands.")

    parser.add_argument("command", metavar="command", type=str, choices=sorted(commandlist), help="Command to run (or 'help' for commands list)")
    parser.add_argument("project", metavar="project", type=str, help="Project name", nargs='?')

    levelnames = ['critical', 'error', 'warning', 'info', 'debug']
    parser.add_argument("-l", dest='loglevel', type=str, default='info', choices=levelnames, help="Set log level")
    
    parser.add_argument("-c", dest='configdir', type=str, default=basedir+"/config", help="Set config directory")
    parser.add_argument("-o", dest='outdir', type=str, default=basedir+"/out", help="Set output directory")
    parser.add_argument("-p", dest='projdir', type=str, default=None, help="Set output directory")

    parser.add_argument("-d", dest='dedup', action='store_true', help="Deduplicate cards (only output one of each)")
    parser.add_argument("--nofront", dest='nofront', action='store_true', help="Do not build fronts")
    parser.add_argument("--noback", dest='noback', action='store_true', help="Do not build backs")

    options = parser.parse_args()

    if options.loglevel:
        options.loglevel = getattr(logging, options.loglevel.upper(), logging.INFO)
        
    if options.projdir is None and not options.project is None:
        options.projdir = basedir+"/projects/"+options.project

    return options


def main():
    options = argv_parse_check()
    if options.command == 'help':
        print("Available commands:")
        for c in sorted(commandlist):
            print("\t%s : %s"%(c, commandlist[c]))
        return

    config.ConfigManager.setConfigDir(options.configdir)

    if options.command == 'config':
        command_config(options)
        return
    
    if options.project is None:
        print("Command '%s' requires a project name. Use --help for more informations."%(options.command))
        return
    
    globals()["command_%s"%(options.command)](options)
    return

def command_config(options):
    list = config.ConfigManager.getGames()
    print("Games:")
    for i in sorted(list):
        print("\t%s : %s"%(i, list[i]))
    print()
    
    list = config.ConfigManager.getSizes()
    print("Sizes:")
    for i in sorted(list):
        print("\t%s : %s"%(i, list[i]))
    print()
            
def command_new(options):
    projects.ProjectsManager.new(options.project, options.projdir)

def command_build(options):
    p = projects.Project(options.project, options.projdir)
    cards.CardsManager.build(options.outdir, p, cards.MODE_EXT, options.dedup, options.nofront, options.noback)

def command_pdf(options):
    p = projects.Project(options.project, options.projdir)
    pdf.PdfManager.outPdf(options.outdir, p, cards.MODE_CUT)

def command_safecheck(options):
    p = projects.Project(options.project, options.projdir)
    cards.CardsManager.build(options.outdir, p, cards.MODE_SAFECHECK, options.dedup, options.nofront, options.noback)
    
def command_pdfsafecheck(options):
    p = projects.Project(options.project, options.projdir)
    pdf.PdfManager.outPdf(options.outdir, p, cards.MODE_SAFECHECK)

def command_check(options):
    p = projects.Project(options.project, options.projdir)
    p.check()



