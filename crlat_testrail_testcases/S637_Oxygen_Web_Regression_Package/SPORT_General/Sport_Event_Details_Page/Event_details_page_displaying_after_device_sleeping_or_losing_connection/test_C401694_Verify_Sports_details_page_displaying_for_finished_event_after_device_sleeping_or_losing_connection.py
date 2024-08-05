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
class Test_C401694_Verify_Sports_details_page_displaying_for_finished_event_after_device_sleeping_or_losing_connection(Common):
    """
    TR_ID: C401694
    NAME: Verify Sports details page displaying for finished event after device sleeping or losing connection
    DESCRIPTION: This test case verifies Sports details page displaying for finished event after device sleeping or losing connection
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
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

    def test_004_chose_any_event_and_navigate_to_event_details_page(self):
        """
        DESCRIPTION: Chose any event and navigate to Event details page
        EXPECTED: Event details page is opened
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

    def test_007_back_to_device_after_sleeping_or_losing_connection(self):
        """
        DESCRIPTION: Back to device after sleeping or losing connection
        EXPECTED: * Response with updated is received
        EXPECTED: * Page doesn't reload
        EXPECTED: * Price/Odds buttons is greyed out and not clickable
        """
        pass

    def test_008_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: * Blank grey page with text at the top 'No markets are currently available for this event' is displayed in case if displayed: 'N' attribute is received
        EXPECTED: * If displayed: 'N' attribute is NOT received, grey out content will be displayed on Event details page
        """
        pass
