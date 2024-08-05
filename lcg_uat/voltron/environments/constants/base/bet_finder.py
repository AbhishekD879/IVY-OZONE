
class BetFinder(object):
    """
    src/app/lazy-modules/locale/translations/en-US/bf.lang.ts
    """
    BET_FINDER = 'Bet Filter'
    BET_FINDER_RESULTS = 'Bet Filter Results'
    BF_HEADER_TITLE = 'BET FILTER'
    BF_HEADER_TEXT = 'Use filters or Coral\'s Digital Tipster to find your best bets, also save your selection for future use.'
    BF_HEADER_MESSAGE = 'Create your search below:'
    BF_HEADER_MESSAGE_HORSERACING = BF_HEADER_MESSAGE
    BF_HEADER_TEXT_LADBROKES = 'Use the below filters to find the bet that suits you best. Save your selections so you can quickly browse your runners in future.'

    SEARCH_BY = 'Search by Horse, Trainer or Jockey'
    TYPE_HERE = 'Type here...'
    SORT_BY = 'Sort by'
    ODDS = 'Odds'
    ODDS_RANGE = 'Odds Range'
    PROVEN_GROUND = 'Proven on the Ground'
    TIME = 'Time'
    FORM = 'Form:'

    COURSE_WINNER = 'Course Winner'
    DISTANCE_WINNER = 'Distance Winner'
    WINNER_LAST_TIME = 'Winner Last Time'
    WINNER_LAST_3_STARTS = 'Winner Within Last 3'
    PLACED_LAST_TIME = 'Placed Last Time'
    PLACED_LAST_3_STARTS = 'Placed Within Last 3'
    COURSE_DISTANCE_WINNER = 'Course and Distance Winner'
    GOING_GROUND_TYPE = 'Going (Ground Type)'
    PROVEN_GOING = 'Proven'
    SUPERCOMPUTER_FILTERS = 'Digital Tipster Filters'
    SELECTION_SUPERCOMPUTER = 'Selection'
    ALTERNATIVE_SUPERCOMPUTER = 'Alternative'
    EACH_WAY_SUPERCOMPUTER = 'Each-Way'
    SELECT_STAR_RATING = 'Select Star Rating'
    MEETINGS = 'Meetings'
    ALL_MEETINGS = 'All Meetings'
    RESET = 'Reset'
    RESET_FILTERS = 'Reset filters'
    SAVE_SELECTION = 'Save Selection'
    FIND_BETS = 'Find Bets'
    SELECTION = 'selection'
    NO_SELECTION = 'NO SELECTIONS FOUND'
    NO_RESULTS = 'No result found'
    FOUND = 'found'
    RESULTS = 'Result'

    ODDS_0 = 'Odds On'
    ODDS_1 = 'Evens - 7/2'
    ODDS_4 = '4/1 - 15/2'
    ODDS_8 = '8/1 - 14/1'
    ODDS_16 = '16/1 - 28/1'
    ODDS_32 = '33/1 or Bigger'
    ODDS_LIST = [ODDS_0, ODDS_1, ODDS_4, ODDS_8, ODDS_16, ODDS_32]
    DTF = ['SELECTION', 'ALTERNATIVE', 'EACH-WAY']  # DTF = Digital Tipster Filters

    SELECT_CRITERIA_FOR_TEAMS_TEXT = 'Select criteria for the teams you wish to bet on.'
    YOUR_TEAMS_CRITERIA_INFO = 'High Scoring - Teams ranked in the top half of their division by most goals scored.\n' \
                               'Mean Defence - Teams ranked in the top half of their division by fewest goals conceded.\n' \
                               'Favourite - Teams priced shorter than their opponents to win their match.\n' \
                               'Outsider - Teams priced longer than their opponents to win their match.'

    SELECT_CRITERIA_FOR_OPPOSITION_TEXT = 'Select criteria for the teams you wish to bet against.'
    THE_OPPOSITION_CRITERIA_INFO = 'High Scoring - Teams ranked in the top half of their division by most goals scored.\n' \
                                   'Leaky Defence - Teams ranked in the bottom half of their division by fewest goals conceded.'
    FB_BET_FILTER_PLAYING_AT_TEXT = 'PLAYING AT'
    FB_BET_FILTER_HOME = 'Home'
    FB_BET_FILTER_AWAY = 'Away'
    FB_BET_FILTER_LAST_GAME_TEXT = 'LAST GAME'
    FB_BET_FILTER_WIN = 'Win'
    FB_BET_FILTER_DRAW = 'Draw'
    FB_BET_FILTER_LOSE = 'Lose'
    FB_BET_FILTER_LAST_GAMES_POINTS_TOTAL_TEXT = 'LAST 6 GAMES POINTS TOTAL'
    FB_BET_FILTER_ZERO_SIX_POINTS = '0 - 6 Points'
    FB_BET_FILTER_SEVEN_TWELVE_POINTS = '7 - 12 Points'
    FB_BET_FILTER_THIRTEEN_EIGHTEEN_POINTS = '13 - 18 Points'
    FB_BET_FILTER_KEY_TRENDS_TEXT = 'KEY TRENDS'
    FB_BET_FILTER_HIGH_SCORING = 'High Scoring'
    FB_BET_FILTER_MEAN_DEFENCE = 'Mean Defence'
    FB_BET_FILTER_CLEAN_SHEET_LAST_GAME = 'Clean Sheet Last Game'
    FB_BET_FILTER_LEAGUE_POSITIONS_TEXT = 'LEAGUE POSITIONS'
    FB_BET_FILTER_TOP_HALF = 'Top Half'
    FB_BET_FILTER_BOTTOM_HALF = 'Bottom Half'
    FB_BET_FILTER_ABOVE_OPPOSITION = 'Above Opposition'
    FB_BET_FILTER_ODDS_TEXT = 'ODDS'
    FB_BET_FILTER_FAVOURITE = 'Favourite'
    FB_BET_FILTER_OUTSIDER = 'Outsider'

    FB_BET_FILTER_LAST_GAME = 'LAST GAME'
    FB_BET_FILTER_OPPOSITION_WIN = 'Win'
    FB_BET_FILTER_OPPOSITION_DRAW = 'Draw'
    FB_BET_FILTER_OPPOSITION_LOSE = 'Lose'
    FB_BET_FILTER_OPPOSITION_LAST_GAMES_POINTS_TOTAL_TEXT = 'LAST 6 GAMES POINTS TOTAL'
    FB_BET_FILTER_OPPOSITION_ZERO_SIX_POINTS = '0 - 6 Points'
    FB_BET_FILTER_OPPOSITION_SEVEN_TWELVE_POINTS = '7 - 12 Points'
    FB_BET_FILTER_OPPOSITION_THIRTEEN_EIGHTEEN_POINTS = '13 - 18 Points'
    FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT = 'KEY TRENDS'
    FB_BET_FILTER_OPPOSITION_HIGH_SCORING = 'High Scoring'
    FB_BET_FILTER_OPPOSITION_LEAKY_DEFENCE = 'Leaky Defence'
    FB_BET_FILTER_OPPOSITION_CONCEDED_LAST_GAMES = 'Conceded 2+ Last Games'
    FB_BET_FILTER_OPPOSITION_LEAGUE_POSITIONS_TEXT = 'LEAGUE POSITIONS'
    FB_BET_FILTER_OPPOSITION_TOP_HALF = 'Top Half'
    FB_BET_FILTER_OPPOSITION_BOTTOM_HALF = 'Bottom Half'
    FB_BET_FILTER_OPPOSITION_BELOW_OPPOSITION = 'Below Opposition'

    EXPECTED_EXPECTED_LIST_OF_YOUR_TEAMS_CATEGORIES = \
        [FB_BET_FILTER_PLAYING_AT_TEXT, FB_BET_FILTER_HOME, FB_BET_FILTER_AWAY, FB_BET_FILTER_LAST_GAME_TEXT,
         FB_BET_FILTER_WIN, FB_BET_FILTER_DRAW, FB_BET_FILTER_LOSE, FB_BET_FILTER_LAST_GAMES_POINTS_TOTAL_TEXT,
         FB_BET_FILTER_ZERO_SIX_POINTS, FB_BET_FILTER_SEVEN_TWELVE_POINTS, FB_BET_FILTER_THIRTEEN_EIGHTEEN_POINTS,
         FB_BET_FILTER_KEY_TRENDS_TEXT, FB_BET_FILTER_HIGH_SCORING, FB_BET_FILTER_MEAN_DEFENCE,
         FB_BET_FILTER_CLEAN_SHEET_LAST_GAME, FB_BET_FILTER_LEAGUE_POSITIONS_TEXT, FB_BET_FILTER_TOP_HALF,
         FB_BET_FILTER_BOTTOM_HALF, FB_BET_FILTER_ABOVE_OPPOSITION, FB_BET_FILTER_ODDS_TEXT,
         FB_BET_FILTER_FAVOURITE, FB_BET_FILTER_OUTSIDER]

    EXPECTED_LIST_OF_OPPOSITION_CATEGORIES = \
        [FB_BET_FILTER_LAST_GAME, FB_BET_FILTER_OPPOSITION_WIN, FB_BET_FILTER_OPPOSITION_DRAW,
         FB_BET_FILTER_OPPOSITION_LOSE,
         FB_BET_FILTER_OPPOSITION_LAST_GAMES_POINTS_TOTAL_TEXT, FB_BET_FILTER_OPPOSITION_ZERO_SIX_POINTS,
         FB_BET_FILTER_OPPOSITION_SEVEN_TWELVE_POINTS, FB_BET_FILTER_OPPOSITION_THIRTEEN_EIGHTEEN_POINTS,
         FB_BET_FILTER_OPPOSITION_KEY_TRENDS_TEXT, FB_BET_FILTER_OPPOSITION_HIGH_SCORING,
         FB_BET_FILTER_OPPOSITION_LEAKY_DEFENCE, FB_BET_FILTER_OPPOSITION_CONCEDED_LAST_GAMES,
         FB_BET_FILTER_OPPOSITION_LEAGUE_POSITIONS_TEXT, FB_BET_FILTER_OPPOSITION_TOP_HALF,
         FB_BET_FILTER_OPPOSITION_BOTTOM_HALF, FB_BET_FILTER_OPPOSITION_BELOW_OPPOSITION]

    FB_BET_FILTER_BET_PAYS = '£10.00 bet pays'
    FB_BET_FILTER_MAXIMUM_PAYOUT = 'Maximum payout is £1,000,000'
    FB_BET_FILTER_SINGLE = 'Single'
    FB_BET_FILTER_DOUBLE = 'Double'
    FB_BET_FILTER_TREBLE = 'Treble'
    FB_BET_FILTER_FOURFOLD = 'Fourfold Accumulator'
