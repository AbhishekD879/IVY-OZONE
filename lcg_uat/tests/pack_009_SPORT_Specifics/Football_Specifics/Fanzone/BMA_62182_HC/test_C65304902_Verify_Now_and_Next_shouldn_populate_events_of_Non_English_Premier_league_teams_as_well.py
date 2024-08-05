from time import sleep
from crlat_ob_client.utils.date_time import get_date_time_as_string
from datetime import datetime
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
import pytest
import voltron.environments.constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.prod # can't create events in prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304902_Verify_Now_and_Next_shouldn_populate_events_of_Non_English_Premier_league_teams_as_well(Common):
    """
    TR_ID: C65304902
    NAME: Verify Now and Next shouldn populate events of Non English Premier league teams as well
    DESCRIPTION: Verify Now and Next shouldn populate events of Non English Premier league teams as well
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play and event should be configured such a way that EPL team vs Non EPL team(Arsenal vs Real Madrid )
    PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
    PRECONDITIONS: 5) HC should be created in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        Create the Fanzone team
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        home_team = vec.fanzone.TEAMS_LIST.manchester_city.title()
        away_team = "Real Madrid"
        self.cms_config.update_fanzone(home_team,
                                       typeId=str(
                                           self.ob_config.football_config.autotest_class.autotest_premier_league.type_id))
        now = datetime.now()
        time_format = '%Y-%m-%d %H:%M:%S'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                            url_encode=False)
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=home_team,
            away_team=away_team,
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_city,
            away_team_external_id="", start_date=str(date_from))
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True, timeout=10)
        self.site.wait_content_state("football", timeout=10)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.manchester_city.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_navigate_to_fanzone_page_any_of_the_below_listed_entry_pointsa_fanzone_in_sports_ribbononly_mobileb_fanzone_in_a_zall_sportsc_launch_banner_in_home_paged_launch_banner_in_football_landing_page(
            self):
        """
        DESCRIPTION: Navigate to Fanzone page any of the below listed entry points
        DESCRIPTION: a. Fanzone in Sports Ribbon(only mobile)
        DESCRIPTION: b. Fanzone in A-Z/All sports
        DESCRIPTION: c. Launch Banner in Home page
        DESCRIPTION: d. Launch banner in Football landing page
        EXPECTED: User should be navigated to Fanzone page
        """
        sleep(20)
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()

    def test_002_verify_user_is_able_to_see_events_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify user is able to see Events in Now and Next tab
        EXPECTED: User should be able to see Events section in Now and Next tab
        """
        sleep(10)
        self.device.refresh_page()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name='NOW & NEXT')
        carousel = list(self.site.fanzone.tab_content.highlight_carousels.values())[0]
        carousel_items = carousel.items_names[0]
        if self.device_type == 'mobile':
            self.assertIn("Real Madrid", carousel_items.split("\n")[1],
                          msg="Real Madrid is not displayed on UI Now and Next Tab")
            self.assertIn(vec.fanzone.TEAMS_LIST.manchester_city.title(), carousel_items.split("\n")[0],
                          msg=f'"{vec.fanzone.TEAMS_LIST.manchester_city.title()} is not displayed on UI Now and Next Tab"')
        else:
            self.assertIn("Real Madrid", carousel_items.split("v")[1].strip(),
                          msg="Real Madrid is not displayed on UI Now and Next Tab")
            self.assertIn(vec.fanzone.TEAMS_LIST.manchester_city.title(), carousel_items.split("v")[0].strip(),
                          msg=f'"{vec.fanzone.TEAMS_LIST.manchester_city.title()} is not displayed on UI Now and Next Tab"')

    def test_003_verify_now_and_next_will_populate_events_of_non_english_premier_league_teams1arsenal2aston_villa3brentford4brighton5burnley6chelsea7crystal_palace8everton9leeds_united10leicester_city11liverpool12man_city13man_united14newcastle15norwich_city16southampton17tottenham18watford19west_ham20wolves(
            self):
        """
        DESCRIPTION: Verify Now and Next will populate events of Non English Premier league teams
        DESCRIPTION: 1.Arsenal
        DESCRIPTION: 2.Aston villa
        DESCRIPTION: 3.Brentford
        DESCRIPTION: 4.Brighton
        DESCRIPTION: 5.Burnley
        DESCRIPTION: 6.Chelsea
        DESCRIPTION: 7.Crystal Palace
        DESCRIPTION: 8.Everton
        DESCRIPTION: 9.Leeds United
        DESCRIPTION: 10.Leicester City
        DESCRIPTION: 11.Liverpool
        DESCRIPTION: 12.Man City
        DESCRIPTION: 13.Man United
        DESCRIPTION: 14.Newcastle
        DESCRIPTION: 15.Norwich City
        DESCRIPTION: 16.Southampton
        DESCRIPTION: 17.Tottenham
        DESCRIPTION: 18.Watford
        DESCRIPTION: 19.West Ham
        DESCRIPTION: 20.Wolves
        EXPECTED: Verify Now and Next should populate events of Non English Premier League teams, when any of the EPL team is playing the match with non EPL team
        EXPECTED: ex: Arsenal vs Real Madrid
        """
    # Covered in above step
