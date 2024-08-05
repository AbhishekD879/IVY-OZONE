import pytest
from datetime import datetime, date
from time import sleep
from crlat_ob_client.utils.date_time import get_date_time_as_string
from tests.base_test import vtest
from tests.Common import Common
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
class Test_C65304900_Verify_Now_and_Next_tab_will_not_populate_matches_of_non_selected_teams_in_Show_Your_Color_page(Common):
    """
    TR_ID: C65304900
    NAME: Verify Now and Next tab will not populate matches of non selected teams in Show Your Color page
    DESCRIPTION: Verify Now and Next tab will not populate matches of non selected teams in Show Your Color page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
    PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
    PRECONDITIONS: 5) HC should be created in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
        PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
        PRECONDITIONS: 5) HC should be created in CMS, as per below path
        PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
        """
        now = datetime.now()
        time_format = '%Y-%m-%d %H:%M:%S'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                            url_encode=False)
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.__class__.home_team = vec.fanzone.TEAMS_LIST.aston_villa.title()
        self.__class__.away_team = vec.fanzone.TEAMS_LIST.brentford.title()
        self.cms_config.update_fanzone(self.home_team, typeId=str(
            self.ob_config.football_config.autotest_class.autotest_premier_league.type_id))
        self.cms_config.update_fanzone(self.away_team, typeId=str(
            self.ob_config.football_config.autotest_class.autotest_premier_league.type_id))
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=self.home_team,
            away_team=self.away_team,
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.brentford, start_date=date_from)

        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.manchester_city.title(), typeId=str(typeId))
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.manchester_united.title(), typeId=str(typeId))

        self.__class__.team1 = vec.fanzone.TEAMS_LIST.manchester_city.title()
        self.__class__.team2 = vec.fanzone.TEAMS_LIST.manchester_united.title()
        self.ob_config.create_fanzone_league_event_id(
            league_id=typeId,
            home_team=self.team1,
            away_team=self.team2,
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_city,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_united)
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
        teams[vec.fanzone.TEAMS_LIST.brentford.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.brentford.title()].click()
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
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        result = wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                                 name='Fanzone page not displayed',
                                 timeout=5)
        self.assertTrue(result, msg='fanzone page not loaded')

    def test_002_mobile_verify_user_is_able_to_see_events_in_highlight_carouseldesktop_events_will_be_populating_as_per_the_existing_production_order_in_football_landing_pagelink_httpssportsladbrokescomsportfootballmatchestoday(
            self):
        """
        DESCRIPTION: Mobile: Verify user is able to see Events in "Highlight Carousel"
        DESCRIPTION: Desktop: Events will be populating as per the existing Production order in Football landing page.
        DESCRIPTION: Link: https://sports.ladbrokes.com/sport/football/matches/today
        EXPECTED: User should be able to see "Events" as described
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(vec.fanzone.NOW_AND_NEXT)
        carousel = list(self.site.fanzone.tab_content.highlight_carousels.values())[0]
        self.__class__.events = carousel.items_as_ordered_dict
        self.assertTrue(self.events, msg="Events are not found under Now and Next tab")
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

    def test_003_verify_user_is_presented_with_events_related_to_this_subscribed_team_alone(self):
        """
        DESCRIPTION: Verify user is presented with events related to this Subscribed team alone.
        EXPECTED: User should see events related to his subscribed Fanzone only, he should not see any events in which his subscribed team his not playing or part of
        """
        event_name = self.home_team + '\n' + self.away_team if self.device_type == 'mobile' else self.home_team + ' v ' + self.away_team
        self.assertIn(event_name, self.events,
                      msg=' User not seen events related to his subscribed Fanzone only')

        event_name = self.team1 + '\n' + self.team2 if self.device_type == 'mobile' else self.team1 + ' v ' + self.team2
        self.assertNotIn(event_name, self.events,
                         msg='User is seeing events in which his subscribed team his not playing')
