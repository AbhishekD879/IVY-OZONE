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
class Test_C44870352_Verify_that_for_new_user_Segmented_Banners__New_Customer_Promo_is_displayed_clear_Cache_and_cookies(Common):
    """
    TR_ID: C44870352
    NAME: Verify that for new user Segmented Banners - New Customer Promo is displayed (clear Cache and cookies)
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_new_promotion_in_cms_select_show_for_new_users_option_and_save_changes(self):
        """
        DESCRIPTION: Add new Promotion in CMS, select **'Show for new users**' option and save changes
        EXPECTED: Promotion is added successfully
        """
        pass

    def test_002_clear_browsers_cookies_and_launch_the_app(self):
        """
        DESCRIPTION: Clear browser`s cookies and launch the app
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
        DESCRIPTION: Verify presence of added on step #1 Promotion
        EXPECTED: Added on step #1 Promotion is NOT present on front end
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_008_verify_presence_of_added_on_step_1_promotion(self):
        """
        DESCRIPTION: Verify presence of added on step #1 Promotion
        EXPECTED: Added on step #1 Promotion is NOT present on front end
        EXPECTED: 'ExistingUser = True' cookie is still present
        """
        pass
