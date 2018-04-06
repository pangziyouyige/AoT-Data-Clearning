
# coding: utf-8

# In[167]:

from urllib.request import urlretrieve
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from pandas.plotting import scatter_matrix
import seaborn as sns
sns.set()


# In[6]:

# Get today's date, so everyday at the end to run this script
datem = datetime.today().strftime("%Y-%m-%d")


# In[113]:

# Create the new url to grab data from the AoT platform
uil="http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/2/001e061130f7/"+datem+".csv.gz"
# Generate the variable names
new_labels=["id","time","coresense","frame","aot","sensor","reading"]


# In[114]:

# Read data from web, use the default index
data = pd.read_csv(uil, compression='gzip', error_bad_lines=False, delimiter=";", header=0, names=new_labels, parse_dates=True)
data.head()
data.info()
data.shape


# In[115]:

# Update the datatype for the sensor column, reading column, and the time column
data.sensor=data.sensor.astype("category")
data.time=pd.to_datetime(data["time"])
data.reading=pd.to_numeric(data["reading"], errors="coerce")
# Double check whether the time zone is correct or not
#data.time=data.time.dt.tz_localize('US/Central')
#data.time=data.time.dt.tz_convert("US/Pacific")
data.info()


# In[185]:

# Subset the data.
data1=data[["time","sensor", "reading"]]
# Since the sensor column contains multiple sensors, pivot the data to tidy the data, set datetime as the index
data2=data1.pivot_table(index="time", columns="sensor", values="reading")
# Set the index name and columns name
data2.index.name="DateTime"
data2.columns.name="Sensing"
data2.loc["2018-04-04 00:00":"2018-04-04 05:00"]
# If need hierachical index, uncomment the following codes. For example, combine all three sensors data
# data2.reset_index()
# data2.set_index(["nodeNo","time])
# data2=data2.sort_index()


# In[171]:

# Use seaborn to check correlation (example: tempearture vs. humidity)
corr = data2.corr()
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns)
plt.show()


# In[178]:

#Check the correlation of every variable, after resample at hourly scale
hourly=data2.resample("60Min").mean()
corr_hour = hourly.corr()
sns.heatmap(corr_hour, xticklabels=corr_hour.columns, yticklabels=corr_hour.columns)
plt.show()


# In[129]:

# test rolling average for temperature
unsmoothed = data2["h2s"]
smoothed = unsmoothed.rolling(window=60).mean()
compare=pd.DataFrame({"smoothed": smoothed, "unsmoothed": unsmoothed})
compare.plot(alpha=0.5)
plt.show()


# In[182]:

# test the tempearture one day versus one week
plt.subplot(3,1,3)
data2.temperature.plot()
plt.subplot(3,1,2)
data2.temperature.plot(kind="hist", bins=50)
plt.subplot(3,1,1)
data2.temperature.plot(kind="hist", bins=50, cumulative=True)
plt.show()


# In[157]:

# Down sample the data
hourly=data2.resample("h").mean()
daily_max=data2.resample("D").max()
daily_min=data2.resample("D").min()
daily_max


# In[ ]:




# In[38]:

url="http://www.mcs.anl.gov/research/projects/waggle/downloads/beehive1/001e061130f7.html"
r=requests.get(url)
html_84=r.text
soup=BeautifulSoup(html_84)
a_tags = soup.find_all("<a>")


# In[58]:




# In[ ]:



