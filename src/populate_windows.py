#!/usr/bin/python
# -*- coding: utf-8 -*-

from dbcon import *
import json
from os import listdir
from os.path import isfile, join, basename

# VERBOSE FLAGS
VADD = False
VFND = True
VLST = False
VDPL = False

WINDOWS_DATA_FOLDER = "data/windows"

fs = [WINDOWS_DATA_FOLDER + "/" + f for f in listdir(WINDOWS_DATA_FOLDER) if isfile(join(WINDOWS_DATA_FOLDER, f))]

con = connect()
cur = con.cursor()

a, b = 0, 0

# For every file
for fpath in fs:
  print basename(fpath)
  f = open(fpath, "r")
  
  # Get the apps
  data = json.loads(f.read())
  f.close()
  print len(data)
  
  for x in data:
    c = x["category"].split("/")[0].strip()
    
    if c not in ct.windows:
      continue
    
    cat = ct.windows[c]
    p = x["price"].split(" ")[0].strip().replace(",", ".") if x["price"] != u"Δωρεάν" else None
    t = x["title"]
    
    # Add or retrieve the app
    if cur.execute("SELECT * FROM `app` WHERE `name` = %s", t) > 0:
      appID = cur.fetchone()[0]
      if VFND: print "[F] (%s): %s" % (appID, t)
      a += 1
    else:
      if VADD: print "Adding app:", t
      cur.execute("INSERT INTO `app` (`name`) VALUES (%s)", t)
      appID = con.insert_id()
      if VADD: print "Got ID:", appID
      b += 1
    
    # Add the listing (if necessary)
    if cur.execute("SELECT * FROM `listing` WHERE `app` = %s AND `platform` = 3", appID) > 0:
      if VDPL: print "[DPL] (%s): %s EXISTS IN %s" % (appID, t, ct.categories[cur.fetchone()[2]])
      continue
    
    if VLST: print "Add listing for app with ID:", appID, "category:", cat, "price:", p
    cur.execute("INSERT INTO `listing` (`app`, `platform`, `category`, `price`) VALUES (%s, 3, %s, %s)", (appID, cat, p))

con.commit()
cur.close()
con.close()

print a, b
