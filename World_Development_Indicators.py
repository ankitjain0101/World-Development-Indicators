import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('E:/College/Analytics/Python/World Development Indicators/database.sqlite')

pd.read_sql(""" SELECT *
                FROM sqlite_master
                WHERE type='table';""",
           conn)

pd.read_sql("""SELECT *
               FROM Indicators
               LIMIT 10;""",
           conn)

# checking for missing values in one column
pd.read_sql("""SELECT COUNT(*)
               FROM Indicators
               WHERE IndicatorName IS NULL;""",
           conn)
# checking for missing values in all columns
pd.read_sql("""SELECT COUNT(*) - COUNT(CountryName) AS missing_CountryName,
                      COUNT(*) - COUNT(CountryCode) AS missing_CountryCode,
                      COUNT(*) - COUNT(IndicatorName) AS missing_IndicatorName,
                      COUNT(*) - COUNT(IndicatorCode) AS missing_IndicatorCode, 
                      COUNT(*) - COUNT(Year) AS missing_Year, 
                      COUNT(*) - COUNT(Value) AS missing_Value
                FROM Indicators;""",
           conn)

# selecting distinct indicators
pd.read_sql("""SELECT DISTINCT IndicatorName
                FROM Indicators;""",
           conn)

#Data manipulation
pd.read_sql("""SELECT DISTINCT IndicatorName
               FROM Indicators
               WHERE IndicatorName LIKE 'GDP%';""",
           conn)

pd.read_sql(""" SELECT *
                FROM Indicators
                WHERE IndicatorName ='GDP per capita (current US$)'
                AND CountryName = "India"
                AND Year>=2010;""",
           conn)

pd.read_sql("""SELECT *
               FROM Indicators
               WHERE IndicatorName='GDP per capita (current US$)'
               AND (CountryName= 'United States' OR CountryName= 'United Kingdom')
               AND Year>=2010;""",
           conn)

pd.read_sql("""SELECT *
               FROM Indicators
               WHERE IndicatorName='GDP per capita (current US$)'
               AND CountryName IN ("United States", "China", "India")
               AND Year=2014;""",
            conn)
#Highest GDP per capita
pd.read_sql("""SELECT CountryName, MAX (Value)
               FROM Indicators
               WHERE IndicatorName = 'GDP per capita (current US$)'
               AND Year = 2012;""",
            conn)

pd.read_sql("""SELECT * 
               FROM Indicators
               WHERE IndicatorName='GDP per capita (current US$)'
               AND Year= 2012
               ORDER BY Value DESC
               LIMIT 3;""",
           conn)


pd.read_sql(""" SELECT CountryName, AVG(Value)
                FROM Indicators
                WHERE IndicatorName= 'GDP per capita (current US$)'
                AND CountryName IN ('Brazil', 'China', 'India', 'Angola')
                AND Year>2010
                GROUP BY CountryName;""",
           conn)

#Indicators GDP related measured in 2014 in United States
pd.read_sql(""" SELECT Indicators.*, Series.LongDefinition
                FROM Indicators
                LEFT JOIN Series 
                ON Indicators.IndicatorName  = Series.IndicatorName
                WHERE Indicators.IndicatorName LIKE 'GDP%'
                AND CountryName ='United States'
                AND Year=2014;""",
            conn)

df=pd.read_sql(""" SELECT *,
                   CASE WHEN Value < 10000 THEN 'Low'
                   WHEN Value > 80000 THEN 'High'
                   ELSE 'Medium' END AS Category
                   FROM Indicators
                   WHERE IndicatorName='GDP per capita (current US$)'
                   AND Year=2014;""",
              conn)
fig, axes= plt.subplots(1,2, figsize=(8,4),sharey=True)

ax1= sns.distplot(df.Value, bins=40, hist_kws={'edgecolor':'k'}, color='mediumseagreen',kde=False,ax=axes[0])
ax1.set_title('Histogram')
ax1.set(xlabel="GDP per capita (current US$) - Value")
ax1= sns.despine()

ax2= sns.countplot(x='Category', data=df, palette="BuGn_r", ax=axes[1])
ax2.set_title('Frequency Count')
ax2.set(xlabel="GDP per capita (current US$) - Category")
ax2= sns.despine();

# adding the mean of last 3 years using window function

pd.read_sql(""" SELECT *,
                ROUND(AVG(Value) OVER (PARTITION BY CountryCode),0) AS AVG_3Y
                FROM Indicators
                WHERE IndicatorName='GDP per capita (current US$)'
                AND Year IN (2012,2013,2014);""",
           conn)

# Second highest GDP country from each year
pd.read_sql(""" WITH GDP_3 AS 
                (SELECT *,
                RANK () OVER (PARTITION BY Year ORDER BY Value DESC) AS myrank
                FROM Indicators
                WHERE IndicatorName='GDP per capita (current US$)'
                AND Year IN (2012,2013,2014))
                
                SELECT *
                FROM GDP_3
                WHERE myrank = 2;""",
           conn)