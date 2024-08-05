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
class Test_C2064791_Verify_general_view_of_Football_bet_filter_screen(Common):
    """
    TR_ID: C2064791
    NAME: Verify general view of Football bet filter screen
    DESCRIPTION: This test case verifies general view of Football bet filter screen
    PRECONDITIONS: Make sure Football Bet Filter feature is turned on in CMS: System configuration -> Connect -> football Filter
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Select 'Connect' from header ribbon
    PRECONDITIONS: 3. Select 'Football Bet Filter' item
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: Load SportBook > Go to Football > 'Coupons' tab > Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
    """
    keep_browser_open = True

    def test_001_verify_the_sub_header_section(self):
        """
        DESCRIPTION: Verify the sub header section
        EXPECTED: **Coral:**
        EXPECTED: - [<] back button in the left is displayed
        EXPECTED: - 'FOOTBALL BET FILTER' near back button
        EXPECTED: - 'For online bets only' label - if user selected online betting before opening Bet Filter page
        EXPECTED: - 'For in-shop bets only' - if user selected in-shop betting before opening Bet Filter page
        EXPECTED: - [reset icon] + RESET label - resetting all filters to their default values
        EXPECTED: **Ladbrokes:**
        EXPECTED: - [<] back button in the left is displayed (Mobile only, in the header)
        EXPECTED: - 'FOOTBALL BET FILTER' in the left on the black background
        EXPECTED: - 'Reset filters' link in the right on the black background - resetting all filters to their default values
        """
        pass

    def test_002_verify_three_horizontal_tabs(self):
        """
        DESCRIPTION: Verify three horizontal tabs
        EXPECTED: - YOUR TEAMS (selected by default)
        EXPECTED: - THE OPPOSITION
        EXPECTED: - SAVED FILTERS
        """
        pass

    def test_003_verify_info_section_beneath_your_teams_tab(self):
        """
        DESCRIPTION: Verify info section beneath YOUR TEAMS tab
        EXPECTED: **Coral:**
        EXPECTED: - 'Select criteria for teams you wish to bet on' text and 'i' icon next to it
        EXPECTED: - Tapping 'i' icon expands the text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Mean Defence [bold] - Teams ranked in the top half of their division by fewest goals conceded.
        EXPECTED: Favourite [bold] - Teams priced shorter than their opponents to win their match.
        EXPECTED: Outsider [bold] - Teams priced longer than their opponents to win their match.
        EXPECTED: **Ladbrokes:**
        EXPECTED: - 'Create your search below
        EXPECTED: For online bets only [bold]
        EXPECTED: Use the below filters to find the bet that suits you best. Save your selections so you can quickly browse your runners in the future.' text
        EXPECTED: Select criteria for the teams you wish to bet on' text and 'i' icon next to it
        EXPECTED: - Tapping 'i' icon expands the grey text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Mean Defence [bold] - Teams ranked in the top half of their division by fewest goals conceded.
        EXPECTED: Favourite [bold] - Teams priced shorter than their opponents to win their match.
        EXPECTED: Outsider [bold] - Teams priced longer than their opponents to win their match.
        """
        pass

    def test_004_verify_info_section_beneath_the_opposition_tab(self):
        """
        DESCRIPTION: Verify info section beneath THE OPPOSITION tab
        EXPECTED: **Coral:**
        EXPECTED: - 'Select criteria for the teams you wish to bet against' text and 'i' icon next to it
        EXPECTED: - Tapping 'i' icon expands the text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Leaky Defence [bold] - Teams ranked in the bottom half of their division by fewest goals conceded.
        EXPECTED: **Ladbrokes:**
        EXPECTED: - 'Create your search below
        EXPECTED: For online bets only [bold]
        EXPECTED: Use the below filters to find the bet that suits you best. Save your selections so you can quickly browse your runners in the future.' text
        EXPECTED: Select criteria for the teams you wish to bet against' text and 'i' icon next to it
        EXPECTED: - Tapping 'i' icon expands the grey text area that says:
        EXPECTED: High Scoring [bold] - Teams ranked in the top half of their division by most goals scored.
        EXPECTED: Leaky Defence [bold] - Teams ranked in the bottom half of their division by fewest goals conceded.
        """
        pass

    def test_005_verify_your_teams_tab_filters(self):
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

    def test_006_verify_the_opposition_tab_filters(self):
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
        EXPECTED: * ABOVE OPPOSITION
        """
        pass

    def test_007_verify_find_bets_x_button(self):
        """
        DESCRIPTION: Verify 'FIND BETS (X)' button
        EXPECTED: - Green button, enabled by default
        EXPECTED: - X - value that shows how many selections are available and changes after filtering applied
        EXPECTED: - The footer panel is sticky and always visible to a user
        """
        pass

    def test_008_add_many_filters_so_that_no_selections_are_found(self):
        """
        DESCRIPTION: Add many filters, so that no selections are found
        EXPECTED: - "FIND BETS" gets disabled (pale gray according to coral design)
        EXPECTED: - "FIND BETS (0)" button. (X) gets '0' value
        """
        pass

    def test_009_check_save_filters_button(self):
        """
        DESCRIPTION: Check SAVE FILTERS button
        EXPECTED: The button is unavailable until at least one filter is selected
        """
        pass
