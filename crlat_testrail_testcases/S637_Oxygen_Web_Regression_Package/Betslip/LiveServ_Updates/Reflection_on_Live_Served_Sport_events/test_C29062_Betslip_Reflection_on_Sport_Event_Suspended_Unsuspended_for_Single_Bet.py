import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29062_Betslip_Reflection_on_Sport_Event_Suspended_Unsuspended_for_Single_Bet(Common):
    """
    TR_ID: C29062
    NAME: Betslip Reflection on <Sport> Event Suspended/Unsuspended for Single Bet
    DESCRIPTION: This test case verifies Betslip reflection when <Sport> Event is Suspended/Unsuspended for Single Bet.
    DESCRIPTION: AUTOTEST [C9690060]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_single_sport_bet_to_the_betslip(self):
        """
        DESCRIPTION: Add single <Sport> bet to the Betslip
        EXPECTED: 
        """
        pass

    def test_002_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is opened, selection is displayed
        """
        pass

    def test_003_trigger_the_following_situation_for_this_eventeventstatuscodesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode="S"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: *   'Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out.
        EXPECTED: *  'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: *   Error message 'Sorry, the event has been suspended' is shown below corresponding single
        EXPECTED: *  Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **From OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: ![](index.php?/attachments/get/33911)
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections has been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections has been suspended' with duration: 5s
        EXPECTED: ![](index.php?/attachments/get/33912)
        """
        pass

    def test_004_from_ox_99_for_ladbrokeswait_5_secverify_that_message_on_the_top_ob_betslip_is_removed(self):
        """
        DESCRIPTION: **From OX 99 for Ladbrokes:**
        DESCRIPTION: Wait 5 sec
        DESCRIPTION: Verify that message on the top ob Betslip[ is removed
        EXPECTED: Message  'One of your selections has been suspended' is removed from the top of the Betslip
        """
        pass

    def test_005_make_the_event_active_againeventstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make the event active again:
        DESCRIPTION: eventStatusCode="A"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: *  'Stake' field and 'Bet Now' ('Log In and Bet') buttons are enabled and not greyed out.
        EXPECTED: *  Both error messages disappear from the Betslip
        EXPECTED: **After OX99**
        EXPECTED: * Selection becomes enabled
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        pass
