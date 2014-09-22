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

ANDROID_DATA_FOLDER = "data/android"

fs = [ANDROID_DATA_FOLDER + "/" + f for f in listdir(ANDROID_DATA_FOLDER) if isfile(join(ANDROID_DATA_FOLDER, f))]

con = connect()
cur = con.cursor()

# For every file (category)
for fpath in fs:
  fname = basename(fpath).split(".")[0]
  print fname
  
  # Get the apps
  f = open(fpath, "r")
  data = json.loads(f.read())
  cat = ct.android[fname]
  
  # For each app
  for x in data:
    t = x["title"]
    p = x["price"] if x["price"] != "FREE" else None
    
    # Add or retrieve the app
    if cur.execute("SELECT * FROM `app` WHERE `name` = %s", t) > 0:
      appID = cur.fetchone()[0]
      if VFND: print "[F] (%s): %s" % (appID, t)
    else:
      if VADD: print "Adding app:", t
      cur.execute("INSERT INTO `app` (`name`) VALUES (%s)", t)
      appID = con.insert_id()
      if VADD: print "Got ID:", appID
    
    # Add the listing (if necessary)
    if cur.execute("SELECT * FROM `listing` WHERE `app` = %s AND `platform` = 1", appID) > 0:
      if VDPL: print "[DPL] (%s): %s EXISTS IN %s" % (appID, t, ct.categories[cur.fetchone()[2]])
      continue
    
    if VLST: print "Add listing for app with ID:", appID, "category:", cat, "price:", p
    cur.execute("INSERT INTO `listing` (`app`, `platform`, `category`, `price`) VALUES (%s, 1, %s, %s)", (appID, cat, p))

con.commit()
cur.close()
con.close()
