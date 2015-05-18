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



#I
#1000 Version - data cycle 2013.10, build 20131335, metadata AptXP1000.
#
#1     1906 1 0 LOWI Innsbruck Kranebitten
#01234567890123456789
#          1    ^

# "2015" file:
#A
#1000 Generated by WorldEditor
#
#1   1470 0 0 0B7 Warren-Sugarbush
#01234567890123456789
#          1  ^

#XP10 custom cenery pack: 
#A
#1000 Generated by WorldEditor
#
#1   1906 1 0 LOWI Innsbruck Kranebitten
#01234567890123456789
#          1  ^ 
#    elev 0 0 ICAO Name


#known bugs:
# cannot process the airport LOWI from the 2013 file



import os, sys
import psycopg2
from lxml import etree

db_params = {"host":"localhost", "database":"landcover", "user":"mherweg"}
infile = open("apt.dat.lowi-in", 'r')


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

def insert_or_update(icao,linearray):
    cur.execute("SELECT icao  FROM apt_dat WHERE icao LIKE '%s'" % icao)
    #print icao,  cur.rowcount 
    if cur.rowcount == 1:
        sql = cur.mogrify("UPDATE apt_dat SET layout = %s WHERE icao LIKE %s;" ,(linearray, icao))
        print "UPDATE", icao
        fn_pgexec(sql)
    else:
        sql = cur.mogrify("INSERT INTO apt_dat(icao,layout) VALUES (%s,%s)", (icao,linearray))
        #print "sql:" , sql
        fn_pgexec(sql)
        print "INSERT" , icao
             

# main loop

icao=""
counter = 0
for line in infile:
        line = line.strip()
        # 1 for airports, 16 for seaports, ....
        if line.startswith("1 ") or line.startswith("16 ") or line.startswith("17 "):
            
            #the previous icao:
            #if icao != "" and icao !="LOWI":
            if icao != "":
            #if icao == "LOWI":    
                # write previous airport to DB
                print icao, counter
                counter = counter +1
                insert_or_update(icao, linearray)
                if (counter%100 == 0):
                    conn.commit()
                    print "=============COMMIT=============="
                    
            
            #the next airport:
            apt_header = line.split()
            icao = apt_header[4]
            name = ' '.join(apt_header[5:])
            #print icao, name
            
            linearray = []
            linearray.append(line)
             
        else:
            #read all the lines of that airport
            if icao != "" and line != "" and line != "99":
                linearray.append(line)
                
# last airport in apt.dat:
if icao != "":
    insert_or_update(icao, linearray)
    print icao, counter



conn.commit()
cur.close()
conn.close()
#EOF











