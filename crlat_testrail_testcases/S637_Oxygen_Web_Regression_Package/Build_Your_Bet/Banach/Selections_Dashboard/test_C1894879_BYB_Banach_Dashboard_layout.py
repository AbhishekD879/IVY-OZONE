import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.build_your_bet
@vtest
class Test_C1894879_BYB_Banach_Dashboard_layout(Common):
    """
    TR_ID: C1894879
    NAME: BYB Banach Dashboard layout
    DESCRIPTION: This test case verifies triggering selections dashboard and price generation
    DESCRIPTION: Note:
    DESCRIPTION: * some selections are not allowed for combos or require additional selections to place a bet, those rules are covered in related TC's. For this test case use only valid combos of selections.
    DESCRIPTION: * **'Build Your Bet'** name is used on Coral and **'Bet Builder'** name is used on Ladbrokes
    DESCRIPTION: AUTOTEST: [C2322997]
    PRECONDITIONS: CMS config:
    PRECONDITIONS: 1. Build Your Bet tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: a. Banach leagues are added and enabled in CMS -> YourCall -> YourCall Leagues
    PRECONDITIONS: b. Event belonging to Banach league is mapped (on Banach side)
    PRECONDITIONS: 2. BYB markets are added in CMS -> BYB -> BuildYourBet Markets Page
    PRECONDITIONS: Requests:
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach event data: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/obEventId=xxxxx
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes) tab on the event details page is loaded
    """
    keep_browser_open = True

    def test_001_add_few_combinable_selections_to_bybbet_builder_dashboard_from_different_markets_accordionsmatch_result_or_both_teams_to_scoredouble_chanceanytime_goalscoreroverunder_marketscorrect_score_etc(self):
        """
        DESCRIPTION: Add few combinable selections to BYB/Bet Builder Dashboard from different markets accordions:
        DESCRIPTION: Match Result or Both teams to score
        DESCRIPTION: Double Chance
        DESCRIPTION: Anytime goalscorer
        DESCRIPTION: Over/Under markets
        DESCRIPTION: Correct Score etc
        EXPECTED: *  Selected selections are highlighted within accordions
        EXPECTED: *  **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes Dashboard appears with slide animation and is displayed in an expanded state (only when the page is accessed and selections are added for the first time):
        EXPECTED: on mobile in the bottom of the screen over footer menu
        EXPECTED: on tablet/desktop in the bottom of the market area and above footer menu (if market area is too long to be shown within screen)
        EXPECTED: *  User is able to collapse the Dashboard
        """
        pass

    def test_002_verify_the_build_your_bet_for_coral_bet_builder_for_ladbrokes_dashboard_content_in_the_collapsed_state(self):
        """
        DESCRIPTION: Verify the **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes Dashboard content in the collapsed state
        EXPECTED: **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes Dashboard consists of
        EXPECTED: *  Dashboard touchable area
        EXPECTED: *  Odds touchable area
        """
        pass

    def test_003_verify_the_dashboard_touchable_area_content(self):
        """
        DESCRIPTION: Verify the dashboard touchable area content
        EXPECTED: The following information is displayed:
        EXPECTED: *  icon with number of selections
        EXPECTED: *  **Build Your Bet** (for Coral)/ **Bet Builder** (for Ladbrokes text
        EXPECTED: *  name of selections (in the same order they were added, separated by comma)
        EXPECTED: *  'Open' label with arrow
        """
        pass

    def test_004_verify_selections_name(self):
        """
        DESCRIPTION: Verify selections name
        EXPECTED: Name of selection is displayed in the following formats:
        EXPECTED: *  For Match Result, Both teams to score, Player to be carded and Anytime goalscorer - <Market Name> <Selection Name> (e.g. Both Teams to score YES or Player to be carded CRISTIANO RONALDO)
        EXPECTED: *  For Over/Under markets - Total <Statistic name> OVER or UNDER XX.X (e.g. Total Booking Points OVER 33.5)
        """
        pass

    def test_005_verify_odds_touchable_area_content(self):
        """
        DESCRIPTION: Verify Odds touchable area content
        EXPECTED: The following information is displayed:
        EXPECTED: *  <Corresponding Odds value> with corresponding user format (decimal or fractional)
        EXPECTED: *  PLACE BET text below
        """
        pass

    def test_006_click_within_dashboard_touchable_area(self):
        """
        DESCRIPTION: Click within Dashboard touchable area
        EXPECTED: *  Dashboard touchable area is shown with the following change: 'Close' label with upside down arrow
        EXPECTED: *  Dashboard expands with slide animation
        EXPECTED: *  Selection lines with information about added selections are displayed below the Dashboard touchable area in the same order they were added
        """
        pass

    def test_007_verify_content_of_selection_lines(self):
        """
        DESCRIPTION: Verify content of selection lines
        EXPECTED: *  Name of selection is displayed in the same formats as in step #4
        EXPECTED: *  'Remove' icon is shown on the right
        """
        pass

    def test_008_scroll_market_area(self):
        """
        DESCRIPTION: Scroll market area
        EXPECTED: *  Market area scrollable
        EXPECTED: *  on mobile dashboard is sticked to the bottom of the screen
        EXPECTED: *  on tablet/desktop is sticked to the bottom of market area
        """
        pass

    def test_009_add_one_more_valid_selection_to_dashboard(self):
        """
        DESCRIPTION: Add one more valid selection to Dashboard
        EXPECTED: *  Added selections lines are shown
        EXPECTED: *  Icon with number of selections is updated
        EXPECTED: *  Odds touchable area is updated with odds value
        EXPECTED: *  Scroll appears (for 5 and more selections in dashboard)
        """
        pass

    def test_010_scroll_up_and_down_within_section_with_selections_lines(self):
        """
        DESCRIPTION: Scroll up and down within section with selections lines
        EXPECTED: *  Section with selections lines is scrollable
        EXPECTED: *  Page content with markets is NOT scrollable
        """
        pass

    def test_011_click_remove_icon_for_the_any_selection_line(self):
        """
        DESCRIPTION: Click 'Remove' icon for the any selection line
        EXPECTED: *  Selection is not highlighted within market accordion
        EXPECTED: *  Selection is removed from Dashboard
        EXPECTED: *  Odds touchable area is shown with updated odds value
        EXPECTED: *  Icon with number of selections is updated
        """
        pass

    def test_012_click_within_dashboard_touchable_area(self):
        """
        DESCRIPTION: Click within Dashboard touchable area
        EXPECTED: Dashboard collapses with slide animation
        """
        pass

    def test_013_remove_remaining_selections_from_dashboard(self):
        """
        DESCRIPTION: Remove remaining selections from Dashboard
        EXPECTED: Dashboard disappears with slide animation
        """
        pass

    def test_014_add_only_one_selection_to_dashboard(self):
        """
        DESCRIPTION: Add only ONE selection to dashboard
        EXPECTED: *  Selection appears on sliding dashboard
        EXPECTED: *  'Please add another selection to place the bet' notification is shown above the dashboard as per GD
        """
        pass
