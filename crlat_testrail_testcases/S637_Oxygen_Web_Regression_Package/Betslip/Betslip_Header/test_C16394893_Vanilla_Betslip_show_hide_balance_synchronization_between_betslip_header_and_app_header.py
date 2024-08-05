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
class Test_C16394893_Vanilla_Betslip_show_hide_balance_synchronization_between_betslip_header_and_app_header(Common):
    """
    TR_ID: C16394893
    NAME: [Vanilla] Betslip: show/hide balance synchronization between betslip header and app header
    DESCRIPTION: **This test case is applicable from OX99**
    DESCRIPTION: This test case verifies synchronization of show/hide balance functionality between betslip header and app header
    DESCRIPTION: AUTOTEST: [C24641831]
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have some selections added to betslip
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_user_balance_on__app_header__betslip_header(self):
        """
        DESCRIPTION: Verify displaying of user balance on:
        DESCRIPTION: - App header
        DESCRIPTION: - Betslip header
        EXPECTED: User balance is displayed on:
        EXPECTED: - App header
        EXPECTED: - Betslip header
        """
        pass

    def test_002_1_open_betslip_tap_account_balance_area__hide_balance_button2_verify_displaying_of_user_balance_on__betslip_header(self):
        """
        DESCRIPTION: 1) Open betslip, tap 'Account Balance' area > 'Hide Balance' button
        DESCRIPTION: 2) Verify displaying of user balance on:
        DESCRIPTION: - Betslip header
        EXPECTED: User balance is displayed as 'Balance' word
        """
        pass
