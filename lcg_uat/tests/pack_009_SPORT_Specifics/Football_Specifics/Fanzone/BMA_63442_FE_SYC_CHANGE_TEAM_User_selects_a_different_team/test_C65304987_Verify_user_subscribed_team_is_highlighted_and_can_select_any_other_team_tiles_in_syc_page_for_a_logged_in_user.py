import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304987_Verify_user_subscribed_team_is_highlighted_and_can_select_any_other_team_tiles_in_syc_page_for_a_logged_in_user(Common):
    """
    TR_ID: C65304987
    NAME: Verify user subscribed team is highlighted and can select any other team tiles in fanzone team selection page for a logged in user
    DESCRIPTION: This test case is to verify user subscribed team is highlighted and can select any other team tiles in fanzone team selection page for a logged in user
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User should be  in promotion page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
        """
        fanzone_status = self.get_initial_data_system_configuration().get(vec.sb.FANZONE)
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        manchester_city_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title())
        if manchester_city_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='SYC is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.manchester_city.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.manchester_city.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_open_syc_promotion(self):
        """
        DESCRIPTION: Open SYC promotion
        EXPECTED: SYC promotion should be open
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')

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

    def test_003_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Previously subscribed team should be in highlighted box
        """
        team = self.site.show_your_colors.items_as_ordered_dict.get(vec.fanzone.TEAMS_LIST.manchester_city.title())
        team_ui_box_border = team.css_property_value('border').split(" ")[0]
        self.assertEqual(team_ui_box_border, vec.fanzone.SYC_SELECTED_TEAM_BORDER,
                         msg=f'Team UI box border is not equal to Zepplin team box border'
                             f'actual result "{team_ui_box_border}"')

    def test_004_click_on_other_team_tiles_and_i_dont_select_any_of_the_team(self):
        """
        DESCRIPTION: Click on other team tiles and I DON'T SELECT ANY OF THE TEAM
        EXPECTED: The selected team tile should be highlighted
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        for team in teams.items():
            if team[0] != "":
                team[1].scroll_to_we()
                team[1].click()
                dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM)
                dialog_alert.exit_button.click()
                sleep(1)
                team_ui_box_border = team[1].css_property_value('border').split(" ")[0]
                self.assertEqual(team_ui_box_border, vec.fanzone.SYC_SELECTED_TEAM_BORDER,
                                 msg=f'Team UI box border is not equal to Zepplin team box border'
                                     f'actual result "{team_ui_box_border}"')
