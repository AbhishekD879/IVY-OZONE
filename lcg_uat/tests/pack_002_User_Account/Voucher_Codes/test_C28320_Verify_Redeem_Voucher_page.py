import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.crl_tst2  # Coral only
# @pytest.mark.crl_stg2
# @pytest.mark.crl_prod no voucher codes
# @pytest.mark.crl_hl
@pytest.mark.user_account
@pytest.mark.vouchers
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-527')
@pytest.mark.quarantine
@pytest.mark.login
@vtest
class Test_C28320_Verify_Redeem_Voucher_page(BaseUserAccountTest):
    """
    TR_ID: C28320
    NAME: Verify Redeem Voucher page
    DESCRIPTION: This test case verifies 'Redeem Voucher' page
    """
    keep_browser_open = True

    def test_000_login(self):
        """
        DESCRIPTION: Login as default user
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_001_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu icon
        """
        self.site.header.right_menu_button.click()

    def test_002_click_voucher_code(self):
        """
        DESCRIPTION: 'Voucher Code' page is opened
        """
        self.site.right_menu.click_item(item_name=self.site.window_client_config.offers_menu_title)
        self.site.right_menu.click_item('VOUCHER CODES')
        self.site.wait_content_state('Voucher Code', timeout=5)

    def test_003_check_voucher_code_page(self):
        """
        DESCRIPTION: Check page header, back button and fields
        """
        page_title = self.site.voucher_code.header_line.page_title.title
        has_back_button = self.site.voucher_code.header_line.has_back_button
        self.assertEqual(page_title, vec.betslip.VOUCHER_FORM,
                         msg='Page title %s doesn\'t match the expected page title %s'
                         % (page_title, vec.betslip.VOUCHER_FORM))
        self.assertTrue(has_back_button, msg='Page doesn\'t have back button')

    def test_004_verify_sports_voucher_code(self):
        """
        DESCRIPTION: Check the sport voucher code section
        """
        sports_form = self.site.voucher_code.sports_form
        sports_form.voucher_input.value = tests.settings.voucher_codes_expired
        claim_now_btn_state = sports_form.claim_now_button.is_enabled(timeout=3)
        self.assertTrue(claim_now_btn_state, msg='Claim Now button is disabled')

        sports_form.claim_now_button.click()
        info_texts = self.site.voucher_code.info_panels_text
        for text in info_texts:
            self.assertEqual(text, vec.betslip.VOUCHER_PAST_VALID,
                             msg=f'Error message "{text}" is not as expected "{vec.betslip.VOUCHER_PAST_VALID}"')

        sports_form.voucher_input.value = tests.settings.voucher_codes_invalid

        sports_form.claim_now_button.is_enabled(timeout=3)
        sports_form.claim_now_button.click()
        self.site.voucher_code.info_panels.wait_to_change()
        info_texts2 = self.site.voucher_code.info_panels_text
        for text in info_texts2:
            self.assertEqual(text, vec.betslip.VOUCHER_SERVER_ERROR,
                             msg=f'Error message "{text}" is not as expected "{vec.betslip.VOUCHER_SERVER_ERROR}"')

        sports_form.voucher_input.value = '1111-1111-1111-1111-1111'
        claim_now_btn_state = sports_form.claim_now_button.is_enabled(expected_result=False)
        self.assertFalse(claim_now_btn_state, msg='Claim Now button is not disabled')

        sports_form.voucher_input.click()
        sports_form.voucher_input.clear()

        sports_form.voucher_input.value = tests.settings.voucher_codes_exceeded
        sports_form.claim_now_button.is_enabled(timeout=3)
        sports_form.claim_now_button.click()
        self.site.voucher_code.info_panels.wait_to_change()
        error_msg = self.site.voucher_code.info_panels_text[0]
        self.assertEqual(error_msg, vec.betslip.VOUCHER_CLAIMED_MAX,
                         msg=f'Error message "{error_msg}" is not as expected "{vec.betslip.VOUCHER_CLAIMED_MAX}"')

        # sports_form.voucher_input.click()  # no such voucher code
        # sports_form.voucher_input.value = tests.settings.voucher_codes_redeemed
        # sports_form.claim_now_button.is_enabled(timeout=3)
        # sports_form.claim_now_button.click()
        # self.site.voucher_code.info_panels.wait_to_change()
        # info_texts = self.site.voucher_code.info_panels_text
        # for text in info_texts:
        #     self.assertEqual(text, vec.betslip.VOUCHER_ALREADY_REDEEMED,
        #                      msg=f'Error message "{text}" is not as expected "{vec.betslip.VOUCHER_ALREADY_REDEEMED}"')

    def test_005_check_view_all_offers(self):
        """
        DESCRIPTION: Verify View all offers button is enabled and redirects to Promotions page
        """
        view_all_offers_btn_state = self.site.voucher_code.sports_form.view_offers_button.is_enabled()
        self.assertTrue(view_all_offers_btn_state, msg='View all offers button is disabled')
        self.site.voucher_code.sports_form.view_offers_button.click()
        self.site.wait_content_state('Promotions', timeout=5)
