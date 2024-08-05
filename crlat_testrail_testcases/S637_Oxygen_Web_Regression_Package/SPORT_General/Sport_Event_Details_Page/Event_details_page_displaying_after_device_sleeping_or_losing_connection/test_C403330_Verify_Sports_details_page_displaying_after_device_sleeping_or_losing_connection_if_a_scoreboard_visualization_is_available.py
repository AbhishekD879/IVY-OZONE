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
class Test_C403330_Verify_Sports_details_page_displaying_after_device_sleeping_or_losing_connection_if_a_scoreboard_visualization_is_available(Common):
    """
    TR_ID: C403330
    NAME: Verify Sports details page displaying after device sleeping or losing connection if a scoreboard/visualization is available
    DESCRIPTION: This test case verifies Sports details page displaying after device sleeping or losing connection if a scoreboard/visualization is available
    PRECONDITIONS: - To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: - Event is **In-Play **(live) when:
    PRECONDITIONS: rawlsOffCode = "Y" OR** (rawlsOffCode="-" **AND  **isStarted==true)**
    PRECONDITIONS: - Make sure you have LIVE football event with mapped Visualizations from Perform feed
    PRECONDITIONS: Link for mapping visualization: https://coral-vis-rtc-tst2.symphony-solutions.eu/#/sports/football/provider/perform/tournaments/all/events?_k=5ytaoz
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_go_to_sports_landing_page(self):
        """
        DESCRIPTION: Go to Sports Landing page
        EXPECTED: Sports Landing page is opened
        """
        pass

    def test_003_clicktap_on_in_play_tab(self):
        """
        DESCRIPTION: Click/Tap on In-Play tab
        EXPECTED: Sports In-Play page is opened
        """
        pass

    def test_004_navigate_to_event_details_page_with_mapped_visualization(self):
        """
        DESCRIPTION: Navigate to Event Details page with mapped visualization
        EXPECTED: * Event details page is opened
        EXPECTED: * The mapped Visualization is displayed on Event details page for tablet and mobile view
        EXPECTED: * The mapped Visualization is displayed in 'Match Centre' widget for desktop view
        """
        pass

    def test_005_trigger_situation_with_device_sleeping_or_losing_connection(self):
        """
        DESCRIPTION: Trigger situation with device sleeping or losing connection
        EXPECTED: Device is in sleep mode or connection is interrupted
        """
        pass

    def test_006_trigger_finishing_of_event_from_step_4(self):
        """
        DESCRIPTION: Trigger finishing of event from step 4
        EXPECTED: Event is finished successfully
        """
        pass

    def test_007_back_to_device_after_sleeping_or_losing_connection_and_verify_event_details_page_displaying(self):
        """
        DESCRIPTION: Back to device after sleeping or losing connection and verify Event details page displaying
        EXPECTED: * Response with updates is received
        EXPECTED: * Page doesn't reload
        EXPECTED: * Price/Odds buttons are greyed out and not clickable
        """
        pass

    def test_008_verify_mapped_visualization_displaying_on_event_details_page(self):
        """
        DESCRIPTION: Verify mapped Visualization displaying on Event details page
        EXPECTED: The last state of scoreboard is displayed (FT, Team Scores, etc)
        """
        pass

    def test_009_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Blank grey page with text at the top 'No markets are currently available for this event' is displayed
        EXPECTED: * The scoreboard is not displayed on Event details page anymore (tablet and mobile view)
        EXPECTED: * Match Centre widget with scoreboard is not displayed anymore (desktop view)
        """
        pass
