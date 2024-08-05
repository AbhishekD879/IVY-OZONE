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
class Test_C29308_Promotions_displaying_with_different_VIP_levels_when_Show_to_Existing_users_option_value(Common):
    """
    TR_ID: C29308
    NAME: Promotions displaying with different VIP levels when 'Show to Existing users' option value
    DESCRIPTION: This test case verifies Promotions displaying for users with different VIP levels when 'Show to Existing users' option value is set
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-8896 Promotions - Add New/Existing functionality
    PRECONDITIONS: 1. 'Show to Existing Users' option value is set for Promotions
    PRECONDITIONS: 2. All other conditions for Promotions displaying are met
    """
    keep_browser_open = True

    def test_001_clear_all_cookies_and_load_invictus_application(self):
        """
        DESCRIPTION: Clear all cookies and load Invictus application
        EXPECTED: *   'viplevel' cookie is NOT present in browser
        EXPECTED: *   'Existing user:True' cookie is NOT present to browser
        """
        pass

    def test_002_select_promotion_with_empty_include_vip_levels_option_value_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with empty 'Include VIP Levels' option value and verify its displaying
        EXPECTED: Promotion is NOT displayed in application
        """
        pass

    def test_003_select_promotion_with_include_vip_levels__x_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels'  = 'X' and verify its displaying
        EXPECTED: Promotion is NOT displayed in application
        """
        pass

    def test_004_login_to_application_with_user_for_which_viplevel__x(self):
        """
        DESCRIPTION: Login to application with user for which 'viplevel' = 'X'
        EXPECTED: 
        """
        pass

    def test_005_select_promotion_with_empty_include_vip_levels_option_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with empty 'Include VIP levels' option and verify its displaying
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_006_select_promotion_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels' = 'X' and verify its displaying in application
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_007_select_promotion_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels' <> 'X' and verify its displaying in application
        EXPECTED: Promotion is NOT displayed in application
        """
        pass

    def test_008_logout_from_the_application(self):
        """
        DESCRIPTION: Logout from the application
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps 5-7
        EXPECTED: 
        """
        pass
