import datetime

"""
It is possible to add range functionality to any data type that we want 
to store.

tl;dr: create a scoring function which returns an integer representing
the score of the data, and add to `score_conv` map.

For example, if we wanted to add range functionality to twitter handlers,
(get usernames that start with 'a' -> 'c'), we can define a new function
and add it to score_conv in this way:

# Get the lexicographic value(Unicode) of the twitter handler.
def score_handler(twitter_handler):
    # This function will convert 'twitter_handler' to an integer representation
    # such that 'a' < 'b'
    pass

# 'screen_name' is the column name that we want to use range on.
score_conv = {
    'created_at': score_date,
    'screen_name': score_handler
}

"""

def score_date(date):
    """ Calculate the numeric value of date for sorting.
    
    @Params
    date : date as string in format of 'day_of_week month day hh:mm:ss +timezome yyyy'
        i.e.: 'Wed Nov 11 19:25:39 +0000 2020'
    
    @Returns Integer value of the date string.

    """
    return int(datetime.datetime.strptime(date,'%a %b %d %H:%M:%S %z %Y').timestamp());

"""
Dictionary of columns that supports range querying.
key = column_name : value = function_handle
"""
score_conv = {
    'created_at': score_date
}
