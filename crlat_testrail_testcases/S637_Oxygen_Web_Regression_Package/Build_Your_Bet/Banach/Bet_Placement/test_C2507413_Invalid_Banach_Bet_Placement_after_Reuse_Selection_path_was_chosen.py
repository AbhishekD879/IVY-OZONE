import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2507413_Invalid_Banach_Bet_Placement_after_Reuse_Selection_path_was_chosen(Common):
    """
    TR_ID: C2507413
    NAME: [Invalid] Banach. Bet Placement after Reuse Selection path was chosen
    DESCRIPTION: Test case verifies bet placement after Reuse Selection
    DESCRIPTION: NOTE: 'Reuse selection' button seems to be removed in OX100 redesign
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for successful selections adding| 51001
    PRECONDITIONS: || Response message for failed selections adding| 51002
    PRECONDITIONS: || Client sends Place bet message | 50011
    PRECONDITIONS: || Response message for Bet Placement | 51101
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: **User sees Betslip after Reuse Selection path was chosen**
    """
    keep_browser_open = True

    def test_001_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on PLACE BET button
        EXPECTED: - Bet receipt is displayed
        EXPECTED: - User balance is updated
        """
        pass

    def test_002_verify_bet_receipt_on_ui(self):
        """
        DESCRIPTION: Verify Bet receipt on UI
        EXPECTED: Bet receipt contains correct info for the following items:
        EXPECTED: - Title Bet receipt
        EXPECTED: - Names of selections as they were on dashboard
        EXPECTED: - Odds
        EXPECTED: - Bet id
        EXPECTED: - Stake and Est. Returns
        EXPECTED: - buttons "Reuse selection" and "Done"
        """
        pass

    def test_003_tap_done_button(self):
        """
        DESCRIPTION: Tap Done button
        EXPECTED: - Bet receipt is removed
        EXPECTED: - Selections are cleared from UI
        """
        pass
