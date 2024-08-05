import pytest
from datetime import datetime
from time import sleep
from crlat_siteserve_client.utils.date_time import get_date_time_as_string
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.prod # can't create events in prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305306_To_verify_UI_of_live_events_and_upcoming_events_in_Now_and_Next_Tab_in_Fanzone_page(Common):
    """
    TR_ID: C65305306
    NAME: To verify UI of live events and upcoming events in Now and Next Tab in Fanzone page
    DESCRIPTION: To verify UI of live events and upcoming events in Now and Next Tab in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in Ob
    PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
    PRECONDITIONS: 5) HC should be created in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    """
    keep_browser_open = True

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        home_team = vec.fanzone.TEAMS_LIST.southampton.title()
        away_team = vec.fanzone.TEAMS_LIST.watford.title()
        astonVilla_fanzone = self.cms_config.get_fanzone(home_team)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(home_team,
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)

        now = datetime.now()
        time_format = '%Y-%m-%d %H:%M:%S'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                            url_encode=False, days=1)
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=str(home_team),
            away_team=str(away_team),
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.southampton,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.watford, start_date=str(date_from))

        time_format = '%Y-%m-%d %H:%M:%S'
        in_play_date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                            url_encode=False)
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=str(home_team),
            away_team=str(away_team),
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.southampton,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.watford, start_date=str(in_play_date_from))

    def test_001_navigate_to_fanzone_page_any_of_the_below_listed_entry_pointsa_fanzone_in_sports_ribbononly_mobileb_fanzone_in_a_zall_sportsc_launch_banner_in_home_paged_launch_banner_in_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page any of the below listed entry points
        DESCRIPTION: a. Fanzone in Sports Ribbon(only mobile)
        DESCRIPTION: b. Fanzone in A-Z/All sports
        DESCRIPTION: c. Launch Banner in Home page
        DESCRIPTION: d. Launch banner in Football landing page
        EXPECTED: User should be navigated to Fanzone page
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                                             verify_name=False)
        self.assertTrue(self.dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')
        self.dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I am in button is displayed',
                        timeout=5)
        self.assertTrue(self.site.show_your_colors, msg='"SYC selection page"is not displayed after click')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.southampton.title()].click()
        self.__class__.dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        self.assertTrue(self.dialog_confirm, msg='Team confirmation pop-up is not appeared')
        self.dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS,
                                                 timeout=15)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        self.assertTrue(dialog_alert, msg='Failed to load dailog alert pop-up ')
        dialog_alert.exit_button.click()
        banner= fanzone_banner = self.site.home.fanzone_banner()
        self.assertTrue(fanzone_banner.let_me_see.is_displayed(),
                        msg='No Fanzone entry point shown on Football SLP')
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    def test_002_verify_ui_of_live_events_and_next_games_is_as_per_the_zeplin(self):
        """
        DESCRIPTION: Verify UI of Live events and next games is as per the Zeplin
        EXPECTED: Ui should be as per the Zeplin screen
        EXPECTED: Zeplin Link: HTTPs://app.zeplin.io/project/5f296ce76014322057c71b9f/screen/614c5b69a23dc0b1ca01a8a6
        EXPECTED: Note: It should be similar to Football landing page in desktop without 'MORE' link.
        """
        self.site.fanzone.tabs_menu.click_button(button_name='NOW & NEXT')
        self.__class__.carousel = list(self.site.fanzone.tab_content.highlight_carousels.values())[0]
        carousel_items = self.carousel.items_names[0]
        if self.device_type == 'mobile':
            self.assertIn(vec.fanzone.TEAMS_LIST.southampton.title(), carousel_items.split("\n")[0],
                          msg="Real Madrid is not displayed on UI Now and Next Tab")
            self.assertIn(vec.fanzone.TEAMS_LIST.watford.title(), carousel_items.split("\n")[1],
                          msg=f'"{vec.fanzone.TEAMS_LIST.manchester_city.title()} is not displayed on UI Now and Next Tab"')
        else:
            self.assertIn(vec.fanzone.TEAMS_LIST.southampton.title(), carousel_items.split("v")[0].strip(),
                          msg="Real Madrid is not displayed on UI Now and Next Tab")
            self.assertIn(vec.fanzone.TEAMS_LIST.watford.title(), carousel_items.split("v")[1].strip(),
                          msg=f'"{vec.fanzone.TEAMS_LIST.manchester_city.title()} is not displayed on UI Now and Next Tab"')

    def test_003_click_on_event(self):
        """
        DESCRIPTION: Click on Event
        EXPECTED: User should be navigated to EDP
        """
        events = self.carousel.items_as_ordered_dict
        list(events.values())[0].click()
        self.site.wait_content_state(state_name='EventDetails', timeout=20)
