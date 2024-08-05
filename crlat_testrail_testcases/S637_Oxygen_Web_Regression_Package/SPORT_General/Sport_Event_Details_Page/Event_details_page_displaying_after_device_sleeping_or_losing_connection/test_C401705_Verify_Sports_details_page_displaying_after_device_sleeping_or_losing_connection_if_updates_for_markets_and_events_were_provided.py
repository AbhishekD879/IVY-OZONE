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
class Test_C401705_Verify_Sports_details_page_displaying_after_device_sleeping_or_losing_connection_if_updates_for_markets_and_events_were_provided(Common):
    """
    TR_ID: C401705
    NAME: Verify Sports details page displaying after device sleeping or losing connection if updates for markets and events were provided
    DESCRIPTION: This test case verifies Sports details page displaying after device sleeping or losing connection if updates for markets and events were provided
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

    def test_003_chose_any_event_and_navigate_to_event_details_page(self):
        """
        DESCRIPTION: Chose any event and navigate to Event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_trigger_situation_with_device_sleeping_or_losing_connection(self):
        """
        DESCRIPTION: Trigger situation with device sleeping or losing connection
        EXPECTED: Device is in sleep mode or connection is interrupted
        """
        pass

    def test_005_make_changes_for_the_event_from_step_3_change_name_start_datetime_etc_and_save_this_changes(self):
        """
        DESCRIPTION: Make changes for the event from step 3 (change name, start date/time, etc.) and save this changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_back_to_device_after_sleeping_or_losing_connection(self):
        """
        DESCRIPTION: Back to device after sleeping or losing connection
        EXPECTED: * Response with updates is received
        EXPECTED: * Page content is reloaded
        EXPECTED: * The changes from step 5 are applied and visible
        """
        pass

    def test_007_trigger_situation_with_device_sleeping_or_losing_connection_again(self):
        """
        DESCRIPTION: Trigger situation with device sleeping or losing connection again
        EXPECTED: Device is in sleep mode or connection is interrupted
        """
        pass

    def test_008_make_changes_for_the_market_from_event_in_step_3_change_name_start_datetime_delete_market_etc_and_save_this_changes(self):
        """
        DESCRIPTION: Make changes for the market from event in step 3 (change name, start date/time, delete market etc.) and save this changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_009_back_to_device_after_sleeping_or_losing_connection(self):
        """
        DESCRIPTION: Back to device after sleeping or losing connection
        EXPECTED: * Response with updated is received
        EXPECTED: * Page content is reloaded
        EXPECTED: * The changes from step 8 are applied and visible
        """
        pass

    def test_010_repeat_steps_2_9_for_in_play_events(self):
        """
        DESCRIPTION: Repeat steps 2-9 for In-Play events
        EXPECTED: * Response with updated is received
        EXPECTED: * Page content is reloaded
        EXPECTED: * The changes are applied and visible
        """
        pass
