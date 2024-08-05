import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C11257183_Betslip_header_UI(Common):
    """
    TR_ID: C11257183
    NAME: Betslip: header UI
    DESCRIPTION: **This test case is applicable from OX99**
    DESCRIPTION: This test case verifies betslip header UI
    PRECONDITIONS: - You should have a user with free bets
    PRECONDITIONS: - You should be logged out and have no selections added to betslip
    PRECONDITIONS: - Betslip should be opeend
    """
    keep_browser_open = True

    def test_001_verify_betslip_header_ui(self):
        """
        DESCRIPTION: Verify betslip header UI
        EXPECTED: - 'Betslip' label is centered in the header and white colored
        EXPECTED: - "Please log in to see your balance" message is NOT displayed below the betslip header
        EXPECTED: **Coral:** Header is blue colored
        EXPECTED: **Ladbrokes:** Header is blue red
        """
        pass

    def test_002___login_as_user_with_free_bets__add_some_selections_to_betslip__verify_betslip_header_ui(self):
        """
        DESCRIPTION: - Login as user with free bets
        DESCRIPTION: - Add some selections to betslip
        DESCRIPTION: - Verify betslip header UI
        EXPECTED: - 'Betslip' label is centered in the header and white colored
        EXPECTED: - Free bets icon is NOT displayed below the betslip header
        EXPECTED: **Coral:**
        EXPECTED: - Header is blue colored
        EXPECTED: - Account balance is displayed on a dark blue background area next to the 'Betslip' label at the top right corner
        EXPECTED: **Ladbrokes:**
        EXPECTED: - Header is blue red
        EXPECTED: - Account balance is displayed on a dark red background area next to the 'Betslip' label at the top right corner
        """
        pass

    def test_003___tap_account_balance_area__hide_balance_button_and_verify_account_balance_area(self):
        """
        DESCRIPTION: - Tap 'Account Balance' area > 'Hide Balance' button and verify 'Account Balance' area
        EXPECTED: **Coral:** Account balance is replaced with white colored 'Balance' word on a dark blue background area
        EXPECTED: **Ladbrokes:** Account balance is replaced with white colored 'Balance' word on a dark red background area
        """
        pass
