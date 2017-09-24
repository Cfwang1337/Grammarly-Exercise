from datetime import datetime
from pandas import Timestamp
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

    date_index = list(set(grammarly_df.index))
    date_index = sorted(date_index)

    result_df = pd.DataFrame(columns=['date'])
    result_df['date'] = date_index
    result_df = result_df.set_index("date")

    for feb_date in ["04", "10", "14"]:

        date_to_format = '2016-02-{0}'.format(feb_date)

        cohort_slice = grammarly_df[(grammarly_df.index == datetime.strptime(date_to_format, '%Y-%m-%d')) & (grammarly_df['isFirst'] == True)]
        cohort_slice_cohort = list(set(cohort_slice['uid']))

        print "FEB {0} COHORT".format(feb_date), len(cohort_slice_cohort)

        sub_result_set = []

        for name, group in grouped_by_date:
            print name, group[group['uid'].isin(cohort_slice_cohort)].uid.nunique(), float(group[group['uid'].isin(cohort_slice_cohort)].uid.nunique())/float(len(cohort_slice_cohort))
            if group[group['uid'].isin(cohort_slice_cohort)].uid.nunique() > 0:
                sub_result_set.append([name, group[group['uid'].isin(cohort_slice_cohort)].uid.nunique(), float(group[group['uid'].isin(cohort_slice_cohort)].uid.nunique())/float(len(cohort_slice_cohort))])

        sub_result_df = pd.DataFrame(sub_result_set, columns=[
            "date",
            "uid_count_{0}".format(feb_date),
            "retention_rate_{0}".format(feb_date)
        ])
        sub_result_df = sub_result_df.set_index("date")
        result_df = result_df.join(sub_result_df, how='left')
    
    result_df.to_csv("retention_curve_feb.csv")

    sns.set_style("darkgrid")
    x_axis = mdates.date2num([datetime.strptime(str(d).split(" ")[0], '%Y-%m-%d').date() for d in result_df.index])
    y_axis_1 = [float(y) for y in result_df['retention_rate_04']]
    y_axis_2 = [float(y) for y in result_df['retention_rate_10']]
    y_axis_3 = [float(y) for y in result_df['retention_rate_14']]

    #VISUALIZE DAILY ACTIVE USERS

    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111)

    ax.set_xlabel("Date")
    ax.set_ylabel("Retention rate")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot_date(x_axis, y_axis_1, 'r-')
    plt.plot_date(x_axis, y_axis_2, 'b-')
    plt.plot_date(x_axis, y_axis_3, 'g-')
    plt.gcf().autofmt_xdate()
    plt.show()

    return


#COUNT BY SOURCE
def evaluate_source(grammarly_df):
    grouped_by_source = grammarly_df.groupby('utmSource_cleaned')

    total_users = grouped_by_source.uid.nunique()
    print total_users.sort_values(ascending=False)

    result_set = []

    for name, group in grouped_by_source:
        grouped_by_uid = group.groupby(['uid', 'date'])
        duration = []
        for uid, uid_group in grouped_by_uid:
            duration.append((max(uid_group['timestamp'].values) - min(uid_group['timestamp'].values))/3600000.0)

        print name, group.uid.nunique(), group.timestamp.nunique(), float(group.timestamp.nunique())/float(group.uid.nunique()), np.mean(duration)
        result_set.append([name, group.uid.nunique(), group.timestamp.nunique(), float(group.timestamp.nunique())/float(group.uid.nunique()), np.mean(duration)])

    result_df = pd.DataFrame(result_set, columns=[
        "Source",
        "UniqueUsers",
        "Pings",
        "PingsPerUser",
        "AverageDuration"
    ])

    result_df = result_df.set_index("Source")
    result_df.to_csv("evaluate_source.csv")

    for comparison in ["UniqueUsers", "Pings", "PingsPerUser", "AverageDuration"]:
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

    return


#TODO VISUALIZE THIS
def retention_rate_by_source(grammarly_df):

    date_index = list(set(grammarly_df.index))
    date_index = sorted(date_index)

    result_df = pd.DataFrame(columns=['date'])
    result_df['date'] = date_index
    result_df = result_df.set_index("date")

    grouped_by_source = grammarly_df.groupby('utmSource_cleaned')

    for name, group in grouped_by_source:
        cohort_slice = group[
            (group.index == datetime.strptime("2016-02-01", '%Y-%m-%d')) & (group['isFirst'] == True)]
        cohort_slice_cohort = list(set(cohort_slice['uid']))

        grouped_by_date = group.groupby('date')
        print name
        if len(cohort_slice_cohort) > 3:
            sub_result_set = []
            for date, dategroup in grouped_by_date:
                # print name, len(cohort_slice_cohort)

                print date, dategroup[dategroup['uid'].isin(cohort_slice_cohort)].uid.nunique(), float(
                    dategroup[dategroup['uid'].isin(cohort_slice_cohort)].uid.nunique()) / float(len(cohort_slice_cohort))
                sub_result_set.append([date, dategroup[dategroup['uid'].isin(cohort_slice_cohort)].uid.nunique(), float(
                    dategroup[dategroup['uid'].isin(cohort_slice_cohort)].uid.nunique()) / float(len(cohort_slice_cohort))])

            sub_result_df = pd.DataFrame(sub_result_set, columns=[
                "date",
                "count_{0}".format(name),
                "retention_rate_{0}".format(name)
            ])
            sub_result_df = sub_result_df.set_index("date")
            result_df = result_df.join(sub_result_df, how='left')

    result_df.to_csv("retention_curve_by_source.csv")

    sns.set_style("darkgrid")
    x_axis = mdates.date2num([datetime.strptime(str(d).split(" ")[0], '%Y-%m-%d').date() for d in result_df.index])
    y_axis_1 = [float(y) for y in result_df['retention_rate_answers']]
    y_axis_2 = [float(y) for y in result_df['retention_rate_biznesowe+rewolucje']]
    y_axis_3 = [float(y) for y in result_df['retention_rate_handbook']]
    y_axis_4 = [float(y) for y in result_df['retention_rate_mosalingua+fr']]
    y_axis_5 = [float(y) for y in result_df['retention_rate_other']]
    y_axis_6 = [float(y) for y in result_df['retention_rate_program']]
    y_axis_7 = [float(y) for y in result_df['retention_rate_shmoop_left']]
    y_axis_8 = [float(y) for y in result_df['retention_rate_twitter']]

    #VISUALIZE DAILY ACTIVE USERS

    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111)

    ax.set_xlabel("Date")
    ax.set_ylabel("Retention rate")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot_date(x_axis, y_axis_1, 'b-', label='answers')
    plt.plot_date(x_axis, y_axis_2, 'g-', label='biznesowe+rewolucje')
    plt.plot_date(x_axis, y_axis_3, 'r-', label='handbook')
    plt.plot_date(x_axis, y_axis_4, 'c-', label='mosalingua+fr')
    plt.plot_date(x_axis, y_axis_5, 'b-', label='other')
    plt.plot_date(x_axis, y_axis_6, 'y-', label='program')
    plt.plot_date(x_axis, y_axis_7, 'k-', label='shmoop_left')
    plt.plot_date(x_axis, y_axis_8, 'm-', label='twitter')

    plt.text(Timestamp('2016-02-29 00:00:00'), 0.65625, 'twitter')
    plt.text(Timestamp('2016-02-29 00:00:00'), 0.611111111111, 'shmoop_left')
    plt.text(Timestamp('2016-02-29 00:00:00'), 0.554945054945, 'answers')
    plt.text(Timestamp('2016-02-29 00:00:00'), 0.543766578249, 'biznesowe+rewolucje')
    plt.text(Timestamp('2016-02-29 00:00:00'), 0.525, 'mosalingua+fr')
    plt.text(Timestamp('2016-02-29 00:00:00'), 0.467741935484, 'program')
    plt.text(Timestamp('2016-02-29 00:00:00'), 0.4375, 'handbook')
    plt.text(Timestamp('2016-02-29 00:00:00'), 0.240479916536, 'other')

    plt.gcf().autofmt_xdate()
    plt.show()

    return


#TODO EQUALLY WEIGHT PINGS AND DURATION; MEASURE
#TODO WHAT ABOUT AVERAGE TIME BETWEEN PINGS?

#TODO VISUALIZE EVALUATION BY TRAFFIC SOURCE

if __name__ == "__main__":
    main()