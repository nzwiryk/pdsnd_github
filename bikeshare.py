import time
import pandas as pd

# maps city name to data file
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
# mapping city names to normalized terms
VALID_CITY_NAMES = {'chicago': 'chicago',
                    '1': 'chicago',
                    'nyc': 'new york city',
                    'new york': 'new york city',
                    'new york city': 'new york city',
                    '2': 'new york city',
                    'washington': 'washington',
                    '3': 'washington'
                    }
# define months for filtering
MONTHS = ['all',
          'january',
          'february',
          'march',
          'april',
          'may',
          'june',
          ]
# dict to normalize user input
VALID_MONTHS = {month: month for month in MONTHS}
# add numeric values so user can enter '1' for january
VALID_MONTHS.update({str(num): month for num, month in enumerate(MONTHS)})
# why not, let's add abbreviations - 'jan' will now select january
VALID_MONTHS.update({month[0:3]: month for month in MONTHS})
# define days for filtering - note monday is index zero to sync with pd.DateTimeIndex
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
VALID_DAYS = {day: day for day in DAYS}
# add numeric values - starting at 1 for monday - so user can select day by numbered list
VALID_DAYS.update({str(num + 1): day for num, day in enumerate(DAYS)})
# day abbreviations - tue is tuesday, etc.
VALID_DAYS.update({day[0:3]: day for day in DAYS})


def get_filters() -> tuple[str, str, str]:
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # bools to keep while loop alive until valid input found
    valid_city_input = False
    valid_month_input = False
    valid_day_input = False
    # gets user input for city, waits for valid input
    while not valid_city_input:
        city_input = str(input(
            "Enter the name of the city you would like to analyze:\n"
            "1. chicago \n"
            "2. new york city\n"
            "3. washington.\n")).lower()
        # tries to lookup user input - catches exception and prints try again statement
        try:
            city = VALID_CITY_NAMES[city_input]
            valid_city_input = True
        # if user input is no good, kick out this message
        except KeyError:
            print('please enter a valid selection: chicago, new york city, or washington:\n')

    # gets user month, similar structure as the data input
    while not valid_month_input:
        month_input = str(input(
            'Enter the month to filter by - or enter \'all\':\n'
            '0. All\n'
            '1. January\n'
            '2. February\n'
            '3. March\n'
            '4. April\n'
            '5. May\n'
            '6. June\n'
        )).lower()
        # checks to see if user input is a valid month
        try:
            month = VALID_MONTHS[month_input]
            valid_month_input = True
        except KeyError:
            print('please enter a valid month to filter by, or enter or enter \'all\':\n')

    # gets user day filter input, checks validity
    while not valid_day_input:
        day_input = str(input('Please enter the day of the week you would like to filter by or enter \'all\':\n'
                              '1. Monday\n'
                              '2. Tuesday\n'
                              '3. Wednesday\n'
                              '4. Thursday\n'
                              '5. Friday\n'
                              '6. Saturday\n'
                              '7. Sunday\n'
                              '8. All\n')).lower()
        # check user input against valid day dict to normalize
        try:
            day = VALID_DAYS[day_input]
            valid_day_input = True
        except KeyError:
            print('please enter a valid day of the week to filter by, or enter \'all\':\n')

    print('-' * 40)
    return city, month, day


def load_data(city: str, month: str, day: str) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        (pd.DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    # gets the filename depending on the city
    city_datafile = CITY_DATA[city]
    # defines what columns are timestamps
    date_columns = ['Start Time', 'End Time']
    # reads in dataframe from city data file
    # reads first column as index and to_datetimes date_columns on loading
    df = pd.read_csv(f'{city_datafile}', index_col=0, parse_dates=date_columns)
    # 1 = january, 12 = december
    # creates month column from start time
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    # monday = 0, sunday = 6
    # creates day of week column from start time
    df['day'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    # check if user applied month filter and filters
    # if they did, apply filter
    if month != 'all':
        df = df[df.month == MONTHS.index(month)]
    # check if user applied day filter and filters
    # if they did, apply filter
    if day != 'all':
        df = df[df.day == DAYS.index(day)]
    return df


def time_stats(df: pd.DataFrame):
    """
    Displays statistics on the most frequent times of travel.

    Prints the most common month, day, and hour of travel.
    Also prints time to run.

    Args:
        (pd.DataFrame) df - input dataframe containing filtered data to be analyzed
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # gets the most common month of travel using mode
    most_common_month = MONTHS[int(df['month'].mode())]
    print(f'the most common month is {most_common_month}')
    # gets the most common day of travel and prints
    most_common_day = DAYS[int(df['day'].mode())]
    print(f'the most common day of the week is {most_common_day}')
    # gets the most common start hour and prints
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    most_common_hour = int(df['hour'].mode())
    print(f'the most common hour of the day is {most_common_hour}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df: pd.DataFrame):
    """
    Displays statistics on the most popular stations and trips.

    Gets:
      - the most common start station
      - the most common end station
      - the most common trip (start/end combination)

    Args:
        (pd.DataFrame) df - input dataframe containing filtered data to be analyzed

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # gets the most common starting station via mode and prints
    most_common_start = str(df['Start Station'].mode()[0])
    print(f'the most commonly used start station is {most_common_start}')
    # gets the most common ending station via mode and prints
    most_common_end = str(df['End Station'].mode()[0])
    print(f'the most commonly used end station is {most_common_end}')
    # concatenates start and end station to get trip data
    df['trip'] = df.apply(lambda x: str(x['Start Station']) + ' to ' + str(x['End Station']), axis=1)
    # uses mode on new trip column to get the most commons start/end combination
    most_common_trip = str(df['trip'].mode()[0])
    print(f'the most common start and end station combination is {most_common_trip}')
    # prints total time to calculate station stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df: pd.DataFrame):
    """
    Displays statistics on the total and average trip duration.

    Args:
        (pd.DataFrame) df - input dataframe containing filtered data to be analyzed

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # gets total travel time by summing trip duration amd prints
    total_travel_time = df['Trip Duration'].sum()
    print(f'The total travel time is {str(total_travel_time)} seconds')
    # gets the average trip time by mean function and prints
    mean_travel_time = df['Trip Duration'].mean()
    print(f'The average (mean) travel time is {str(mean_travel_time)} seconds')
    # prints time to calculate trip duration stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df: pd.DataFrame, city: str):
    """Displays statistics on bikeshare users.

    Prints user counts by type, gender, and age.

    Args:
        (pd.DataFrame) df - input dataframe containing filtered data to be analyzed
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # gets count of each user type
    user_type_stats = df['User Type'].value_counts()
    print('Customer counts by user type:')
    # since value_counts is a pd.Series, lets to_string it to make printing prettier
    print(user_type_stats.to_string(index=True))
    # gets count by gender with value_counts
    if city != 'washington':
        user_gender_stats = df['Gender'].value_counts()
        print('Customer counts by gender:')
        # similar to above, to_string and print the user_gender_stats
        print(user_gender_stats.to_string(index=True))
        # drops any null birth year to avoid screwing up min/max
        yob = df['Birth Year'].dropna()
        # prints oldest, newest birth year, as well as the most common year
        print(f'the earliest user birth year is {int(yob.min())}')
        print(f'the most recent user birth year is {int(yob.max())}')
        print(f'the most common user birth year is {int(yob.mode())}')
    # print stats to calc user stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(df: pd.DataFrame, start_index: int = 0, increment: int = 5):
    """
    Prints slices of raw data recursively until user inputs otherwise
    :param df: input filtered dataframe to view
    :param start_index: start position to show raw data
    :param increment: how many rows to show at a time
    """
    # end row for printing slice
    end_index = start_index + increment
    print(df.iloc[start_index:end_index].to_string(index=False))
    # prompts user if they want to see more data
    view_raw_next = str(input('\nWould you like to view more raw data? Enter yes or no.\n'))
    if view_raw_next.lower() == 'yes' or view_raw_next.lower() == 'y':
        # calls recursively until user doesn't want to see more
        if end_index + increment > len(df):
            # if the next print will go beyond length of dataframe, adjust call to avoid issues
            show_raw_data(df, start_index=end_index, increment=len(df) - end_index)
        elif end_index >= len(df):
            print('no more raw data to show')
        else:
            show_raw_data(df, start_index=end_index, increment=increment)


# defines main function, which will be run when this script is executed
def main():
    # keeps alive until break
    while True:
        # loads city/month/day from user input
        city, month, day = get_filters()
        # loads data from parsed user input
        df = load_data(city, month, day)
        # gets time stats and prints
        time_stats(df)
        # gets station stats and prints
        station_stats(df)
        # gets trip duration stats and prints
        trip_duration_stats(df)
        # gets user stats and prints
        user_stats(df, city)
        # checks if user wants to read raw data
        view_raw_data = str(input('\nWould you like to view raw data? Enter yes or no.\n'))
        if view_raw_data.lower() == 'yes' or view_raw_data.lower() == 'y':
            show_raw_data(df)

        # prompts user for restarting script
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            print('exiting...')
            break


# if this python script is executed (as opposed to imported from another script), run main
if __name__ == "__main__":
    main()


