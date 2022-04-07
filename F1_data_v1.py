#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 15:08:06 2022

@author: elizabethtnguyen
"""

# import packages 
import pandas as pd
import subprocess
import pandasql as ps
import matplotlib.pyplot as plt

races = pd.read_csv('races.csv')
drivers = pd.read_csv('drivers.csv')
results = pd.read_csv('results.csv')
standing = pd.read_csv('driver_standings.csv')
pit_stops = pd.read_csv('pit_stops.csv')

#cleaned races dataset
df_races_cleaned = races['raceId'].reset_index()
df_races_cleaned['raceId'] = df_races_cleaned['level_0']
df_races_cleaned['year'] = df_races_cleaned['level_1']
df_races_cleaned['name'] = df_races_cleaned['level_4']
df_races_cleaned['round'] = df_races_cleaned['level_2']
df_races_cleaned['date'] = df_races_cleaned['level_5']

races = df_races_cleaned


#cleaning driver table with SQL

print('I noticed some code are missing from the Driver''s table, lets try to clean up the table')


q8= """
select driverId,driverRef,number,code,forename,
case when length(code) <=2 then upper(substr(forename,1,3)) else code end code
from drivers

"""

print(ps.sqldf(q8, locals()))
drivers = ps.sqldf(q8, locals())


#query to pull top 5 F1 driver with most win from 1950-2021

print('Top 5 F1 driver with the most win from 1950-2021')

q1 = """
select drivers.driverId, drivers.driverRef, count(results.position) count
from drivers
left join results
on drivers.driverId  = results.driverId
where results.position = "1"
group by 1,2
order by 3 desc
limit 5
"""

#print(ps.sqldf(q1, locals()))
df_1 = ps.sqldf(q1, locals())

#bar chart for visualization
print('Bar chart of top 5 F1 drivers')

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
Drivers = df_1['driverRef']
Wins = df_1['count']
ax.bar(Drivers,Wins)
plt.show()

#last 5 Australian Grand Prix winners from 1950-2021
print('Last 5 Australian GP winners from 1950-2021')
q2 = """

select  drivers.driverRef, races.name, count(results.position) wins
from drivers
left join results
on drivers.driverId  = results.driverId
left join races
on results.raceId = races.raceId
where results.position = "1" and races.name = "Australian Grand Prix"
group by 1,2
order by 3 desc
limit 5
"""

#print(ps.sqldf(q2, locals()))
df_2 = ps.sqldf(q2, locals())
#Driver who won the most races in 2021
print('Driver who won the most races in 2021')

q3= """
select  drivers.driverRef,count(distinct results.raceId) wins
from drivers
left join results
on drivers.driverId  = results.driverId
left join races
on results.raceId = races.raceId
where races.year = "2021"
and position = 1
group by 1
order by 2 desc
limit 10
"""

#print(ps.sqldf(q3, locals()))
df_3 = ps.sqldf(q3, locals())

#bar chart for visualization
print('Bar chart')

import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
Drivers = df_2['driverRef']
Wins = df_2['wins']
ax.bar(Drivers,Wins)
plt.show()

#Driver who finished the most 2nd in F1 from 1950-2021 for Monaco GP
print('Driver who finished the most 2nd in F1 from 1950-2021 for Monaco GP')

q4= """
select  drivers.driverRef, races.name, count(results.position) wins
from drivers
left join results
on drivers.driverId  = results.driverId
left join races
on results.raceId = races.raceId
where results.position = "2" and races.name = "Monaco Grand Prix"
group by 1,2
order by 3 desc
limit 5
"""

#print(ps.sqldf(q4, locals()))
df_4 = ps.sqldf(q4, locals())

#5 fastest lap times in F1 at Monaco GP from 1950-2022, Driver and Year
print('Fastest lap time in F1 at Monaco GP from 1950-2021; Driver and Year')

q5= """
select  drivers.driverRef, races.name, results.fastestLaptime, races.year
from drivers
left join results
on drivers.driverId  = results.driverId
left join races
on results.raceId = races.raceId
where races.name = "Monaco Grand Prix"
order by 3 asc
limit 5
"""

#print(ps.sqldf(q5, locals()))
df_5 = ps.sqldf(q5, locals())


#Hamilton vs Verstappen points on 07-18-2021, who had the most points?
print('Who had the most points on 07-18-2021?')

q6= """
select drivers.driverRef,standing.driverId, standing.points, races.round, races.date
from standing
left join races
on races.raceId = standing.raceId
left join drivers
on standing.driverId = drivers.driverId
where races.round between 1 and 10 and races.year = 2021 and races.round = 10
order by 3 desc
limit 5


"""

#print(ps.sqldf(q6, locals()))
df_6 = ps.sqldf(q6, locals())

#2021 who had the fastest and slowest pit stops?'
print('Who had the fastest and slowest pit stop?')

q6= """
SELECT sub1.driverRef,sub2.name,sub1.fastes_pit FROM

(select drivers.driverRef, races.name, min(pit_stops.duration) fastes_pit, max(pit_stops.duration) slowest_pit
from pit_stops
left join drivers
on pit_stops.driverId = drivers.driverId
left join races
on pit_stops.raceId = races.raceId
where races.year = 2021
group by 1
order by 3 asc) sub1

INNER JOIN

(select drivers.driverRef, races.name, min(pit_stops.duration) fastes_pit, max(pit_stops.duration) slowest_pit
from pit_stops
left join drivers
on pit_stops.driverId = drivers.driverId
left join races
on pit_stops.raceId = races.raceId
where races.year = 2021 --and driverRef = "bottas"
group by 1,2
order by 3 asc) sub2


ON sub1.driverRef = sub2.driverRef AND sub1.fastes_pit = sub2.fastes_pit


"""

print(ps.sqldf(q6, locals()))
df_6 = ps.sqldf(q6, locals())


#2021 How many times did each driver pit in 2021
print("How many times did each driver pit in 2021?")

q7= """
select drivers.driverRef, races.year, count(pit_stops.stop) total_pit
from drivers
left join pit_stops
on pit_stops.driverId = drivers.driverId
left join races
on pit_stops.raceId = races.raceId
where races.year = 2021
group by 1,2
order by 3 desc

"""

#print(ps.sqldf(q7, locals()))
#df_7 = ps.sqldf(q7, locals())








