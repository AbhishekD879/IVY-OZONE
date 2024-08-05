import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # due to creation of promotions in cms this test script is commented for prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29323_Promotions_Displaying_for_New_and_Existing_Users(Common):
    """
    TR_ID: C29323
    NAME: Promotions Displaying for New and Existing Users
    DESCRIPTION: This test case verifies promotions displaying for new and existing users when 'Both' option is selected
    DESCRIPTION: **JIRA Ticket:**
    DESCRIPTION: *   BMA-8896 Promotions - Add New/Existing functionality
    PRECONDITIONS:
    """
    keep_browser_open = True

    def test_001_add_new_promotion_in_cms_selectboth_option_and_save_changes(self):
        """
        DESCRIPTION: Add new Promotion in CMS, select **'Both**' option and save changes
        EXPECTED: Promotion is added successfully
        """
        promotion = self.cms_config.add_promotion(show_to_user='both')
        self.__class__.promotion_title = promotion.title.upper()

    def test_002_clear_browsers_cookies_and_load_invictus_app(self):
        """
        DESCRIPTION: Clear browser`s cookies and load Invictus app
        EXPECTED: **'ExistingUser' **​cookie is empty or not present
        """
        self.site.wait_content_state('HomePage')
        cookie_value = self.get_local_storage_cookie_value('OX.existingUser')
        self.assertFalse(cookie_value,
                         msg=f'"ExistingUser" cookie: "{cookie_value}", expected empty or not present')

    def test_003_verify_presence_of_just_added_promotion(self):
        """
        DESCRIPTION: Verify presence of just added Promotion
        EXPECTED: Added on step #1 Promotion is present on front end
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No Promotions found in the page')
        self.assertIn(self.promotion_title, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title}" not found in promotions list: '
                          f'{list(promotions.keys())}')

    def test_004_log_in_into_app(self):
        """
        DESCRIPTION: Log in into app
        EXPECTED:
        """
        self.site.login(timeout_close_dialogs=30)

    def test_005_verify_cookies_creation_in_resources__cookies(self):
        """
        DESCRIPTION: Verify cookies creation in Resources ->Cookies
        EXPECTED: **'ExistingUser = True'** cookie is added
        """
        cookie_value = self.get_local_storage_cookie_value('OX.existingUser')
        self.assertTrue(cookie_value, msg=f'"ExistingUser" cookie: "{cookie_value}", expected is: "True"')

    def test_006_verify_presence_of_added_on_step_1_promotion(self):
        """
        DESCRIPTION: Verify presence of added on step #1 Promotion
        EXPECTED: Added on step #1 Promotion is present on front end
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertIn(self.promotion_title, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title}" found in promotions list: '
                          f'{list(promotions.keys())}')

    def test_007_logout_from_application_and_verify_promotion_displaying(self):
        """
        DESCRIPTION: Logout from application and verify Promotion displaying
        EXPECTED: Promotion is displayed in application
        """
        self.site.logout()
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertIn(self.promotion_title, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title}" found in promotions list: '
                          f'{list(promotions.keys())}')
        cookie_value = self.get_local_storage_cookie_value('OX.existingUser')
        self.assertTrue(cookie_value, msg=f'"ExistingUser" cookie: "{cookie_value}", expected is: "True"')
