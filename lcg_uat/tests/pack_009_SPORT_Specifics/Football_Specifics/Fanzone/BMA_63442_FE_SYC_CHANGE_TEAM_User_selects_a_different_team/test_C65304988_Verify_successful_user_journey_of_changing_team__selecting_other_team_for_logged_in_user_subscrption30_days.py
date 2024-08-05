import tests
import pytest
from time import sleep
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65304988_Verify_successful_user_journey_of_changing_team__selecting_other_team_for_logged_in_user_subscrption30_days(Common):
    """
    TR_ID: C65304988
    NAME: Verify successful user journey of changing team - selecting other team for logged in user ( subscrption>=30 days)
    DESCRIPTION: This test case is to verify user subscribed team is highlighted and can select any other team tiles in fanzone team selection page for a logged in user who completed 30 days or more from subscription to fanzone
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
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        self.site.login(tests.settings.fanzone_completed_users)
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
        team_ui_box_border = teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].css_property_value('border').split()[0]
        self.assertTrue(team_ui_box_border == vec.fanzone.SYC_SELECTED_TEAM_BORDER,
                        msg=f'"{teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].name}" '
                            f' Previously subscribed team selection is not in highlighted box ')

    def test_003_select_any_other_team_tile(self):
        """
        DESCRIPTION: Select any other team tile
        EXPECTED: The selected team tile should be highlighted and gets confiramtion popup
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        self.assertTrue(teams, msg='teams are not displayed')
        aston_villa = teams.get(vec.fanzone.TEAMS_LIST.aston_villa.title())
        aston_villa.click()
        confirm_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        self.assertTrue(confirm_dialog, msg='Confirmation pop-up is not appeared')

    def test_004_click_on_confirm_button(self):
        """
        DESCRIPTION: Click on confirm Button
        EXPECTED: Desktop:
        EXPECTED: User selection will store in BE and User navigate to SYC promotion page
        EXPECTED: Mobile:
        EXPECTED: User selection will store in BE and User navigate to preference centre screen
        """
        # should not be automated as user can be used and next run tc will failed
