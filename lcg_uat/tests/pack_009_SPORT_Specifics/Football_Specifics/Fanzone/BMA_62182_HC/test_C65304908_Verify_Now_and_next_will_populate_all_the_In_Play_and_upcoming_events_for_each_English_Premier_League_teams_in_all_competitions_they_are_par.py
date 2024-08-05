import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.prod # Can't create events in Prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304908_Verify_Now_and_next_will_populate_all_the_In_Play_and_upcoming_events_for_each_English_Premier_League_teams_in_all_competitions_they_are_participating_in_current_season(Common):
    """
    TR_ID: C65304908
    NAME: Verify Now and next will populate all the In-Play and upcoming events for each English Premier League teams in all competitions they are participating in current season
    DESCRIPTION: Verify Now and next will populate all the In-Play and upcoming events for each English Premier League teams in all competitions they are participating in current season
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB for couple of Type Ids/Leagues like EPL,FA Cup, league One etc., some of the events should be In-Play
    PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
    PRECONDITIONS: 5) HC should be created in CMS for various Type Id's as per the Events available in OB, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module6) Surface Bets are configured in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2

    def test_000_precondition(self):
        username = self.gvc_wallet_user_client.register_new_user().username
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                      field_name='enabled',
                                                                      field_value=True)
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id = event.selection_ids[event.team1]
            self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=self.selection_id,
                                                                                 priceNum=self.price_num,
                                                                                 priceDen=self.price_den)

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
        events_section = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events_section, msg="Events are not found under Now and Next tab")

    def test_003_verify_displayed_surface_bets_are_from_selections_of_different_type_ids(self):
        """
        DESCRIPTION: Verify displayed Surface Bets are from selections of different Type Id's
        EXPECTED: Populated Surface Bets should belong to various Type Id's
        """
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')

    def test_004_verify_events_from_different_type_ids_are_populated_in_form_hc(self):
        """
        DESCRIPTION: Verify events from different Type Id's are populated in form HC
        EXPECTED: Events from different Type Id's should populate in the form of HC
        """
        events = self.site.fanzone.tab_content.highlight_carousels
        self.assertTrue(events, msg="Events are not found in HC")
