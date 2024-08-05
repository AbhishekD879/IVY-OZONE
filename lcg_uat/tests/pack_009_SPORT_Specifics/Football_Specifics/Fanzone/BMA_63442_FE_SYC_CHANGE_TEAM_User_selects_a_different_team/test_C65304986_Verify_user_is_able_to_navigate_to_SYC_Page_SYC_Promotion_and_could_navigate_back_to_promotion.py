import random
import pytest
import tests
from time import sleep
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@pytest.mark.issue('https://jira.corp.entaingroup.com/browse/OZONE-8944')
@vtest
class Test_C65304986_Verify_user_is_able_to_navigate_to_SYC_team_selection_page_from_SYC_Promotion_and_could_navigate_back_to_promotion_or_any_other_page_from_SYC_team_selection_page_for_a_logged_in_user(Common):
    """
    TR_ID: C65304986
    NAME: Verify user is able to navigate to SYC team selection page from SYC Promotion and could navigate back to promotion or any other page from SYC team selection page for a logged in user
    DESCRIPTION: This test case is to verify user is able to navigate to SYC team selection page from SYC Promotion and could navigate back to promotion or any other page from SYC team selection page for a logged in user
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
            if 'beta' in tests.HOSTNAME:
                self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                      field_name='enabled',
                                                                      field_value=True)
            else:
                raise SiteServeException(f'Fanzone is not enabled for "{tests.HOSTNAME}"')
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_001_open_syc_promotion(self):
        """
        DESCRIPTION: Open SYC promotion
        EXPECTED: SYC promotion should be open
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        self.site.wait_content_state(state_name='FanZoneEvents')
        sleep(3)

    def test_002_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_003_click_on_back_button_on_team_selection_page(self):
        """
        DESCRIPTION: Click on back button on team selection page
        EXPECTED: user should be navigated back to SYC promotion
        """
        # if self.device_type != "mobile":
        #     back_button = self.site.show_your_colors.back_button
        #     self.assertTrue(back_button, msg="Back Button in sys page is not displayed")
        # else:
        #     back_button = self.site.header.back_button
        #     self.assertTrue(back_button, msg="Back Button in sys page is not displayed")
        # back_button.click()
        self.device.go_back()
        self.site.wait_content_state(state_name='FanZoneEvents')

    def test_004_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: user should be navigated to SYC team selection page
        """
        self.test_002_click_on_cta_button_in_promotion()

    def test_005_click_on_horseracing(self, sport='Horse Racing'):
        """
        DESCRIPTION: Click on Horse racing sport
        EXPECTED: user should navigate to Horse racing landing page
        """
        if self.device_type == 'mobile':
            navigation_menu = self.site.navigation_menu
            footer_list = set(navigation_menu.items_names) - {'Home', 'Gaming', 'Casino'}
            self.site.navigation_menu.click_item(random.choice(list(footer_list)), timeout=10)
            self.site.wait_content_state_changed(timeout=5)
        else:
            az_sports = self.site.sport_menu.sport_menu_items_group('Main')
            self.assertTrue(az_sports, msg='No sports found in "A-Z Sports" section')
            az_sports.click_item(sport)
            self.site.wait_content_state(sport)

    def test_006_go_to_promotions_and_open_syc_promotion(self):
        """
        DESCRIPTION: Go to promotions and open SYC promotion
        EXPECTED: SYC promotion should be open
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        self.test_001_open_syc_promotion()

    def test_007_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: user should be navigated to SYC team selection page
        """
        self.test_002_click_on_cta_button_in_promotion()

    def test_008_repeate_step_no_56__7_with_other_sport_pages(self):
        """
        DESCRIPTION: Repeate step no 5,6 & 7 with other sport pages
        """
        for sport in ['Football', 'Tennis']:
            self.test_005_click_on_horseracing(sport=sport)
            self.test_006_go_to_promotions_and_open_syc_promotion()
            self.test_002_click_on_cta_button_in_promotion()  # calling 2nd test method instead of 7th as both will do the same functionality
