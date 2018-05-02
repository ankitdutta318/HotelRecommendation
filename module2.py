# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 15:45:23 2018

@author: ANKIT
"""

import csv
from math import sin,cos,sqrt,atan2,radians
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import warnings
import sys
import webbrowser as wb
warnings.filterwarnings("ignore")


R = 6373.0
print("Enter user ID:")
ID=input()

with open('socialgraph.csv') as csvfile:
    readCSV=csv.reader(csvfile,delimiter=',')
    friends=[]
    for row in readCSV:
        #print(row)
        if(row[0]==ID):
            friends.append(row[1])

print("Friends:",friends)
print("\n")
with open('ratings.csv') as rate:
    readCSV2=csv.reader(rate,delimiter=',')
    venues=[]
    for row in readCSV2:
        if((row[2]=='5' or '4') and (row[0] in friends)):
            if(row[1] not in venues):
                venues.append(row[1])


with open('user_locate.csv') as user_loc:
    readCSV3=csv.reader(user_loc,delimiter=',')
    u_loc=[]
    for row in readCSV3:
        if(row[0]==ID):
            u_loc.append(row[1])
            u_loc.append(row[2])


if len(u_loc)==0:
    print("Data insufficient or wrong ID entered!")
    sys.exit()

with open('venue_locate.csv') as venue_loc:
    readCSV4=csv.reader(venue_loc,delimiter=',')
    v_loc=[]
    for row in readCSV4:
        if(row[0] in venues):
            v_loc.append((row[1],row[2]))

d=[]
dist=[]
for i in v_loc:
    lat1 = radians(float(u_loc[0]))
    lon1 = radians(float(u_loc[1]))
    lat2 = radians(float(i[0]))

    lon2 = radians(float(i[1]))
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    #print(dlon,dlat)

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = round(R * c,2)
    if(distance<100.0):
        d.append((i[0],i[1]))
        dist.append(distance)

with open('venue_locate.csv') as venue_loc:
    readCSV5=csv.reader(venue_loc,delimiter=',')
    v=[]
    for row in readCSV5:
        if (row[1],row[2]) in d:
            v.append(row[0])

##print(len(venues))
print ("User location-->",u_loc[0],u_loc[1])
print ("\n")
#print(v_loc)
#print(d)
#print(dist)
#print(v)

w=[]
for i in range(0,len(d)):
    w.append(("Venue ID: "+str(v[i]),"Distance: "+str(dist[i])+"kms"))

if(len(d)==0):
    print("Sorry,can't recommend any venues near you!")
else:
    print("Recommended Venues:",w)

wb.open('https://www.google.co.in/maps/dir//'+u_loc[0]+','+u_loc[1]+'/@'+u_loc[0]+','+u_loc[1]+',17z/data=!4m8!1m7!3m6!1s0x0:0x0!2zNDDCsDAwJzU0LjAiTiAxMDXCsDE2JzE0LjAiVw!3b1!8m2!3d'+u_loc[0]+'!4d-'+u_loc[1])

for i in d:
    wb.open('https://www.google.co.in/maps/dir//'+i[0]+','+i[1]+'/@'+i[0]+','+i[1]+',17z/data=!4m8!1m7!3m6!1s0x0:0x0!2zNDDCsDAwJzU0LjAiTiAxMDXCsDE2JzE0LjAiVw!3b1!8m2!3d'+i[0]+'!4d-'+i[1])


    m = Basemap(projection='mill',llcrnrlat=-90,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    #m.fillcontinents(color='green', lake_color='blue')
    m.drawmapboundary(fill_color='#FFFFFF')
    m.bluemarble(scale=0.5)
    ul1=u_loc[0]
    ul2=u_loc[1]
    x,y = m(float(u_loc[1]),float(u_loc[0]))
    m.plot(x,y,'ro',markersize=4)
    for i in range(0,len(d)):
        x,y=m(float(d[i][1]),float(d[i][0]))
        m.plot(x,y,'yo',markersize=4)

    plt.title('Geo Plotting')
    plt.show()