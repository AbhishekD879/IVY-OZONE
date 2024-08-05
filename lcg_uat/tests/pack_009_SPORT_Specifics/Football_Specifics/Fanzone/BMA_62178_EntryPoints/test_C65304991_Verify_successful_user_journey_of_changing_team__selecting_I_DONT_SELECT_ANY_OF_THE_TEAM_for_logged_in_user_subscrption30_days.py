import tests
import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod # no user available for prod and Beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304991_Verify_successful_user_journey_of_changing_team__selecting_I_DONT_SELECT_ANY_OF_THE_TEAM_for_logged_in_user_subscrption30_days(Common):
    """
    TR_ID: C65304991
    NAME: Verify successful user journey of changing team - selecting I DONT SELECT ANY OF THE TEAM  for logged in user (subscrption>=30 days)
    DESCRIPTION: This test case is to verify successful user journey of changing team - selecting I DONT SELECT ANY OF THE TEAM  for logged in user who completed 30 days or more from subscription to fanzone
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User should subscribe to fanzone and should be completed 30 or more days
    PRECONDITIONS: 4) User should be  in SYC promotion page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User has access to CMS
        PRECONDITIONS: Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: User has completed the Fanzone Syc successfully in FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.norwich_city.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.norwich_city.title())

        self.site.login(username=tests.settings.fanzone_completed_users)
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
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
        self.site.wait_content_state(state_name='PromotionDetails')
        promotion_details = self.site.promotion_details.tab_content.promotion
        fanzone_syc_button = promotion_details.detail_description.fanzone_syc_button
        fanzone_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Previously subscribed team should be in highlighted box
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        team_ui_box_border = teams[vec.fanzone.TEAMS_LIST.norwich_city.title()].css_property_value('border').split()[0]
        self.assertTrue(team_ui_box_border == vec.fanzone.SYC_SELECTED_TEAM_BORDER,
                        msg=f'"{teams[vec.fanzone.TEAMS_LIST.norwich_city.title()].name}" '
                            f' Previously subscribed team selection is not in highlighted box ')

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
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
                                           verify_name=False)
        self.assertTrue(dialog.select_custom_team_name_input,
                        msg='Choice name has not Displayed to entered input')
        self.assertTrue(dialog.exit_button.is_displayed(),
                        msg='CTA Exit Button Not Displayed')
        self.assertTrue(dialog.confirm_button.is_displayed(),
                        msg='CTA Confirm Button Not Displayed')

    def test_005_enter_user_choce_team_name_and_click_on_confirm_button(self):
        """
        DESCRIPTION: Enter user choce team name and click on confirm button
        EXPECTED: User should get thank you message popup
        """
        # should not be automated as user can be used and next run tc will failed

    def test_006_click_on_exit_button_or_any_other_portion_of_page(self):
        """
        DESCRIPTION: Click on exit button or any other portion of page
        EXPECTED: Popup should disappear and user should navigate to SYC promotion page
        """
        # should not be automated as user can be used and next run tc will failed

    def test_007_check_fanzone_entry_points(self):
        """
        DESCRIPTION: Check fanzone entry points
        EXPECTED: Entry points shpuld not availabe for user
        """
        # should not be automated as user can be used and next run tc will failed
