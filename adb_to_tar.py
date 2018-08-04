#!/usr/bin/env python2

#Converts Android Debug Bridge (ADB) backup file format to tar.gz file format.
#Author: Chris Mack (chris.mack@planetcrypto.com)
import sys
import shutil
import os
if len(sys.argv) != 2:
  print "Use: %s <path to adb backup>" % sys.argv[0]
  exit(1)

def progress(copied, to_copy):
  percent = int(float(copied)/float(to_copy)*100)
  percent = str(percent) + "%"
  sys.stdout.write("Converted %s bytes of %s bytes (%s)\r" % (copied, to_copy, percent))
  return 0

def write_file(fsrc, callback):
  tar_magic = "\x1f\x8b\x08\x00\x00\x00\x00\x00"
  to_copy = os.stat(fsrc.name).st_size
  out_name = sys.argv[1] + ".tar.gz"
  length = 16*1024
  copied = 0
  o = open(out_name, 'w')
  o.write(tar_magic)
  while True:
    buf = fsrc.read(length)
    if not buf:
      break
    o.write(buf)
    copied += len(buf)
    callback(copied, to_copy)

if __name__ == "__main__":

  f = open(sys.argv[1], 'rb')
  old_header = f.read(24)
  if "ANDROID BACKUP" not in old_header:
    print "%s is not ADB Backup, exiting now" % sys.argv[1]
    exit(1)
  write_file(f, progress)
  sys.stdout.write("\n")
  sys.stdout.flush()
  print "New file is %s.tar.gz" % sys.argv[1]
  exit(0)
