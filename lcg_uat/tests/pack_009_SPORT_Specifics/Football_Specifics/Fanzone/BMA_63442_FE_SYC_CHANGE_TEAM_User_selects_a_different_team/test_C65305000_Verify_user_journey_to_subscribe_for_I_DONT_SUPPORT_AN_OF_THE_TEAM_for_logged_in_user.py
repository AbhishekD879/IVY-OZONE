import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.utils.exceptions import SiteServeException
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305000_Verify_user_journey_to_subscribe_for_I_DONT_SUPPORT_AN_OF_THE_TEAM_from_SYC_promotion_for_logged_in_user(Common):
    """
    TR_ID: C65305000
    NAME: Verify user journey to subscribe for I DON'T SUPPORT AN OF THE TEAM  from SYC promotion  for logged in user
    DESCRIPTION: This test case is to verify user journey to subscribe for I DON'T SUPPORT AN OF THE TEAM  from SYC promotion  for logged in user
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User not  subscribed to fanzone
    PRECONDITIONS: 4) User should be  in SYC promotion page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be logged into ladbroks
        PRECONDITIONS: 3) User not  subscribed to fanzone
        PRECONDITIONS: 4) User should be  in SYC promotion page
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

    def test_001_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')
        sleep(3)

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Team selection page should be diaplyed with all available team tiles
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_003_select_i_dont_select_any_of_the_team(self):
        """
        DESCRIPTION: Select I DONT SELECT ANY OF THE TEAM
        EXPECTED: The selected team tile should be highlighted and gets free text popup
        """
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')
        self.site.show_your_colors.scroll_to_we(self.site.show_your_colors.i_dont_support_any_teams)
        self.site.show_your_colors.i_dont_support_any_teams.click()

    def test_004_verify_free_text_popup_ui(self):
        """
        DESCRIPTION: Verify free text popup UI
        EXPECTED: Free text column and 2 CTA buttons
        """
        self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
                                                          verify_name=False)
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not Displayed to entered input')
        self.assertTrue(self.dialog.exit_button.is_displayed(),
                        msg='CTA Exit Button Not Displayed')
        self.assertTrue(self.dialog.confirm_button.is_displayed(),
                        msg='CTA Confirm Button Not Displayed')

    def test_005_enter_user_choce_team_name_and_click_on_confirm_button(self):
        """
        DESCRIPTION: Enter user choce team name and click on confirm button
        EXPECTED: User should get thank you message popup
        """
        self.dialog.select_custom_team_name_input = 'ABC'
        sleep(3)
        self.dialog.confirm_button.click()
        self.__class__.msg_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_THANK_YOU,
                                                              verify_name=False)
        self.assertTrue(self.msg_dialog, msg="Thank you message pop up is not displayed")
        sleep(5)

    def test_006_click_on_exit_button_or_any_other_portion_of_page(self):
        """
        DESCRIPTION: Click on exit button or any other portion of page
        EXPECTED: Popup should disappear and user should navigate to Football or SYC promotion page respectively
        """
        self.msg_dialog.exit_button.click()
        self.site.wait_content_state(state_name="football")

    def test_007_check_fanzone_entry_points(self):
        """
        DESCRIPTION: Check fanzone entry points
        EXPECTED: Entry points shpuld not availabe for user
        """
        self.site.wait_content_state(state_name='Football')
        try:
            self.dialog = None
            self.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                                    timeout=5)
        except VoltronException:
            pass
        self.assertFalse(self.dialog, msg='SYC overlay is still displayed')
        self.navigate_to_page("Homepage")
        if self.device_type == 'mobile':
            self.assertNotIn(vec.sb.FANZONE, self.site.home.menu_carousel.items_names,
                             msg="Fanzone Entry Point is displayed")
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='No items on MenuCarousel found')
            all_items.get(vec.SB.ALL_SPORTS).click()
            self.site.wait_content_state(state_name='AllSports')
            top_sports = self.site.all_sports.top_sports_section.items_names
            self.assertTrue(top_sports, msg='No sports found in "Top Sports" section')
            self.assertNotIn(vec.sb.FANZONE, top_sports,
                             msg="Fanzone Entry Point is displayed")
        else:
            self.assertNotIn(vec.sb.FANZONE.upper(), self.site.header.sport_menu.items_names,
                             msg="Fanzone Entry Point is displayed")
            self.assertNotIn(vec.sb.FANZONE, self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict,
                             msg="Fanzone Entry Point is displayed")
        self.assertFalse(self.site.home.fanzone_banner(timeout=3), msg="Fanzone Banner is displayed on HomePage")
