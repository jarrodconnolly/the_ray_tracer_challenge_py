""" Helper to run putting together examples """
import importlib
import sys
import time
from os.path import exists

# import pyroscope

# pyroscope.configure(
#   application_name = "RT",
#   server_address   = "http://localhost:4040",
# )

if len(sys.argv) <= 1:
  print("Specifcy a chapter to run.")
  sys.exit(1)

CHAPTER_NUMBER = sys.argv[1]

if not exists(f"putting_together/chapter_{CHAPTER_NUMBER}.py"):
  print(f"Chapter {CHAPTER_NUMBER} does not exist")
  sys.exit(1)

start_time = time.process_time_ns()
library = importlib.import_module(f"putting_together.chapter_{CHAPTER_NUMBER}")
library.run()
time_ns = time.process_time_ns() - start_time
print(f"Time: {time_ns // 1000000}ms.")
