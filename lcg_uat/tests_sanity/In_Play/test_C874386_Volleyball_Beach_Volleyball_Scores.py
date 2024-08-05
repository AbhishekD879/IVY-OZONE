import pytest
import voltron.environments.constants as vec

from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from time import sleep
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Need to create event
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.sanity
@vtest
class Test_C874386_Volleyball_Beach_Volleyball_Scores(BaseFallbackScoreboardTest, BaseFeaturedTest):
    """
    TR_ID: C874386
    NAME: Volleyball/Beach Volleyball Scores
    DESCRIPTION: This test case verifies Volleyball/Beach Volleyball Live Score of BIP events
    PRECONDITIONS: 1) In order to have a Scores Volleyball/Beach Volleyball event should be BIP
    PRECONDITIONS: 2) To verify Volleyball/Beach Volleyball data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX", where XX - Category ID; XXX - Type ID
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "VOLLEYBALL"
    PRECONDITIONS: *   **teams** - home or away
    PRECONDITIONS: *   **name** - team name
    PRECONDITIONS: *   **score** - total score for team
    PRECONDITIONS: *   **currentPoints** - points in current set for team
    PRECONDITIONS: ![](index.php?/attachments/get/5692995)
    PRECONDITIONS: 3) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code** ='PLAYER_1'/'PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: ![](index.php?/attachments/get/5700213)
    PRECONDITIONS: 4) [How to generate Live Scores for Volleyball using Bet Genius][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+Updates+for+Volleyball%2C+Beach+Volleyball+and+Badminton
    PRECONDITIONS: [Bet Genius credentials][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 5) [How to generate Live Scores for Volleyball/Beach Volleyball using TI][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: 6) [How to configure Fallback Scoreboard in CMS][4]
    PRECONDITIONS: [4]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    """
    keep_browser_open = True
    module_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME
    home_point_score = '1'
    away_point_score = '3'
    score = {'current': '(1) 1-3 (1)'}

    @retry(stop=stop_after_attempt(2),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def scores_verification(self, score_type=None, team1_score=None, team2_score=None):
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        score_event = events.get(self.live_event_name)
        team1_expected_score = team1_score
        team2_expected_score = team2_score
        if score_type == 'game_score':
            team1_score_actual = score_event.score_table.game_score.home_score
            self.assertEqual(team1_score_actual, team1_expected_score,
                             msg=f'Home score "{team1_score_actual}" is not the same as in response: "{team1_expected_score}"')
            team2_score_actual = score_event.score_table.game_score.away_score
            self.assertEqual(team2_score_actual, team2_expected_score,
                             msg=f'Away score "{team2_score_actual}"  is not the same as in response: "{team2_expected_score}"')
        elif score_type == 'sets_score':
            team1_score_actual = score_event.score_table.sets_score_for_sp.home_score
            self.assertEqual(team1_score_actual, team1_expected_score,
                             msg=f'Home score "{team1_score_actual}" is not the same as in response: "{team1_expected_score}"')
            team2_score_actual = score_event.score_table.sets_score_for_sp.away_score
            self.assertEqual(team2_score_actual, team2_expected_score,
                             msg=f'Away score "{team2_score_actual}"  is not the same as in response: "{team2_expected_score}"')
        elif score_type == 'points_score':
            team1_score_actual = score_event.score_table.points_score.home_score
            self.assertEqual(team1_score_actual, team1_expected_score,
                             msg=f'Home score "{team1_score_actual}" is not the same as in response: "{team1_expected_score}"')
            team2_score_actual = score_event.score_table.points_score.away_score
            self.assertEqual(team2_score_actual, team2_expected_score,
                             msg=f'Away score "{team2_score_actual}"  is not the same as in response: "{team2_expected_score}"')
        else:
            raise Exception("provided score type is not a valid score type for Volleyball")

    def create_events(self):
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.volleyball_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.volleyball_config.category_id)
        self.__class__.widget_section_name = 'In-Play LIVE Volleyball'
        # Simple event
        event_params = self.ob_config.add_volleyball_event_to_austrian_league(is_live=True)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self._logger.info(f'*** Create Vollyball event "{self.event_name}"')

        # Score event
        start_time = self.get_date_time_formatted_string(days=-4)
        live_event = self.ob_config.add_volleyball_event_to_austrian_league(start_time=start_time, is_live=True,
                                                                            score=self.score, perform_stream=True)
        self.__class__.team1 = live_event.team1
        self.__class__.team2 = live_event.team2
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=live_event.event_id,
                                                         query_builder=self.ss_query_builder,
                                                         raise_exceptions=False)

        self.__class__.league_name_watch_live = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                          in_play_page_watch_live=True)

        self.__class__.league_name_in_play_sport_tab = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                 in_play_page_sport_tab=True)
        self.__class__.league_name_in_play_live_stream_homepage = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                            in_play_tab_home_page=True)
        self.__class__.league_name_in_play_module_slp = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                  in_play_module_slp=True)
        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                               in_play_tab_slp=True)

        self.__class__.live_event_name = self.team1 + ' v ' + self.team2
        self.__class__.sport_name = vec.sb.VOLLEYBALL if self.brand != 'bma' else vec.sb.VOLLEYBALL.upper()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Volleyball' tab
        EXPECTED: 'Volleyball' tab on the 'In-Play' page is opened
        """
        self.create_events()

    def test_001_load_the_application_and_navigate_to_in_play_page__volleyballbeach_volleyball_tab(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Volleyball'/'Beach Volleyball' tab
        EXPECTED: 'Volleyball'/'Beach Volleyball' tab on the 'In-Play' page is opened
        """
        self.check_sport_presence_on_inplay(sport_name='/volleyball')
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')
        self.site.inplay.inplay_sport_menu.click_item(self.sport_name)
        self.site.wait_content_state(state_name='InPlay')

    def test_002_verify_volleyball_event_with_scores_available(self, slp=False):
        """
        DESCRIPTION: Verify 'Volleyball' event with scores available
        EXPECTED: * Total score (Sets) and PointsInCurrentSet for particular team are shown vertically at the same row as team's name near the Price/Odds button
        EXPECTED: * Score for the home player is shown in front of home player name
        EXPECTED: * Score for the away player is shown in front of away player name
        EXPECTED: * PointsInCurrentSet for the home player is shown on the first row
        EXPECTED: * PointsInCurrentSet for the away player is shown on the second row
        EXPECTED: * 'Live' label is displayed
        EXPECTED: * 'Watch Live' icon is displayed if live stream is available
        """
        section_name = self.league_name_in_play_sport_tab
        if not slp:
            self.__class__.sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No sections found')
            if not self.sections.get(section_name):
                sleep(30)
                self.device.refresh_page()
                self.site.wait_content_state(state_name='InPlay')
                self.sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        else:
            self.__class__.sections = self.site.sports_page.tab_content.in_play_module.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No sections found')

        self.__class__.section = self.sections.get(section_name)
        self.assertTrue(self.section, msg=f'"{section_name}" section not found on page')
        if not self.section.is_expanded() and not slp:
            self.section.expand()
            self.assertTrue(self.section.is_expanded(), msg=f'"{section_name}" section is not expanded')
        self.scores_verification(score_type='points_score', team1_score=self.home_point_score,
                                 team2_score=self.away_point_score)
        self.scores_verification(score_type='sets_score', team1_score=self.home_set_scores,
                                 team2_score=self.away_set_scores)
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        score_event = events.get(self.live_event_name)
        self.assertTrue(score_event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
        self.assertTrue(score_event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

        home_game_score_element = score_event.score_table.game_score.home_score_element()
        away_game_score_element = score_event.score_table.game_score.away_score_element()
        first_player = score_event.event_first_player()
        second_player = score_event.event_second_player()
        if home_game_score_element.location['y'] == first_player.location['y']:
            self.assertTrue(home_game_score_element.location['x'] > first_player.location['x'],
                            msg="position of the elements are not expected")
        if away_game_score_element.location['y'] == second_player.location['y']:
            self.assertTrue(away_game_score_element.location['x'] > second_player.location['x'],
                            msg="position of the elements are not expected")
        game_color_code = home_game_score_element.value_of_css_property('color')
        expected_color = vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY if (self.device_type == 'mobile' or self.brand != 'bma') else vec.colors.COMPLIANCE_INFO_FONT_COLOR_GREY_DESKTOP
        self.assertEqual(game_color_code, expected_color,
                         msg=f'colors of game score "{game_color_code}" not matching with expected "{expected_color}"')

    def test_003_verify_volleyball_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify Volleyball event which doesn't have LIVE Score available
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * Total score (Sets) and PointsInCurrentSet are NOT displayed
        """
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        event = events.get(self.event_name)
        self.softAssert(self.assertTrue, event,
                        msg=f'Event {self.event_name} was not found in the list of events {list(events.keys())}')
        self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
        self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

    def test_004_repeat_steps_2_3_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 2-3 for:
        DESCRIPTION: - Homepage -> 'Featured' tab/section
        DESCRIPTION: - Homepage -> 'In-Play' tab
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        EXPECTED:
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state('Homepage')
            score_event = self.get_event_for_homepage_inplay_tab(
                event_name=self.live_event_name,
                sport_name=self.sport_name.upper(),
                league_name=self.league_name_in_play_live_stream_homepage,
                raise_exceptions=False)
            self.softAssert(self.assertTrue, score_event, msg=f'Event "{self.live_event_name}" not found for "In-Play tab"')
            home_score_actual = score_event.score_table.sets_score_for_sp.home_score
            self.assertEqual(home_score_actual, self.home_set_scores,
                             msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.home_set_scores}"')

            away_score_actual = score_event.score_table.sets_score_for_sp.away_score
            self.assertEqual(away_score_actual, self.away_set_scores,
                             msg=f'Away score "{away_score_actual}"  is not the same as in response: "{self.away_set_scores}"')

            event = self.get_event_for_homepage_inplay_tab(
                event_name=self.event_name,
                sport_name=self.sport_name.upper(),
                league_name=self.league_name_in_play_live_stream_homepage,
                raise_exceptions=False)
            self.softAssert(self.assertTrue, event, msg=f'Event "{self.event_name}" not found for "In-Play tab"')
            self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
            self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')
        else:
            self.navigate_to_page(name='/')
            self.site.wait_content_state('Homepage')
            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            inplay_volleyball_tab = inplay_sports.get(self.sport_name)
            self.assertTrue(inplay_volleyball_tab, msg=f'"{self.sport_name}" tab not found')
            inplay_volleyball_tab.click()
            self.assertTrue(inplay_volleyball_tab.is_selected(),
                            msg=f'"{self.sport_name}" tab is not selected')
            leagues = self.site.home.get_module_content(module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.softAssert(self.assertTrue, self.section,
                            msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found in "{leagues.keys()}"')
            self.scores_verification(score_type='points_score', team1_score=self.home_point_score,
                                     team2_score=self.away_point_score)
            self.scores_verification(score_type='sets_score', team1_score=self.home_set_scores,
                                     team2_score=self.away_set_scores)

            self.test_003_verify_volleyball_event_which_doesnt_have_live_score_available()

            # 'In-Play' page -> 'Watch Live' tab
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state('in-play')
        if self.brand == 'bma' or self.device_type == 'mobile':
            self.league_name_watch_live = self.league_name_watch_live.upper()
        else:
            self.league_name_watch_live = 'Austria - AVL'

        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_watch_live,
                                        watch_live_page=True)
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        score_event = events.get(self.live_event_name)
        home_score_actual = score_event.score_table.sets_score_for_sp.home_score
        self.assertEqual(home_score_actual, self.home_set_scores,
                         msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.home_set_scores}"')

        away_score_actual = score_event.score_table.sets_score_for_sp.away_score
        self.assertEqual(away_score_actual, self.away_set_scores,
                         msg=f'Away score "{away_score_actual}"  is not the same as in response: "{self.away_set_scores}"')

        # Sports Landing page -> 'In-Play' tab
        if self.device_type == 'desktop':
            self.navigate_to_page(name='sport/volleyball')
            self.site.wait_content_state(vec.sb.VOLLEYBALL)
            self.site.sports_page.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
            self.site.wait_content_state('Volleyball')

            events = self.get_inplay_events(league_name=self.league_name_in_play_tab_slp, watch_live_page=False)
            self.assertTrue(events, msg='There is no Events on the page')
            self.softAssert(self.assertTrue, self.live_event_name in events,
                            msg=f'Event {self.live_event_name} was not found in the list of events {events.keys()}')
            score_event = events.get(self.live_event_name)
            home_score_actual = score_event.score_table.sets_score_for_sp.home_score
            self.assertEqual(home_score_actual, self.home_set_scores,
                             msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.home_set_scores}"')
            away_score_actual = score_event.score_table.sets_score_for_sp.away_score
            self.assertEqual(away_score_actual, self.away_set_scores,
                             msg=f'Away score "{away_score_actual}" is not the same as in response: "{self.away_set_scores}"')
            event = events.get(self.event_name)
            self.softAssert(self.assertTrue, event,
                            msg=f'Event "{self.event_name}" was not found in the list of events "{events.keys()}"')
            self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
            self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

        # Sports Landing page -> 'In-Play' module **Mobile**
        if self.device_type != 'desktop':
            self.navigate_to_page(name='sport/volleyball')
            self.site.wait_content_state(state_name=vec.sb.VOLLEYBALL)
            self.softAssert(self.assertTrue, self.site.sports_page.tab_content.has_inplay_module(),
                            msg='In Play module is not enabled for Volleyball landing page')
            inplay_section = self.site.sports_page.tab_content.in_play_module.items_as_ordered_dict

            self.assertTrue(inplay_section, msg='In-Play module has no any sections')
            self.__class__.section = inplay_section.get(self.league_name_in_play_module_slp)
            self.assertTrue(self.section,
                            msg=f'"{self.league_name_in_play_module_slp}" not found in leagues: "{inplay_section.keys()}"')
            self.test_002_verify_volleyball_event_with_scores_available(slp=True)
            self.test_003_verify_volleyball_event_which_doesnt_have_live_score_available()

        # 'In-Play & Live Stream ' section on Homepage **Desktop**
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')
            inplay_live_stream = self.site.home.desktop_modules.inplay_live_stream_module
            if self.brand == 'bma':
                volleyball = vec.sb.VOLLEYBALL.upper()
            else:
                volleyball = vec.sb.VOLLEYBALL
            inplay_live_stream.menu_carousel.items_as_ordered_dict.get(volleyball).click()
            in_play_tabs = inplay_live_stream.tabs_menu
            in_play_tabs.click_button(vec.sb.LIVE_STREAM.upper())

            self.assertEqual(in_play_tabs.current, vec.sb.LIVE_STREAM.upper(),
                             msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected. Actual "{in_play_tabs.current}"')

            leagues = self.site.home.get_module_content(
                module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.assertTrue(self.section, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
            self.scores_verification(score_type='points_score', team1_score=self.home_point_score,
                                     team2_score=self.away_point_score)
            self.scores_verification(score_type='sets_score', team1_score=self.home_set_scores,
                                     team2_score=self.away_set_scores)

    def test_005_desktopnavigate_to_volleyball_landing_page__matches_tab_and_verify_scoresset_number_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Volleyball landing page > 'Matches' tab and verify scores/set number for 'In-play' widget
        EXPECTED: * 'LIVE' badge is displayed below the Event name
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        if self.device_type == 'desktop':
            self.site.open_sport(name=self.sport_name)
            self.site.wait_content_state(state_name=vec.sb.VOLLEYBALL)
            self.site.sports_page.tabs_menu.click_button(vec.SB.TABS_NAME_MATCHES.upper())
            sections = self.site.sports_page.in_play_widget.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Volleyball page')
            self.assertIn(self.widget_section_name, sections.keys(),
                          msg=f'{self.widget_section_name} not found in {sections.keys()}')
            self.__class__.section = sections.get(self.widget_section_name)
            events = self.section.content.items_as_ordered_dict
            self.assertTrue(events, msg='There is no Events on the page')

            event = events.get(self.live_event_name)
            self.softAssert(self.assertTrue, event,
                            msg=f'Event "{self.live_event_name}" was not found in the list of events {events.keys()}')
            event.scroll_to()
            home_score = event.in_play_card.current_left_score
            away_score = event.in_play_card.current_right_score
            self.assertEqual(self.home_point_score, home_score,
                             msg=f'Actual score value "{home_score}"'
                             f' for Home team is not the same as expected "{self.home_point_score}"')
            self.assertEqual(self.away_point_score, away_score,
                             msg=f'Actual score value "{away_score}"'
                             f' for Away team is not the same as expected "{self.away_point_score}"')
            self.assertTrue(event.in_play_card.live_icon, msg="LIVE icon is not displayed for the event")
            set_score_home = event.in_play_card.current_left_score_element
            set_score_away = event.in_play_card.current_left_score_element
            self.assertEqual(set_score_home.location['y'], set_score_away.location['y'],
                             msg=f'position of the Set "{set_score_home.location["y"]}" and Point "{set_score_away.location["y"]}" '
                                 f'are not in SAME row')

    def test_006_desktopnavigate_to_volleyball_landing_page__matches_tab_and_verify_scoresset_number_for_live_stream_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Volleyball landing page > 'Matches' tab and verify scores/set number for 'Live Stream' widget
        EXPECTED: * 'LIVE' badge is displayed next to event class/type
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        """
        if self.device_type == 'desktop':
            widgets = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle')
            if not widgets:
                widgets = self.cms_config.get_system_configuration_item('DesktopWidgetsToggle')
            widget_available = widgets.get('liveStream')
            if not widget_available:
                raise CmsClientException('"Live Stream" widget is not configured in CMS')

            self.site.login()
            self.navigate_to_page(name='sport/volleyball')
            self.site.wait_content_state(state_name=vec.sb.VOLLEYBALL)
            event = self.site.sports_page.live_stream_widget
            self.softAssert(self.assertTrue, self.live_event_name in event.name,
                            msg=f'Event "{self.live_event_name}" was not found')
            self.assertTrue(event.live_now_label, msg='LIVE lable is not shown in WATCH LIVE widget')
            expected_point_score = self.home_point_score + ' - ' + self.away_point_score
            point_score = event.point_score
            self.assertEqual(expected_point_score, point_score, msg=f'Actual score value "{point_score}"'
                             f' for Teams is not the same as expected "{expected_point_score}"')

            set_score_wb = event.set_score_element
            point_score_wb = event.point_score_element
            self.assertEqual(set_score_wb.location['y'], point_score_wb.location['y'],
                             msg=f'position of the Set "{set_score_wb.location["y"]}" and Point "{point_score_wb.location["y"]}" '
                                 f'are not in SAME row')
