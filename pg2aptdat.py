#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Martin Herweg    m.herweg@gmx.de
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#


import os, sys
import psycopg2
from lxml import etree

db_params = {"host":"localhost", "database":"landcover", "user":"mherweg"}
outfile = open("apt.dat.out", 'w')


try:
    conn = psycopg2.connect(**db_params)
except:
    print "Cannot connect to database."
cur = conn.cursor()

def fn_pgexec(sql):
    try:
        cur.execute(sql)
    except psycopg2.Error, e:
        print e
        #print sql
    return cur


#MAIN

icao="EDLM"
#sql = "SELECT DISTINCT icao,layout FROM apt_dat WHERE icao LIKE 'LOWI' ORDER BY icao"
sql = "SELECT DISTINCT icao,layout FROM apt_dat ORDER BY icao"

fn_pgexec(sql)

#cur.execute("SELECT icao  FROM apt_dat WHERE icao LIKE '%s'" % icao)
#print icao,  cur.rowcount 

print "A"
print "1000 Generated by WorldEditor"
        
if cur.rowcount == 0:
    print icao ,"not found"
else:
    db_result = cur.fetchall()
    for row in db_result:
        print
        icao = row[0]
        linearray= row[1]
        for line in linearray:
            print line
            
#optional footer:            
print "99"
            
        
        
        
        
        
        
            



