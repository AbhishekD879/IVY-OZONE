import pytest
import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Promotions.BasePromotionTest import BasePromotionTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.cms
@pytest.mark.promotions
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29309_promotions_displaying_with_different_VIP_levels_when_Show_to_New_users_option_value_is_set(BasePromotionTest):
    """
    TR_ID: C29309
    NAME: promotions displaying with different VIP levels when 'Show to New users' option value is set
    DESCRIPTION: This test case verifies Promotions displaying for users with different VIP levels when 'Show to New users' option value is set
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-8896
    PRECONDITIONS: 1. 'Show to New Users' option value is set for Promotions
    PRECONDITIONS: 2. All other conditions for Promotions displaying are met
    """
    keep_browser_open = True

    def test_001_clear_all_cookies_and_load_invictus_application(self):
        """
        DESCRIPTION: Clear all cookies and load Invictus application
        EXPECTED: *   'viplevel' cookie is NOT present in browser
        EXPECTED: *   'Existing user:True' cookie is NOT present to browser
        """
        vipLevelsInput = '12' if self.brand == 'bma' else '62'
        promotion = self.cms_config.add_promotion(show_to_user='both')
        self.__class__.promotion_title_empty_vip_levels, self.__class__.promotion_title_empty_vip_levels_id = \
            promotion.title.upper(), promotion.id
        self.__class__.promotion_title_13_vip_levels = self.cms_config.add_promotion(show_to_user='existing',
                                                                                     vipLevelsInput='13').title.upper()
        self.__class__.promotion_title_14_vip_levels = self.cms_config.add_promotion(show_to_user='existing',
                                                                                     vipLevelsInput=vipLevelsInput).title.upper()
        self.site.wait_content_state('HomePage')

    def test_002_select_promotionwith_empty_include_vip_levels_option_value_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with empty 'Include VIP Levels' option value and verify its displaying
        EXPECTED: Promotion is displayed in application
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = None
        iteration = 1
        while iteration <= 10:
            promotions = self.site.promotions.tab_content.items_as_ordered_dict
            result = self.promotion_title_empty_vip_levels in list(promotions.keys())
            if result:
                break
            else:
                sleep(30)
                iteration += 1
                self.device.refresh_page()
        self.assertIn(self.promotion_title_empty_vip_levels, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title_empty_vip_levels}" NOT found in promotions list: '
                          f'{list(promotions.keys())}')

    def test_003_select_promotion_with_include_vip_levels__x_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels'  = 'X' and verify Offer displaying
        EXPECTED: Promotion is NOT displayed in application
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertNotIn(self.promotion_title_14_vip_levels, list(promotions.keys()),
                         msg=f'Promotion: "{self.promotion_title_14_vip_levels}" found in promotions list: '
                             f'{list(promotions.keys())}')

    def test_004_login_to_application_with_user_for_which_viplevel__x(self):
        """
        DESCRIPTION: Login to application with user for which 'viplevel' = 'X'
        EXPECTED:
        """
        username = tests.settings.platinum_user_vip_level_14 if self.brand == 'bma' else tests.settings.gold_user_vip_level_62
        self.site.login(username=username)

    def test_005_select_promotion_with_empty_include_vip_levels_option_and_verify_its_displaying(self):
        """
        DESCRIPTION: Select Promotion with empty 'Include VIP levels' option and verify its displaying
        EXPECTED: Promotion is NOT displayed in application
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertIn(self.promotion_title_empty_vip_levels, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title_empty_vip_levels}" NOT found in promotions list: '
                          f'{list(promotions.keys())}')

    def test_006_select_promotion_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels' = 'X' and verify its displaying in application
        EXPECTED: Promotion is NOT displayed in application
        """
        self.cms_config.update_promotion(promotion_id=self.promotion_title_empty_vip_levels_id, disabled=True)
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

        promotions = None
        iteration = 1
        while iteration <= 9:
            promotions = self.site.promotions.tab_content.items_as_ordered_dict
            result = self.promotion_title_14_vip_levels in list(promotions.keys())
            if result:
                break
            else:
                sleep(60)
                iteration += 1
                self.device.refresh_page()
        self.assertIn(self.promotion_title_14_vip_levels, list(promotions.keys()),
                      msg=f'Promotion: "{self.promotion_title_13_vip_levels}" NOT found in promotions list: '
                          f'{list(promotions.keys())}')

    def test_007_select_promotion_with_include_vip_levels__x_and_verify_its_displaying_in_application(self):
        """
        DESCRIPTION: Select Promotion with 'Include VIP levels' <> 'X' and verify its displaying in application
        EXPECTED: Promotion is NOT displayed in application
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertNotIn(self.promotion_title_13_vip_levels, list(promotions.keys()),
                         msg=f'Promotion: "{self.promotion_title_13_vip_levels}" found in promotions list: '
                             f'{list(promotions.keys())}')

    def test_008_logout_from_the_application(self):
        """
        DESCRIPTION: Logout from the application
        EXPECTED:
        """
        self.site.logout()

    def test_009_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps 5-7
        EXPECTED:
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertNotIn(self.promotion_title_14_vip_levels, list(promotions.keys()),
                         msg=f'Promotion: "{self.promotion_title_14_vip_levels}" found in promotions list: '
                             f'{list(promotions.keys())}')

        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertNotIn(self.promotion_title_13_vip_levels, list(promotions.keys()),
                         msg=f'Promotion: "{self.promotion_title_13_vip_levels}" found in promotions list: '
                             f'{list(promotions.keys())}')
