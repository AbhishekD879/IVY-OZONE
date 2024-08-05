from time import sleep
import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # in production we can not config promotions
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.promotions_banners_offers
@vtest
class Test_C44870353_Verify_Promotions_Displaying_for_Existing_Users(Common):
    """
    TR_ID: C44870353
    NAME: "Verify Promotions Displaying for Existing Users
    DESCRIPTION: This test case verifies promotions displaying for existing users
   """
    keep_browser_open = True

    def test_001_add_new_promotion_in_cms_select_show_for_existing_users_option_and_save_changes(self):
        """
        DESCRIPTION: Add new Promotion in CMS, select **'Show for existing users**' option and save changes
        EXPECTED: Promotion is added successfully
        """
        promotion = self.cms_config.add_promotion(show_to_user='existing')
        self.__class__.promotion_title, self.__class__.promo_id = promotion.title.upper(), promotion.id

    def test_002_clear_browsers_cookies_and_load_app(self):
        """
        DESCRIPTION: Clear browser`s cookies and load app
        """
        self.delete_cookies()
        self.device.navigate_to('Homepage')
        self.site.wait_content_state('HomePage')

    def test_003_verify_added_promotion_displaying(self):
        """
        DESCRIPTION: Verify added Promotion displaying
        EXPECTED: Promotion with selected 'Show for existing users' option is NOT displayed in application
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertNotIn(self.promotion_title, list(promotions.keys()),
                         msg=f'Promotion: "{self.promotion_title}" found in promotions list: '
                             f'{list(promotions.keys())}')

    def test_004_login_into_the_app_and_verify_presence_of_just_added_promotion(self):
        """
        DESCRIPTION: Login into the app and verify presence of just added Promotion
        EXPECTED: Added on step #1 Promotion is present on front end
        """
        self.site.login(timeout_close_dialogs=30)
        wait_for_result(lambda: self.site.wait_content_state(state_name='Promotions'), timeout=10)
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        # the newly created  promotion is taking time to reflect in the front end
        sleep(50)
        self.assertIn(self.promotion_title, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title}" not found in promotions list: '
                          f'{list(promotions.keys())}')
