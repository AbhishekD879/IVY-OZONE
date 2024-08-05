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
class Test_C28121_Verify_REUSE_SELECTION_and_DONE_buttons_on_the_Bet_Receipt(Common):
    """
    TR_ID: C28121
    NAME: Verify REUSE SELECTION and DONE buttons on the Bet Receipt
    DESCRIPTION: This test case verifies REUSE SELECTION and DONE buttons on the Bet Receipt
    DESCRIPTION: AUTOTEST C2604507
    PRECONDITIONS: - User is logged in with positive balance
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add selection/(s) to the Betslip
        EXPECTED: Selection is displayed on the Betslip
        """
        pass

    def test_003_enter_value_into_stake_field_and_place_bet(self):
        """
        DESCRIPTION: Enter value into 'Stake' field and place bet
        EXPECTED: -   Bet is placed
        EXPECTED: -   Bet Receipt is present with 'REUSE SELECTION' and 'DONE' buttons at the bottom of Bet Receipt
        """
        pass

    def test_004_tap_reuse_selection_button(self):
        """
        DESCRIPTION: Tap 'REUSE SELECTION' button
        EXPECTED: - Bet Receipt is closed
        EXPECTED: - Betslip opening is triggered and contains the same selection/(s)
        EXPECTED: - Stake field is empty
        """
        pass

    def test_005_enter_value_into_stake_field_and_place_bets(self):
        """
        DESCRIPTION: Enter value into 'Stake' field and place bet/(s)
        EXPECTED: -   Bet/(s) is placed
        EXPECTED: -   Bet Receipt is present with 'REUSE SELECTION' and 'DONE' buttons
        """
        pass

    def test_006_tap_done_button(self):
        """
        DESCRIPTION: Tap 'DONE' button
        EXPECTED: -   Bet Receipt is closed
        EXPECTED: -   Tablet/Desktop: message informs user that there are no bets in Betslip
        EXPECTED: -   Mobile: Betslip is closed
        """
        pass
