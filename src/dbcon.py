#!/usr/bin/python
# -*- coding: utf-8 -*-

import categories as ct
import sys
from subprocess import Popen, PIPE
import MySQLdb as mdb

DB_HOST = "localhost"
DB_NAME = "app"
DB_USER = "uapp"
DB_PASS = "app123"
DB_SCHEMA = "db/app.sql"

def reset_schema():
  print "Reseting DB Schema ..."
  process = Popen('mysql -h%s %s -u%s -p%s' % (DB_HOST, DB_NAME, DB_USER, DB_PASS), stdout=PIPE, stdin=PIPE, shell=True)
  process.communicate('source ' + DB_SCHEMA)[0]

def connect():
  con =  mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME, charset='utf8', use_unicode=True)
  con.autocommit(False)
  return con

def init():
  print "Initializing DB ..."
  con = connect()
  cur = con.cursor()
  
  print "Adding platforms ..."
  cur.execute("INSERT INTO `platform` (`name`) VALUES ('android'), ('ios'), ('windows')")
  
  print "Adding categories ..."
  for i in ct.categories.keys():
    cur.execute("INSERT INTO `category` (`id`, `name`) VALUES (%s, '%s')" % (i, ct.categories[i]))
  
  con.commit()
  cur.close()
  con.close()

if "init" in sys.argv:
  reset_schema()
  init()
