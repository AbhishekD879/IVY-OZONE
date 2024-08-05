import voltron.environments.constants as vec
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
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28323_Redeem_Invalid_Sports_Voucher_Code(BaseUserAccountTest):
    """
    TR_ID: C28323
    NAME: Redeem Invalid Sports Voucher Code
    DESCRIPTION: This test case verifies redemption of an Invalid Sports Voucher Code
    """
    keep_browser_open = True

    def test_001_click_login(self):
        """
        DESCRIPTION: Login as default user
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(item_name=self.site.window_client_config.offers_menu_title)

    def test_002_click_voucher_code(self):
        """
        DESCRIPTION: 'Voucher Code' page is opened
        """
        self.site.right_menu.click_item('VOUCHER CODES')
        self.site.wait_content_state('Voucher Code', timeout=5)

    def test_003_check_voucher_code_page(self):
        """
        DESCRIPTION: Check page header, back button and fields
        """
        page_title = self.site.voucher_code.header_line.page_title.title
        has_back_button = self.site.voucher_code.header_line.has_back_button
        self.assertEqual(page_title, vec.betslip.VOUCHER_FORM,
                         msg=f'Page title "{page_title}" doesn\'t match the expected page title '
                             f'"{vec.betslip.VOUCHER_FORM}"')
        self.assertTrue(has_back_button, msg='Page doesn\'t have back button')

    def test_004_verify_games_voucher_code(self):
        """
        DESCRIPTION: Check the sport voucher code section
        """
        sports_form = self.site.voucher_code.sports_form
        sports_form.voucher_input.value = '1111122222'
        is_disabled = sports_form.claim_now_button.is_enabled(expected_result=False)
        self.assertFalse(is_disabled, msg='Claim Now button is not disabled')

        # enter promocode of invalid format (more than 30 digits)
        self.site.voucher_code.sports_form.voucher_input.value = '1' * 31
        claim_now_btn_state = self.site.voucher_code.sports_form.claim_now_button.is_enabled(expected_result=False)
        self.assertFalse(claim_now_btn_state, msg='Claim Now button is not disabled')

    def test_005_check_view_all_offers(self):
        """
        DESCRIPTION: Verify View all offers button is enabled and redirects to Promotions page
        """
        view_all_offers_btn_state = self.site.voucher_code.sports_form.view_offers_button.is_enabled()
        self.assertTrue(view_all_offers_btn_state, msg='View all offers button is disabled')
        self.site.voucher_code.sports_form.view_offers_button.click()
        self.site.wait_content_state('Promotions')
