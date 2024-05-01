import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = list(CITY_DATA.keys())

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Choose a city: \nChicago, New York or Washington\n').lower()

    while city not in cities:
            city = input('Sorry, I don\'t recognize that city. Please try again\n').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    all_months = input('Would you like to filter by month? Y / N ').lower()
    while all_months != 'y' and all_months != 'n':
        all_months = input('Not sure what you mean. Can you choose again please: Y / N ').lower()

    if all_months == 'y':
        month = input('Choose the month you want to filter by: \nJanuary, February, March, April, May, June\n').lower()
        while month not in months:
            month = input('Sorry, I don\'t recognize that month. Please try again\nJanuary, February, March, April, May, June\n').lower()
    elif all_months == 'n':
        month = 'all'

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    all_days = input("Would you like to filter by a specific day? Y / N ").lower()
    while all_days != 'y' and all_days != 'n':
        all_days = input('Not sure what you mean. Can you choose again please: Y / N ').lower()

    if all_days == 'y':
        day = input("Choose the day you want to filter by: \nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n").lower()
        while day not in days:
            day = input('Sorry, I don\'t recognize that day. Please try again\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday\n').lower()
    elif all_days == 'n':
        day = 'all'

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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = int(df['month'].mode()[0])
    common_month_name = months[common_month - 1]
    print(f'The most common month is: {common_month_name}\n')

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f'The most common day is: {common_day}\n')

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f'The most common start hour is: {common_hour}\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f'The most common start station is: {start_station}\n')

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f'The most common end station is: {end_station}\n')

    # TO DO: display most frequent combination of start station and end station trip
    df['Start - End Stations'] = df['Start Station'] + ' to ' + df['End Station']
    start_end_stations = df['Start - End Stations'].mode()[0]
    print(f'The most frequent combination of start station and end station trip is from {start_end_stations}\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = df['Trip Duration'].sum() / 60 / 60
    print(f'Total travel time is: {total_travel:0.2f} hours')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print(f'The average travel time is: {mean_travel_time:0.2f} minutes')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The statistics of user types are: ')
    print(user_types)
    print()

    # TO DO: Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print('The statistics of user gender are: ')
        print(user_gender)
        print()
    except KeyError:
        print('There is no gender data for this city')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])

        print(f'Our oldest user was born in {earliest_birth}')
        print(f'Our youngest user was born in {most_recent_birth}')
        print(f'However the most common year of birth is {most_common_birth}')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except KeyError:
        print('There is no birth date data for this city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Displays raw data
def raw_data(df):
    raw_data = input('Would you like to see 5 lines of raw data? Y / N ').lower()
    row_index = 5
    while raw_data == 'y':
        try:
            print(df.head(row_index))
            raw_data = input('Would you like to see 5 more lines of raw data? Y / N ').lower()
            row_index += 5
        except:
            print('There are no more rows to show')

    print('-'*40)


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
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()