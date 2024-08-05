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
class Test_C47660499_Verify_BOG_icon_on_Bet_Receipt(Common):
    """
    TR_ID: C47660499
    NAME: Verify BOG icon on Bet Receipt
    DESCRIPTION: This test case verifies that the BOG icon is displayed on the Bet Receipt and My Bets section
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-49331]
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has a positive balance
    PRECONDITIONS: * BOG has been enabled in CMS
    PRECONDITIONS: * 'GP available' checkbox is selected for the event in TI tool on the market level
    """
    keep_browser_open = True

    def test_001_add_selection_with_available_bog_icon_to_betslipquickbet(self):
        """
        DESCRIPTION: Add selection with available BOG icon to Betslip/Quickbet
        EXPECTED: Selection is added to the BetSlip
        """
        pass

    def test_002_enter_a_value_in_the_stake_field_and_place_a_bet(self):
        """
        DESCRIPTION: Enter a value in the 'Stake' field and place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_003_verify_bog_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'BOG' icon on the Bet Receipt
        EXPECTED: * 'BOG' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        """
        pass

    def test_004_add_selection_without_bog_icon_available_to_betslipquickbet_for_mobile_and_place_bet(self):
        """
        DESCRIPTION: Add selection without 'BOG' icon available to Betslip/Quickbet (for mobile) and place bet
        EXPECTED: There is NO 'BOG' icon displayed on Betslip/Quickbet (for mobile)
        """
        pass

    def test_005_add_a_couple_of_hourse_selection_with_bog_icon_to_betslipquickbet(self):
        """
        DESCRIPTION: Add a couple of <Hourse> selection with BOG icon to Betslip/Quickbet
        EXPECTED: * <Hourse> selections are added to the BetSlip
        EXPECTED: * Multiple bets are shown on the BetSlip
        """
        pass

    def test_006_enter_a_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter a value in 'Stake' field for one of Multiple bet and place a bet
        EXPECTED: * Multiple Bet is placed successfully
        EXPECTED: * Bet Receipt for Multiple is displayed
        """
        pass

    def test_007_verify_bog_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'BOG' icon on the Bet Receipt
        EXPECTED: 'BOG' icon is displayed under EACH selection (under market name/event name section)
        """
        pass
