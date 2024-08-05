from collections import namedtuple


class FANZONE(object):
    """
    Fanzone related constants/messages
    """
    _expected_teams_list = namedtuple('excpeted_options_list',
                                      ('arsenal', 'aston_villa', 'brentford', 'brighton_and_hove_albion',
                                       'burnley', 'chelsea', 'crystal_palace',
                                       'everton', 'leeds_united', 'leicester_city',
                                       'liverpool', 'manchester_city', 'manchester_united', 'newcastle_united',
                                       'norwich_city', 'southampton', 'tottenham_hotspur',
                                       'watford', 'west_ham_united', 'wolverhampton_wanderers'))
    TEAMS_LIST = _expected_teams_list(arsenal='ARSENAL', aston_villa='ASTON VILLA', brentford='BRENTFORD',
                                      brighton_and_hove_albion='BRIGHTON', burnley='BURNLEY',
                                      chelsea='CHELSEA', crystal_palace='CRYSTAL PALACE', everton='EVERTON',
                                      leeds_united='LEEDS',
                                      leicester_city='LEICESTER',
                                      liverpool='LIVERPOOL', manchester_city='MAN CITY',
                                      manchester_united='MAN UTD', newcastle_united='NEWCASTLE',
                                      norwich_city='NORWICH', southampton='SOUTHAMPTON',
                                      tottenham_hotspur='TOTTENHAM',
                                      watford='WATFORD', west_ham_united='WEST HAM',
                                      wolverhampton_wanderers='WOLVES')
    NOW_AND_NEXT = 'NOW & NEXT'
    STATS = 'STATS'
    CLUB = 'CLUB'
    FANZONE_GAMES = 'FANZONE GAMES'
    I_DONT_SUPPORT_ANY_OF_THE_TEAM_MSG = "We’re sorry your team isn’t listed yet. Drop the team you follow below, and we’ll hopefully add a Fanzone for you to show your colours in the future."
    THANK_YOU_MESSAGE = "We hope to add a Fanzone for your team in the future so you can show your colours."
    SYC_POP_UP_NAME = "Ladbrokes Fanzone"
    SYC_POP_UP_DESCRIPTION = "Tell us which Premier League team you support and gain access to Fanzone where you’ll see exclusive matchday markets and offers, stats, team news and more."
    SYC_POP_UP_REMINED_ME_LATER = "REMIND ME LATER"
    SYC_POP_UP_I_M_IN = "I\'M IN"
    SYC_POP_UP_DONT_SHOW_ME_AGAIN = "DON\'T SHOW ME THIS AGAIN"
    SYC_TEAM_FONT_FAMILY = "Roboto Condensed"
    SYC_TEAM_COLOR = 'rgba(0, 0, 0, 1)'
    SYC_TEAM_BG_COLOR = "rgba(255, 255, 255, 1)"
    SYC_TEAM_BORDER_RADIUS = '4px'
    SYC_TEAM_FONT_SIZE = '13px'
    SYC_SELECTED_TEAM_BORDER = '2px'
    SYC_TOTAL_TEAMS_COUNT = 21
    PROMOTION_TITLE = 'LADBROKES FANZONE'
    FANZONE_SYC = 'Show Your Colours'
    TEAMS_CONFIRMATION_MESSAGE_MOBILE = "You're selecting {team_name} as your Premier League side, which you won't be able to change for another {duration} days. On the next screen you can tell us which Fanzone notifications you want to receive."
    TEAMS_CONFIRMATION_MESSAGE_DESKTOP = "You're selecting {team_name} as your Premier League side, which you won't be able to change for {duration} days. Don’t miss out on exclusive matchday offers, in-play updates, team news and more! Go to the Ladbrokes app and set your push notification preferences to on."
    TEAM_ALERTS_MSG = "Don’t miss out on exclusive matchday offers, in-play updates, team news and more! Go to the Ladbrokes app and set your push notification preferences to on."
    UNSUBSCRIBE_MSG = "Are you sure you’d like to unsubscribe? You’ll lose access to Fanzone once you click “Confirm”. If you signed up less than 30 days ago you will need to wait until the 30 days expire to re-subscribe."
    CHANGE_TEAM_MESSAGE = 'Looks like you only picked a team less than 30 days ago. You need wait another 1 days before you can change your mind.'
    MARKET_TEAM_FONT_FAMILY = "Roboto Condensed"
    MARKET_TEAM_COLOR = 'rgba(0, 0, 0, 1)'
    MARKET_TEAM_BG_COLOR = "rgba(0, 0, 0, 0)"
    MARKET_TEAM_BORDER_RADIUS = '0px'
    MARKET_TEAM_FONT_SIZE = '13px'
    EVERTON_HOME_BG_COLOR = 'rgba(0, 51, 153, 1)'
    EVERTON_FANZONE_BG_COLOR = 'rgba(0, 51, 153, 0.8)'
