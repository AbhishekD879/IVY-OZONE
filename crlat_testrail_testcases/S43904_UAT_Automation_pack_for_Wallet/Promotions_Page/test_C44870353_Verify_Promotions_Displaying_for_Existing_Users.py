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
class Test_C44870353_Verify_Promotions_Displaying_for_Existing_Users(Common):
    """
    TR_ID: C44870353
    NAME: "Verify Promotions Displaying for Existing Users
    DESCRIPTION: This test case verifies promotions displaying for existing users
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_new_promotion_in_cms_select_show_for_existing_users_option_and_save_changes(self):
        """
        DESCRIPTION: Add new Promotion in CMS, select **'Show for existing users**' option and save changes
        EXPECTED: Promotion is added successfully
        """
        pass

    def test_002_clear_browsers_cookies_and_load_app(self):
        """
        DESCRIPTION: Clear browser`s cookies and load app
        EXPECTED: 
        """
        pass

    def test_003_verify_added_promotion_displaying(self):
        """
        DESCRIPTION: Verify added Promotion displaying
        EXPECTED: Promotion with selected 'Show for existing users' option is NOT displayed in application
        """
        pass

    def test_004_login_into_the_app_and_verify_presence_of_just_added_promotion(self):
        """
        DESCRIPTION: Login into the app and verify presence of just added Promotion
        EXPECTED: Added on step #1 Promotion is present on front end
        """
        pass
