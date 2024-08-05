import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304985_Verify_SYC_promotion_content_and_CTA_button_as_per_cms_configuration(Common):
    """
    TR_ID: C65304985
    NAME: Verify SYC promotion content and CTA button as per cms configuration
    DESCRIPTION: This test case is to verify SYC promotion content and CTA button as per cms configuration
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be in promotion page in ladbrokes
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be in promotion page in ladbrokes
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        promotions = self.cms_config.get_promotions()
        syc_promo = list(filter(lambda param: param['title'] == vec.fanzone.PROMOTION_TITLE.title(), promotions))
        self.assertTrue(syc_promo, msg='"SYC Promotions"is not configured in cms')
        self.__class__.syc_description = list(filter(lambda param: param['title'] == vec.fanzone.PROMOTION_TITLE.title(), promotions))[0]['description']
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')

    def test_001_go_to_syc_promotion_and_click_on_see_more_button(self):
        """
        DESCRIPTION: Go to SYC promotion and click on see more button
        EXPECTED: SYC promotion should be open
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_002_check_promotion_page(self):
        """
        DESCRIPTION: Check promotion page
        EXPECTED: Content and CTA button should be as configured in cms
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')

    def test_003_click_on_cta_buttonclick_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA buttonClick on CTA button in promotion
        EXPECTED: Button should be clickable
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fanzone_syc_button = promotion_details.detail_description.fanzone_syc_button
        self.assertIn(vec.fanzone.FANZONE_SYC, self.syc_description,
                      msg=f'{vec.fanzone.FANZONE_SYC} CTA Button is Expected: ", '
                          f'but actual CTA button is not same in: "{self.syc_description}"')
        fanzone_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
