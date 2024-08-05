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
class Test_C44870355_Verify_that_VIP_users_Platinium_Gold_Bronze_Silver_can_see_their_status_and_get_promotions_configured_in_CMS_for_the_respective_level(Common):
    """
    TR_ID: C44870355
    NAME: Verify that VIP users (Platinium, Gold, Bronze, Silver) can see their status and get promotions configured in CMS for the respective level.
    DESCRIPTION: This test case verifies Promotions displaying for users with different VIP levels when 'Show to Existing users' option value is set
    PRECONDITIONS: IMS levels required
    PRECONDITIONS: Platinum (IMS=77)
    PRECONDITIONS: Gold (IMS=76)
    PRECONDITIONS: Silver (IMS=64)
    PRECONDITIONS: Bronze (IMS=63)
    """
    keep_browser_open = True

    def test_001_clear_all_cookies_and_load_invictus_application(self):
        """
        DESCRIPTION: Clear all cookies and load Invictus application
        EXPECTED: 'viplevel' cookie is NOT present in browser
        EXPECTED: 'Existing user:True' cookie is NOT present to browser
        """
        pass

    def test_002_select_promotion_with_empty_include_vip_levels_option_value_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with empty 'Include VIP Levels' option value and verify its displaying
        EXPECTED: Promotion is NOT displayed in application
        """
        pass

    def test_003_select_promotion_with_include_vip_levels___77for_platinum_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels'  = '77'(For Platinum) and verify its displaying
        EXPECTED: Promotion is NOT displayed in application
        """
        pass

    def test_004_login_to_application_with_platinum_user(self):
        """
        DESCRIPTION: Login to application with platinum user
        EXPECTED: Platinum user should be logged in.
        """
        pass

    def test_005_select_promotion_with_empty_include_vip_levels_option_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with empty 'Include VIP levels' option and verify its displaying
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_006_select_promotion_with_include_vip_levels__77_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels' = '77' and verify its displaying in application
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_007_logout_from_the_application(self):
        """
        DESCRIPTION: Logout from the application
        EXPECTED: user should be logged out
        """
        pass

    def test_008_repeat_steps_1_7_for_vip_level__76_for_gold_users(self):
        """
        DESCRIPTION: Repeat steps 1-7 for vip level = '76' for Gold users
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_1_7_for_vip_level__64_for_silver_users(self):
        """
        DESCRIPTION: Repeat steps 1-7 for vip level = '64' for silver users
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_1_7_for_vip_level__63_for_bronze_users(self):
        """
        DESCRIPTION: Repeat steps 1-7 for vip level = '63' for bronze users
        EXPECTED: 
        """
        pass
