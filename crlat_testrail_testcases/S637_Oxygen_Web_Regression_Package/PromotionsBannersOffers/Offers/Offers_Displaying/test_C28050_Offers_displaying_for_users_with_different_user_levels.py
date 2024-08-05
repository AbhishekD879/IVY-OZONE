import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C28050_Offers_displaying_for_users_with_different_user_levels(Common):
    """
    TR_ID: C28050
    NAME: Offers displaying for users with different user levels
    DESCRIPTION: This test case verifies Offers displaying for users with different user levels.
    PRECONDITIONS: 1) To load CMS use the next links:
    PRECONDITIONS: DEV -  https://coral-cms-dev0.symphony-solutions.eu/login
    PRECONDITIONS: TST2 -  https://coral-cms-tst2.symphony-solutions.eu/login
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/login
    PRECONDITIONS: HL -  https://coral-cms-hl.symphony-solutions.eu/login
    PRECONDITIONS: PROD -  https://coral-cms.symphony-solutions.eu/login
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    PRECONDITIONS: 3) There are offers with different value for 'Include VIP Levels' option
    PRECONDITIONS: To verify User's level  enter in Console: window.bmadata and check 'viplevel' parameter value. or go to Resources -> Cookies -> 'viplevel'
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_do_not_log_into_it_cookies_and_storage_should_be_clearverify_offers_displaying_for_logged_out_user(self):
        """
        DESCRIPTION: Load Oxygen application and do not log into it (Cookies and storage should be clear).
        DESCRIPTION: Verify Offers displaying for logged out user.
        EXPECTED: *   Offers with filled in 'Include VIP levels' field are displayed
        EXPECTED: *   Offers with empty 'Include VIP levels' field are displayed
        """
        pass

    def test_002_login_to_application_with_user_for_which_viplevel_x_where_x___any_digital_number(self):
        """
        DESCRIPTION: Login to application with user for which 'viplevel': "X", where X - any digital number
        EXPECTED: 
        """
        pass

    def test_003_verify_offers_displaying_when_include_vip_levels__x_for_this_offer(self):
        """
        DESCRIPTION: Verify Offers displaying when 'Include VIP Levels' = 'X' for this Offer
        EXPECTED: Offer is displayed in application
        """
        pass

    def test_004_verify_offer_displaying_when_include_vip_levels__numbers_diapason_which_includes_xfor_example_if_x__3_then_appropriate_diapason_is_2_4(self):
        """
        DESCRIPTION: Verify offer displaying when 'Include VIP Levels' = <*numbers diapason which includes X*>.
        DESCRIPTION: For example, if X = 3, then appropriate diapason  is 2-4
        EXPECTED: Offer is displayed in application
        """
        pass

    def test_005_logout_from_the_application_previously_logged_in_user_vip_level_is_used_after_log_out(self):
        """
        DESCRIPTION: Logout from the application (previously logged in user vip level is used after log out)
        EXPECTED: Offer is displayed in application
        """
        pass

    def test_006_verify_offer_displaying_when_include_vip_levels__x_for_this_offer(self):
        """
        DESCRIPTION: Verify Offer displaying when 'Include VIP levels' <> X for this Offer
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_007_verify_offer_displaying_when_include_vip_levels__numbers_diapason_which_does_not_include_xfor_example_if_x__3_then_appropriate_diapason_is_4_7(self):
        """
        DESCRIPTION: Verify Offer displaying when 'Include VIP Levels' = *<numbers diapason which does not include X>.*
        DESCRIPTION: For example, if X = 3, then appropriate diapason is 4-7
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_008_logout_from_the_application_previously_logged_in_user_vip_level_is_used_after_log_out(self):
        """
        DESCRIPTION: Logout from the application (previously logged in user vip level is used after log out)
        EXPECTED: Offer is NOT displayed in application
        """
        pass
