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
class Test_C29322_Promotions_Displaying_for_Existing_Users(BasePromotionTest):
    """
    TR_ID: C29322
    NAME: Promotions Displaying for Existing Users
    DESCRIPTION: This test case verifies promotions displaying for existing users
    """
    keep_browser_open = True

    def test_001_add_new_promotion_in_cms(self):
        """
        DESCRIPTION: Add new Promotion in CMS, select **'Show for existing users**' option and save changes
        EXPECTED: Promotion is added successfully
        """
        promotion = self.cms_config.add_promotion(show_to_user='existing')
        self.__class__.promotion_title, self.__class__.promo_id = \
            promotion.title.upper(), promotion.id

    def test_002_load_invictus_app(self):
        """
        DESCRIPTION: Clear browser`s cookies and load app
        """
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
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No Promotions found in the page')
        self.assertIn(self.promotion_title, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title}" not found in promotions list: '
                          f'{list(promotions.keys())}')
