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
class Test_C29320_Include_VIP_levels_option_for_Promotions(Common):
    """
    TR_ID: C29320
    NAME: 'Include VIP levels' option for Promotions
    DESCRIPTION: This test case verifies Promotions displaying in application depending on 'Include VIP' levels option value.
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-8132 VIP Segmentation for Promotions within CMS
    PRECONDITIONS: Users with different VIP levels:
    PRECONDITIONS: felina2 - viplevel = 5, passward: ytrewq
    PRECONDITIONS: felina3 - viplevel = 8, passward: qwerty
    PRECONDITIONS: felina4 - viplevel = 6, passward: qwerty
    PRECONDITIONS: peterparker - viplevel = 7. passward: ytrewq
    PRECONDITIONS: 'viplevel = 1' - assigned to the user by default
    """
    keep_browser_open = True

    def test_001_add_new_promotion_with_empty_include_vip_levels_option_field_and_save_it(self):
        """
        DESCRIPTION: Add new promotion with empty 'Include VIP levels' option field and save it.
        EXPECTED: *   Promotion is succesffully saved
        EXPECTED: *   'Include VIP levels' option is NOT mandatory
        """
        pass

    def test_002_load_invictus_application_and_verify_promotion_displaying_when_user_is_not_logged_in(self):
        """
        DESCRIPTION: Load Invictus application and verify promotion displaying when user is not logged in
        EXPECTED: Promotion is displayed in application
        """
        pass

    def test_003_verify_promotion_displaying_for_logged_in_users_with_different_vip_levels(self):
        """
        DESCRIPTION: Verify promotion displaying for logged in users with different VIP levels
        EXPECTED: Promotion is displayed for all users regardless off their VIP level
        """
        pass

    def test_004_in_cms_change_include_vip_levels_option_value_to_1_for_selected_promotionsave_changes(self):
        """
        DESCRIPTION: In CMS change 'Include VIP levels' option value to '1' for selected promotion.
        DESCRIPTION: Save changes.
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_005_load_invictus_application_and_login_with_user_for_which_vip_level__1verify_promotion_displaying_for_the_user(self):
        """
        DESCRIPTION: Load invictus application and login with user for which 'VIP level = 1'.
        DESCRIPTION: Verify Promotion displaying for the user.
        EXPECTED: Promotion is displayed for the user.
        """
        pass

    def test_006_logout_from_the_applicationverify_promotion_displaying_after_logout(self):
        """
        DESCRIPTION: Logout from the application.
        DESCRIPTION: Verify promotion displaying after logout.
        EXPECTED: Promotion is displayed (VIP level of previously logged in user is saved).
        """
        pass

    def test_007_login_with_user_for_which_vip_level_1verify_promotion_displaying_for_the_user(self):
        """
        DESCRIPTION: Login with user for which 'VIP level <>1'.
        DESCRIPTION: Verify Promotion displaying for the user.
        EXPECTED: Promotion is NOT displayed for the user.
        """
        pass

    def test_008_logout_from_the_applicationverify_promotion_displaying_after_logout(self):
        """
        DESCRIPTION: Logout from the application.
        DESCRIPTION: Verify Promotion displaying after logout.
        EXPECTED: Promotion is NOT displayed (VIP level of previously logged in user is saved)
        """
        pass

    def test_009_in_cms_set_include_vip_levels_option_value__1_3save_changes(self):
        """
        DESCRIPTION: In CMS set 'Include VIP levels' option value = '1-3'.
        DESCRIPTION: Save changes.
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_010_login_to_application_with_user_for_which_vip_level__1verify_promotion_displaying_for_the_user(self):
        """
        DESCRIPTION: Login to application with user for which 'VIP level = 1'.
        DESCRIPTION: Verify Promotion displaying for the user.
        EXPECTED: Promotion is displayed for the user
        """
        pass

    def test_011_logout_from_the_applicationrepeat_step_10_with_user_for_which_vip_level__2(self):
        """
        DESCRIPTION: Logout from the application.
        DESCRIPTION: Repeat step 10 with user for which 'VIP level = 2'.
        EXPECTED: Promotion is displayed for the user
        """
        pass

    def test_012_logout_from_the_applicationrepeat_step_10_with_user_for_which_vip_level__3(self):
        """
        DESCRIPTION: Logout from the application.
        DESCRIPTION: Repeat step 10 with user for which 'VIP level = 3'.
        EXPECTED: Promotion is displayed for the user.
        """
        pass

    def test_013_logout_from_the_applicationrepeat_step_10_with_user_for_which_vip_level_1_2_3(self):
        """
        DESCRIPTION: Logout from the application.
        DESCRIPTION: Repeat step 10 with user for which 'VIP level <>1, 2, 3'.
        EXPECTED: Promotion is NOT displayed for the user
        """
        pass
