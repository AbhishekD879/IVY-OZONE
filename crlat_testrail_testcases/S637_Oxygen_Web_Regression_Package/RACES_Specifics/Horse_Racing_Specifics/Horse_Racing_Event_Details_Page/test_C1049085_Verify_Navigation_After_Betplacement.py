import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1049085_Verify_Navigation_After_Betplacement(Common):
    """
    TR_ID: C1049085
    NAME: Verify Navigation After Betplacement
    DESCRIPTION: This test case verifies navigation after bet placement when user selects outcome from event details page
    DESCRIPTION: Applies to mobile, tablet and desktop
    DESCRIPTION: **Jira ticket: BMA-5233, BMA-11096**
    DESCRIPTION: AUTOTEST: [C9698409]
    PRECONDITIONS: User should be logged in to place a bet.
    """
    keep_browser_open = True

    def test_001_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_add_selection_to_the_quick_betbetslip__enter_stake_in_stake_field_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Add selection to the Quick Bet/BetSlip > Enter stake in 'Stake' field and tap 'Bet Now' button
        EXPECTED: * Bet is successfully placed
        EXPECTED: * 'Quick Bet'/Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: * Balance is decreased accordingly
        """
        pass

    def test_003_tap_done_button_on_bet_receipt_page(self):
        """
        DESCRIPTION: Tap 'Done' button on Bet Receipt page
        EXPECTED: * Bet Slip Slider closes
        EXPECTED: * User stays on the same page
        """
        pass
