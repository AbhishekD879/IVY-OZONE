import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2604122_Football_Bet_Filter_page(Common):
    """
    TR_ID: C2604122
    NAME: Football Bet Filter page
    DESCRIPTION: This test case verifies general view of Football bet filter screen and 'SAVED FILTERS' tab functionality
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=739487&group_order=asc
    DESCRIPTION: Info:
    DESCRIPTION: 'In-Shop' - user with card number and pin (The Grid - Ladbrokes; Connect - Coral).
    DESCRIPTION: 'Online' - user with username and password.
    DESCRIPTION: 'Multi-channel' - user who was 'In-Shop' and is upgraded to 'Online' (e.g. has both card#/pin and username/password)
    PRECONDITIONS: Following API returns events for applying Football filters on (After navigating to Football Filter search in console: retailCoupon):
    PRECONDITIONS: Online betting:
    PRECONDITIONS: https://sandbox-api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADb3b4313883004240a754070676e25258
    PRECONDITIONS: In-Shop betting:
    PRECONDITIONS: https://sandbox-api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADee73ca08b7e84aad8954e5c955e1dba8
    PRECONDITIONS: OR
    PRECONDITIONS: Online betting:
    PRECONDITIONS: https://api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LAD0cc93c420eeb433aaf57a1ca299ed93c
    PRECONDITIONS: In-Shop betting:
    PRECONDITIONS: https://api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADe196db0611e240d7a8ea3fc67135c37c
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Log in (Only for Coral Connect RHM)
    """
    keep_browser_open = True

    def test_001_verify_navigation_to_bet_filter_connect_page___football_bet_filter_coral_only_football_page___coupons_tab_accumulatorsaccas___separate_coupon_with_couponsortcode_parameter_equal_to_mr__bet_filter_link(self):
        """
        DESCRIPTION: Verify navigation to bet filter:
        DESCRIPTION: * Connect page -> Football Bet Filter (Coral only)
        DESCRIPTION: * Football page -> Coupons tab (Accumulators/ACCAS) -> Separate Coupon with couponSortCode parameter equal to "MR"-> Bet Filter link
        EXPECTED: * Football Bet Filter Page is opened
        EXPECTED: * Football Filter page is opened:
        EXPECTED: * On Connect page, Right menu, and A-Z menu API for in-shop betting returns events (Coral Only)
        EXPECTED: * On Coupon page API for a separate coupon online betting returns events
        """
        pass

    def test_002_verify_the_breadcrumb_section_coral_only(self):
        """
        DESCRIPTION: Verify the breadcrumb section (Coral Only)
        EXPECTED: * [< 'FOOTBALL BET FILTER'] breadcrumb
        EXPECTED: * 'For online bets only' label - if user selected online betting before opening Bet Filter page
        EXPECTED: * 'For in-shop bets only' - if user selected in-shop betting before opening Bet Filter page
        EXPECTED: * [reset icon] + RESET label - resetting all filters to their default values
        """
        pass

    def test_003_verify_three_horizontal_tabs(self):
        """
        DESCRIPTION: Verify three horizontal tabs
        EXPECTED: * YOUR TEAMS (selected by default)
        EXPECTED: * THE OPPOSITION
        EXPECTED: * SAVED FILTERS
        """
        pass

    def test_004_verify_info_section_beneath_your_teams_tab(self):
        """
        DESCRIPTION: Verify info section beneath YOUR TEAMS tab
        EXPECTED: * 'Select criteria for teams you wish to bet on' text and 'i' icon next to it
        EXPECTED: * Tapping 'i' icon expands text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Mean Defence [bold] - Teams ranked in the top half of their division by fewest goals conceded.
        EXPECTED: Favourite [bold] - Teams priced shorter than their opponents to win their match.
        EXPECTED: Outsider [bold] - Teams priced longer than their opponents to win their match.
        EXPECTED: 'Select criteria for the teams you wish to bet against' text
        """
        pass

    def test_005_verify_info_section_beneath_the_opposition_tab(self):
        """
        DESCRIPTION: Verify info section beneath THE OPPOSITION tab
        EXPECTED: * 'Select criteria for the teams you wish to bet against' text and 'i' icon next to it
        EXPECTED: * Tapping 'i' icon expands text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Leaky Defence [bold] - Teams ranked in the bottom half of their division by fewest goals conceded.
        """
        pass

    def test_006_verify_your_teams_tab_filters(self):
        """
        DESCRIPTION: Verify YOUR TEAMS tab filters
        EXPECTED: Tab contains:
        EXPECTED: PLAYING AT filter with following options:
        EXPECTED: * HOME
        EXPECTED: * AWAY
        EXPECTED: LAST GAME filter with following options:
        EXPECTED: * WIN
        EXPECTED: * DRAW
        EXPECTED: * LOSE
        EXPECTED: LAST 6 GAMES POINT TOTAL filter with following options:
        EXPECTED: * 0-6 POINTS
        EXPECTED: * 7-12 POINTS
        EXPECTED: * 13-18 POINTS
        EXPECTED: KEY TRENDS filter with following options:
        EXPECTED: * HIGH SCORING
        EXPECTED: * MEAN DEFENCE
        EXPECTED: * CLEAN SHEET LAST GAME
        EXPECTED: LEAGUE POSITIONS filter with following options:
        EXPECTED: * TOP HALF
        EXPECTED: * BOTTOM HALF
        EXPECTED: * ABOVE OPPOSITION
        EXPECTED: ODDS filter with following options:
        EXPECTED: * FAVOURITE
        EXPECTED: * OUTSIDER
        """
        pass

    def test_007_verify_the_opposition_tab_filters(self):
        """
        DESCRIPTION: Verify THE OPPOSITION tab filters
        EXPECTED: Tab contains:
        EXPECTED: LAST GAME filter with following options:
        EXPECTED: * WIN
        EXPECTED: * DRAW
        EXPECTED: * LOSE
        EXPECTED: LAST 6 GAMES POINT TOTAL filter with following options:
        EXPECTED: * 0-6 POINTS
        EXPECTED: * 7-12 POINTS
        EXPECTED: * 13-18 POINTS
        EXPECTED: KEY TRENDS filter with following options:
        EXPECTED: * HIGH SCORING
        EXPECTED: * LEAKY DEFENCE
        EXPECTED: * CONCEDED 2+ LAST GAME
        EXPECTED: LEAGUE POSITIONS filter with following options:
        EXPECTED: * TOP HALF
        EXPECTED: * BOTTOM HALF
        EXPECTED: * BELOW OPPOSITION
        """
        pass

    def test_008_verify_find_bets_x_button(self):
        """
        DESCRIPTION: Verify 'FIND BETS (X)' button
        EXPECTED: * Enabled by default
        EXPECTED: * X - value that shows how many selections are available and changes after filtering applied
        EXPECTED: * The footer panel is sticky and always visible to a user
        """
        pass

    def test_009_add_many_filters_so_that_no_selections_are_found(self):
        """
        DESCRIPTION: Add many filters, so that no selections are found
        EXPECTED: * "FIND BETS" gets disabled
        EXPECTED: * The inscription below reads NO SELECTIONS FOUND
        """
        pass

    def test_010_check_save_filters_button(self):
        """
        DESCRIPTION: Check SAVE FILTERS button
        EXPECTED: The button is unavailable until at least one filter is selected
        """
        pass

    def test_011__make_random_selections_for_each_filter_on_both_tabs_your_teams_the_opposition_tap_save_filter_button(self):
        """
        DESCRIPTION: * Make random selections for each filter on both tabs (YOUR TEAMS, THE OPPOSITION)
        DESCRIPTION: * Tap 'Save filter' button
        EXPECTED: * 'Enter the name in the field below' pop-up appears
        EXPECTED: * Entry field with watermark 'Name' allows to enter up to 25 symbols
        EXPECTED: * 'Cancel' button closes pop-up
        EXPECTED: * 'Save' button saves filter
        """
        pass

    def test_012_save_filter_and_check_it_on_saved_filters_tab(self):
        """
        DESCRIPTION: Save filter and check it on 'SAVED FILTERS' tab
        EXPECTED: * New filter is added at the top of the filters list
        EXPECTED: * New filter is selected
        EXPECTED: * 'Delete' link is located from the right (exception is 'None' filter)
        """
        pass

    def test_013__select_none_tap_apply_button_check_your_teams_the_opposition_tabs(self):
        """
        DESCRIPTION: * Select 'None'
        DESCRIPTION: * Tap 'Apply' button
        DESCRIPTION: * Check 'YOUR TEAMS', 'THE OPPOSITION' tabs
        EXPECTED: Nothing is selected
        """
        pass
