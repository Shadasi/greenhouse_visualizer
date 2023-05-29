import sqlite3
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime as dt
import requests
import os
import json
import datetime

from dotenv import load_dotenv, find_dotenv
from sqlite3 import Error

load_dotenv(find_dotenv())

API_URL = os.environ.get("API_URL")
# SENSOR_NAME = os.environ.get("SENSOR_NAME")
# POLL_INTERVAL = os.environ.get("POLL_INTERVAL")

headers = {
    'Content-Type': 'application/json'
}

def create_connection(db_file):
       """ create a database connection to the SQLite database
       specified by the db_file
       :param db_file: database file
       :return: Connection object or None
       """
       conn = None
       try:
              conn = sqlite3.connect(db_file)
       except Error as e:
              print(e)

       return conn


def selectTemperature(dayToQuery):
       dayToQuery = list(dayToQuery)
       start_of_day = dt.datetime.combine(dt.date.today(), dt.time(00, 00, 00))
       end_of_day = dt.datetime.combine(dt.date.today(), dt.time(23, 59, 59))
       response = requests.get(API_URL + 'temp', params={ "start":dayToQuery[0] ,"end":dayToQuery[1] } )
       return response.content


def selectHumidity(dayToQuery):
       dayToQuery = list(dayToQuery)
       start_of_day = dt.datetime.combine(dt.date.today(), dt.time(00, 00, 00))
       end_of_day = dt.datetime.combine(dt.date.today(), dt.time(23, 59, 59))
       response = requests.get(API_URL + 'humidity', params={ "start":dayToQuery[0] ,"end":dayToQuery[1] } )
       return response.content
       

def plotHumidityAndTemp(tempRows, humidityRows):
       


       x_points_s1 = []       
       x_points_s2 = []
       y_points_s1 = []
       y_points_s2 = []

       humidityRows = json.loads(humidityRows)
       tempRows = json.loads(tempRows)


       for i in range(len(humidityRows)):
              time_to_plot = dt.datetime.utcfromtimestamp(humidityRows[i]["timestamp"])
              # print(time_to_plot, ', ' ,round(rows[i][2], 2))
              if(humidityRows[i]["sensor_name"] == "SENSOR_ONE"):
                     x_points_s1.append(time_to_plot)
                     y_points_s1.append(round(humidityRows[i]["humidity"], 1))
              else:
                     x_points_s2.append(time_to_plot)
                     y_points_s2.append(round(humidityRows[i]["humidity"], 1))
          
       plt.figure()

       plt.subplot(211)     
       ax=plt.gca()

       xfmt = md.DateFormatter('%d-%m-%y %H:%M', 'US/Central')
       ax.xaxis.set_major_formatter(xfmt)     
       ax.set_xlabel('Date')
       ax.set_ylabel('Humidity%')

       plt.plot(x_points_s1, y_points_s1, 'b-', label="Sensor 1")
       plt.plot(x_points_s2, y_points_s2, 'g-', label="Sensor 2")
       
       plt.legend()

       x_points_s1 = []       
       x_points_s2 = []
       y_points_s1 = []
       y_points_s2 = []

       for i in range(len(tempRows)):
              time_to_plot = dt.datetime.utcfromtimestamp(tempRows[i]["timestamp"])
              if(tempRows[i]["sensor_name"] == "SENSOR_ONE"):
                     x_points_s1.append(time_to_plot)
                     y_points_s1.append(round(tempRows[i]["temperature"], 1))
              else:
                     x_points_s2.append(time_to_plot)
                     y_points_s2.append(round(tempRows[i]["temperature"], 1))
              
       plt.subplot(212)
       ax=plt.gca()

       xfmt = md.DateFormatter('%d-%m-%y %H:%M', 'US/Central')
       ax.xaxis.set_major_formatter(xfmt)     
       ax.set_xlabel('Date')
       ax.set_ylabel('Temperature F°')

       plt.plot(x_points_s1, y_points_s1, 'm-', label="Sensor 1")
       plt.plot(x_points_s2, y_points_s2, 'y-', label="Sensor 2")
       
       # ax.autoscale()

       plt.legend()
       plt.show()


def getUserInput():
       date = input("Enter dat you want to query:")
       # print("Username is: " + date)
       return convertToDate(date)

def convertToDate(date):
       # format should be ddmmyy
       print(date)
       startDate = datetime.datetime.strptime(date, "%m%d%Y")       
       endDate = startDate + datetime.timedelta(days=1)

       # print(startDate)
       # print(endDate)

       startTimestamp = time.mktime(startDate.timetuple())
       endTimestamp = time.mktime(endDate.timetuple())

       print(startTimestamp)
       print(endTimestamp - 1)

       return {startTimestamp, (endTimestamp - 1)}


def main():
       
       dayToQuery = getUserInput()

       # create a database connection
       print("Select humidity")
       humidityRows = selectHumidity(dayToQuery)
       print("Select temperature")
       tempRows = selectTemperature(dayToQuery)
       plotHumidityAndTemp(tempRows, humidityRows)




if __name__ == '__main__':
       main()