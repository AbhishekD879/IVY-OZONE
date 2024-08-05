import re

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
import pytest
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import wait_for_category_in_inplay_structure, \
    wait_for_category_in_inplay_sports_ribbon_home_page, \
    wait_for_category_in_inplay_ls_structure


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.sanity
@vtest
class Test_C874382_Tennis_Scores_and_Sets(BaseFallbackScoreboardTest, BaseFeaturedTest, BaseSportTest):
    """
    TR_ID: C874382
    NAME: Tennis Scores and Sets
    DESCRIPTION: This test case verifies the Tennis Live Score of BIP events.
    PRECONDITIONS: 1) In order to have Tennis Scores, the event should be BIP
    PRECONDITIONS: 2) To verify Tennis data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX", where XX - Category ID; XXX - Type ID
    PRECONDITIONS: Look at the attribute:
    PRECONDITIONS: *   **categoryCode** = "TENNIS"
    PRECONDITIONS: *   **runningSetIndex** : X,
    PRECONDITIONS: where X - number of current active set
    PRECONDITIONS: *   **setsScore -> X** : Y and Z,
    PRECONDITIONS: where X - number of current active set;
    PRECONDITIONS: Y - score for participate 1;
    PRECONDITIONS: Z - score for participate 2;
    PRECONDITIONS: *   **role_code**='PLAYER_1'/'PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: *   **score** - to see a Game score for particular participant
    PRECONDITIONS: ![](index.php?/attachments/get/5998192)
    PRECONDITIONS: 3) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code**='GAME'and **periodIndex**='X' with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **periodCode**='SET', **periodIndex**='X' - to look at the scorers for the specific Set (where 'X' - set number)
    PRECONDITIONS: *   **role_code**='PLAYER_1'/'PLAYER_2' - to determine HOME and AWAY teams
    PRECONDITIONS: *   **value** - to see a Set score for particular participant
    PRECONDITIONS: ![](index.php?/attachments/get/5998209)
    PRECONDITIONS: 4) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: CLOCK
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code**='GAME'and **periodIndex**='X' with the highest value  - to look at the scorers for the full match
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: ![](index.php?/attachments/get/5998230)
    PRECONDITIONS: 5) [How to generate Live Scores for Tennis using Amelco][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: 6) [How to generate Live Scores for Tennis using TI][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: 7) [How to configure Fallback Scoreboard in CMS][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    """
    keep_browser_open = True
    module_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME
    score = {'current': '(1) 2 1-3 2 (1)'}
    home_score_expected = '1'
    away_score_expected = '3'
    home_set_scores = '1'
    away_set_scores = '1'
    home_game_score = '2'
    away_game_score = '2'

    def scores_verification(self, score_type=None, team1_score=None, team2_score=None, event=None):

        if event is None:
            events = self.section.items_as_ordered_dict
            self.assertTrue(events, msg='There is no Events on the page')
            self.softAssert(self.assertTrue, self.live_event_name in events,
                            msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
            score_event = events.get(self.live_event_name)
        else:
            score_event = event

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
            team1_score_actual = score_event.score_table.sets_score.home_score
            self.assertEqual(team1_score_actual, team1_expected_score,
                             msg=f'Home score "{team1_score_actual}" is not the same as in response: "{team1_expected_score}"')
            team2_score_actual = score_event.score_table.sets_score.away_score
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
            raise Exception("provided score type is not a valid score type for tennis")

    def create_events(self):
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.tennis_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.tennis_config.category_id)
        self.__class__.widget_section_name = 'In-Play LIVE Tennis'
        # Simple event
        event_params = self.ob_config.add_tennis_event_to_autotest_trophy(is_live=True)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self._logger.info(f'*** Create Tennies event "{self.event_name}"')

        # Score event
        start_time = self.get_date_time_formatted_string(days=-4)
        live_event = self.ob_config.add_tennis_event_to_autotest_trophy(start_time=start_time, is_live=True, score=self.score,
                                                                        perform_stream=True)
        self.__class__.team1 = live_event.team1
        self.__class__.team2 = live_event.team2
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=live_event.event_id,
                                                         query_builder=self.ss_query_builder,
                                                         raise_exceptions=False)
        if self.brand != 'bma':
            self.__class__.league_name_watch_live = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                              in_play_page_watch_live=True).replace('Auto Test - ', '')
        else:
            self.__class__.league_name_watch_live = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                              in_play_page_watch_live=True).replace('AUTO TEST - ', '')
        self.__class__.league_name_in_play_sport_tab = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                 in_play_page_sport_tab=True).replace('AUTO TEST - ', 'TENNIS - ')
        self.__class__.league_name_in_play_live_stream_homepage = self.get_accordion_name_for_event_from_ss(
            event=resp[0],
            in_play_tab_home_page=True).replace('AUTO TEST - ', 'TENNIS - ')
        self.__class__.league_name_in_play_module_slp = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                                  in_play_module_slp=True)
        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=resp[0],
                                                                                               in_play_tab_slp=True).replace('AUTO TEST - ', 'TENNIS - ')

        self.__class__.live_event_name = self.team1 + ' v ' + self.team2
        self.__class__.live_event_id = live_event.event_id
        self.__class__.sport_name = 'Tennis' if not self.brand == 'ladbrokes' else 'TENNIS'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Football' tab
        EXPECTED: 'Football' tab on the 'In-Play' page is opened
        """
        self.create_events()
        self.__class__.expected_home_score = self.home_score_expected
        self.__class__.expected_away_score = self.away_score_expected

    def test_001_load_the_application_and_navigate_to_in_play_page__tennis_tab(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Tennis' tab
        EXPECTED: 'Tennis' tab on the 'In-Play' page is opened
        """
        self.check_sport_presence_on_inplay(sport_name='/tennis')
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')
        self.site.inplay.inplay_sport_menu.click_item(vec.siteserve.TENNIS_TAB)
        self.site.wait_content_state(state_name='InPlay')

    def test_002_verify_tennis_event_with_scores_available(self, section=None):
        """
        DESCRIPTION: Verify Tennis event with Scores available
        EXPECTED: Game Score, Set Score and Set Number are displayed
        """
        self.site.wait_content_state_changed(timeout=20)
        if section is None:
            # self.__class__.sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            # self.assertTrue(self.sections, msg='No sections found')
            section_name = self.league_name_in_play_sport_tab
            self.__class__.section = self.get_section(section_name)
            self.assertTrue(self.section, msg=f'"{section_name}" section not found on page')
            if not self.section.is_expanded():
                self.section.expand()
                self.assertTrue(self.section.is_expanded(), msg=f'"section is not expanded')
        else:
            self.__class__.section = section
        self.scores_verification(score_type='game_score', team1_score=self.home_game_score,
                                 team2_score=self.away_game_score)

        self.scores_verification(score_type='sets_score', team1_score=self.home_set_scores,
                                 team2_score=self.away_set_scores)

        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        self.__class__.score_event = events.get(self.live_event_name)
        is_set_number_present = self.score_event.has_set_number()
        self.assertTrue(is_set_number_present, msg=f'Set number is not present')

    def test_003_verify_game_score_displaying(self):
        """
        DESCRIPTION: Verify Game Score displaying
        EXPECTED: *   Score for the home player is shown in front of home player name
        EXPECTED: *   Score for the away player is shown in front of away player name
        EXPECTED: *   Game score is displayed in grey (coral desktop)
        EXPECTED: *   Game score is displayed in black (coral mobile, ladbrokes mobile and desktop)
        """
        home_game_score_element = self.score_event.score_table.game_score.home_score_element()
        away_game_score_element = self.score_event.score_table.game_score.away_score_element()

        first_player = self.score_event.event_first_player()
        second_player = self.score_event.event_second_player()

        if home_game_score_element.location['y'] == first_player.location['y']:
            self.assertTrue(home_game_score_element.location['x'] > first_player.location['x'],
                            msg="position of the elements are not expected")
        if away_game_score_element.location['y'] == second_player.location['y']:
            self.assertTrue(away_game_score_element.location['x'] > second_player.location['x'],
                            msg="position of the elements are not expected")
        game_color_code = home_game_score_element.value_of_css_property('color')
        if self.brand == 'bma' and self.device_name == 'Desktop Chrome':
            self.assertEqual(game_color_code, vec.colors.GREY_COLOR,
                             msg="colors of game score not matching")
        else:
            self.assertEqual(game_color_code, vec.colors.BLACK_COLOR,
                             msg="colors of game score not matching")

    def test_004_verify_set_score_displaying(self):
        """
        DESCRIPTION: Verify Set Score displaying
        EXPECTED: *   Score for the home player is shown in front of home player name
        EXPECTED: *   Score for the away player is shown in front of away player name
        EXPECTED: *   Set score is displayed in grey (Coral desktop)
        EXPECTED: *   Set score is displayed in black (Coral mobile, ladbrokes mobile and desktop)
        EXPECTED: *   Set scores are displayed in columns for all finished sets
        """
        home_sets_score_element = self.score_event.score_table.sets_score.home_score_element()
        away_sets_score_score_element = self.score_event.score_table.sets_score.away_score_element()

        first_player = self.score_event.event_first_player()
        second_player = self.score_event.event_second_player()

        if home_sets_score_element.location['y'] == first_player.location['y']:
            self.assertTrue(home_sets_score_element.location['x'] > first_player.location['x'],
                            msg="position of the elements are not expected")
        if away_sets_score_score_element.location['y'] == second_player.location['y']:
            self.assertTrue(away_sets_score_score_element.location['x'] > second_player.location['x'],
                            msg="position of the elements are not expected")
        game_color_code = home_sets_score_element.value_of_css_property('color')
        if self.brand == 'bma' and self.device_name == 'Desktop Chrome':
            self.assertEqual(game_color_code, vec.colors.GREY_COLOR,
                             msg="colors of game score not matching")
        else:
            self.assertEqual(game_color_code, vec.colors.BLACK_COLOR,
                             msg="colors of game score not matching")

    def test_005_verify_set_number(self):
        """
        DESCRIPTION: Verify Set Number
        EXPECTED: Number of Set is shown in format:** '<set>1st/2nd/3th Set'**
        """
        set_number = self.score_event.set_number
        result = re.search("\d[a-z]+\s[S][e][t]", set_number)
        self.assertTrue(result, msg="Set number displayed in different format expression than expected")

    def test_006_verify_event_which_doesnt_have_live_score_available(self):
        """
        DESCRIPTION: Verify event which doesn't have LIVE Score available
        EXPECTED: Only 'LIVE' label is shown
        """
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        event = events.get(self.event_name)
        self.softAssert(self.assertTrue, event,
                        msg=f'Event {self.event_name} was not found in the list of events {list(events.keys())}')
        self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
        self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

    def test_007_repeat_steps_2_6_for__homepage___featured_tabsection__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(
            self):
        """
        DESCRIPTION: Repeat steps 2-6 for:
        DESCRIPTION: - Homepage -> 'Featured' tab/section
        DESCRIPTION: - Homepage -> 'In-Play' tab
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        """
        # Homepage -> 'In-Play' tab
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state('Homepage')
            wait_for_category_in_inplay_structure(category_id=self.ob_config.tennis_config.category_id)
            score_event = self.get_event_for_homepage_inplay_tab(
                event_name=self.live_event_name,
                sport_name=self.sport_name.upper(),
                league_name=self.league_name_in_play_live_stream_homepage,
                raise_exceptions=False)
            self.softAssert(self.assertTrue, score_event, msg=f'Event "{self.live_event_name}" not found for "In-Play tab"')

            self.scores_verification(score_type='game_score', team1_score=self.home_game_score,
                                     team2_score=self.away_game_score, event=score_event)

            self.scores_verification(score_type='sets_score', team1_score=self.home_set_scores,
                                     team2_score=self.away_set_scores, event=score_event)

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
            wait_for_category_in_inplay_sports_ribbon_home_page(
                category_id=self.ob_config.backend.ti.tennis.category_id)
            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            inplay_tennis_tab = inplay_sports.get(vec.inplay.IN_PLAY_TENNIS)
            self.assertTrue(inplay_tennis_tab, msg=f'"{vec.inplay.IN_PLAY_TENNIS}" tab not found')
            inplay_tennis_tab.click()
            self.assertTrue(inplay_tennis_tab.is_selected(),
                            msg=f'"{vec.inplay.IN_PLAY_TENNIS}" tab is not selected')

            leagues = self.site.home.get_module_content(
                module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.softAssert(self.assertTrue, self.section,
                            msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found in "{leagues.keys()}"')
            self.scores_verification(score_type='game_score', team1_score=self.home_game_score,
                                     team2_score=self.away_game_score)

            self.scores_verification(score_type='sets_score', team1_score=self.home_set_scores,
                                     team2_score=self.away_set_scores)
            self.test_006_verify_event_which_doesnt_have_live_score_available()

        # 'In-Play' page -> 'Watch Live' tab
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state('in-play')
        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.tennis.category_id)

        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_watch_live, watch_live_page=True)
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        score_event = events.get(self.live_event_name)

        self.scores_verification(score_type='game_score', team1_score=self.home_game_score,
                                 team2_score=self.away_game_score, event=score_event)

        self.scores_verification(score_type='sets_score', team1_score=self.home_set_scores,
                                 team2_score=self.away_set_scores, event=score_event)

        # Sports Landing page -> 'In-Play' tab
        if self.device_type == 'desktop':
            self.navigate_to_page(name='sport/tennis')
            self.site.wait_content_state('Tennis')
            self.site.tennis.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
            self.site.wait_content_state('Tennis')

            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.tennis.category_id)
            events = self.get_inplay_events(league_name=self.league_name_in_play_tab_slp, watch_live_page=False)
            self.assertTrue(events, msg='There is no Events on the page')
            self.softAssert(self.assertTrue, self.live_event_name in events,
                            msg=f'Event {self.live_event_name} was not found in the list of events {events.keys()}')
            score_event = events.get(self.live_event_name)
            self.scores_verification(score_type='game_score', team1_score=self.home_game_score,
                                     team2_score=self.away_game_score, event=score_event)

            self.scores_verification(score_type='sets_score', team1_score=self.home_set_scores,
                                     team2_score=self.away_set_scores, event=score_event)
            event = events.get(self.event_name)
            self.softAssert(self.assertTrue, event,
                            msg=f'Event "{self.event_name}" was not found in the list of events "{events.keys()}"')
            self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
            self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

        # Sports Landing page -> 'In-Play' module **Mobile**
        if self.device_type != 'desktop':
            self.navigate_to_page(name='sport/tennis')
            self.site.wait_content_state(state_name='Tennis')
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.tennis.category_id)
            self.softAssert(self.assertTrue, self.site.sports_page.tab_content.has_inplay_module(),
                            msg='In Play module is not enabled for Cricket landing page')
            inplay_section = self.site.sports_page.tab_content.in_play_module.items_as_ordered_dict
            self.assertTrue(inplay_section, msg='In-Play module has no any sections')
            self.__class__.section = inplay_section.get(self.league_name_in_play_module_slp)
            self.assertTrue(self.section, msg=f'"{self.league_name_in_play_module_slp}" not found in leagues: "{inplay_section.keys()}"')
            self.test_002_verify_tennis_event_with_scores_available(section=self.section)
            self.test_006_verify_event_which_doesnt_have_live_score_available()

        # 'In-Play & Live Stream ' section on Homepage **Desktop**
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')
            inplay_live_stream = self.site.home.desktop_modules.inplay_live_stream_module
            if self.brand == 'bma':
                tennis = vec.sb.TENNIS.upper()
            else:
                tennis = vec.sb.TENNIS
            inplay_live_stream.menu_carousel.items_as_ordered_dict.get(tennis).click()
            in_play_tabs = inplay_live_stream.tabs_menu
            in_play_tabs.click_button(vec.sb.LIVE_STREAM.upper())

            self.assertEqual(in_play_tabs.current, vec.sb.LIVE_STREAM.upper(),
                             msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected. Actual "{in_play_tabs.current}"')

            leagues = self.site.home.get_module_content(module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.assertTrue(self.section, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
            self.test_002_verify_tennis_event_with_scores_available(section=self.section)

            in_play_tabs.click_button(vec.sb.IN_PLAY.upper())
            leagues = self.site.home.get_module_content(
                module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            self.__class__.section = leagues.get(self.league_name_in_play_tab_slp)
            self.test_006_verify_event_which_doesnt_have_live_score_available()

    def test_008_desktopnavigate_to_tennis_landing_page__matches_tab_and_verify_scoresset_number_for_in_play_widget(
            self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Tennis landing page > 'Matches' tab and verify scores/set number for 'In-play' widget
        EXPECTED: * 'LIVE'/'Set Number' is displayed below the Event name
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        if self.device_type == 'desktop':
            self.site.open_sport(name=self.sport_name)
            self.site.wait_content_state(state_name='Tennis')
            self.site.tennis.tabs_menu.click_button(vec.SB.TABS_NAME_MATCHES.upper())
            sections = self.site.tennis.in_play_widget.items_as_ordered_dict
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
            home_score = event.in_play_card.current_left_score_tn
            away_score = event.in_play_card.current_right_score_tn
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

    def test_009_desktopnavigate_to_tennis_landing_page__matches_tab_and_verify_scoresset_number_for_live_stream_widget(
            self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Tennis landing page > 'Matches' tab and verify scores/set number for 'Live Stream' widget
        EXPECTED: * 'LIVE'/'Set Number' red badge is displayed next to event class/type
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
            self.navigate_to_page(name='sport/tennis')
            self.site.wait_content_state(state_name='Tennis')
            event = self.site.tennis.live_stream_widget
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
            self.assertEqual(event.event_name().location['y'], event.match_score_element().location['y'])

            self.site.logout()
