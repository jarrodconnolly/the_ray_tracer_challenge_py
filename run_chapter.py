""" Helper to run putting together examples """
import importlib
import sys
from os.path import exists

if len(sys.argv) <= 1:
  print("Specifcy a chapter to run.")
  sys.exit(1)

CHAPTER_NUMBER = sys.argv[1]

if not exists(f"putting_together/chapter_{CHAPTER_NUMBER}.py"):
  print(f"Chapter {CHAPTER_NUMBER} does not exist")
  sys.exit(1)

library = importlib.import_module(f"putting_together.chapter_{CHAPTER_NUMBER}")
library.run()
