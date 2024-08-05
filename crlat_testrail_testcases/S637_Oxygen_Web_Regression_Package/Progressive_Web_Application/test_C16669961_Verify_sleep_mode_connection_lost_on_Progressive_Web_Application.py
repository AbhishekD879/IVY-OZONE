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
class Test_C16669961_Verify_sleep_mode_connection_lost_on_Progressive_Web_Application(Common):
    """
    TR_ID: C16669961
    NAME: Verify sleep mode/connection lost on Progressive Web Application
    DESCRIPTION: This test case verifies that correct data is displayed in PWA after device sleeping or losing connection.
    PRECONDITIONS: User has Coral Progressive Web App installed.
    """
    keep_browser_open = True

    def test_001_open_coral_pwaadd_sport_selection_to_quick_bet(self):
        """
        DESCRIPTION: Open Coral PWA
        DESCRIPTION: Add <Sport> selection to Quick Bet
        EXPECTED: App is open
        EXPECTED: Quick Bet is open
        EXPECTED: Added selection is displayed
        """
        pass

    def test_002_trigger_situation_with_device_sleeping_or_losing_connection(self):
        """
        DESCRIPTION: Trigger situation with device sleeping or losing connection
        EXPECTED: Device is in sleep mode or connection is lost
        """
        pass

    def test_003_unlock_deviceverify_quick_bet(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify Quick Bet
        EXPECTED: App is open
        EXPECTED: Quick bet is shown correctly
        """
        pass

    def test_004_add_sport_selection_to_betslipnavigate_to_betslip(self):
        """
        DESCRIPTION: Add <Sport> selection to Betslip
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Betslip is open
        EXPECTED: Added selection is displayed
        """
        pass

    def test_005_trigger_situation_with_device_sleeping_or_losing_connection(self):
        """
        DESCRIPTION: Trigger situation with device sleeping or losing connection
        EXPECTED: Device is in sleep mode or connection is lost
        """
        pass

    def test_006_unlock_deviceverify_betslip(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify Betslip
        EXPECTED: App is open
        EXPECTED: Betslip is shown correctly
        """
        pass

    def test_007_choose_any_event_and_navigate_to_event_details_page(self):
        """
        DESCRIPTION: Choose any event and navigate to Event details page
        EXPECTED: Event details page is open
        """
        pass

    def test_008_trigger_situation_with_device_sleeping_or_losing_connection(self):
        """
        DESCRIPTION: Trigger situation with device sleeping or losing connection
        EXPECTED: Device is in sleep mode or connection is lost
        """
        pass

    def test_009_make_changes_for_the_event_from_step_7_change_name_start_datetime_odds_etc_and_save_these_changes(self):
        """
        DESCRIPTION: Make changes for the event from Step 7 (change name, start date/time, odds, etc.) and save these changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_010_unlock_deviceverify_edp(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify EDP
        EXPECTED: Changes from Step 9 are applied and visible
        """
        pass
