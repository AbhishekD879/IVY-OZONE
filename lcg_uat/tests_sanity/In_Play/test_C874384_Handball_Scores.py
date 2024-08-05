import pytest
import voltron.environments.constants as vec
from time import sleep
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tests.base_test import vtest
from selenium.common.exceptions import StaleElementReferenceException
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't create events
@pytest.mark.desktop
@pytest.mark.sanity
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C874384_Handball_Scores(BaseFallbackScoreboardTest, BaseFeaturedTest):
    """
    TR_ID: C874384
    NAME: Handball Scores
    DESCRIPTION: This test case verifies Handball Live Score of BIP events
    PRECONDITIONS: 1) In order to have a Scores Handball event should be BIP
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::::LIVE_EVENT"
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "HANDBALL"
    PRECONDITIONS: *   **teams** - home or away
    PRECONDITIONS: *   **name** - team name
    PRECONDITIONS: *   **score** - total score for team
    PRECONDITIONS: ![](index.php?/attachments/get/6165168)
    PRECONDITIONS: 3) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **value** - to see a Game score for particular participant
    PRECONDITIONS: *   **role_code**='HOME'/'AWAY' - to determine HOME and AWAY teams
    PRECONDITIONS: ![](index.php?/attachments/get/6165169)
    PRECONDITIONS: 4) [How to generate Live Scores for Handball using Bet Genius][1]
    PRECONDITIONS: [Bet Genius credentials][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Bet+Genius
    PRECONDITIONS: 5) [How to generate Live Scores for Badminton using TI][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: 6) [How to configure Fallback Scoreboard in CMS][4]
    PRECONDITIONS: [4]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    """
    keep_browser_open = True
    scores_updated = False
    module_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME
    home_game_score = '1'
    away_game_score = '3'
    score = {'current': f'{home_game_score}-{away_game_score}'}
    expected_home_score = None
    expected_away_score = None

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
            team1_score_actual = score_event.score_table.match_score.home_score
            self.assertEqual(team1_score_actual, team1_expected_score,
                             msg=f'Home score "{team1_score_actual}" is not the same as in response: "{team1_expected_score}"')
            team2_score_actual = score_event.score_table.match_score.away_score
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
            raise Exception("provided score type is not a valid score type for handball")

    def create_events(self):
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.handball_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.handball_config.category_id)
        self.__class__.widget_section_name = 'In-Play LIVE Handball'
        # Simple event
        event_params = self.ob_config.add_handball_event_to_croatian_premijer_liga(is_live=True)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self._logger.info(f'*** Create Handball event "{self.event_name}"')

        # Score event
        live_event = self.ob_config.add_handball_event_to_croatian_premijer_liga(is_live=True, score=self.score,
                                                                                 perform_stream=True)
        self.__class__.team1 = live_event.team1
        self.__class__.team2 = live_event.team2
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=live_event.event_id,
                                                         query_builder=self.ss_query_builder,
                                                         raise_exceptions=False)

        self.__class__.league_name_watch_live = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                          in_play_page_watch_live=True)
        self.__class__.league_name_in_play_sport_tab = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                 in_play_page_sport_tab=True)
        self.__class__.league_name_in_play_live_stream_homepage = self.get_accordion_name_for_event_from_ss(
            event=resp[0],
            in_play_tab_home_page=True)
        self.__class__.league_name_in_play_module_slp = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                  in_play_module_slp=True)
        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                               in_play_tab_slp=True)

        self.__class__.live_event_name = self.team1 + ' v ' + self.team2
        self.__class__.live_event_id = live_event.event_id
        self.__class__.sport_name = 'Handball' if self.brand != 'bma' else 'HANDBALL'
        start_time = self.get_date_time_formatted_string(days=-4)
        self.ob_config.update_event_start_time(eventID=self.live_event_id, start_time=start_time)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Handball' tab
        EXPECTED: 'Handball' tab on the 'In-Play' page is opened
        """
        self.create_events()

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        # covered in step 2

    def test_002_load_handball___in_play(self):
        """
        DESCRIPTION: Load 'Handball' -> 'In-Play'
        EXPECTED: 'In-Play' tab is opened
        """
        self.check_sport_presence_on_inplay(sport_name='/handball')
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')
        self.site.inplay.inplay_sport_menu.click_item(self.sport_name)
        self.site.wait_content_state(state_name='InPlay')

    def test_003_verify_handball_event_with_scores_available(self, slp=False, section=False):
        """
        DESCRIPTION: Verify 'Handball' event with scores available
        EXPECTED: * Event is shown
        EXPECTED: * Live scores are displayed
        EXPECTED: * 'LIVE' label is displayed
        EXPECTED: * 'Watch live' icon is displayed if live stream is available
        """
        section_name = self.league_name_in_play_sport_tab
        if not slp and not section:
            self.__class__.sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No sections found')
            if not self.sections.get(section_name):
                sleep(20)
                self.sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            self.__class__.section = self.sections.get(section_name)
        elif not section:
            self.__class__.sections = self.site.sports_page.tab_content.in_play_module.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No sections found')
            self.__class__.section = self.sections.get(section_name.title() if self.brand == 'bma' else section_name)
        self.assertTrue(self.section, msg=f'"{section_name.title()}" section not found on page')
        if not self.section.is_expanded() and not slp:
            self.section.expand()
            self.assertTrue(self.section.is_expanded(), msg=f'"{section_name.title()}" section is not expanded')
        self.scores_verification(score_type='game_score', team1_score=self.home_game_score,
                                 team2_score=self.away_game_score)
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        score_event = events.get(self.live_event_name)
        self.assertTrue(score_event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
        self.assertTrue(score_event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

    def test_004_verify_score_displaying(self):
        """
        DESCRIPTION: Verify score displaying
        EXPECTED: Match score is shown between price/odds buttons and event name
        """
        # covered in step 3

    def test_005_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have 'Live Score' available
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * 'Live Scores' are NOT displayed
        """
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        event = events.get(self.event_name)
        self.softAssert(self.assertTrue, event,
                        msg=f'Event {self.event_name} was not found in the list of events {list(events.keys())}')
        self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
        self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

    def test_006_repeat_steps_3_5_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(
            self):
        """
        DESCRIPTION: Repeat steps №3-5 for:
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
            self.softAssert(self.assertTrue, score_event,
                            msg=f'Event "{self.live_event_name}" not found for "In-Play tab"')
            home_score_actual = score_event.score_table.match_score.home_score
            self.assertEqual(home_score_actual, self.home_game_score,
                             msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.home_game_score}"')
            away_score_actual = score_event.score_table.match_score.away_score
            self.assertEqual(away_score_actual, self.away_game_score,
                             msg=f'Away score "{away_score_actual}"  is not the same as in response: "{self.away_game_score}"')
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
            inplay_handball_tab = inplay_sports.get(self.sport_name)
            self.assertTrue(inplay_handball_tab, msg=f'"{self.sport_name}" tab not found')
            inplay_handball_tab.click()
            self.assertTrue(inplay_handball_tab.is_selected(),
                            msg=f'"{self.sport_name}" tab is not selected')
            leagues = self.site.home.get_module_content(
                module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.softAssert(self.assertTrue, self.section,
                            msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found in "{leagues.keys()}"')
            self.test_003_verify_handball_event_with_scores_available(section=True)
            self.test_005_verify_event_which_doesnt_have_live_score_available()
            # 'In-Play' page -> 'Watch Live' tab
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state('in-play')
        if self.device_type != 'mobile':
            league_name_watch_live = []
            league_name_watch_live = self.league_name_watch_live.split('-')
            self.__class__.league_name_watch_live = league_name_watch_live[0] + '-' + league_name_watch_live[1]
        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_watch_live,
                                        watch_live_page=True)
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        score_event = events.get(self.live_event_name)
        home_score_actual = score_event.score_table.match_score.home_score
        self.assertEqual(home_score_actual, self.home_game_score,
                         msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.home_game_score}"')
        away_score_actual = score_event.score_table.match_score.away_score
        self.assertEqual(away_score_actual, self.away_game_score,
                         msg=f'Away score "{away_score_actual}"  is not the same as in response: "{self.away_game_score}"')
        # Sports Landing page -> 'In-Play' tab
        if self.device_type == 'desktop':
            self.navigate_to_page(name='sport/handball')
            self.site.wait_content_state('Handball')
            self.site.sports_page.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
            self.site.wait_content_state('Handball')
            events = self.get_inplay_events(league_name=self.league_name_in_play_tab_slp, watch_live_page=False)
            self.assertTrue(events, msg='There is no Events on the page')
            self.softAssert(self.assertTrue, self.live_event_name in events,
                            msg=f'Event {self.live_event_name} was not found in the list of events {events.keys()}')
            score_event = events.get(self.live_event_name)
            home_score_actual = score_event.score_table.match_score.home_score
            self.assertEqual(home_score_actual, self.home_game_score,
                             msg=f'Home score "{home_score_actual}" is not the same as in response:'
                                 f' "{self.home_game_score}"')
            away_score_actual = score_event.score_table.match_score.away_score
            self.assertEqual(away_score_actual, self.away_game_score,
                             msg=f'Away score "{away_score_actual}" is not the same as in response:"{self.away_game_score}"')
            event = events.get(self.event_name)
            self.softAssert(self.assertTrue, event,
                            msg=f'Event "{self.event_name}" was not found in the list of events "{events.keys()}"')
            self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
            self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')
        # Sports Landing page -> 'In-Play' module **Mobile**
        if self.device_type != 'desktop':
            self.navigate_to_page(name='sport/handball')
            self.site.wait_content_state(state_name='Handball')
            if self.device_type == 'mobile':
                self.softAssert(self.assertTrue, self.site.sports_page.tab_content.has_inplay_module(),
                                msg='In Play module is not enabled for Handball landing page')
                inplay_section = self.site.sports_page.tab_content.in_play_module.items_as_ordered_dict
            else:
                self.site.sports_page.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
                active_tab = self.site.sports_page.tabs_menu.current
                self.assertEqual(active_tab, vec.inplay.BY_IN_PLAY.upper(),
                                 msg=f'In-Play tab is not active, active is "{active_tab}"')
                inplay_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(inplay_section, msg='In-Play module has no any sections')
            self.__class__.section = inplay_section.get(self.league_name_in_play_module_slp)
            self.assertTrue(self.section,
                            msg=f'"{self.league_name_in_play_module_slp}" not found in leagues: "{inplay_section.keys()}"')
            self.test_003_verify_handball_event_with_scores_available(slp=True)
            self.test_005_verify_event_which_doesnt_have_live_score_available()
        # 'In-Play & Live Stream ' section on Homepage **Desktop**
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')
            inplay_live_stream = self.site.home.desktop_modules.inplay_live_stream_module
            if self.brand == 'bma':
                handball = vec.sb.HANDBALL.upper()
            else:
                handball = vec.sb.HANDBALL
            inplay_live_stream.menu_carousel.items_as_ordered_dict.get(handball).click()
            in_play_tabs = inplay_live_stream.tabs_menu
            in_play_tabs.click_button(vec.sb.LIVE_STREAM.upper())
            self.assertEqual(in_play_tabs.current, vec.sb.LIVE_STREAM.upper(),
                             msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected. Actual "{in_play_tabs.current}"')
            leagues = self.site.home.get_module_content(
                module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.assertTrue(self.section, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
            self.scores_verification(score_type='game_score', team1_score=self.home_game_score,
                                     team2_score=self.away_game_score)

    def test_007_for_desktop_expected_results_are_to_be_updated_due_to_redesign_for_desktoprepeat_steps_3_5_on_handball_landing_page_for_in_play_widget(
            self):
        """
        DESCRIPTION: **For Desktop:** (expected results are to be updated due to redesign for desktop)
        DESCRIPTION: Repeat steps №3-5 on Handball Landing page for 'In-play' widget
        EXPECTED: * 'LIVE' label is shown below the team names
        EXPECTED: * Scores are displayed on the both sides of 'LIVE' label
        """
        if self.device_type == 'desktop':
            self.site.open_sport(name=self.sport_name)
            self.site.wait_content_state(state_name='Handball')
            self.site.handball.tabs_menu.click_button(vec.SB.TABS_NAME_MATCHES.upper())
            sections = self.site.sports_page.in_play_widget.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Tennis page')
            self.assertIn(self.widget_section_name, sections.keys(),
                          msg=f'{self.widget_section_name} not found in {sections.keys()}')
            self.__class__.section = sections.get(self.widget_section_name)
            events = self.section.content.items_as_ordered_dict
            self.assertTrue(events, msg='There is no Events on the page')
            event = events.get(self.live_event_name)
            self.softAssert(self.assertTrue, event,
                            msg=f'Event "{self.live_event_name}" was not found in the list of events {events.keys()}')
            event.scroll_to()
            home_score = event.in_play_card.left_score
            away_score = event.in_play_card.right_score
            self.assertEqual(self.home_game_score, home_score,
                             msg=f'Actual score value "{home_score}"'
                                 f' for Home team is not the same as expected "{self.home_game_score}"')
            self.assertEqual(self.away_game_score, away_score,
                             msg=f'Actual score value "{away_score}"'
                                 f' for Away team is not the same as expected "{self.away_game_score}"')
            live_icon = event.in_play_card.live_icon
            self.softAssert(self.assertTrue, live_icon,
                            msg=f'Live icon is not displayed')
            self.assertEqual(event.in_play_card.current_left_score_element_tn().location['y'],
                             event.in_play_card.current_right_score_element_tn().location['y'],
                             msg="home and away scores are not displayed on the same row")

    def test_008_for_desktoprepeat_steps_3_5_on_handball_landing_page_for_live_stream_widget_if_available(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps №3-5 on Handball Landing page for 'Live Stream' widget (if available)
        EXPECTED: * 'LIVE' label is shown in the same line as event class/type
        EXPECTED: * Scores are displayed in the same line as team names
        """
        if self.device_type == 'desktop':
            widgets = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle')
            if not widgets:
                widgets = self.cms_config.get_system_configuration_item('DesktopWidgetsToggle')
            widget_available = widgets.get('liveStream')
            if not widget_available:
                raise CmsClientException('"Live Stream" widget is not configured in CMS')
            self.site.login()
            self.navigate_to_page(name='sport/handball')
            self.site.wait_content_state(state_name='Handball')
            sleep(1)
            event = self.site.sports_page.live_stream_widget
            self.softAssert(self.assertTrue, self.live_event_name in event.name,
                            msg=f'Event "{self.live_event_name}" was not found')
            home_score = event.left_score
            away_score = event.right_score
            self.assertEqual(self.home_game_score, home_score,
                             msg=f'Actual score value "{home_score}"'
                                 f' for Home team is not the same as expected "{self.home_game_score}"')
            self.assertEqual(self.away_game_score, away_score,
                             msg=f'Actual score value "{away_score}"'
                                 f' for Away team is not the same as expected "{self.away_game_score}"')
            sleep(1)
            self.assertEqual(event.event_name().location['y'], event.match_score_element().location['y'])
            self.site.logout()
