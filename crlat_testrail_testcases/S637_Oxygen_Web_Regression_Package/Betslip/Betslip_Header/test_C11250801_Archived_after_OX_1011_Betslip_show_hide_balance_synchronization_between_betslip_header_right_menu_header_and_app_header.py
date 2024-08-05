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
class Test_C11250801_Archived_after_OX_1011_Betslip_show_hide_balance_synchronization_between_betslip_header_right_menu_header_and_app_header(Common):
    """
    TR_ID: C11250801
    NAME: [Archived after OX 101.1] Betslip: show/hide balance synchronization between betslip header, right menu header and app header
    DESCRIPTION: **This test case is applicable from OX99**
    DESCRIPTION: This test case verifies synchronization of show/hide balance functionality between betslip header, right menu header and app header
    DESCRIPTION: AUTOTEST: [C12192723]
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have some selections added to betslip
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_user_balance_on__app_header__right_menu_header__betslip_header(self):
        """
        DESCRIPTION: Verify displaying of user balance on:
        DESCRIPTION: - App header
        DESCRIPTION: - Right menu header
        DESCRIPTION: - Betslip header
        EXPECTED: User balance is displayed on:
        EXPECTED: **Mobile and Tablet**
        EXPECTED: - App header
        EXPECTED: - Right menu header
        EXPECTED: **Mobile**
        EXPECTED: - Betslip header
        """
        pass

    def test_002_1_open_right_menu_and_tap_hide_balance2_verify_displaying_of_user_balance_on__app_header__right_menu_header__betslip_header(self):
        """
        DESCRIPTION: 1) Open right menu and tap 'Hide Balance'
        DESCRIPTION: 2) Verify displaying of user balance on:
        DESCRIPTION: - App header
        DESCRIPTION: - Right menu header
        DESCRIPTION: - Betslip header
        EXPECTED: User balance is NOT displayed on:
        EXPECTED: **Mobile and Tablet**
        EXPECTED: - App header
        EXPECTED: - Right menu header
        EXPECTED: **Mobile**
        EXPECTED: - Betslip header
        """
        pass

    def test_003_mobile_only1_open_betslip_tap_account_balance_area__show_balance_button2_verify_displaying_of_user_balance_on__app_header__right_menu_header__betslip_header(self):
        """
        DESCRIPTION: **Mobile only:**
        DESCRIPTION: 1) Open betslip, tap 'Account Balance' area > 'Show Balance' button
        DESCRIPTION: 2) Verify displaying of user balance on:
        DESCRIPTION: - App header
        DESCRIPTION: - Right menu header
        DESCRIPTION: - Betslip header
        EXPECTED: User balance is displayed on:
        EXPECTED: **Mobile only:**
        EXPECTED: - App header
        EXPECTED: - Right menu header
        EXPECTED: - Betslip header
        """
        pass
