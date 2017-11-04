#!/usr/bin/env python3
# coding=utf-8

VERSION = "1.0"

print("PyCardMaker v%s"%(VERSION))
print("By Guillaume 'Elektordi' Genty")
print()

import logging
logging.basicConfig(level=logging.INFO)

try:
    from src import main
    main.main()
    
except (KeyboardInterrupt, SystemExit):
    pass
    
except Exception:
    logging.getLogger("pycardmaker").exception("Uncaught exception.")

