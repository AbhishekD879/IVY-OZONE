import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
# @pytest.mark.crl_tst2  # Coral only
# @pytest.mark.crl_stg2
@pytest.mark.portal_only_test
@pytest.mark.user_account
@pytest.mark.vouchers
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C28329_Redeem_Sports_Voucher_Code_after_Logout(BaseUserAccountTest):
    """
    TR_ID: C28329
    NAME: Redeem Sports Voucher Code after Logout
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log In
        EXPECTED: User is logged in
        """
        self.site.login(async_close_dialogs=False)

    def test_002_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu icon
        EXPECTED: Right Menu is opened
        """
        self.site.header.right_menu_button.click()

    def test_003_tap_on_offers_item(self):
        """
        DESCRIPTION: Tap on 'OFFERS' menu item
        EXPECTED: 'OFFERS' page is opened
        """
        self.site.right_menu.click_item(item_name=self.site.window_client_config.offers_menu_title)

    def test_004_select_voucher_code_from_my_account_submenu(self):
        """
        DESCRIPTION: Select 'Voucher Code' from 'My Account' submenu
        EXPECTED: 'Redeem Voucher' page is opened
        """
        self.site.right_menu.click_item('VOUCHER CODES')
        self.site.wait_content_state('Voucher Code', timeout=5)

    def test_005_enter_any_voucher_code_in_sports_voucher_code_field(self):
        """
        DESCRIPTION: Enter any Voucher Code in ** 'Sports Voucher Code:'**field
        EXPECTED: 'Claim Now' button became active
        """
        sports_form = self.site.voucher_code.sports_form
        sports_form.voucher_input.value = tests.settings.voucher_codes_invalid
        is_enabled = sports_form.claim_now_button.is_enabled(timeout=3)
        self.assertTrue(is_enabled, msg='Claim Now button is not enabled')

    def test_006_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: User should be logged in, but session should be OVER on the server
        EXPECTED: To trigger event when session is over on the server please perform the following steps:
        EXPECTED: Login to Invictus in one browser tab -> open 'Redeem Voucher' page
        EXPECTED: Login to Invictus in second browser tab, logout -> session is over on the server
        EXPECTED: Navigate back to the first browser tab where user is still logged in, however there is no active session already
        """
        self.logout_in_new_tab()

    def test_007_verify_sports_voucher_code_section(self):
        """
        DESCRIPTION: Verify  'Sports Voucher Code:'  section
        EXPECTED: User is logged out from the application
        EXPECTED: User is not able to see the content of '**Redeem Voucher**' page
        EXPECTED: User is redirected to the Homepage
        """
        self.verify_logged_out_state()
