from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns


def main():
    grammarly_df = pd.DataFrame.from_csv("grammarly_data_csv.csv")

    print "0. DAILY ACTIVE USERS\n1. RETENTION CURVE\n2. EVALUATE SOURCES"
    choice = raw_input("CHOOSE AN OPTION ")

    while choice.lower() != "q" and choice in [str(x) for x in range(0, 3)]:
        if choice == "0":
            daily_active_users(grammarly_df)
        elif choice == "1":
            retention_curve(grammarly_df)
        elif choice == "2":
            evaluate_source(grammarly_df)
        choice = raw_input("CHOOSE AN OPTION ")
    exit()


# COUNT DAILY ACTIVE USERS
def daily_active_users(grammarly_df):

    grouped_by_date = grammarly_df.groupby('date')
    user_count = pd.DataFrame(grouped_by_date.uid.nunique())
    user_count.columns = ['count']
    print user_count
    sns.set_style("darkgrid")
    x_axis = mdates.date2num([datetime.strptime(str(d).split(" ")[0], '%Y-%m-%d').date() for d in user_count.index])
    y_axis = [float(y) for y in user_count['count']]

    #TODO VISUALIZE DAILY ACTIVE USERS
    plt.figure(figsize=(15, 8))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot_date(x_axis, y_axis, 'b-')
    plt.gcf().autofmt_xdate()
    plt.show()
    return


# COUNT RETENTION CURVE
def retention_curve(grammarly_df):
    grouped_by_date = grammarly_df.groupby('date')
    for feb_date in ["04", "10", "14"]:

        date_to_format = '2016-02-{0}'.format(feb_date)

        cohort_slice = grammarly_df[(grammarly_df.index == datetime.strptime(date_to_format, '%Y-%m-%d')) & (grammarly_df['isFirst'] == True)]
        cohort_slice_cohort = list(set(cohort_slice['uid']))
        # print cohort_slice
        print "FEB {0} COHORT".format(feb_date), len(cohort_slice_cohort)

        #TODO MAYBE THERE IS A MORE EFFICIENT WAY TO DO THIS

        for name, group in grouped_by_date:
            print name, group[group['uid'].isin(cohort_slice_cohort)].uid.nunique(), float(group[group['uid'].isin(cohort_slice_cohort)].uid.nunique())/float(len(cohort_slice_cohort))
    return
    #TODO VISUALIZE RETENTION CURVE


#COUNT BY SOURCE
def evaluate_source(grammarly_df):
    grouped_by_source = grammarly_df.groupby('utmSource_cleaned')

    total_users = grouped_by_source.uid.nunique()
    print total_users.sort_values(ascending=False)

    #AVERAGE DURATION OF VISITS
    #NUMBER OF PINGS BY USER
    for name, group in grouped_by_source:
        grouped_by_uid = group.groupby(['uid', 'date'])
        duration = []

        # print name
        for uid, uid_group in grouped_by_uid:
            # print uid, max(uid_group['timestamp'].values) - min(uid_group['timestamp'].values)
            duration.append((max(uid_group['timestamp'].values) - min(uid_group['timestamp'].values))/3600000.0)

        print name, group.uid.nunique(), group.timestamp.nunique(), float(group.timestamp.nunique())/float(group.uid.nunique()), np.mean(duration)
    return

#TODO EQUALLY WEIGHT PINGS AND DURATION; MEASURE
#TODO WHAT ABOUT AVERAGE TIME BETWEEN PINGS?

#TODO VISUALIZE EVALUATION BY TRAFFIC SOURCE

if __name__ == "__main__":
    main()