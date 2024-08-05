import voltron.environments.constants as vec
import pytest
from time import sleep
from tests.base_test import vtest
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
class Test_C65305218_To_verify_SYC_team_selection_page_UI(Common):
    """
    TR_ID: C65305218
    NAME: To verify SYC -team selection page UI
    DESCRIPTION: This test case is to verify team selection page UI
    PRECONDITIONS: 1) User is in logged in state
    PRECONDITIONS: 2) User has Not subscribed for Fanzone Previously
    PRECONDITIONS: 3) In CMS-Fanzone SYC- data should be created, which will trigger SYC popup in front end
    PRECONDITIONS: 4) User is in SYC- team selection page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        fanzone_teams = self.cms_config.get_fanzones()
        for fanzone_team in fanzone_teams:
            self.cms_config.update_fanzone(fanzone_team['name'])
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='SYC is displayed',
                        timeout=5)

    def test_001_check_ui_of_team_selection_page_as_per_zeplin_image_provided(self):
        """
        DESCRIPTION: Check UI of team selection page as per zeplin image provided
        EXPECTED: UI should be as per Zeplin image
        """
        sys_desc = self.site.show_your_colors.select_your_team_message
        self.assertEqual(self.cms_config.get_fanzone_syc()['sycDescription'], sys_desc.text,
                         msg="Show your colours page description is not matched")
        if self.device_type != "mobile":
            self.assertTrue(self.site.show_your_colors.back_button, msg="Back Button in sys page is not displayed")
        else:
            self.assertTrue(self.site.header.back_button.is_displayed(), msg="Back Button in sys page is not displayed")
        self.__class__.teams = self.site.show_your_colors.items_as_ordered_dict
        for team in self.teams.items():
            team_ui_box_font_family = team[1].css_property_value('font-family')
            self.assertIn(vec.fanzone.SYC_TEAM_FONT_FAMILY, team_ui_box_font_family,
                          msg=f'Team UI box font family is not equal to Zepplin team box font family'
                              f'actual result "{team_ui_box_font_family}"')
            team_ui_box_color = team[1].css_property_value('color')
            self.assertEqual(team_ui_box_color, vec.fanzone.SYC_TEAM_COLOR,
                             msg=f'Team UI box color is not equal to Zepplin team box color'
                                 f'actual result "{team_ui_box_color}"')
            team_ui_box_bgcolor = team[1].css_property_value('background-color')
            self.assertEqual(team_ui_box_bgcolor, vec.fanzone.SYC_TEAM_BG_COLOR,
                             msg=f'Team UI box background-color is not equal to Zepplin team box background-color'
                                 f'actual result "{team_ui_box_bgcolor}"')
            team_ui_box_border = team[1].css_property_value('border-radius')
            self.assertEqual(team_ui_box_border, vec.fanzone.SYC_TEAM_BORDER_RADIUS,
                             msg=f'Team UI box border is not equal to Zepplin team box border'
                                 f'actual result "{team_ui_box_border}"')
            team_ui_box_font_size = team[1].css_property_value('font-size')
            self.assertEqual(team_ui_box_font_size, vec.fanzone.SYC_TEAM_FONT_SIZE,
                             msg=f'Team UI box font-size is not equal to Zepplin team box font-size'
                                 f'actual result "{team_ui_box_font_size}"')

    def test_002_check_there_are_20_teams_provided_and_i_dont_support_any_of_the_team__selections(self):
        """
        DESCRIPTION: Check there are 20 teams provided and "i don't support any of the team " selections
        EXPECTED: selections should display
        """
        self.assertLessEqual(len(self.teams.items()), vec.fanzone.SYC_TOTAL_TEAMS_COUNT, msg="Teams count is not matching")
        self.assertTrue(self.site.show_your_colors.i_dont_support_any_teams,
                        msg="I don't support any of the team selection not found on UI")

    def test_003_check_selecting_a_team(self):
        """
        DESCRIPTION: check selecting a team
        EXPECTED: Selection should be highlighted and should get a popup
        """
        for team in self.teams.items():
            if team[0] != "":
                team[1].scroll_to_we()
                team[1].click()
                dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
                dialog_confirm.select_different_button.click()
                sleep(1)
                team_ui_box_border = team[1].css_property_value('border').split(" ")[0]
                self.assertEqual(team_ui_box_border, vec.fanzone.SYC_SELECTED_TEAM_BORDER,
                                 msg=f'Team UI box border is not equal to Zepplin team box border'
                                     f'actual result "{team_ui_box_border}"')

    def test_004_check_all_the_selections_are_able_to_select(self):
        """
        DESCRIPTION: Check all the selections are able to select
        EXPECTED: Should able to select
        EXPECTED: Selection should be highlighted and should get a popup
        """
        # Covered in above step
