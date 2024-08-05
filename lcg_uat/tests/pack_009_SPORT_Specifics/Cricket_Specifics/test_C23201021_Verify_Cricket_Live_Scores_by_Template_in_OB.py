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


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot have access to prod OB
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.in_play
@pytest.mark.cricket
@pytest.mark.live_scores
@vtest
class Test_C23201021_Verify_Cricket_Live_Scores_by_Template_in_OB(BaseFallbackScoreboardTest):
    """
    TR_ID: C23201021
    NAME: Verify Cricket Live Scores by Template in OB
    DESCRIPTION: This test case verifies that Live Score for Cricket are shown and updated through OB name template
    PRECONDITIONS: To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attribute scoreboard:
    PRECONDITIONS: Verify score value for **'ALL'**
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: Create event in OB:
    PRECONDITIONS: Event name template can be different (integer and fractional):
    PRECONDITIONS: **|Team A| x1-y2|Team B|**
    PRECONDITIONS: **|Team A| x1 |Team B| y1/y2**
    PRECONDITIONS: **|Team A| x1/x2 |Team B| y1**
    PRECONDITIONS: **|Team A| x1/x2 |Team B| y1/y2**
    PRECONDITIONS: **|Team A| x1 |Team B| y1 y2/y3**
    PRECONDITIONS: **|Team A| x1 x2/x3 |Team B| y1**
    PRECONDITIONS: **|Team A| x1 x2/x3 |Team B| y1 y2/y3**
    PRECONDITIONS: e.g.
    PRECONDITIONS: **|Team A| 1-0|Team B|**
    PRECONDITIONS: **|Team A| 0 |Team B| 1/3**
    PRECONDITIONS: **|Team A| 1/2 |Team B| 2**
    PRECONDITIONS: **|Team A| 2/3 |Team B| 3/1**
    PRECONDITIONS: **|Team A| 1 |Team B| 1 3/1**
    PRECONDITIONS: **|Team A| 4 2/1 v |Team B| 1**
    PRECONDITIONS: **|Team A| 1 1/3 v |Team B| 1 3/1**
    PRECONDITIONS: **|Team A| 1 1/3 v |Team B 3rd T20| 1 3/1** (following event name is added after PROD incident https://jira.egalacoral.com/browse/BMA-48652)
    PRECONDITIONS: **|Team A 3rd T20| 1 1/3 v |Team B 3rd T20| 1 3/1** (following event name is added after PROD incident https://jira.egalacoral.com/browse/BMA-48652)
    PRECONDITIONS: To check scores are updated just edit the scores in event name
    PRECONDITIONS: See templates here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Testing+Fallback
    """
    keep_browser_open = True
    cricket_home_score = '5/3'
    cricket_sport_number, sport_event_count, in_play_event_count = None, None, None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.is_mobile and tests.settings.cms_env != 'prd0':
            cms_config = cls.get_cms_config()
            if cls.in_play_event_count is not None:
                cms_config.update_inplay_event_count(event_count=cls.in_play_event_count)
            if cls.cricket_sport_number is not None and cls.sport_event_count is not None:
                cms_config.update_inplay_sport_event_count(sport_number=cls.cricket_sport_number,
                                                           event_count=cls.sport_event_count)

    def get_accordion_name_for_event_from_ss(self, event: dict, **kwargs) -> str:
        """
        Gets league name from event response
        :param event - event response
        :param kwargs: in_play_tab_slp - In Play tab on SLP (Sport Landing Page,
        :param kwargs: in_play_tab_home_page - In Play tab on Homepage
        :param kwargs: live_stream_tab_homepage - Live Stream tab on Homepage
        :param kwargs: in_play_page_sport_tab - In Play page sport tab (e.g.: Football, Cricket, etc.)
        :param kwargs: in_play_page_watch_live - In Play page Watch Live tab
        :param kwargs: in_play_module_slp - In Play Module on SLP
        :param kwargs: in_play_module_homepage - In Play Module on Homepage Featured/Highlights tab
        :return: League name
        """
        in_play_tab_slp = kwargs.get('in_play_tab_slp')
        in_play_tab_home_page = kwargs.get('in_play_tab_home_page')
        live_stream_tab_homepage = kwargs.get('live_stream_tab_homepage')
        in_play_page_watch_live = kwargs.get('in_play_page_watch_live')
        in_play_page_sport_tab = kwargs.get('in_play_page_sport_tab')
        in_play_module_slp = kwargs.get('in_play_module_slp')
        in_play_module_homepage = kwargs.get('in_play_module_homepage')
        prematch = not any((in_play_tab_slp, in_play_tab_home_page, live_stream_tab_homepage, in_play_page_sport_tab,
                            in_play_page_watch_live, in_play_module_slp, in_play_module_homepage))
        type_name = event['event']['typeName']
        category_code = event['event']['categoryCode'].title().replace('_', ' ')
        class_name = event['event']['className'].replace(category_code, '', 1).lstrip()

        if prematch:
            league_name = f'{class_name.replace(category_code, "").lstrip().upper()} - {type_name.upper()}'
            return league_name

        if self.brand != 'ladbrokes':
            if self.device_type != 'desktop':
                if any((in_play_page_watch_live, in_play_tab_home_page, live_stream_tab_homepage, in_play_module_slp)):
                    league_name = type_name
                elif in_play_tab_slp or in_play_page_sport_tab:
                    league_name = type_name.upper()
                elif in_play_module_homepage:
                    league_name = category_code
                else:
                    league_name = type_name
            else:
                if any((in_play_page_watch_live,)):
                    league_name = type_name.upper()
                elif any((in_play_page_sport_tab, in_play_tab_home_page, in_play_tab_slp)):
                    league_name = f'{category_code} - {type_name}'.upper()
                else:
                    league_name = type_name
        else:
            if self.device_type != 'desktop':
                if any((in_play_page_watch_live, in_play_page_sport_tab, in_play_tab_home_page, live_stream_tab_homepage,
                        in_play_module_slp, in_play_tab_slp)):
                    league_name = type_name.upper()
                elif in_play_module_homepage:
                    league_name = category_code.upper()
                else:
                    league_name = type_name.upper()
            else:
                if any((in_play_page_watch_live, )):
                    league_name = type_name.title()
                elif any((in_play_tab_slp, in_play_page_sport_tab, in_play_tab_home_page, live_stream_tab_homepage)):
                    league_name = f'{category_code} - {type_name}'.upper()
                else:
                    league_name = type_name

        return league_name.strip()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create live event with scores
        EXPECTED: Event is successfully created
        """
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.cricket_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.cricket_config.category_id)
        self.check_sport_presence_on_inplay(sport_name='cricket')

        event_params = self.ob_config.add_autotest_cricket_event(is_live=True, perform_stream=True)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.event_id = event_params.event_id
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        event = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id, query_builder=self.ss_query_builder)
        sport_name_raw = self.get_sport_name_for_event(event=event[0])
        self.__class__.sport_name = sport_name_raw.title() if self.brand == 'ladbrokes' else sport_name_raw.upper()

        self.__class__.league_name_watch_live = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                          in_play_page_watch_live=True)
        self.__class__.league_name_in_play_sport_tab = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                 in_play_page_sport_tab=True)
        self.__class__.league_name_in_play_live_stream_homepage = self.get_accordion_name_for_event_from_ss(
            event=event[0],
            in_play_tab_home_page=True)
        self.__class__.league_name_in_play_module_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                  in_play_module_slp=True)
        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                               in_play_tab_slp=True)

    def test_001_load_oxygen_application_verify_that_scores_are_shown_and_updated_on_pages_where_scores_are_available(self):
        """
        DESCRIPTION: Load Oxygen application
        DESCRIPTION: Verify that scores are shown and updated on pages where scores are available:
        EXPECTED:  Application is loaded
        """
        self.site.wait_content_state(state_name='Homepage', timeout=25)

    def test_002_verify_scores_on_watch_live_and_cricket_pages_from_inplay_page(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **Cricket** pages
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **Cricket** pages
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        """
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=vec.sb.WATCH_LIVE_LABEL)

        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.cricket.category_id)

        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_watch_live)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_watch_live}" league')
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.cricket_home_score, away_score=self.new_away_score,
                                    cricket_score=True)
        self.wait_for_score_update_from_inplay_ms(score=self.cricket_home_score, team='home', event_id=self.event_id)
        self.verify_event_score_template(events=events,
                                         expected_home_score=self.cricket_home_score,
                                         expected_away_score=self.new_away_score)
        self.site.inplay.inplay_sport_menu.click_item(self.sport_name)
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=self.sport_name)
        events = self.get_inplay_events(sport_name=self.sport_name, league_name=self.league_name_in_play_sport_tab, watch_live_page=False)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_sport_tab}" league')
        self.__class__.cricket_home_score = '2/3'
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.cricket_home_score, away_score=self.new_away_score,
                                    cricket_score=True)
        self.wait_for_score_update_from_inplay_ms(score=self.cricket_home_score, team='home', event_id=self.event_id)
        self.verify_event_score_template(events=events,
                                         expected_home_score=self.cricket_home_score,
                                         expected_away_score=self.new_away_score)

    def test_003_verify_scores_on_home_page_featured_tab_inplay_module(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'Featured' tab** :
        DESCRIPTION: Verify that scores for the event on :
        DESCRIPTION: In-play module
        DESCRIPTION: Highlight carousel
        DESCRIPTION: Featured module (created by Type_id/Event_id)
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: - Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        """
        if self.is_mobile:
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')

            resp = get_in_play_module_from_ws()
            self.softAssert(self.assertTrue, resp, msg='In Play module is not configured for Homepage Featured tab')
            sports_name = [sport_segment.get('categoryName') for sport_segment in resp['data']]
            self.softAssert(self.assertIn, self.sport_name.title(), sports_name,
                            msg=f'"{self.sport_name.title()}" is not found in list of sports "{sports_name}" of In Play module')
            sport_number = sports_name.index(self.sport_name.title())
            self.__class__.cricket_sport_number = sport_number + 1
            self.__class__.in_play_event_count = self.cms_config.get_inplay_event_count()
            self.__class__.sport_event_count = self.cms_config.get_sport_event_count(
                sport_number=self.cricket_sport_number)
            initial_number_of_events = self.cms_config.get_max_number_of_inplay_event(
                sport_category=self.ob_config.backend.ti.cricket.category_id)
            sport_event_count = initial_number_of_events + 20
            inplay_event_count = initial_number_of_events + 90
            self.cms_config.update_inplay_event_count(event_count=inplay_event_count)
            self.cms_config.update_inplay_sport_event_count(sport_number=self.cricket_sport_number,
                                                            event_count=sport_event_count)
            sleep(30)  # to avoid delays in CMS
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Homepage', timeout=15)
            in_play_module = self.site.home.tab_content.in_play_module
            in_play_module_items = in_play_module.items_as_ordered_dict
            self.assertTrue(in_play_module_items, msg='No sports found on Inplay module')
            sport_name = self.sport_name.upper() if self.brand == 'ladbrokes' else self.sport_name.title()
            sport_section = in_play_module_items.get(sport_name)
            self.assertTrue(sport_section, msg=f'"{sport_name}" sport section not found')
            events = sport_section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events were found under {sport_name} section')
            self.__class__.cricket_home_score = '1/2'
            self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                        home_score=self.cricket_home_score, away_score=self.new_away_score,
                                        cricket_score=True)
            self.wait_for_score_update_from_inplay_ms(score=self.cricket_home_score, team='home',
                                                      event_id=self.event_id, delimiter='42/0,')
            self.verify_event_score_template(events=events,
                                             expected_home_score=self.cricket_home_score,
                                             expected_away_score=self.new_away_score)

    def test_004_verify_scores_on_in_play_and_live_stream_tab_module(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Home page > **'In Play'** tab
        DESCRIPTION: Home page > **'Live stream'** tab
        DESCRIPTION: **For Desktop**
        DESCRIPTION: Home page > **'In play and live stream'** module
        DESCRIPTION: Check 'In-play' tab and 'Live Stream' tabs
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: NOTE: on **'Live stream'** tab updates come through the push in the event name
        """
        if self.is_mobile:
            in_play_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play,
                                                   raise_exceptions=False)
            self.softAssert(self.assertTrue, in_play_tab,
                            msg=f'Tab with internal id "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play}" '
                                f'is not configured')
            self.site.home.tabs_menu.click_button(in_play_tab)
            self.assertTrue(self.site.home.tabs_menu.items_as_ordered_dict.get(in_play_tab).is_selected(timeout=3),
                            msg=f'"{in_play_tab}" tab is not selected')

            wait_for_category_in_inplay_structure(category_id=self.ob_config.backend.ti.cricket.category_id)

            inplay_list_live = self.site.home.tab_content.live_now.items_as_ordered_dict
            self.assertTrue(inplay_list_live, msg=f'No live events on In-play')
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
            self.__class__.cricket_home_score = '2/1'
            self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                        home_score=self.cricket_home_score, away_score=self.new_away_score,
                                        cricket_score=True)
            self.wait_for_score_update_from_inplay_ms(score=self.cricket_home_score,
                                                      team='home',
                                                      event_id=self.event_id)
            self.verify_event_score_template(events=events,
                                             expected_home_score=self.cricket_home_score,
                                             expected_away_score=self.new_away_score)

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
            self.assertTrue(league, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found among leagues "{leagues.keys()}"')
            events = league.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
            self.wait_for_score_update_from_inplay_ms(score=self.cricket_home_score,
                                                      team='home',
                                                      event_id=self.event_id)
            self.verify_event_score_template(events=events,
                                             expected_home_score=self.cricket_home_score,
                                             expected_away_score=self.new_away_score)
        else:
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')

            wait_for_category_in_inplay_sports_ribbon_home_page(category_id=self.ob_config.backend.ti.cricket.category_id)

            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            cricket = inplay_sports.get(self.sport_name)
            self.assertTrue(cricket, msg=f'"{self.sport_name}" not found among "{inplay_sports.keys()}"')
            cricket.click()
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
                    self.__class__.cricket_home_score = '4/3'
                    self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                                home_score=self.cricket_home_score, away_score=self.new_away_score,
                                                cricket_score=True)
                    self.wait_for_score_update_from_inplay_ms(score=self.cricket_home_score,
                                                              team='home',
                                                              event_id=self.event_id)
                    self.verify_event_score_template(events=events,
                                                     expected_home_score=self.cricket_home_score,
                                                     expected_away_score=self.new_away_score)

            result = self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.click_button(button_name=vec.sb.LIVE_STREAM.upper())
            self.assertTrue(result,
                            msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected')
            leagues = self.site.home.get_module_content(module_name=module_name).accordions_list.items_as_ordered_dict
            if self.league_name_in_play_live_stream_homepage in leagues.keys():
                league = leagues.get(self.league_name_in_play_live_stream_homepage)
                self.assertTrue(league, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
                events = league.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
                if self.event_name in list(events.keys()):
                    self.__class__.cricket_home_score = '4/1'
                    self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                                home_score=self.cricket_home_score, away_score=self.new_away_score,
                                                cricket_score=True)
                    self.wait_for_score_update_from_inplay_ms(score=self.cricket_home_score,
                                                              team='home',
                                                              event_id=self.event_id)
                    self.verify_event_score_template(events=events,
                                                     expected_home_score=self.cricket_home_score,
                                                     expected_away_score=self.new_away_score)
                else:
                    self._logger.info(
                        f'"{self.league_name_in_play_live_stream_homepage}" is not displayed, due to hard coded limitation of 4 events')

    def test_005_go_to_cricket_landing_page_in_play_tab(self):
        """
        DESCRIPTION: Go to **Cricket Landing page > 'In Play'** tab
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        """
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='Cricket')
        delimiter = '42/10,' if self.is_mobile else '42'
        if self.is_mobile:
            resp = get_in_play_module_from_ws(delimiter=delimiter)
            self.softAssert(self.assertTrue, resp,
                            msg='In Play module is not configured for Cricket Landing Page')
            self.softAssert(self.assertTrue, self.site.sports_page.tab_content.has_inplay_module(),
                            msg='In Play module is not shown on Cricket landing page')
            inplay_section = self.site.sports_page.tab_content.in_play_module.items_as_ordered_dict
            league_name = self.league_name_in_play_module_slp
        else:
            self.softAssert(self.assertTrue, self.site.sports_page.tab_content,
                            msg='In Play module is not enabled for Cricket landing page')
            in_play_tab_name = self.expected_sport_tabs.in_play
            result = self.site.cricket.tabs_menu.click_button(button_name=in_play_tab_name)
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
        self.__class__.cricket_home_score = '2/3'
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score='2/3', away_score=self.new_away_score,
                                    cricket_score=True)
        self.wait_for_score_update_from_inplay_ms(score=self.cricket_home_score, team='home',
                                                  event_id=self.event_id, delimiter=delimiter)
        self.verify_event_score_template(events=events,
                                         expected_home_score=self.cricket_home_score,
                                         expected_away_score=self.new_away_score)

    def test_006_navigate_to_edp_of_the_appropriate_event(self):
        """
        DESCRIPTION: Navigate to **EDP** of the appropriate event
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Team name and scores are shown in one line
        EXPECTED: - Score corresponds to the name in response from SiteServer
        EXPECTED: ![](index.php?/attachments/get/36816)
        """
        self.navigate_to_edp(event_id=self.event_id)
        title = self.site.sport_event_details.scoreboard_title_bar
        self.assertNotIn(self.cricket_home_score, title.home_team_name,
                         msg=f'Home Score is showed in the event name "{title.home_team_name}"')
        self.assertNotIn(self.new_away_score, title.away_team_name,
                         msg=f'Away Score is showed in the event name "{title.away_team_name}"')
        actual_event_name = title.event_name
        expected_event_name = f'{vec.siteserve.CRICKET_LEAGUE_NAME.title()} {self.team1} {self.team2} {self.cricket_home_score} ' \
                              f'{self.new_away_score}'
        self.assertEqual(actual_event_name, expected_event_name,
                         msg=f'Actual event name "{actual_event_name}" '
                             f'with team names and scores are not same as expected "{expected_event_name}"')

    def test_007_for_desktop_sports_landing_page__in_play_widget_and_live_stream_widget(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Sports Landing page > 'In-Play' widget and 'Live Stream 'widget
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        """
        self._logger.warning('This is covered in scope of step 5')
