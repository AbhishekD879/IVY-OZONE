from time import sleep
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec
import pytest
import tests


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305138_Data_in_standing_about_the_competition_for_which_Fanzone_user_team_is_playing(Common):
    """
    TR_ID: C65305138
    NAME: Data in standing about the competition for which Fanzone user team is playing
    DESCRIPTION: To verify user is able to see the data in standing about the competition for which Fanzone user team is playing
    PRECONDITIONS: 1)User has access to CMS and valid credentials to login
    PRECONDITIONS: 2)User has access to FE and valid credentials to login
    PRECONDITIONS: 3)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 4)Premier league table and icon is configured in CMS successfully , League table is mapped to the Team for the competition team is playing
    PRECONDITIONS: 5)User has logged into Lads FE and is on Fanzone page
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
        manchesterCity_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title())
        if not manchesterCity_fanzone['fanzoneConfiguration']['showCompetitionTable']:
            raise CMSException(f'"showCompetitionTable is not enabled for {vec.fanzone.TEAMS_LIST.manchester_city.title()}"')
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_autotest_premier_league_football_outright_event()
            selection_name, selection_id = list(event.selection_ids.items())[0]
            self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                          fanzone_team=vec.fanzone.TEAMS_LIST.manchester_city,
                                                          team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_city)
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title(),
                                           typeId=str(self.ob_config.football_config.autotest_class.autotest_premier_league.type_id))
        else:
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

    def test_001_verify_if_user_is_able_to_see_premier_league_table_and_icon_in_now_and_next_tab_in_fe(self):
        """
        DESCRIPTION: Verify If user is able to see Premier League table and icon in Now and Next Tab in FE
        EXPECTED: User should be able to see Premier League table and icon in Now and Next Tab in FE
        """
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click() as per the new change, after subscription, we will be in fanzone page only
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)
        self.assertTrue(self.site.fanzone.premier_leauge_link, msg="Premier League Table is not displayed")

    def test_002_click_on_the_teams_bets_header_link(self):
        """
        DESCRIPTION: Click on the Teams bets header link
        EXPECTED: User should be able to see the league table is opened as overlay with close option(X)
        """
        self.device.driver.execute_script("return arguments[0].click();", self.site.fanzone.premier_leauge_link)
        self.assertTrue(self.site.fanzone.premier_leauge.close_button, msg="Close Button in Premier League Table is not displayed")

    def test_003_verify_the_opened_overlay_data_is_the_league_table_of_the_competition_team_is_participating(self):
        """
        DESCRIPTION: Verify the opened overlay data is the league table of the competition team is participating
        EXPECTED: User should be able to league table of the competition team is participating
        """
        # covered in step 2
