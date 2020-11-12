import datetime

def score_date(date):
    # calculate numeric value of date for sorting. Note, some dates have
    # same score, so we might not be able to use sets, or we can store list
    # of uid that have same score in same key.
    return int(datetime.datetime.strptime(date,'%a %b %d %H:%M:%S %z %Y').timestamp());

score_conv = {
    'created_at': score_date
}