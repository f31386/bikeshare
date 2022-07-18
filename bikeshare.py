# EXPLORE US BIKESHARE DATA
# =========================

# 2nd Project for Udacity Nanodegree 'Programming for Data Science with Python'

# created with Python 3.9.7, Numpy 1.20.3 and Pandas 1.3.4
# by Christian Schupp, ZF Friedrichshafen AG

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june'] # only the 1st 6 months
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_day():
    """
    Asks user to specify a weekday and checks if it is in the list 'days'

    Returns:
        (str) xday - name of the weekday
    """
    invalid_day = True
    while invalid_day:
        xday = input("Which day? \n").strip().lower()
        if xday in days: #correct input
            invalid_day = False #ends loop
        else: #invalid input
            print("Sorry, Input '{}' could not be processed, please type in a weekday, e.g. Monday, Tuesday, etc.".format(xday))
        
    return xday
    
def get_month():
    """
    Asks user to specify a month and checks if it is in the list 'months'
    
    note: the list 'months' only contains the first 6 months (january to june), because the provided
          data only covers these months

    Returns:
        (str) xday - name of the weekday
    """
    invalid_month = True
    while invalid_month:
        xmonth = input("Which month? (only from january to june)\n").strip().lower()
        if xmonth in months: #correct input
            invalid_month = False #ends loop
        else: #invalid input
            print("Sorry, Input '{}' could not be processed, please type in a month from january to june, e.g. 'january, february, etc.".format(xmonth))
    
    return xmonth

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. 

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    bikers = 5
    print("    ,__o    " * bikers)
    print("   _-\_<,   " * bikers)
    print("  (*)/'(*)  " * bikers)
    print("************" * bikers)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    invalid = True
    while invalid:
        city = input('Would you like to see data for Chicago, New York City, or Washington? \n')
        if city.strip().lower() == 'chicago' or city.strip().lower() == 'new york city' or city.strip().lower() == 'washington':
            city = city.strip().lower()
            invalid = False
        else: #invalid input
            print("Could not identyfy city '{}', please type in one of the city names mentioned.".format(city))
    
    # get user input for filtering (day, month)
    invalid = True
    while invalid:
        filt = input("Would you like to filter the data by month, day or both? Otherwise type 'no'. \n").strip().lower()
        if filt == 'no': # no filtering
            month = 'all'
            day = 'all'
            invalid = False
            
        elif filt == 'month': # only by month
            day = 'all'
            month = get_month() # get user input for month (all, january, february, ... , june)
            invalid = False

            
        elif filt == 'day':  # only by weekday
            month = 'all'
            day = get_day() # get user input for day of week (all, monday, tuesday, ... sunday)
            invalid = False

        
        elif filt == 'both': # by weekday and month  
            day = get_day() # get user input for day of week (all, monday, tuesday, ... sunday)
            month = get_month() # get user input for month (all, january, february, ... , june)
            invalid = False

        else: # illegible input
            print("Sorry, Input '{}' could not be processed, please try again ('month', day', 'both' or 'no').".format(filt))
            
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
    df['month'] = df['Start Time'].dt.month #month as integer
    df['day_of_week'] = df['Start Time'].dt.day_of_week
       
    # filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        #print(df['Start Time'].head())
           
    # filter by day of week if applicable
    if day != 'all':
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        df - df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month      :', months[most_common_month-1].title())

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', days[most_common_day].title())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour :', str(most_common_hour) + ':00 to', str(most_common_hour+1) + ':00')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        df - df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station                          :', most_common_start)

    # display most commonly used end station
    most_common_stop = df['End Station'].mode()[0]
    print('Most Commonly Used End   Station                          :', most_common_stop)

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' --> ' + df['End Station']
    most_common_combination = df['combination'].mode()[0]
    print('Most Frequent Combination of Start Station and End Station:', most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        df - df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time:', np.sum(pd.to_timedelta(df['Trip Duration'], 'Sec')))

    # display mean travel time
    print('Mean  Travel Time:', np.mean(pd.to_timedelta(df['Trip Duration'], 'Sec')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        df - df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of User Types:')
    users = df['User Type'].fillna('not specified').unique()
    for user in users:
        if user == 'not specified':
            print(' - User Type not Specified, Count:', np.sum(df['Gender'].isnull()))
        else:
            print(' - Usertype:', user + '; Count:', df['User Type'].value_counts()[user])

    # Display counts of gender
    print('\nCounts of Gender:')
    # if 'Gender' in df.columns:
    try:
        genders = df['Gender'].fillna('not specified').unique()
        for gender in genders:
            if gender == 'not specified':
                print(' - Gender not specified; Count:', np.sum(df['Gender'].isnull()))
            else:
                print(' - Gender:', gender + '; Count:', df['Gender'].value_counts()[gender])        
    # else:
    except KeyError:
        print(' - Sorry, no data about gender avaliable for this city')

    # Display earliest, most recent, and most common year of birth
    print('\n Counts by Year of Birth')
    try:
        print(' - Earliest   :',int(np.min(df['Birth Year'].dropna(axis=0))))
        print(' - Most Recent:',int(np.max(df['Birth Year'].dropna(axis=0))))
        print(' - Most Common:',int(df['Birth Year'].dropna(axis=0).mode()[0]))
    except KeyError:
        print(' - Sorry, no data about birth year avaliable for this city')
    
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    """
    Displays (next) 5 lines of the filtered raw data, as long as the user does not type 'no'
    or there are no more lines left.
    
    Args:
        df - df - Pandas DataFrame containing city data filtered by month and day
    """
    show_data = True
    line = 0
    num_lines = df['Start Time'].count()
    while show_data:
        user_input = input('\nWould you like to see (the next) 5 lines of raw_data? Enter yes or no.\n').strip().lower()
        if user_input != 'no':
            if line > (num_lines - 5): # 5 or less lines left
                show_data = False #exit while loop
                print('\nLast five lines of raw data:')
                line = num_lines - 5
                
            for n in range(5):
                print('-'*40)
                print(df.iloc[line, :-4])  # last four lines are no raw data
                line += 1
                
        else: # user_input = 'no'
            show_data = False

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.strip().lower() != 'yes':
            print("\n", '-'*40, "\n  Good Bye!\n", '-'*40)
            break


if __name__ == "__main__":
	main()
