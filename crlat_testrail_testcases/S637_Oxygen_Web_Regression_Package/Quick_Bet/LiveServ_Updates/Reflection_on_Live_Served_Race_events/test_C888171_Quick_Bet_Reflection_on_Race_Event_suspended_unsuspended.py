import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C888171_Quick_Bet_Reflection_on_Race_Event_suspended_unsuspended(Common):
    """
    TR_ID: C888171
    NAME: Quick Bet Reflection on <Race> Event suspended/unsuspended
    DESCRIPTION: This test case verifies Quick Bet reflection when <Race> event is Suspended/Unsuspended.
    DESCRIPTION: AUTOTEST [C2009639]
    PRECONDITIONS: This test case is applied for **Mobile** application.
    """
    keep_browser_open = True

    def test_001_go_to_the_race_event_details_page(self):
        """
        DESCRIPTION: Go to the <Race> event details page
        EXPECTED: 
        """
        pass

    def test_002_make_single_selection(self):
        """
        DESCRIPTION: Make single selection
        EXPECTED: Quick Bet is opened with selection added
        """
        pass

    def test_003_enter_any_value_in_stake_field_suspend_event_in_backoffice_tool_trigger_the_following_situation_for_this_eventeventstatuscode_s(self):
        """
        DESCRIPTION: Enter any value in Stake field. Suspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"S"**
        EXPECTED: 
        """
        pass

    def test_004_check_update_in_quick_bet(self):
        """
        DESCRIPTION: Check update in Quick Bet
        EXPECTED: * 'Your Event has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: - Stake box, E/W option & Price(dropdown) are disabled
        EXPECTED: - 'LOGIN & PLACE BET' button and 'Add to Betslip' button are disabled
        """
        pass

    def test_005_unsuspend_event_in_backoffice_tool_trigger_the_following_situation_for_this_eventeventstatuscode_a(self):
        """
        DESCRIPTION: Unsuspend event in Backoffice tool. Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode= **"A"**
        EXPECTED: 
        """
        pass

    def test_006_check_update_in_quick_bet(self):
        """
        DESCRIPTION: Check update in Quick Bet
        EXPECTED: - Message is removed
        EXPECTED: - Stake box, E/W option & Price(dropdown) are enabled
        EXPECTED: - 'LOGIN & PLACE BET' button and 'Add to Betslip' button are enabled
        """
        pass
