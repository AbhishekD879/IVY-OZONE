import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17995882_Vanilla_Verify_Connect_right_menu_option(Common):
    """
    TR_ID: C17995882
    NAME: [Vanilla] Verify Connect right menu option
    DESCRIPTION: UPDATE: Updated on 20.11.2019 - after discussion with Manu, Connect menu options where changed to be the same as on production
    DESCRIPTION: This test case is to verify all option menus under Connect right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env_with_regular_username_not_connect_card_number(self):
        """
        DESCRIPTION: Log in to test env with regular username (not connect card number)
        EXPECTED: User is logged in, My Account button appears
        """
        pass

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_003_clicktap_connect_menu_option(self):
        """
        DESCRIPTION: Click/tap Connect menu option
        EXPECTED: Connect menu is displayed with the following options:
        EXPECTED: - Shop exclusive promos
        EXPECTED: - Shop bet tracker
        EXPECTED: - Football bet filter
        EXPECTED: - Shop locator
        """
        pass

    def test_004_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_005_log_in_to_test_env_with_retail_user_username_with_connect_card_number(self):
        """
        DESCRIPTION: Log in to test env with Retail User username (with connect card number)
        EXPECTED: User is logged in, My Account button appears
        """
        pass

    def test_006_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_007_clicktap_connect_menu_option(self):
        """
        DESCRIPTION: Click/tap Connect menu option
        EXPECTED: Connect menu is displayed with the following options:
        EXPECTED: - Use connect online
        EXPECTED: - Shop exclusive promos
        EXPECTED: - Shop bet tracker
        EXPECTED: - Football bet filter
        EXPECTED: - Shop locator
        EXPECTED: - Change PIN
        """
        pass

    def test_008_reopen_right_menu__connect_and_clicktap_change_pin_option(self):
        """
        DESCRIPTION: Reopen right menu-> Connect and click/tap Change Pin option
        EXPECTED: Change Pin page is displayed
        """
        pass
