import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2024331_Verify_AEM_banner_carousel_on_the_connect_landing_page(Common):
    """
    TR_ID: C2024331
    NAME: Verify AEM banner carousel on the connect landing page
    DESCRIPTION: This test case verifies AEM banners carousel on Connect landing page
    DESCRIPTION: |||:Environment |:Endpoint
    DESCRIPTION: || dev |  https://ec2-35-177-34-113.eu-west-2.compute.amazonaws.com
    DESCRIPTION: || stg |  https://banners-cms-stg.coral.co.uk
    DESCRIPTION: || prod |  https://banners-cms.coral.co.uk
    DESCRIPTION: Parameters and possible values:
    DESCRIPTION: |||:Parameter|:Possible values
    DESCRIPTION: || locale | en-gb
    DESCRIPTION: || channel | connect
    DESCRIPTION: || brand | coral
    DESCRIPTION: || userType | existing; anonymous
    DESCRIPTION: || imsLevel | 1; 2; 3; 4; 5; 6; 7; 8; 9; 10; 11; 12; 13; 14; 17
    PRECONDITIONS: Go to CMS and make sure AEM banners are enabled: System-configuration -> DYNAMICBANNERS -> enabled
    PRECONDITIONS: 1. Load sportsbook app
    PRECONDITIONS: 2. Select 'Connect' item on header ribbon (user remains logged out)
    """
    keep_browser_open = True

    def test_001_verify_aem_banners_presence_on_connect_landing_page(self):
        """
        DESCRIPTION: Verify AEM banners presence on Connect Landing page
        EXPECTED: * AEM banners carousel is at the top of the page
        """
        pass

    def test_002_verify_that_aem_banners_are_displayed_correctly_for_the_logged_out_user(self):
        """
        DESCRIPTION: Verify that AEM banners are displayed correctly for the logged out user
        EXPECTED: - Banners images and sequence correspond to JSON received from the link ***endpoint*/bin/lc/coral/offers.json/locale/en-gb/channels/connect/pages/homepage/userType/anonymous/response.json**
        EXPECTED: - After tapping banner user is redirected to target Url (from JSON)
        """
        pass

    def test_003__log_in_with_in_shop_user_using_connect_card_number_and_pin_go_to_connect_landing_page_and_verify_that_aem_banners_are_displayed_correctly_for_in_shop_logged_in_user(self):
        """
        DESCRIPTION: * Log in with In-Shop user (using Connect card number and PIN)
        DESCRIPTION: * Go to Connect Landing page and verify that AEM banners are displayed correctly for in-shop logged in user
        EXPECTED: * Banners images and sequence correspond to JSON received from the link
        EXPECTED: ***endpoint*/bin/lc/coral/offers.json/locale/en-gb/channels/connect/pages/homepage/userType/anonymous/response.json**
        EXPECTED: * After tapping banner user is redirected to target Url (from JSON)
        """
        pass

    def test_004__log_in_with_multi_channel_user_using_username_and_password_verify_that_aem_banners_are_displayed_correctly_for_mc_logged_in_user_e_g_with_viplevel__1(self):
        """
        DESCRIPTION: * Log in with Multi-channel user (using username and password)
        DESCRIPTION: * Verify that AEM banners are displayed correctly for MC logged in user (e. g.: with VipLevel = 1)
        EXPECTED: * Banners images and sequence correspond to JSON received from the link
        EXPECTED: ***endpoint*/bin/lc/coral/offers.json/locale/en-gb/channels/connect/pages/homepage/userType/existing/imsLevel/1/response.json**
        EXPECTED: * After tapping banner user is redirected to target Url (from JSON)
        """
        pass

    def test_005__log_in_under_multi_channel_user_with_another_viplevel_egviplevel__12_and_verify_that_set_of_banners_has_changed(self):
        """
        DESCRIPTION: * Log in under Multi-channel user with another VipLevel, e.g.:VipLevel = 12, and verify that set of banners has changed
        EXPECTED: * Banners images and sequence correspond to JSON received from the link
        EXPECTED: ***endpoint*/bin/lc/coral/offers.json/locale/en-gb/channels/connect/pages/homepage/userType/existing/imsLevel/12/response.json**
        EXPECTED: * After tapping banner user is redirected to target Url (from JSON)
        """
        pass
