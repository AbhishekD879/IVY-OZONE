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
class Test_C29310_Promotions_displaying_for_users_with_different_VIP_levels_when_Show_to_Both_users_value_is_set(Common):
    """
    TR_ID: C29310
    NAME: Promotions displaying for users with different VIP levels when 'Show to Both users' value is set
    DESCRIPTION: This test case verifies Promotions displaying for users with different VIP levels when 'Show to Both users' option value is set
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-8896
    PRECONDITIONS: 1. 'Show to Both Users' option value is set for Promotionrs
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
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_003_select_promotion_with_include_vip_levels__x_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels'  = 'X' and verify its displaying
        EXPECTED: Promotion with filled in 'Include VIP levels' field is displayed for New user
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
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_006_select_promotionwith_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels' = 'X' and verify its displaying in application
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_007_select_promotion_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels' <> 'X' and verify its displaying in application
        EXPECTED: Promotion is NOT displayed in application
        """
        pass

    def test_008_logout_from_application_and_repeat_steps_5_7(self):
        """
        DESCRIPTION: Logout from application and repeat steps 5-7
        EXPECTED: 
        """
        pass

    def test_009_login_to_application_with_user_for_which_viplevel__x(self):
        """
        DESCRIPTION: Login to application with user for which 'viplevel' <> 'X'
        EXPECTED: 
        """
        pass

    def test_010_select_promotion_with_empty_include_vip_levels_option_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with empty 'Include VIP levels' option and verify its displaying
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_011_select_promotion_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels' = 'X' and verify its displaying in application
        EXPECTED: Promotion is NOT displayed in application
        """
        pass

    def test_012_logout_from_the_application(self):
        """
        DESCRIPTION: Logout from the application
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_10_11(self):
        """
        DESCRIPTION: Repeat steps 10-11
        EXPECTED: 
        """
        pass
