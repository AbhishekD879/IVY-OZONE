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
class Test_C29063_Betslip_Reflection_on_Sport_Market_Suspended_Unsuspended_for_Single_Bet(Common):
    """
    TR_ID: C29063
    NAME: Betslip Reflection on <Sport> Market Suspended/Unsuspended for Single Bet
    DESCRIPTION: This test case verifies Betslip reflection for Single bet when its Market is Suspended.
    DESCRIPTION: AUTOTEST: [C13122022]
    PRECONDITIONS: Access to OB TI is required
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
        EXPECTED: Betslip is opened, selection is displayed
        """
        pass

    def test_003_enter_stake(self):
        """
        DESCRIPTION: Enter Stake
        EXPECTED: 
        """
        pass

    def test_004_trigger_suspension_of_the_market_where_selection_belongs_tomarketstatuscodesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger suspension of the market where selection belongs to:
        DESCRIPTION: **marketStatusCode="S" **
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX 99**
        EXPECTED: 1. 'Stake' field is disabled and greyed out.
        EXPECTED: 2. 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: 3. Error message 'Sorry, the market has been suspended' is shown on the red background below the single
        EXPECTED: 4. Warning message 'Please beware that 1 of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **From OX99**
        EXPECTED: **Coral:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: **Ladbrokes:**
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_005_make_the_market_active_againmarketstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make the market active again:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: * 'Stake' field and 'Bet Now' ('Log In and Bet') button is enabled
        EXPECTED: * Both error messages disappear from the Betslip
        EXPECTED: **After OX99**
        EXPECTED: * Selection become enabled
        EXPECTED: * 'Place Bet ( 'Login&Place Bet' (Coral)/'Login and Place Bet'(Ladbrokes)) button enabled
        EXPECTED: * Messages disappear from the Betslip
        """
        pass
