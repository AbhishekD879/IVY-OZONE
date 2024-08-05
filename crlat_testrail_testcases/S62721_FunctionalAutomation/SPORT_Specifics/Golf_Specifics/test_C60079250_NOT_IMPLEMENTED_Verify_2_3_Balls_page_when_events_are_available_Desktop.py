import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60079250_NOT_IMPLEMENTED_Verify_2_3_Balls_page_when_events_are_available_Desktop(Common):
    """
    TR_ID: C60079250
    NAME: NOT IMPLEMENTED: Verify '2/3 Balls' page when events are available (Desktop)
    DESCRIPTION: Test case verifies '2/3 Balls' page when events are available.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-12454: Display content for 2 & 3 Balls Golf events (Desktop)
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_golf_page(self):
        """
        DESCRIPTION: Go to 'Golf' page
        EXPECTED: *   Golf Landing page is opened
        EXPECTED: *   2/3 Balls' -> 'Today' page is opened by default
        """
        pass

    def test_003_verify_displaying_of_market_section(self):
        """
        DESCRIPTION: Verify displaying of Market section
        EXPECTED: *   Markets that contain the most current event are expanded by default
        EXPECTED: *   Market name is displayed in the header
        """
        pass

    def test_004_verify_displaying_of_competitionsection(self):
        """
        DESCRIPTION: Verify displaying of Competition section
        EXPECTED: *   Competitions that contain the most current event are expanded by default
        EXPECTED: *   Competition name is displayed in the header above event name
        EXPECTED: *   List of events is displayed within opened Competition section
        """
        pass

    def test_005_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: *   All events are displayed chronologically based on event start time
        EXPECTED: *   Player names are displayed within event section in one row
        EXPECTED: *   'Price/Odds' buttons are displayed within event section in one row
        EXPECTED: *   Start time of the event is shown beneath the player names
        """
        pass

    def test_006_verify_displaying_of_priceodds_buttons(self):
        """
        DESCRIPTION: Verify displaying of 'Price/Odds' buttons
        EXPECTED: *   The 'Price/Odds' buttons are displayed in one row for each player next to each other
        EXPECTED: *   One Two Type is displayed in Subheader above each of the 'Price/Odds' buttons ('2 Balls' market)
        EXPECTED: *   One Two Three Type is displayed in Subheader above each of the 'Price/Odds' buttons ('3 Balls' market)
        """
        pass

    def test_007_verify_displaying_of_player_names(self):
        """
        DESCRIPTION: Verify displaying of Player names
        EXPECTED: *   Each player name is displayed next to each other separated by a Vs (Player 1 Vs Player 2) in case events from '2 Balls' are shown
        EXPECTED: *   Each player name is displayed next to each other separated by a / (Player 1/Player 2/Player 3) in case events from '3 Balls' are shown
        EXPECTED: *   If player name is too long, X number of characters are showing with adding three dots in the end (Matsuy.../Mockle.../Woodla...)
        EXPECTED: *   If one of names is short (For example: Na) other names that are long should display fully (Na/Mickleson/Woodland)
        """
        pass
