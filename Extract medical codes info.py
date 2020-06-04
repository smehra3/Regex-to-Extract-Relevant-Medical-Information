
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-text-mining/resources/d9pwm) course resource._
# 
# ---

# # Assignment 1
# 
# In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data. 
# 
# Each line of the `dates.txt` file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.
# 
# The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates. 
# 
# Here is a list of some of the variants you might encounter in this dataset:
# * 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# * Mar-20-2009; Mar 20, 2009; March 20, 2009;  Mar. 20, 2009; Mar 20 2009;
# * 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# * Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# * Feb 2009; Sep 2009; Oct 2010
# * 6/2008; 12/2009
# * 2009; 2010
# 
# Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:
# * Assume all dates in xx/xx/xx format are mm/dd/yy
# * Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# * If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# * If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
# * Watch out for potential typos as this is a raw, real-life derived dataset.
# 
# With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.
# 
# For example if the original series was this:
# 
#     0    1999
#     1    2010
#     2    1978
#     3    2015
#     4    1985
# 
# Your function should return this:
# 
#     0    2
#     1    4
#     2    0
#     3    1
#     4    3
# 
# Your score will be calculated using [Kendall's tau](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient), a correlation measure for ordinal data.
# 
# *This function should return a Series of length 500 and dtype int.*

# In[2]:


import pandas as pd
import re

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
df.head(10)

def date_sorter():
    dateslist = []
    # type1 = r'\d{1,2}[/]\d{1,2}[/]\d{2,4}' this doesn't work for all date, so after the first run we change it
    type1 = r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
    type2 = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))[a-z]*[.]?[- ](\d{1,2})[,]?[- ](\d{4})'
    type3 = r'(\d{1,2}) ((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))[a-z]*[.,]? (\d{4})'
    type4 = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))[a-z]* (\d{1,2})[a-z]{2}[,] (\d{4})'
    type5 = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))[a-z]*[,]? (\d{4})'
    # for type 5 there for example line 339 Apr, 1998
    type6 = r'(\d{1,2})[/](\d{4})'
    type7 = r'\d{4}'
    month_dict = {'Jan': '01', 'Feb': '02' ,'Mar': '03','Apr':'04','May':'05','Jun':'06',
                  'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    count = 0
    for s in df:
        count += 1
        if len(re.findall(type1,s)) != 0:
            
            date=list(re.findall(type1,s)[0]) # change to list, because re.findall(type1,s)[0] is a tuple, and we can't change value
            if len(date[2])==2: # change ab into 19ab
                date[2] ='19'+date[2]
            if len(date[0])==1:
                date[0] = '0'+ date[0]
            if len(date[1])==1:
                date[1] = '0'+ date[1]
            dateslist.append(date[2]+date[0]+date[1])
        elif len(re.findall(type2,s)) != 0: 
            
            date=list(re.findall(type2,s)[0])
            if len(date[1])==1:
                date[1] = '0'+ date[1]
            date[0] = month_dict[date[0]]
            dateslist.append(date[2]+date[0]+date[1])
        elif len(re.findall(type3,s)) != 0:
            
            date=list(re.findall(type3,s)[0])
            if len(date[0])==1:
                date[0] = '0'+ date[0]
            date[1] = month_dict[date[1]]
            dateslist.append(date[2]+date[1]+date[0])
        elif len(re.findall(type4,s)) != 0:
            
            date=list(re.findall(type4,s)[0])
            if len(date[1])==1:
                date[1] = '0'+ date[1]
            date[0] = month_dict[date[0]]
            dateslist.append(date[2]+date[0]+date[1])
        elif len(re.findall(type5,s)) != 0:
            # print(count) use this output to check for exceptions and mistakes
            date=list(re.findall(type5,s)[0])
            date[0] = month_dict[date[0]]
            dateslist.append(date[1]+date[0]+'01')
        elif len(re.findall(type6,s)) != 0:
            date=list(re.findall(type6,s)[0])
            if len(date[0])== 1:
                date[0] = '0'+date[0]
            dateslist.append(date[1]+date[0]+'01')
        elif len(re.findall(type7,s))!= 0:
            date=re.findall(type7,s)[0]
            dateslist.append(date+'01'+'01')
        else :
            print(s)    # because the question only mention part of the date form
        # try this you will find that there are 3 line with date 4-13-82 1-14-81 4-13-89, so 
        dates = pd.Series(dateslist)
        dates.sort_values(inplace=True)
        order = pd.Series(dates.index)
    return order
a = date_sorter()


# In[ ]:




