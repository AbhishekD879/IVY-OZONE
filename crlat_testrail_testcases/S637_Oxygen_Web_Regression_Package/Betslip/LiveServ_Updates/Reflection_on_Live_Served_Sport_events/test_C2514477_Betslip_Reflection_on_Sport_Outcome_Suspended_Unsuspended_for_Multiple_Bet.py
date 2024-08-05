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
class Test_C2514477_Betslip_Reflection_on_Sport_Outcome_Suspended_Unsuspended_for_Multiple_Bet(Common):
    """
    TR_ID: C2514477
    NAME: Betslip Reflection on <Sport> Outcome Suspended/Unsuspended for Multiple Bet
    DESCRIPTION: This test case verifies Betslip reflection for Multiples section when outcome is Suspended.
    DESCRIPTION: AUTOTEST [C13135318]
    PRECONDITIONS: Access to OB TI is required
    """
    keep_browser_open = True

    def test_001_add_a_few_selections_from_different_active_events(self):
        """
        DESCRIPTION: Add a few selections from different active events
        EXPECTED: 'Multiples' section is shown on the Betslip
        """
        pass

    def test_002_suspend_one_of_outcomesoutcomestatuscodesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Suspend one of outcomes:
        DESCRIPTION: **outcomeStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: * No error messages/labels are displayed for active selections
        EXPECTED: **Before OX99**
        EXPECTED: * Error message 'Sorry, the event has been suspended' is shown on the red background below the single from Suspended event
        EXPECTED: * 'Stake' field is disabled and greyed out for the single from Suspended market
        EXPECTED: * Warning message 'Please beware that 1 of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **After OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_003_unsuspend_the_same_outcomeoutcomestatuscodeaand_at_the_same_tame_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Unsuspend the same outcome:
        DESCRIPTION: **outcomeStatusCode="A"**
        DESCRIPTION: and at the same tame have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: **Before OX99**
        EXPECTED: * Both error messages disappear from the Betslip
        EXPECTED: * 'Stake' field is enabled and not greyed out for the single
        EXPECTED: **After OX99**
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        pass

    def test_004_enter_stake_for_the_multiple_bet(self):
        """
        DESCRIPTION: Enter Stake for the Multiple bet
        EXPECTED: 
        """
        pass

    def test_005_suspend_two_of_outcomesoutcomestatuscodesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Suspend two of outcomes:
        DESCRIPTION: **outcomeStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt and it is still contains selection from Suspended event
        EXPECTED: * No error messages are displayed for active selections
        EXPECTED: **Before OX99**
        EXPECTED: * Error message 'Sorry, the event has been suspended' is shown on the red background below the single from Suspended event
        EXPECTED: * 'Stake' field is disabled and greyed out for the single from Suspended market
        EXPECTED: * 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: * Warning message "Please beware that # of your selections has been suspended. Please remove suspended selections to get new multiple options"
        EXPECTED: **After OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware some of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out for suspended event
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection' for suspended event
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Some of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'Some of your selections have been suspended' with duration: 5s
        """
        pass

    def test_006_unsuspend_the_same_outcomeoutcomestatuscodeaand_at_the_same_tame_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Unsuspend the same outcome:
        DESCRIPTION: **outcomeStatusCode="A"**
        DESCRIPTION: and at the same tame have Betslip page opened to watch for updates
        EXPECTED: * 'Multiples' section is not rebuilt
        EXPECTED: **Before OX99**
        EXPECTED: * Both error messages disappear from the Betslip
        EXPECTED: * 'Stake' field and 'Bet Now' ('Log In and Bet') buttons are enabled and not greyed out for the single
        EXPECTED: **After OX99**
        EXPECTED: * Selection become enabled for unsuspended event
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button still disabled (untill stake will be entered)
        EXPECTED: * Messages disappear from the Betslip
        """
        pass
