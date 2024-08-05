import pytest

from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Promotions.BasePromotionTest import BasePromotionTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.cms
@pytest.mark.promotions
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@pytest.mark.login
@vtest
class Test_C29321_Promotions_Displaying_for_New_Users(BasePromotionTest):
    """
    TR_ID: C29321
    NAME: Promotions Displaying for New Users
    DESCRIPTION: This test case verifies display of promotions for new users
    """
    keep_browser_open = True

    def test_001_add_new_promotion_in_cms(self):
        """
        DESCRIPTION: Add new Promotion in CMS, select **'Show for new users**' option and save changes
        EXPECTED: Promotion is added successfully
        """
        promotion = self.cms_config.add_promotion(show_to_user='new')
        self.__class__.promotion_title, self.__class__.promo_id = \
            promotion.title.upper(), promotion.id

    def test_002_load_invictus_app(self):
        """
        DESCRIPTION: Clear browser`s cookies and load Invictus app
        EXPECTED: 'ExistingUser' ​cookie is empty or not present
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
        """
        self.site.login(timeout_close_dialogs=30)

    def test_005_verify_cookies_creation(self):
        """
        DESCRIPTION: Verify cookies creation in Resources ->Cookies
        EXPECTED: 'ExistingUser = True' cookie is added
        """
        cookie_value = self.get_local_storage_cookie_value('OX.existingUser')
        self.assertTrue(cookie_value, msg=f'"ExistingUser" cookie: "{cookie_value}", expected is: "True"')

    def test_006_verify_presence_of_added_promotion(self):
        """
        DESCRIPTION: Verify presence of added on step #1 Promotion
        EXPECTED: Added on step #1 Promotion is NOT present on front end
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertNotIn(self.promotion_title, list(promotions.keys()),
                         msg=f'Promotion: "{self.promotion_title}" found in promotions list: '
                         f'{list(promotions.keys())}')

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        """
        self.site.logout()

    def test_008_verify_presence_of_added_promotion(self):
        """
        DESCRIPTION: Verify presence of added on step #1 Promotion
        EXPECTED: Added on step #1 Promotion is NOT present on front end
        EXPECTED: 'ExistingUser = True' cookie is still present
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertNotIn(self.promotion_title, list(promotions.keys()),
                         msg=f'Promotion: "{self.promotion_title}" found in promotions list: '
                             f'{list(promotions.keys())}')
        cookie_value = self.get_local_storage_cookie_value('OX.existingUser')
        self.assertTrue(cookie_value, msg=f'"ExistingUser" cookie: "{cookie_value}", expected is: "True"')
