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
class Test_C59906310_Verify_Place_Bet_button_UI_for_Logged_out_user(Common):
    """
    TR_ID: C59906310
    NAME: Verify Place Bet button UI for Logged out user
    DESCRIPTION: This test case verifies 'Place Bet' button UI for Logged out user
    PRECONDITIONS: - The app is installed and launched
    PRECONDITIONS: Designs:
    PRECONDITIONS: Ladbrokes: https://zpl.io/a3BJ7kW
    PRECONDITIONS: Coral: https://zpl.io/brZOn05
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is added to the Betslip
        """
        pass

    def test_002_expand_betslip(self):
        """
        DESCRIPTION: Expand Betslip
        EXPECTED: - The Betslip is expanded
        EXPECTED: - Keyboard is in view
        EXPECTED: - No one value is inputed
        """
        pass

    def test_003_verify_place_bet_button(self):
        """
        DESCRIPTION: Verify 'Place bet' button
        EXPECTED: - 'Place Bet' CTA is 'Login & Place Bet'
        EXPECTED: - Button is in view but inactiv as per design:
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/119064638)
        EXPECTED: Ladbrokes:
        EXPECTED: Design is not provided
        """
        pass

    def test_004_enter_any_value_into_stake_field(self):
        """
        DESCRIPTION: Enter any value into 'Stake' field
        EXPECTED: Stake value is inputed
        """
        pass

    def test_005_verify_place_bet_button(self):
        """
        DESCRIPTION: Verify 'Place bet' button
        EXPECTED: - 'Place bet' CTA is 'Login & Place Bet'
        EXPECTED: - Button is in view and active as per design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/119064639)
        EXPECTED: Coral:
        EXPECTED: Design is not provided
        """
        pass
