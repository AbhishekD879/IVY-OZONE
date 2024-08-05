import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C16669960_Verify_updates_are_received_for_Progressive_Web_Application(Common):
    """
    TR_ID: C16669960
    NAME: Verify updates are received for Progressive Web Application
    DESCRIPTION: This test case verifies the possibility to receive updates while using Web Progressive App.
    DESCRIPTION: NOTE:
    DESCRIPTION: Currently, functionality is applicable only for Coral brand, iOS devices and Safari browser
    PRECONDITIONS: User has Coral Progressive Web App installed.
    """
    keep_browser_open = True

    def test_001_open_coral_pwaadd_sport_selection_to_betslipnavigate_to_betslip(self):
        """
        DESCRIPTION: Open Coral PWA
        DESCRIPTION: Add <Sport> selection to Betslip
        DESCRIPTION: Navigate to Betslip
        EXPECTED: App is open
        EXPECTED: Betslip is open
        EXPECTED: Added selection is displayed
        """
        pass

    def test_002_trigger_the_following_situation_for_this_event_change_price_of_the_added_selection_and_at_the_same_time_have_the_betslip_page_open_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: * change price of the added selection
        DESCRIPTION: * and at the same time have the Betslip page open to watch for updates
        EXPECTED: Price Odds is changed
        """
        pass

    def test_003_trigger_the_following_situation_for_this_event_eventstatuscodes_and_at_the_same_time_have_betslip_page_open_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: * eventStatusCode="S"
        DESCRIPTION: * and at the same time have Betslip page open to watch for updates
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        """
        pass

    def test_004_navigate_to_edp_of_sport_eventtrigger_the_following_situation_for_this_event_change_price_for_some_selection_and_at_the_same_time_have_the_edp_open_to_watch_for_updates(self):
        """
        DESCRIPTION: Navigate to EDP of <Sport> event
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: * change price for some selection
        DESCRIPTION: * and at the same time have the EDP open to watch for updates
        EXPECTED: Price Odds is changed
        """
        pass
