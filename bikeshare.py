import time
import pandas as pd
import numpy as np
import datetime 

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    print('for the follwing Cities: Chicago, New York City, Washington')
    print()
    
    city=""
    month=""
    day=""
    raw_data=""

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while city not in ['Chicago', 'New York City', 'Washington']:
        print('\n* ONLY city from this list [Chicago, New York City, Washington] is accepted.')
        city=input('Please, Enter the name of the City:').title()


    # get user input for month (all, january, february, ... , june)
    while month not in ['All', 'January', 'February', 'March' ,'April','May','June']:
        print('\n* ONLY month from this list [January, February, March ,April,May,'
              'June] is accepted. \n* OR use All to get no month filter')
        month=input('Please, Enter the name of the Month to filter with:').title()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ['All', 'Sunday', 'Monday', 'Tuesday' ,'Wednesday','Thursday','Friday','Saturday']:
        print('\n* ONLY day from this list [Sunday, Monday, Tuesday ,Wednesday,Thursday'
              ',Friday, Saturday]. \n* OR use All to get no day filter')
        day=input('please, Enter the name of the Day to filter with:').title()

        if day in ['All', 'Sunday', 'Monday', 'Tuesday' ,'Wednesday','Thursday','Friday','Saturday']:
            print('\n* Do you like to see some overview for the raw data before filtering?')
            raw_data=input('Please, Enter yes if you like:').lower()
            

    print('-'*40)
    print()

    return city, month, day, raw_data


def load_data(city, month, day,raw_data ):
    """
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """


    df=pd.read_csv(CITY_DATA[city])

    if raw_data.lower() in ['yes','y']:
        print('*** Information about the raw {} bikeshare data ***\n'.format(city))
        print(df.info())
        print()
        print('Data contains the follwing columns for  analysis: ')
        for col in list(df.columns)[1:]:
                        print ("    ",col)
        print()
        print(df.head())

    print ('\n*** The follwing statistics is for {} bikeshare data ***\n'.format(city))

    # Convert time columns to datetime format
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])

    # To Add Month , Week_day , hour , trip_min and start_stop Columns
    df['month']=df['Start Time'].dt.month_name()
    df['week_day']=df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour
    df['trip_min']=df['End Time'].dt.minute-df['Start Time'].dt.minute
    df['start_stop']=df['Start Station']+' to '+df['End Station']

    #print("This took %s seconds to load and prepare selected data.\n" % (time.time() - start_time))
    
    
    if month=='All':                # if No filter by Month
        if day=='All':
            print ('** Data is viewed without any filter **\n')
            return df
        elif day!='All':
            print ('** Data is filtered by Day only: Selected week day is {} **\n'.format(day))
            return df.query('week_day=="{}"'.format(day))
                   
    else:                           # if There is filter by Month
        if day=='All':
            print ('** Data is filtered by Month only: Selected month is {} **\n'.format(month))
            return df.query('month=="{}"'.format(month))
        else:
            print ('** Data is filtered by both month and day: Selected month is {} and week day is {} **\n'.format(month,day))
            return df.query('month=="{}" and week_day=="{}"'.format(month,day))




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('-'*40)
    print('\n    1. Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df.month.value_counts().count()==1:
        print('Please, remove month filter to display the most frequent month in the selected data')
    else:
        print ('The most frequent month in the selected data is {} with ' 
       'total of {} trips.'.format(df.month.value_counts().reset_index()['index'][0],
       df.month.value_counts().reset_index()['month'][0]))

    # display the most common day of week
    if df.week_day.value_counts().count()==1:
        print('Please, remove day filter to display the most frequent day in the selected data')
    else:
        print ('The most frequent day in the selected data is {} with ' 
       'total of {} trips.'.format(df.week_day.value_counts().reset_index()['index'][0],
       df.week_day.value_counts().reset_index()['week_day'][0]))

    # display the most common start hour
    print ('The most frequent hour in the selected data is hr {:.0f}:00 with ' 
       'total of {} trips.'.format(df.hour.value_counts().reset_index()['index'][0],
       df.hour.value_counts().reset_index()['hour'][0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n    2. Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print ('The most frequent Start Station in the selected data is {} with ' 
       'total of {} trips.'.format(df['Start Station'].value_counts().reset_index()['index'][0],
       df['Start Station'].value_counts().reset_index()['Start Station'][0]))
    print()

    # display most commonly used end station
    print ('The most frequent End Station in the selected data is {} with ' 
       'total of {} trips.'.format(df['End Station'].value_counts().reset_index()['index'][0],
       df['End Station'].value_counts().reset_index()['End Station'][0]))
    print()

    # display most frequent combination of start station and end station trip
    print ('The most frequent start_stop stations in the selected data is {} with ' 
       'total of {} trips.'.format(df['start_stop'].value_counts().reset_index()['index'][0],
       df['start_stop'].value_counts().reset_index()['start_stop'][0]))
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n    3. Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time in the selected data is {:.2f} minutes equivalent to {:.0f} days'.format(df['Trip Duration'].sum()/60,
        df['Trip Duration'].sum()/(60*60*24)))
    print()

    # display mean travel time
    print('Average travel time in the selected data is {:.0f} seconds equivalent to {:.1f} minutes'.format(df['Trip Duration'].mean(),
        df['Trip Duration'].mean()/60))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n    4. Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Number of different User Types are:\n')
    print(df['User Type'].value_counts(),'\n')

    # Display counts of gender
    if 'Gender' in list(df.columns):
        print('Counts for gender are:\n')
        print(df['Gender'].value_counts(),'\n')
    else:
        print('Gender data is not available for this data')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in list(df.columns):
        print('Statistics for Birth Year are:\n')
        print('The earliest year of birth is {:.0f}'.format(df['Birth Year'].min()))
        print('The recent year of birth is {:.0f}'.format(df['Birth Year'].max()))
        print ('The most common year of birth in the selected data is {:.0f} with ' 
       'total of {:.0f} counts.'.format(df['Birth Year'].value_counts().reset_index()['index'][0],
       df['Birth Year'].value_counts().reset_index()['Birth Year'][0]))
        print()
    else:
        print('Birth Year data is not available for this data')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, raw_data = get_filters()
        df = load_data(city, month, day, raw_data)         # the saved df now is the filter df

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
