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

sql = "SELECT `app` FROM `listing` GROUP BY `app` HAVING COUNT(*) = 3"
cur.execute(sql)
apps = cur.fetchall()
n = 0
cn = 0
pn = 0
excluded = {}
for x in apps:
  n += 1
  appID = x[0]
  sql = "SELECT t1.* FROM `listing` as t1 WHERE t1.`app` = %s" % appID
  cur.execute(sql)
  pts = {}
  ys = cur.fetchall()
  for y in ys:
    platform = int(y[1])
    categ = int(y[2])
    price = float(y[3]) if y[3] else 0.0
    pts[platform] = {"categ": categ, "price": price}
  if pts[1]["categ"] == pts[2]["categ"] and pts[2]["categ"] == pts[3]["categ"]:
    pass
  else:
    cn += 1
    excluded[appID] = True
  prices = [pts[1]["price"], pts[2]["price"], pts[3]["price"]]
  if any(x == 0.0 for x in prices) and not all(x == 0.0 for x in prices):
    pn += 1

print "Common\t%s" % n
print "Category Mismatch\t%s" % cn
print "Price Mismatch\t%s" % pn

rs = {}
for pt in ct.platforms:
  rs[pt] = {}
  for c in ct.categories:
    rs[pt][c] = {"paid": 0, "free": 0, "mean": 0.0}

for x in apps:
  appID = x[0]
  if appID in excluded:
    continue
  sql = "SELECT t1.* FROM `listing` as t1 WHERE t1.`app` = %s" % appID
  cur.execute(sql)
  pts = {}
  ys = cur.fetchall()
  for y in ys:
    platform = int(y[1])
    categ = int(y[2])
    price = float(y[3]) if y[3] else 0.0
    
    if price > 0.0:
      nn = rs[platform][categ]["paid"]
      m = (nn * rs[platform][categ]["mean"] + price) / (nn + 1)
      rs[platform][categ]["mean"] = m
      rs[platform][categ]["paid"] += 1
    else:
      rs[platform][categ]["free"] += 1

for pt in ct.platforms:
  print "\n%s" % ct.platforms[pt]
  for c in ct.categories:
    print "%s" % ct.categories[c]
    print "Free\tPaid\tMean"
    z = rs[pt][c]
    print "%s\t%s\t%0.2f" % (z["free"], z["paid"], z["mean"])

#con.commit()
cur.close()
con.close()
