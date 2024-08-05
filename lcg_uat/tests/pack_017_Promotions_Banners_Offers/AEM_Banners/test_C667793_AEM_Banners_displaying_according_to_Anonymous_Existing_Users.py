import pytest
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.banners
# @pytest.mark.user_account
# @pytest.mark.aem_banners
# @pytest.mark.medium
# @pytest.mark.promotions_banners_offers
# @pytest.mark.desktop
# @pytest.mark.safari
# @pytest.mark.login
# @pytest.mark.registration
# @vtest
@pytest.mark.na
class Test_C667793_AEM_Banners_displaying_according_to_Anonymous_Existing_Users(BaseAEMBannersTest):
    """
    TR_ID: C667793
    NAME: AEM Banners displaying according to Anonymous / Existing Users
    DESCRIPTION: This test case verifies AEM Banners displaying according to New / Existing Users
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. This test case should be checked on Mobile, Tablet, Desktop
    PRECONDITIONS: 3. To check data from **offer** response open Dev tools -> Network tab
    PRECONDITIONS: 4. User is logged out
    PRECONDITIONS: 5. Local storage is cleared
    """
    keep_browser_open = True

    def test_001_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'userType/anonymous' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        """
        result = self.site.contents.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')
        offer_call = self.get_offers_url()

        parameter = 'userType/anonymous/' if self.brand == 'bma' else 'userType/new/'
        self.assertIn(parameter, offer_call,
                      msg=f'Can not find parameter "{parameter}" in "{offer_call}"')

    def test_002_go_to_any_sport__race_landing_page_and_repeat_step_2(self):
        """
        DESCRIPTION: Go to any <Sport> / <Race> landing page and repeat step #2
        EXPECTED: Appropriate sport / race page opened
        """
        self.navigate_to_page(name='sport/tennis')
        self.site.wait_content_state('tennis')

    def test_003_register_new_user(self):
        """
        DESCRIPTION: Register new user
        EXPECTED: User is logged in
        """
        user = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user)
        self.site.wait_content_state('tennis')

    def test_004_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'userType/existing' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        """
        self.site.back_button_click()
        self.site.wait_content_state('Homepage')
        offer_call = self.get_offers_url()
        self.assertIn('userType/existing/', offer_call,
                      msg=f'Can not find "userType/existing/" in "{offer_call}"')

    def test_005_go_to_any_sport_race_landing_page_and_repeat_step_5(self):
        """
        DESCRIPTION: Go to any <Sport> / <Race> landing page and repeat step #4
        EXPECTED: Appropriate sport / race page opened
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        self.test_004_verify_dynamic_banners_loading()

    def test_006_log_out_and_repeat_step_5(self):
        """
        DESCRIPTION: Log out and repeat step #5
        EXPECTED: User is not signed in.
        EXPECTED: * 'userType/existing' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        """
        self.site.logout()
        self.site.wait_content_state('Homepage')
        offer_call = self.get_offers_url()
        self.assertIn('userType/existing/', offer_call,
                      msg=f'Can not find "userType/existing/" in "{offer_call}"')

    def test_007_clear_local_storage(self):
        """
        DESCRIPTION: Clear local storage
        EXPECTED: Local storage is cleared
        """
        self.delete_cookies()

    def test_008_log_in_with_different_user_and_repeat_steps_5_7(self):
        """
        DESCRIPTION: Log in with different user and repeat steps #5-7
        """
        self.site.login(async_close_dialogs=False, timeout_close_dialogs=5)
        self.site.wait_content_state('Homepage')
        offer_call = self.get_offers_url()
        self.assertIn('userType/existing/', offer_call,
                      msg=f'Can not find "userType/existing/" in "{offer_call}"')
