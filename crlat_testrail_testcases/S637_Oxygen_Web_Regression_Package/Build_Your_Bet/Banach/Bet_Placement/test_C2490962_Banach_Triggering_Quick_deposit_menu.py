import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.build_your_bet
@vtest
class Test_C2490962_Banach_Triggering_Quick_deposit_menu(Common):
    """
    TR_ID: C2490962
    NAME: Banach. Triggering Quick deposit menu
    DESCRIPTION: Test case verifies triggering Quick deposit menu and entering CVV and Amount to continue Banach betting
    DESCRIPTION: AUTOTEST [C2589741]
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **User has added Banach selections dashboard and tapped PLACE BET button**
    """
    keep_browser_open = True

    def test_001_enter_a_stake_higher_then_current_user_balance_in_a_stake(self):
        """
        DESCRIPTION: Enter a stake higher then current user balance in a stake
        EXPECTED: - Total Stake and Estimated Returned are populated with the values
        EXPECTED: Total Stake - amount entered by user
        EXPECTED: Est.Returns - calculated based on Odds value: (odds + 1)*stake
        EXPECTED: - User message above Betslip:
        EXPECTED: Before OX100:
        EXPECTED: **Funds needed for bet: %**
        EXPECTED: After OX100:
        EXPECTED: **Please deposit a min of £% to continue placing your bet**
        EXPECTED: where % is a difference between entered amount and current balance
        EXPECTED: - Buttons **Back** and **Make a quick deposit** are present below Betslip
        """
        pass

    def test_002_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on MAKE A DEPOSIT button
        EXPECTED: - Quick deposit menu is opened
        EXPECTED: - DEPOSIT AND PLACE BET button is disabled
        """
        pass

    def test_003_enter_cvv_and_amount(self):
        """
        DESCRIPTION: Enter CVV and Amount
        EXPECTED: DEPOSIT AND PLACE BET button is enabled
        """
        pass
