import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C16394894_Betslip_reflection_on_Suspended_Unsuspended(Common):
    """
    TR_ID: C16394894
    NAME: Betslip reflection on Suspended/Unsuspended
    DESCRIPTION: This test case verifies Betslip reflection when <Sport> Event is Suspended/Unsuspended for Single Bet.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_single_sport_bet_to_the_betslipnavigate_to_betslip(self):
        """
        DESCRIPTION: Add single <Sport> bet to the Betslip
        DESCRIPTION: Navigate to Betslip
        EXPECTED: Betslip is opened, selection is displayed
        """
        pass

    def test_002_trigger_the_following_situation_for_this_eventeventstatuscodes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this event:
        DESCRIPTION: eventStatusCode="S" and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: * 'Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out.
        EXPECTED: * 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: * Error message 'Sorry, the event has been suspended' is shown below corresponding single
        EXPECTED: * Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **From OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: ![](index.php?/attachments/get/33909)
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        EXPECTED: ![](index.php?/attachments/get/33910)
        """
        pass

    def test_003_from_ox_99_for_ladbrokeswait_5_secverify_that_message_on_the_top_ob_betslip_is_removed(self):
        """
        DESCRIPTION: **From OX 99 for Ladbrokes:**
        DESCRIPTION: Wait 5 sec
        DESCRIPTION: Verify that message on the top ob Betslip[ is removed
        EXPECTED: Message 'Some of your selections have been suspended' is removed from the top of the Betslip
        """
        pass

    def test_004_make_the_event_active_againeventstatuscodea_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make the event active again:
        DESCRIPTION: eventStatusCode="A" and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: * 'Stake' field and 'Bet Now' ('Log In and Bet') buttons are enabled and not greyed out.
        EXPECTED: * Both error messages disappear from the Betslip
        EXPECTED: **After OX99**
        EXPECTED: * Selection becomes enabled
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (until stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        pass

    def test_005_add_few_more_selection_to_betslipnavigate_to_betslip_and_enter_stake_for_the_multiple_bet(self):
        """
        DESCRIPTION: Add few more selection to Betslip
        DESCRIPTION: Navigate to Betslip and Enter Stake for the Multiple bet
        EXPECTED: 
        """
        pass

    def test_006_suspend_two_of_the_eventseventstatuscodes_and_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Suspend two of the events:
        DESCRIPTION: eventStatusCode="S" and at the same time have Betslip page opened to watch for updates
        EXPECTED: - 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: - No error messages are displayed for active selections
        EXPECTED: **Before OX99**
        EXPECTED: * Error message 'Sorry, the event has been suspended' is shown on the red background below the single from Suspended event
        EXPECTED: * 'Stake' field is disabled and greyed out for the single from Suspended market
        EXPECTED: * 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: * Warning message "Please beware that # of your selections has been suspended. Please remove suspended selections to get new multiple options"
        EXPECTED: **After OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware some of your selections have been suspended'
        EXPECTED: ![](index.php?/attachments/get/33915)
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Some of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'Some of your selections have been suspended' with duration: 5s
        EXPECTED: ![](index.php?/attachments/get/33914)
        """
        pass

    def test_007_unsuspend_the_same_eventseventstatuscodea_and_at_the_same_tame_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Unsuspend the same events:
        DESCRIPTION: eventStatusCode="A" and at the same tame have Betslip page opened to watch for updates
        EXPECTED: 'Multiples' section is not rebuilt
        EXPECTED: **Before OX99**
        EXPECTED: * Both error messages disappear from the Betslip
        EXPECTED: * 'Stake' field and 'Bet Now' ('Log In and Bet') buttons are enabled and not greyed out for the single
        EXPECTED: **After OX99**
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        pass

    def test_008_remove_selection_and_add_race_selection_to_betslipprovide_same_verification_for_race_events(self):
        """
        DESCRIPTION: Remove selection and add <Race> selection to Betslip
        DESCRIPTION: Provide same verification for <Race> events
        EXPECTED: Results are the same
        """
        pass
