from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns


def main():
    grammarly_df = pd.DataFrame.from_csv("grammarly_data_csv.csv")

    print "0. DAILY ACTIVE USERS\n1. RETENTION CURVE\n2. EVALUATE SOURCES\n3. RETENTION RATE BY SOURCE"
    choice = raw_input("CHOOSE AN OPTION ")

    while choice.lower() != "q" and choice in [str(x) for x in range(0, 4)]:
        if choice == "0":
            daily_active_users(grammarly_df)
        elif choice == "1":
            retention_curve(grammarly_df)
        elif choice == "2":
            evaluate_source(grammarly_df)
        elif choice == "3":
            retention_rate_by_source(grammarly_df)
        print "0. DAILY ACTIVE USERS\n1. RETENTION CURVE\n2. EVALUATE SOURCES\n3. RETENTION RATE BY SOURCE"
        choice = raw_input("CHOOSE AN OPTION ")
    exit()


# COUNT DAILY ACTIVE USERS
def daily_active_users(grammarly_df):

    grouped_by_date = grammarly_df.groupby('date')
    user_count = pd.DataFrame(grouped_by_date.uid.nunique())
    user_count.columns = ['count']
    print user_count

    user_count.to_csv("daily_active_users.csv")

    sns.set_style("darkgrid")
    x_axis = mdates.date2num([datetime.strptime(str(d).split(" ")[0], '%Y-%m-%d').date() for d in user_count.index])
    y_axis = [float(y) for y in user_count['count']]

    #VISUALIZE DAILY ACTIVE USERS

    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111)

    ax.set_xlabel("Date")
    ax.set_ylabel("Active users")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot_date(x_axis, y_axis, 'b-')
    plt.gcf().autofmt_xdate()
    plt.show()

    return


# CALCULATE RETENTION CURVE
def retention_curve(grammarly_df):
    grouped_by_date = grammarly_df.groupby('date')
    for feb_date in ["04", "10", "14"]:

        date_to_format = '2016-02-{0}'.format(feb_date)

        cohort_slice = grammarly_df[(grammarly_df.index == datetime.strptime(date_to_format, '%Y-%m-%d')) & (grammarly_df['isFirst'] == True)]
        cohort_slice_cohort = list(set(cohort_slice['uid']))
        # print cohort_slice
        print "FEB {0} COHORT".format(feb_date), len(cohort_slice_cohort)

        result_set = []

        for name, group in grouped_by_date:
            print name, group[group['uid'].isin(cohort_slice_cohort)].uid.nunique(), float(group[group['uid'].isin(cohort_slice_cohort)].uid.nunique())/float(len(cohort_slice_cohort))
            if group[group['uid'].isin(cohort_slice_cohort)].uid.nunique() > 0:
                result_set.append([name, group[group['uid'].isin(cohort_slice_cohort)].uid.nunique(), float(group[group['uid'].isin(cohort_slice_cohort)].uid.nunique())/float(len(cohort_slice_cohort))])

        result_df = pd.DataFrame(result_set, columns=[
            "date",
            "uid_count",
            "retention_rate"
        ])
        result_df = result_df.set_index("date")

        result_df.to_csv("retention_curve_feb_{0}.csv".format(feb_date))

        sns.set_style("darkgrid")
        x_axis = mdates.date2num([datetime.strptime(str(d).split(" ")[0], '%Y-%m-%d').date() for d in result_df.index])
        y_axis = [float(y) for y in result_df['retention_rate']]

        #VISUALIZE DAILY ACTIVE USERS

        fig = plt.figure(figsize=(15, 8))
        ax = fig.add_subplot(111)

        ax.set_xlabel("Date")
        ax.set_ylabel("Retention rate")

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.plot_date(x_axis, y_axis, 'b-')
        plt.gcf().autofmt_xdate()
        plt.show()

    return
    #TODO VISUALIZE RETENTION CURVE


#COUNT BY SOURCE

def evaluate_source(grammarly_df):
    grouped_by_source = grammarly_df.groupby('utmSource_cleaned')

    total_users = grouped_by_source.uid.nunique()
    print total_users.sort_values(ascending=False)

    #AVERAGE DURATION OF VISITS
    #NUMBER OF PINGS BY USER

    result_set = []

    for name, group in grouped_by_source:
        # grouped_by_uid = group.groupby(['uid', 'date'])
        # duration = []
        # for uid, uid_group in grouped_by_uid:
        #     duration.append((max(uid_group['timestamp'].values) - min(uid_group['timestamp'].values))/3600000.0)

        # print name, group.uid.nunique(), group.timestamp.nunique(), float(group.timestamp.nunique())/float(group.uid.nunique()), np.mean(duration)
        # result_set.append([name, group.uid.nunique(), group.timestamp.nunique(), float(group.timestamp.nunique())/float(group.uid.nunique()), np.mean(duration)])
        print name, group.uid.nunique(), group.timestamp.nunique(), float(group.timestamp.nunique())/float(group.uid.nunique())
        result_set.append([name, group.uid.nunique(), group.timestamp.nunique(), float(group.timestamp.nunique())/float(group.uid.nunique())])

    result_df = pd.DataFrame(result_set, columns=[
        "Source",
        "UniqueUsers",
        "Pings",
        "PingsPerUser",
        # "AverageDuration"
    ])

    result_df = result_df.set_index("Source")
    result_df.to_csv("evaluate_source.csv")

    for comparison in ["UniqueUsers", "Pings", "PingsPerUser"]:#, "AverageDuration"]:
        result_df = result_df.sort_values(comparison, ascending=True)
        sns.set_style("darkgrid")

        objects = result_df.index
        y_pos = np.arange(len(objects))
        performance = [float(y) for y in result_df[comparison]]

        # VISUALIZE DAILY ACTIVE USERS

        fig = plt.figure(figsize=(15, 8))
        ax = fig.add_subplot(111)

        ax.set_xlabel("Source")
        ax.set_ylabel(comparison)

        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel(comparison)

        plt.show()

        # exit()

    return


#TODO VISUALIZE THIS
def retention_rate_by_source(grammarly_df):

    grouped_by_source = grammarly_df.groupby('utmSource_cleaned')

    for name, group in grouped_by_source:
        cohort_slice = group[
            (group.index == datetime.strptime("2016-02-01", '%Y-%m-%d')) & (group['isFirst'] == True)]
        cohort_slice_cohort = list(set(cohort_slice['uid']))

        grouped_by_date = group.groupby('date')
        print name
        for date, dategroup in grouped_by_date:
            # print name, len(cohort_slice_cohort)
            if len(cohort_slice_cohort) > 0:
                print date, dategroup[dategroup['uid'].isin(cohort_slice_cohort)].uid.nunique(), float(
                    dategroup[dategroup['uid'].isin(cohort_slice_cohort)].uid.nunique()) / float(len(cohort_slice_cohort))

    return


#TODO EQUALLY WEIGHT PINGS AND DURATION; MEASURE
#TODO WHAT ABOUT AVERAGE TIME BETWEEN PINGS?

#TODO VISUALIZE EVALUATION BY TRAFFIC SOURCE

if __name__ == "__main__":
    main()