import pandas as pd; import numpy as np
def smooth_transition(start_date, end_date):                                                                                                                  from scipy.special import expit                                                                                                                           dt = pd.date_range(start_date, end_date, freq='d')                                                                                                    
    midpoint = dt[dt.size//2].date()                                                                                                                          x = np.arange(-dt.size,dt.size) * 5.2 / dt.size                                                                                                           y = pd.Series(expit(x), pd.date_range(dt[0],freq='12h',periods=dt.size*2)).resample('d').mean()                                                           return 1 - y
def linear_transition(start_date, end_date):                                                                                                                  dt = pd.date_range(start_date, end_date, freq='d')                                                                                                        x = np.arange(dt.size*2)  / dt.size*0.5                                                                                                                   y = pd.Series(x, pd.date_range(dt[0],freq='12h',periods=dt.size*2)).resample('d').mean()                                                                  return 1 - y

s1 = smooth_transition('2021-01-01','2022-12-31')
s1 = pd.Series(1, pd.date_range("2020-04-24","2020-12-31")) .append(s1)
s1 = s1 .append( pd.Series(0, pd.date_range("2023-01-01","2024-12-31"))  )
s1.index.name = 'yyyy_mm_dd'
s1.name = 'crisis_weight'
x1 = s1 .reset_index() 
x1.insert(0, 'scenario','smooth_2021Q1_2023Q4')

s1 = smooth_transition('2020-06-01','2022-12-31')
s1 = pd.Series(1, pd.date_range("2020-04-24","2020-05-31")) .append(s1)
s1 = s1 .append( pd.Series(0, pd.date_range("2023-01-01","2024-12-31"))  )
s1.index.name = 'yyyy_mm_dd'
s1.name = 'crisis_weight'
x2 = s1 .reset_index() 
x2.insert(0, 'scenario','smooth_2020Q3_2023Q4')
x1 = x1.append(x2, ignore_index=True)

s1 = linear_transition('2021-01-01','2022-12-31')
s1 = pd.Series(1, pd.date_range("2020-04-24","2020-12-31")) .append(s1)
s1 = s1 .append( pd.Series(0, pd.date_range("2023-01-01","2024-12-31"))  )
s1.index.name = 'yyyy_mm_dd'
s1.name = 'crisis_weight'
x2 = s1 .reset_index() 
x2.insert(0, 'scenario','linear_2021Q1_2023Q4')

x1 = x1.append(x2, ignore_index=True)

#x1.pivot_table('crisis_weight','yyyy_mm_dd','scenario')  .plot(grid=True)

x2 = x1.copy();  x2['yyyy_mm_dd'] = x2['yyyy_mm_dd'].astype("str")
sdf = spark.createDataFrame(x2)
