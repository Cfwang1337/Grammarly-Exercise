from datetime import datetime
import pandas as pd

grammarly_df = pd.DataFrame.from_csv("grammarly_data_csv.csv")

# print grammarly_df[:50]

# COUNT DAILY ACTIVE USERS
# grouped = grammarly_df.groupby('date')
# user_count = grouped.uid.nunique()
# print user_count

#TODO VISUALIZE DAILY ACTIVE USERS

print grammarly_df.index.dtype
print grammarly_df.dtypes

#TODO COUNT RETENTION CURVE

feb_4 = grammarly_df[(grammarly_df.index == datetime.strptime('2016-02-04', '%Y-%m-%d')) & (grammarly_df['isFirst'] == True)]
feb_4_cohort = list(set(feb_4['uid']))
print feb_4


#TODO VISUALIZE RETENTION CURVE


#TODO EVALUATE BY TRAFFIC SOURCE

#TODO VISUALIZE EVALUATION BY TRAFFIC SOURCE

#TODO PREDICT SUCCESS BASED ON TIME OF DAY, SOURCE, AND ISFIRST