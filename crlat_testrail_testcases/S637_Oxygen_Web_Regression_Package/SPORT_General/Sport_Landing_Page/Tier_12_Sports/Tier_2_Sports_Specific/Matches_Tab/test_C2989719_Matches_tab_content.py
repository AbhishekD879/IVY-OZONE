import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2989719_Matches_tab_content(Common):
    """
    TR_ID: C2989719
    NAME: Matches tab content
    DESCRIPTION: This test case verifies the Matches tab load and content positioning when navigating to <sport> landing page for sports that are Tier II, with the latest changes within the CMS being applied.
    DESCRIPTION: The list of sports that are tier I/II/III is available here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs?preview=/118800974/119885865/Sports%20Pages%20-%20Tier%201%2C2%2C3.pdf
    PRECONDITIONS: 1) Following Tabs should be enabled in Sports Pages - SPORT CATEGORIES - #TIER_2_SPORT_NAME within CMS: Matches, Competitions, Outrights
    PRECONDITIONS: 2) Following Modules should be enabled in Sports Pages - SPORT CATEGORIES - #TIER_2_SPORT_NAME within CMS:In play module, Featured events
    PRECONDITIONS: 3) At least 2 LIVE events should be created and active for the chosen TIER_2_SPORT
    PRECONDITIONS: 4) At least 1 upcoming event with a following setting should be created for the chosen TIER_2_SPORT: 'Start Time' value '00:00 AM Current Date' + 23H:55M
    PRECONDITIONS: 5) At least 1 upcoming event with a following setting should be created for the chosen TIER_2_SPORT: 'Start Time' value '00:00 AM Current Date' + 47H:55M
    PRECONDITIONS: 6) At least 4 upcoming events in different leagues (types) should be created in total (accounting 2 previously aforementioned)
    PRECONDITIONS: 6) All aforementioned events should have 2 or more markets being set for them(Primary Markets preferable)
    PRECONDITIONS: 7) All aforementioned events should have a 'stream mapped' / 'stream available' being set for them
    PRECONDITIONS: Oxygen app is running
    PRECONDITIONS: User is on the home page.
    """
    keep_browser_open = True

    def test_001_click_on_the_chosen_tier_2_sport_icon_in_menu_ribbon(self):
        """
        DESCRIPTION: Click on the chosen TIER_2_SPORT icon in menu ribbon
        EXPECTED: Sport landing page loads
        """
        pass

    def test_002_verify_the_default_tab_that_is_loaded_when_user_navigates_to_the_sport_landing_page(self):
        """
        DESCRIPTION: Verify the default tab that is loaded when user navigates to the sport landing page
        EXPECTED: 'Matches' tab loads by default when user navigates to sport landing page
        """
        pass

    def test_003_verify_tab_content(self):
        """
        DESCRIPTION: Verify tab content
        EXPECTED: The tab content consists of(positioning of elements from top to bottom is done as described below):
        EXPECTED: - 'In Play' module with leagues expanded by default
        EXPECTED: - Expanded league(s) with 'Today/Tomorrow' fixture headers(lists) with upcoming events, corresponding to it(them) shown within it(them).
        """
        pass

    def test_004_verify_in_play_module(self):
        """
        DESCRIPTION: Verify 'In-Play' Module
        EXPECTED: In-Play Module consist of:
        EXPECTED: - 'In-Play' name on the header of the module
        EXPECTED: - Event card header with league name, and fixture header titles that represent selection names (i.e. home/draw/away)
        EXPECTED: - Events(event cards) available for today with 'Watch live' or 'Live' icon under the event name
        EXPECTED: - '# More' link on the right side of the event card, below price odds buttons
        EXPECTED: - 'SEE ALL(#)' link with number of available events shown at the title lane of 'In-Play' module
        """
        pass

    def test_005_verify_leagues_section_with_upcoming_events_representation(self):
        """
        DESCRIPTION: Verify League(s) section with upcoming events representation
        EXPECTED: Section consists of:
        EXPECTED: - Headers with type (league) name and 'SEE ALL' link (when league is expanded)
        EXPECTED: - First 3 types (leagues) are expanded by default, the rest are collapsed
        EXPECTED: - Event card(s) header with league date (i.e. Today/Tomorrow) and selection names (i.e. home/draw/away)
        EXPECTED: - Events(event cards) with 'Watch' icon/date of event and '# More' link
        EXPECTED: - All collapsed types (leagues) at the bottom of page are accordions and are collapsable/expandable (with downward arrows in their headers)
        """
        pass

    def test_006_click_on_downward_arrow_of_any_league_lane_that_is_collapsed_by_default(self):
        """
        DESCRIPTION: Click on downward arrow of any league lane that is collapsed by default
        EXPECTED: League becomes expanded
        """
        pass

    def test_007_click_on_the_left_side_of_the_league_lane_from_step_6_again(self):
        """
        DESCRIPTION: Click on the left side of the league lane from step 6 again
        EXPECTED: League becomes collapsed
        """
        pass
