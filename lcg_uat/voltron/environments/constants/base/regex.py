
class Regex(object):
    """
    For storing regex variables
    """
    BET_DATA_TIME_FORMAT = r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2})'
    EXPECTED_EACH_WAY_FORMAT_BET_RECEIPT = r'^EW:\s(\d*/\d*)\sOdds\s-\sPlaces\s(\d*-\d*)$'
    EXPECTED_EACH_WAY_FORMAT_DESKTOP_FUTURE = r'^(E/W)\s?([\d\/]*)\s(Places)\s([-\d]*)$'
    EXPECTED_EACH_WAY_FORMAT_FEATURED = r'^(E/W)\s?([\d/]*)\sodds\s-\splaces\s([-\d]*)$'  # Using on featured module/tab
    EXPECTED_EACH_WAY_FORMAT_EXTRA_PLACE = r'^([\d\/]*)\sthe\sOdds\s([\d-]*)$'
    EXPECTED_EACH_WAY_FORMAT = r'^(Each Way|EACH WAY|EW):\s?([\d\/]*)\s(ODDS|Odds|odds)\s-\s(PLACES|Places|places)(?:\s(\d+(?:-\d+)*))?$'
