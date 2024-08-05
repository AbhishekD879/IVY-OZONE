import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C59906969_Verify_Place_Bet_button_UI_after_Price_Change(Common):
    """
    TR_ID: C59906969
    NAME: Verify Place Bet button UI after Price Change
    DESCRIPTION: This test case verifies Place Bet button UI after Price Change
    PRECONDITIONS: - The app is installed and launched
    PRECONDITIONS: - User is logged in to the Application
    PRECONDITIONS: - Selection is added to the Betslip
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://zpl.io/VD03r5v
    PRECONDITIONS: Coral: https://zpl.io/V0BOGeO
    """
    keep_browser_open = True

    def test_001_expand_betslip(self):
        """
        DESCRIPTION: Expand Betslip
        EXPECTED: - The Betslip is expanded
        EXPECTED: - Keyboard is in view
        """
        pass

    def test_002_enter_any_value_into_stake_field(self):
        """
        DESCRIPTION: Enter any value into 'Stake' field
        EXPECTED: - Stake value is inputed
        EXPECTED: - 'Place bet' CTA is in view and active
        """
        pass

    def test_003___tap_on_place_bet_button__and_during_bet_placement_simulate_price_change(self):
        """
        DESCRIPTION: - Tap on 'Place Bet' Button
        DESCRIPTION: - AND during bet placement simulate price change
        EXPECTED: - The 'Place bet' CTA text is updated as per designs:
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/119071141)
        EXPECTED: Ladbrokes:
        EXPECTED: is not provided
        EXPECTED: - User need to accept the change by tapping the CTA once more to trigger bet placement
        """
        pass
