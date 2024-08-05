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
class Test_C28705_NOT_IMPLEMENTED_Verify_2_3_Balls_page_when_events_are_available_Mobile(Common):
    """
    TR_ID: C28705
    NAME: NOT IMPLEMENTED: Verify '2/3 Balls' page when events are available (Mobile)
    DESCRIPTION: Test case verifies '2/3 Balls' page when events are available.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-10373: Display content for 2 & 3 Balls Golf events (Mobile)
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
        EXPECTED: **Mobile:**
        EXPECTED: * Golf Landing page is opened
        EXPECTED: * Modules like 'In-Play' and sections like 'Outrights', 'Spesials', etc. are present (if available) and displayed one above another
        EXPECTED: **Desktop:**
        EXPECTED: Events tab: Today is opened by default
        """
        pass

    def test_003_verify_displaying_of_market_section(self):
        """
        DESCRIPTION: Verify displaying of Market section
        EXPECTED: *   Markets that contain the most current event are expanded by default
        EXPECTED: *   Market name is displayed in the header
        """
        pass

    def test_004_verify_displaying_of_competition_section(self):
        """
        DESCRIPTION: Verify displaying of Competition section
        EXPECTED: *   Competitions that contain the most current event are expanded by default
        EXPECTED: *   Competition name is displayed in the header above event name
        EXPECTED: *   List of events is displayed within opened Competition section
        """
        pass

    def test_005_verify_event_section(self):
        """
        DESCRIPTION: Verify event section
        EXPECTED: *   All events are displayed chronologically based on event start time
        EXPECTED: *   Player names are displayed within event section under each other
        EXPECTED: *   'Price/Odds' buttons are displayed within event section under each other
        EXPECTED: *   Start time of the event is shown beneath the all player names
        """
        pass

    def test_006_verify_displaying_of_priceodds_buttons(self):
        """
        DESCRIPTION: Verify displaying of 'Price/Odds' buttons
        EXPECTED: *   The 'Price/Odds' buttons are displayed for each player under each other in one column
        """
        pass

    def test_007_verify_displaying_of_player_names(self):
        """
        DESCRIPTION: Verify displaying of Player names
        EXPECTED: *   Each player name is displayed under each other
        """
        pass
