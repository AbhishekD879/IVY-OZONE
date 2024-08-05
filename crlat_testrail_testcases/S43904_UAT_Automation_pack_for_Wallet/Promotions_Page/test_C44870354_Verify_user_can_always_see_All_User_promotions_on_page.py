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
class Test_C44870354_Verify_user_can_always_see_All_User_promotions_on_page(Common):
    """
    TR_ID: C44870354
    NAME: Verify user can always see All User promotions on page
    DESCRIPTION: This test case verifies promotions displaying for new and existing users when 'Both' option is selected
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_new_promotion_in_cms_select_both_option_and_save_changes(self):
        """
        DESCRIPTION: Add new Promotion in CMS, select **'Both**' option and save changes
        EXPECTED: Promotion is added successfully
        """
        pass

    def test_002_clear_browsers_cookies_and_load_invictus_app(self):
        """
        DESCRIPTION: Clear browser`s cookies and load Invictus app
        EXPECTED: 'ExistingUser' ​cookie is empty or not present
        """
        pass

    def test_003_verify_presence_of_just_added_promotion(self):
        """
        DESCRIPTION: Verify presence of just added Promotion
        EXPECTED: Added on step #1 Promotion is present on front end
        """
        pass

    def test_004_log_in_into_app(self):
        """
        DESCRIPTION: Log in into app
        EXPECTED: 
        """
        pass

    def test_005_verify_cookies_creation_in_resources__cookies(self):
        """
        DESCRIPTION: Verify cookies creation in Resources ->Cookies
        EXPECTED: 'ExistingUser = True' cookie is added
        """
        pass

    def test_006_verify_presence_of_added_on_step_1_promotion(self):
        """
        DESCRIPTION: Verify presence of added on step #1 promotion
        EXPECTED: Added on step #1 Promotion is present on front end
        """
        pass

    def test_007_logout_from_application_and_verify_promotion_displaying(self):
        """
        DESCRIPTION: Logout from application and verify Promotion displaying
        EXPECTED: Promotion is displayed in application
        """
        pass
