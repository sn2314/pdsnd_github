#-------------------------------------------------------------------------------
# Name:        Explore US BikeShare data
# Purpose:     Print Statistics about US Bikeshare
#
# Author:      sn2314(Sarfraz Nayeem)
#
# Created:     01/16/2020
# Copyright:   (c) Sarfraz Nayeem 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.


    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    months=['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days=['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
           city = input("Please enter city among chicago, new york city, washington:").lower()
           if city not in CITY_DATA:
              city = input("Please re- enter right city among chicago, new york city, washington :")
              continue
           else:
              break


    # get user input for month (all, january, february, ... , june)
    while True:
            month = input('Please enter month among -January,February,March,April,May or June? Please enter month in full. otherwise enter "all": ').lower()
            if month not in months:
                print('Please re-enter right month among January,February,March,April,May or June')
                continue
            else:
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input('Please enter day among-Monday,Tuesday,Wednesday,Thursday,Friday,Saturday or Sunday ?Please enter day in full. otherwise enter "all": ').lower()
            if day not in days:
                print('Please re-enter right day among Monday,Tuesday,Wednesday,Thursday,Friday,Saturday or Sunday')
                continue
            else:
                break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
    df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #print("Month in load fn",df['Start Time'].dt.month)

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # filter by month to create the new dataframe


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n #1 Calculating The Popular times of travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is ', most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most common day of week is ', most_common_day)

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('The most common Hour of the day is ', most_common_start_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n #2.Calculating The  Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    #most_common_start_station = df['Start Station'].mode()[0]
    print('The correct most common start station is ',df['Start Station'].value_counts().idxmax())
    #print('The most common start station is ', most_common_start_station)
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is ', most_common_end_station)


    # display most frequent combination of start station and end station trip
    df['comb'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_combo = df['comb'].mode()[0]
    print('The most common trip from start to end is ', most_common_combo)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n #3.Calculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is {} seconds '.format(total_travel_time))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time is {} seconds'.format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    print('\n #4.Calculating User Info...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    sus_count = user_type_count.iloc[0]
    print('There are {} users that are suscribers'.format(sus_count))
    cus_count = user_type_count.iloc[1]
    print('There are {} users that are customers'.format(cus_count))
    nouser_type_count = df['User Type'].isnull().sum()
    print('There are {} unidentified user types'.format(nouser_type_count))
    dep_type_count = df['User Type'].size - (sus_count + cus_count + nouser_type_count)
    print('There are {} users that are dependent'.format(dep_type_count))

    #Check for gender column
    try:
        if 'Gender' in df['Gender']:
        # Display counts of gender
            gender_type_count = df['Gender'].value_counts()
            male_count = gender_type_count.iloc[0]
            print('There are {} males'.format(male_count))
            female_count = gender_type_count.iloc[1]
            print('There are {} females'.format(female_count))
            nogender_type_count = df['Gender'].isnull().sum()
            print('There are {} unidentified genders'.format(nogender_type_count))
        else:
            print('Gender information is not available for this city')
    except KeyError:
        print("\nEarliest Year:\nNo Gender available for this month.")


    try:
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest birth year is:', earliest_birth_year)
    except KeyError:
        print("\nEarliest Year:\nNo data available for this month.")


    try:
        most_recent_year = df['Birth Year'].max()
        print('\nMost Recent birth Year:', most_recent_year)
    except KeyError:
        print("\nMost Recent birth Year:\nNo data available for this month.")

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year of birth:', most_common_year)
    except KeyError:
        print("\nMost Common Year:\nNo data available for this month.")


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def display_data(df):
    #get user input for data displaying successive five rows of data at a time
   i = 0
   j = 5
   dat = input("\n Would you like to view first 5 rows of data. Please write 'yes' or 'no' \n").lower()
   while True:

       if dat.lower() == 'no':
           return


       if dat.lower() == 'yes':
           #Code Review issue 1 fixed.Initializing the loop incorrectly
            print(df.iloc[i:j])
            dat= input("\n Would you like to see five more rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()
            i =i+ 5
            j =j+ 5







def main():


    while True:

       city,month,day = get_filters()
       df=load_data(city, month, day)
       time_stats(df)
       station_stats(df)
       trip_duration_stats(df)
       user_stats(df)
       #disp_raw_data(df)
       display_data(df)

       restart = input('\nWould you like to restart? Enter yes to restart or no.\n')
       if restart.lower() != 'yes':
            break


# execute MAIN fn.
if __name__ == '__main__':
    main()
