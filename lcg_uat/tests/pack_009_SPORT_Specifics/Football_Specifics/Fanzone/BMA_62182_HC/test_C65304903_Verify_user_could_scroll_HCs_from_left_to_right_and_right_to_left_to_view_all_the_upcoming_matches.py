import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from datetime import datetime, date
from voltron.environments import constants as vec
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
class Test_C65304903_Verify_user_could_scroll_HCs_from_left_to_right_and_right_to_left_to_view_all_the_upcoming_matches(Common):
    """
    TR_ID: C65304903
    NAME: Verify user could scroll HC's from left to right and right to left to view all the upcoming matches
    DESCRIPTION: Verify user could scroll HC's from left to right and right to left to view all the upcoming matches
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
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
        home_team = vec.fanzone.TEAMS_LIST.aston_villa.title()
        away_team = vec.fanzone.TEAMS_LIST.brentford.title()
        astonVilla_fanzone = self.cms_config.get_fanzone(home_team)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(home_team,
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=home_team,
            away_team=away_team,
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.brentford)
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
        list(teams.values())[1].scroll_to_we()
        list(teams.values())[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_navigate_to_fanzone_page_any_of_the_below_listed_entry_pointsa_fanzone_in_sports_ribbononly_mobileb_fanzone_in_a_zall_sportsc_launch_banner_in_home_paged_launch_banner_in_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page any of the below listed entry points
        DESCRIPTION: a. Fanzone in Sports Ribbon(only mobile)
        DESCRIPTION: b. Fanzone in A-Z/All sports
        DESCRIPTION: c. Launch Banner in Home page
        DESCRIPTION: d. Launch banner in Football landing page
        EXPECTED: User should be navigated to Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name='NOW & NEXT')

    def test_002_verify_user_is_able_to_see_events_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify user is able to see Events in Now and Next tab
        EXPECTED: User should be able to see Events section in Now and Next tab
        """
        carousel = list(self.site.fanzone.tab_content.highlight_carousels.values())[0]
        self.__class__.events = carousel.items_as_ordered_dict
        self.assertTrue(self.events, msg="Events are not found under Now and Next tab")

    def test_003_mobile_verify_user_is_able_to_see_events_in_highlight_carouseldesktop_events_will_be_populating_as_per_the_existing_production_order_in_football_landing_pagelink_httpssportsladbrokescomsportfootballmatchestoday(self):
        """
        DESCRIPTION: Mobile: Verify user is able to see Events in "Highlight Carousel"
        DESCRIPTION: Desktop: Events will be populating as per the existing Production order in Football landing page.
        DESCRIPTION: Link: https://sports.ladbrokes.com/sport/football/matches/today
        EXPECTED: User should be able to see "Events" as described
        """
        expected_date_list = []
        for event in self.events.values():
            event_time = event.event_time
            if event_time != '':
                if event_time.endswith('Today'):
                    today_date = date.today().strftime('%d %b')
                    event_time = event_time.replace('Today', today_date)
                expected_date_list.append(event_time)
        actual_date_list = expected_date_list
        expected_date_list.sort(key=lambda date: datetime.strptime(date, "%H:%M %d %b"))
        self.assertEqual(actual_date_list, expected_date_list,
                         msg=f'Actual timings: "{actual_date_list}" are not in chronological order as '
                             f'Expected timings: "{expected_date_list}" ')

    def test_004_mobile_verify_user_is_able_to_scroll_events_from_left_to_right_and_vise_versanote_for_desktop_its_bau(self):
        """
        DESCRIPTION: Mobile: Verify user is able to scroll events from left to right and Vise versa
        DESCRIPTION: Note: For desktop its BAU
        EXPECTED: User should be able to scroll events from Left to right OR vice versa.
        """
        # not applicable
