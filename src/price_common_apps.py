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

pps = {}

for x in apps:
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
  
  prices = [pts[1]["price"], pts[2]["price"], pts[3]["price"]]
  if any(x == 0.0 for x in prices) and not all(x == 0.0 for x in prices):
    pps[appID] = True


info = []

ps = {
  1: "android",
  2: "ios",
  3: "windows"
}

for x in apps:
  appID = x[0]
  if not appID in pps:
    continue
  sql = "SELECT t1.* FROM `listing` as t1 WHERE t1.`app` = %s" % appID
  cur.execute(sql)
  ys = cur.fetchall()
  
  sql = "SELECT t1.* FROM `app` as t1 WHERE t1.`id` = %s" % appID
  cur.execute(sql)
  zz = cur.fetchone()
  
  obj = {"name": zz[1]}
  
  if zz[1] == "Spray":
    continue
  
  for y in ys:
    platform = int(y[1])
    categ = int(y[2])
    price = float(y[3]) if y[3] else 0.0
    
    ncateg = ct.categories[categ]
    obj["group"] = ncateg
    
    obj[ps[platform]] = price
  
  info.append(obj)

#con.commit()
cur.close()
con.close()

js = "var foods = " +  json.dumps(info) + ";"

print js

text_file = open("app-table.js", "w")
text_file.write(js)
text_file.close()
