import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C28027_Offers_displaying_for_users_with_different_VIP_levels_when_Show_to_New_user_option_value_is_set(Common):
    """
    TR_ID: C28027
    NAME: Offers displaying for users with different VIP levels when 'Show to New user' option value is set
    DESCRIPTION: This test case verifies Offers displaying for users with different VIP levels when 'Show to New user' option value is set
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-8527 VIP Segmentation for Offers
    DESCRIPTION: BMA-8953 Offers/Banners: Both & VIP Level populated = Show to new customers & existing users with specified VIP Level ONLY
    PRECONDITIONS: 1. 'Show to Both Users' option value is set for Offers
    PRECONDITIONS: 2. All other conditions for Offers displaying are met
    """
    keep_browser_open = True

    def test_001_clear_all_cookies_and_load_invictus_application(self):
        """
        DESCRIPTION: Clear all cookies and load Invictus application
        EXPECTED: *   'viplevel' cookie is NOT present in browser
        EXPECTED: *   'Existing user:True' cookie is NOT present to browser
        """
        pass

    def test_002_select_offer_with_empty_include_vip_levels_option_value_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select offer with empty 'Include VIP Levels' option value and verify its displaying
        EXPECTED: Offer is displayed in application
        """
        pass

    def test_003_select_offer_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP Levels' = 'X' and verify its displaying in application
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_004_login_to_application_with_user_for_which_viplevel__x(self):
        """
        DESCRIPTION: Login to application with user for which 'viplevel' = 'X'
        EXPECTED: 
        """
        pass

    def test_005_select_offer_with_empty_include_vip_levels_option_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Offer with empty 'Include VIP levels' option and verify its displaying
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_006_select_offer_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP levels' = 'X' and verify its displaying in application
        EXPECTED: Offer is NOT displayed in application
        """
        pass

    def test_007_select_offer_with_include_vip_levels__x_and_verify_its_displaying_in_applicationselect_offer_with_include_vip_levels__x_and_verify_its_displaying_in_applicatio(self):
        """
        DESCRIPTION: Select Offer with 'Include VIP levels' <> 'X' and verify its displaying in application
        DESCRIPTION: Select Offer with 'Include VIP levels' <> 'X' and verify its displaying in applicatio
        EXPECTED: Offer is NOT displayed in application
        """
        pass
