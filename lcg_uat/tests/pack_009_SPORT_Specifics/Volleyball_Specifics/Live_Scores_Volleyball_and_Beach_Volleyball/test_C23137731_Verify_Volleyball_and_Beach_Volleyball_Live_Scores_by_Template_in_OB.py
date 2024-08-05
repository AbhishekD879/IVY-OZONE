from time import sleep

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure
from voltron.utils.helpers import wait_for_category_in_inplay_sports_ribbon_home_page
from voltron.utils.helpers import wait_for_category_in_inplay_structure


@pytest.mark.lad_tst2  # VOL-5713 + coral mark?
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod # Cannot have access to prod OB
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.in_play
@pytest.mark.volleyball
@pytest.mark.beach_volleyball
@pytest.mark.live_scores
@vtest
class Test_C23137731_Verify_Volleyball_and_Beach_Volleyball_Live_Scores_by_Template_in_OB(BaseFallbackScoreboardTest):
    """
    TR_ID: C23137731
    NAME: Verify Volleyball and Beach Volleyball Live Scores by Template in OB
    DESCRIPTION: This test case verifies that Live Scores for Volleyball and Beach Volleyball are shown and updated through OB name template
    PRECONDITIONS: 1) In order to have a Scores Tennis event should be BIP event
    PRECONDITIONS: 2) In order to get events with Scorers use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attribute 'scoreboard':
    PRECONDITIONS: Verify score value for **'ALL'** (value for sets), **'CURRENT'** (value for games) and **'SUBPERIOD'** (value for points)
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: Create event in OB:
    PRECONDITIONS: Event name template:
    PRECONDITIONS: **|Team/Player A*| (x1) x2-y1 (y2) |Team/Player B|  , where x1,y1 - set scores, x2,y2 - points scores
    PRECONDITIONS: e.g. |Player1 Test*| (1) 15-30 (1) |Player2 Test|
    PRECONDITIONS: - '*' near player name is responsible for serving (identifies who passes the ball)
    PRECONDITIONS: - To check that scores are updated just edit the value of the score in event name
    PRECONDITIONS: - to check that serving is changed just set '*' near another player name. '*' can be set before or after player name
    PRECONDITIONS: See templates here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Testing+Fallback
    """
    keep_browser_open = True
    score = {'current': '1-3', 'set': '(2):(0)'}
    volleyball_sport_number, sport_event_count, in_play_event_count = None, None, None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.is_mobile and tests.settings.cms_env != 'prd0':
            cms_config = cls.get_cms_config()
            if cls.in_play_event_count is not None:
                cms_config.update_inplay_event_count(event_count=cls.in_play_event_count)
            if cls.volleyball_sport_number is not None and cls.sport_event_count is not None:
                cms_config.update_inplay_sport_event_count(sport_number=cls.volleyball_sport_number,
                                                           event_count=cls.sport_event_count)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create live event with scores
        EXPECTED: Event is successfully created
        """
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.volleyball_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.volleyball_config.category_id)
        self.check_sport_presence_on_inplay(sport_name='/volleyball')
        event_params = self.ob_config.add_volleyball_event_to_austrian_league(score=self.score, is_live=True,
                                                                              perform_stream=True)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.event_id = event_params.event_id
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False

        event = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id, query_builder=self.ss_query_builder)
        sport_name_raw = self.get_sport_name_for_event(event=event[0])
        self.__class__.sport_name = sport_name_raw.title() if self.brand == 'ladbrokes' else sport_name_raw.upper()

        self.__class__.league_name_watch_live = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                          in_play_page_watch_live=True)\
            .replace('Avl', 'AVL')
        self.__class__.league_name_in_play_sport_tab = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                 in_play_page_sport_tab=True)
        self.__class__.league_name_in_play_live_stream_homepage = self.get_accordion_name_for_event_from_ss(
            event=event[0],
            in_play_tab_home_page=True)
        self.__class__.league_name_in_play_module_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                  in_play_module_slp=True)
        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                               in_play_tab_slp=True)

    def test_001_load_oxygen_application_verify_that_scores_and_serving_are_showing_and_updating_on_pages_where_scores_are_available(self):
        """
        DESCRIPTION: Load Oxygen application
        DESCRIPTION: Verify that scores and serving are SHOWING and UPDATING on pages where scores are available:
        EXPECTED: Application is loaded
        """
        self.site.wait_content_state(state_name='Homepage', timeout=15)

    def test_002_verify_scores_on_watch_live_and_volleyball_pages_from_inplay_page(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **Volleyball** pages
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **Volleyball** pages
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=vec.sb.WATCH_LIVE_LABEL)

        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.volleyball.category_id)

        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_watch_live)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_watch_live}" league')
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.new_away_score,
                                    points_score=True)
        self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id,
                                                  score_type='CURRENT')
        self.verify_event_score_template(events=events,
                                         expected_player1_points=self.new_home_score,
                                         expected_player2_points=self.new_away_score,
                                         serving_ball=True)
        inplay_sport_menu = self.site.inplay.inplay_sport_menu
        inplay_sport_menu.click_item(self.sport_name)
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=self.sport_name)
        events = self.get_inplay_events(sport_name=self.sport_name, league_name=self.league_name_in_play_sport_tab,
                                        watch_live_page=False)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_sport_tab}" league')
        self.__class__.new_home_score = '8'
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.new_away_score,
                                    points_score=True)
        self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id,
                                                  score_type='CURRENT')
        self.verify_event_score_template(events=events,
                                         expected_player1_points=self.new_home_score,
                                         expected_player2_points=self.new_away_score,
                                         serving_ball=True)

    def test_003_verify_scores_on_home_page_featured_tab_inplay_module(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'Featured' tab** :
        DESCRIPTION: Verify that scores for the event on :
        DESCRIPTION: In-play module
        DESCRIPTION: Highlight carousel
        DESCRIPTION: Featured module (created by Type_id/Event_id)
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        if self.is_mobile:
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')

            resp = get_in_play_module_from_ws()
            self.softAssert(self.assertTrue, resp, msg='Inplay module is not configured for Homepage Featured tab')
            sports_name = [sport_segment.get('categoryName') for sport_segment in resp['data']]
            self.softAssert(self.assertIn, self.sport_name.title(), sports_name,
                            msg=f'"{self.sport_name.title()}" is not found in list of sports "{sports_name}" of In Play module')
            sport_number = sports_name.index(self.sport_name.title())
            self.__class__.volleyball_sport_number = sport_number + 1
            self.__class__.in_play_event_count = self.cms_config.get_inplay_event_count()
            self.__class__.sport_event_count = self.cms_config.get_sport_event_count(
                sport_number=self.volleyball_sport_number)
            initial_number_of_events = self.cms_config.get_max_number_of_inplay_event(
                sport_category=self.ob_config.backend.ti.volleyball.category_id)
            sport_event_count = initial_number_of_events + 30
            inplay_event_count = initial_number_of_events + 90
            self.cms_config.update_inplay_event_count(event_count=inplay_event_count)
            self.cms_config.update_inplay_sport_event_count(sport_number=self.volleyball_sport_number,
                                                            event_count=sport_event_count)
            sleep(30)  # to avoid delays in CMS
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Homepage', timeout=15)
            in_play_module = self.site.home.tab_content.in_play_module
            self.assertTrue(in_play_module, msg='Inplay module is not found on homepage featured tab')
            in_play_module_items = in_play_module.items_as_ordered_dict
            self.assertTrue(in_play_module_items, msg='No sports found on Inplay module')
            sport_section = in_play_module_items.get(vec.siteserve.VOLLEYBALL_ACCORDION)
            self.assertTrue(sport_section, msg=f'"{self.sport_name}" sport section not found')
            events = sport_section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events were found under {self.sport_name.upper()} section')
            self.__class__.new_home_score = '4'
            self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                        home_score=self.new_home_score, away_score=self.new_away_score,
                                        points_score=True)
            self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id,
                                                      delimiter='42/0,', score_type='CURRENT')
            self.verify_event_score_template(events=events,
                                             expected_player1_points_score=self.new_home_score,
                                             expected_player2_points_score=self.new_away_score,
                                             serving_ball=True)

    def test_004_verify_scores_on_in_play_and_live_stream_tabs(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'In Play'** tab
        DESCRIPTION: Home page > **'Live stream'** tab
        DESCRIPTION: **For Desktop**
        DESCRIPTION: Home page > **'In play and live stream'** module
        DESCRIPTION: Check 'In-play' tab and 'Live Stream' tabs
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        EXPECTED: NOTE: on **'Live stream'** tab updates come through the push in the event name
        """
        if self.is_mobile:
            in_play_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play,
                                                   raise_exceptions=False)
            self.softAssert(self.assertTrue, in_play_tab,
                            msg=f'Tab with internal id "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play}" '
                                f'is not configured')
            self.site.home.tabs_menu.click_button(in_play_tab)
            self.assertTrue(self.site.home.tabs_menu.items_as_ordered_dict.get(in_play_tab).is_selected(),
                            msg=f'"{in_play_tab}" tab is not selected')

            wait_for_category_in_inplay_structure(category_id=self.ob_config.backend.ti.volleyball.category_id)

            inplay_list_live = self.site.home.tab_content.live_now.items_as_ordered_dict
            self.assertTrue(inplay_list_live, msg=f'No sports found on homepage {in_play_tab} tab')
            sport_section = inplay_list_live.get(self.sport_name.upper())
            self.assertTrue(sport_section, msg=f'"{self.sport_name.upper()}" sport section not found')
            sport_section.expand()
            self.assertTrue(sport_section.is_expanded(),
                            msg=f'"{self.sport_name.upper()}" section is not expanded')
            if sport_section.has_show_more_leagues_button():
                sport_section.show_more_leagues_button.click()
            leagues = sport_section.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name.upper()}"')
            league = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.assertTrue(league, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
            events = league.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
            self.__class__.new_home_score = '7'
            self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                        home_score=self.new_home_score, away_score=self.new_away_score,
                                        points_score=True)
            self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id,
                                                      score_type='CURRENT')
            self.verify_event_score_template(events=events,
                                             expected_player1_points_score=self.new_home_score,
                                             expected_player2_points_score=self.new_away_score,
                                             serving_ball=True)

            live_stream_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream,
                                                       raise_exceptions=False)
            self.softAssert(self.assertTrue, live_stream_tab,
                            msg=f'Tab with internal id "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream}" '
                                f'is not configured')
            self.site.home.tabs_menu.click_button(live_stream_tab)
            self.assertTrue(self.site.home.tabs_menu.items_as_ordered_dict.get(live_stream_tab).is_selected(),
                            msg=f'"{live_stream_tab}" tab is not selected')
            live_stream_list = self.site.home.tab_content.live_now.items_as_ordered_dict
            self.assertTrue(live_stream_list, msg=f'No sports found on homepage {live_stream_tab} tab')
            sport_section = live_stream_list.get(self.sport_name.upper())
            self.assertTrue(sport_section, msg=f'"{self.sport_name.upper()}" sport section not found')
            sport_section.expand()
            self.assertTrue(sport_section.is_expanded(),
                            msg=f'"{self.sport_name.upper()}" section is not expanded')
            if sport_section.has_show_more_leagues_button():
                sport_section.show_more_leagues_button.click()
            leagues = sport_section.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name.upper()}"')
            league = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.assertTrue(league, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
            events = league.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
            self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id,
                                                      score_type='CURRENT')
            self.verify_event_score_template(events=events,
                                             expected_player1_points_score=self.new_home_score,
                                             expected_player2_points_score=self.new_away_score,
                                             serving_ball=True)
        else:
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')
            wait_for_category_in_inplay_sports_ribbon_home_page(category_id=self.ob_config.backend.ti.volleyball.category_id)

            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            sport = inplay_sports.get(self.sport_name)
            self.assertTrue(sport, msg=f'"{self.sport_name}" not found among "{inplay_sports.keys()}"')
            sport.click()
            self.assertTrue(inplay_sports.get(self.sport_name).is_selected(),
                            msg=f'"{self.sport_name}" tab is not selected')
            module_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME
            leagues = self.site.home.get_module_content(module_name=module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            if self.league_name_in_play_live_stream_homepage in leagues.keys():
                league = leagues.get(self.league_name_in_play_live_stream_homepage)
                events = league.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
                if self.event_name in list(events.keys()):
                    self.__class__.new_home_score = '7'
                    self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                                home_score=self.new_home_score, away_score=self.new_away_score,
                                                points_score=True)
                    self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home',
                                                              event_id=self.event_id, score_type='CURRENT')
                    self.verify_event_score_template(events=events,
                                                     expected_player1_points_score=self.new_home_score,
                                                     expected_player2_points_score=self.new_away_score,
                                                     serving_ball=True)
                else:
                    self._logger.info(
                        f'"{self.event_name}" is not displayed, due to hard coded limitation of 4 events')
            else:
                self._logger.info(f'"{self.league_name_in_play_live_stream_homepage}" is not displayed, due to hard coded limitation of 4 events')

            result = self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.click_button(button_name=vec.sb.LIVE_STREAM.upper())
            self.assertTrue(result,
                            msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected')
            leagues = self.site.home.get_module_content(module_name=module_name).accordions_list.items_as_ordered_dict
            if self.league_name_in_play_live_stream_homepage in leagues.keys():
                league = leagues.get(self.league_name_in_play_live_stream_homepage)
                events = league.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
                if self.event_name in list(events.keys()):
                    self.__class__.new_home_score = '3'
                    self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                                home_score=self.new_home_score, away_score=self.new_away_score,
                                                points_score=True)
                    self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id,
                                                              score_type='CURRENT')
                    self.verify_event_score_template(events=events,
                                                     expected_player1_points_score=self.new_home_score,
                                                     expected_player2_points_score=self.new_away_score,
                                                     serving_ball=True)
                else:
                    self._logger.info(
                        f'"{self.event_name}" is not displayed, due to hard coded limitation of 4 events')
            else:
                self._logger.info(f'"{self.league_name_in_play_live_stream_homepage}" is not displayed, due to hard coded limitation of 4 events')

    def test_005_go_to_volleyball_beach_volleyball_landing_page_in_play_tab(self):
        """
        DESCRIPTION: Go to **Volleyball/Beach Volleyball Landing page > 'In-Play'** tab/module
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        self.navigate_to_page(name='sport/volleyball')
        self.site.wait_content_state(state_name='Volleyball')
        delimiter = '42/36,' if self.is_mobile else '42'
        if self.is_mobile:
            resp = get_in_play_module_from_ws(delimiter=delimiter)
            self.softAssert(self.assertTrue, resp,
                            msg='In Play module is not configured for Volleyball Landing Page')
            self.softAssert(self.assertTrue, self.site.sports_page.tab_content.has_inplay_module(),
                            msg='In Play module is not enabled for Volleyball landing page')
            inplay_section = self.site.sports_page.tab_content.in_play_module.items_as_ordered_dict
            league_name = self.league_name_in_play_module_slp
        else:
            self.softAssert(self.assertTrue, self.site.sports_page.tab_content,
                            msg='In Play module is not enabled for Volleyball landing page')
            in_play_tab_name = self.expected_sport_tabs.in_play
            result = self.site.sports_page.tabs_menu.click_button(button_name=in_play_tab_name)
            self.assertTrue(result,
                            msg=f'"{in_play_tab_name}" tab is not selected')
            inplay_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            league_name = self.league_name_in_play_tab_slp
        self.assertTrue(inplay_section, msg='In Play section is not found')
        league = inplay_section.get(league_name)
        self.assertTrue(league, msg=f'"{league_name}" league not found')
        league.expand()
        events = league.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events were found for "{league_name}" league')
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.final_home_score, away_score=self.new_away_score,
                                    points_score=True)
        self.wait_for_score_update_from_inplay_ms(score=self.final_home_score, team='home', delimiter=delimiter,
                                                  event_id=self.event_id, score_type='CURRENT')
        self.verify_event_score_template(events=events,
                                         expected_player1_points_score=self.final_home_score,
                                         expected_player2_points_score=self.new_away_score,
                                         serving_ball=True)

    def test_006_navigate_to_edp_of_the_appropriate_event(self):
        """
        DESCRIPTION: Navigate to **EDP** of the appropriate event
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Score corresponds to the name in response from SiteServer
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        self.navigate_to_edp(event_id=self.event_id)
        title = self.site.sport_event_details.scoreboard_title_bar
        home_team = title.home_team_name
        away_team = title.away_team_name
        self.assertNotIn(self.final_home_score, home_team,
                         msg=f'Home Score is showed in the event name "{home_team}"')
        self.assertNotIn(self.new_away_score, away_team,
                         msg=f'Away Score is showed in the event name "{away_team}"')
        actual_event_name = title.event_name
        expected_event_name = f'{self.team1} {self.team2} S P {self.home_set_scores} {self.final_home_score} {self.away_set_scores} {self.new_away_score}'
        self.assertEqual(actual_event_name, expected_event_name,
                         msg=f'Actual event name "{actual_event_name}" with team names and scores are not same as expected "{expected_event_name}"')
        self.assertTrue(title.has_serving_ball_icon_home_team(),
                        msg='Serving ball icon is not shown')

    def test_007_for_desktop_sports_landing_page__in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Sports Landing page > 'In-Play' widget and 'Live Stream 'widget
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for a particular team is shown in the same row as the player's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home player is shown opposite the home player name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away player is shown opposite the away player name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: - Serving is shown as a dot near the player with '*' in the name
        """
        self._logger.warning('This is covered in scope of step 5')
