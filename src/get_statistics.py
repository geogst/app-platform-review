#!/usr/bin/python
# -*- coding: utf-8 -*-

from dbcon import *
import json

con = connect()
cur = con.cursor()

rrs = {
  1: "Free",
  2: "(0 - 1]",
  3: "(1 - 3]",
  4: "(3 - 6]",
  5: "(6 - 10]",
  6: "(10 - inf)",
}

def place(v):
  if v == None or v == 0.0:
    return 1
  elif v <= 1.0:
    return 2
  elif v <= 3.0:
    return 3
  elif v <= 6.0:
    return 4
  elif v <= 10.0:
    return 5
  else:
    return 6

rs = {}
ms = {}
for pt in ct.platforms:
  rs[pt] = {}
  ms[pt] = {}
  for c in ct.categories:
    rs[pt][c] = {}
    ms[pt][c] = None
    for pp in range(1,7):
      rs[pt][c][pp] = 0

sql = "SELECT * FROM `listing`"
cur.execute(sql)
for x in cur.fetchall():
#  print x
  appID = x[0]
  pt = int(x[1])
  categ = int(x[2])
  price = float(x[3]) if x[3] else None
#  print appID, pt, categ, price
  
  rr = place(price)
  rs[pt][categ][rr] += 1
  
  ms[pt][categ] = max(price, ms[pt][categ])

for pt in ct.platforms:
  print "\n%s" % ct.platforms[pt]
  for c in ct.categories:
    print "%s" % ct.categories[c]
    print "MAX\t%s" % ms[pt][c]
    for pp in range(1,7):
      print "%s\t" % rrs[pp],
    print ""
    for pp in range(1,7):
      print "%s\t" % rs[pt][c][pp],
    print ""


#con.commit()
cur.close()
con.close()
