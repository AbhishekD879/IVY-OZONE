import time

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure
from voltron.utils.helpers import wait_for_category_in_inplay_sports_ribbon_home_page
from voltron.utils.helpers import wait_for_category_in_inplay_structure
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot have access to prod OB
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.in_play
@pytest.mark.basketball
@pytest.mark.live_scores
@vtest
class Test_C23066013_Verify_Basketball_Live_Scores_by_Template_in_OB(BaseFallbackScoreboardTest):
    """
    TR_ID: C23066013
    NAME: Verify Basketball Live Scores by Template in OB
    DESCRIPTION: This test case verifies that Live Score for Basketball are shown and updated through OB name template
    PRECONDITIONS: To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attribute 'scoreboard':
    PRECONDITIONS: Verify score value for **'ALL'**
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: Create event in OB:
    PRECONDITIONS: Event name template:
    PRECONDITIONS: **|Team/Player A| x-y |Team/Player B|**
    PRECONDITIONS: e.g. |Test team1| 0-0 |Test Team2|
    PRECONDITIONS: To check scores are updated just edit the scores in event name: e.g. from 0-0 to 1-0
    PRECONDITIONS: See templates here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Testing+Fallback
    """
    keep_browser_open = True
    basketball_sport_number, sport_event_count, in_play_event_count = None, None, None
    is_us = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.is_mobile and tests.settings.cms_env != 'prd0':
            cms_config = cls.get_cms_config()
            if cls.in_play_event_count is not None:
                cms_config.update_inplay_event_count(event_count=cls.in_play_event_count)

            if cls.basketball_sport_number is not None and cls.sport_event_count is not None:
                cms_config.update_inplay_sport_event_count(sport_number=cls.basketball_sport_number,
                                                           event_count=cls.sport_event_count)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create live event with scores
        EXPECTED: Event is successfully created
        """
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.basketball_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.basketball_config.category_id)
        self.check_sport_presence_on_inplay(sport_name='basketball')

        event_params = self.ob_config.add_basketball_event_to_us_league(score=self.score, is_live=True,
                                                                        perform_stream=True)

        event = event_params.ss_response
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        if 'US' in event['event'].get('typeFlagCodes', ''):
            self.__class__.is_us = True
            self.__class__.event_name_competitions_tab = f'{event_params.team2} v {event_params.team1}'  # team names displayed reversed for US sports
        else:
            self.__class__.is_us = False
            self.__class__.event_name_competitions_tab = self.event_name
        self.__class__.event_id = event_params.event_id

        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        self.__class__.in_play_event_count = self.cms_config.get_inplay_event_count()

        sport_name_raw = self.get_sport_name_for_event(event=event)
        self.__class__.sport_name = sport_name_raw.title() if self.brand == 'ladbrokes' else sport_name_raw.upper()

        self.__class__.competition_name = event['event']['className'].lstrip()

        self.__class__.league_name_watch_live = self.get_accordion_name_for_event_from_ss(event=event,
                                                                                          in_play_page_watch_live=True)\
            .replace('Usa', 'USA').replace('Nba', 'NBA')
        self.__class__.league_name_in_play_sport_tab = self.get_accordion_name_for_event_from_ss(event=event,
                                                                                                 in_play_page_sport_tab=True)
        self.__class__.league_name_in_play_live_stream_homepage = self.get_accordion_name_for_event_from_ss(
            event=event,
            in_play_tab_home_page=True)
        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=event,
                                                                                               in_play_tab_slp=True)
        self.__class__.league_name_competitions_page = self.get_accordion_name_for_event_from_ss(event=event,
                                                                                                 competition_page=True)\
            .replace('Nba', 'NBA')

    def test_001_load_oxygen_application_verify_that_scores_are_shown_and_updated_on_pages_where_scores_are_available(
            self):
        """
        DESCRIPTION: Load Oxygen application
        DESCRIPTION: Verify that scores are shown and updated on pages where scores are available:
        EXPECTED: Application is loaded
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_scores_on_watch_live_and_basketball_pages_from_inplay_page(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **Basketball** pages
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **Basketball** pages
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: ![](index.php?/attachments/get/36797)
        """
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=vec.sb.WATCH_LIVE_LABEL)

        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.basketball.category_id)

        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_watch_live)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_watch_live}" league')
        expected_scores = self.get_scores_from_initial_data(category_id=str(self.ob_config.backend.ti.basketball.category_id),
                                                            event_id=self.event_id)
        self.verify_event_score_template(events=events, expected_home_score=expected_scores.get('home', ''),
                                         expected_away_score=expected_scores.get('away', ''))
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.new_away_score)
        self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
        self.verify_event_score_template(events=events, expected_home_score=self.new_home_score,
                                         expected_away_score=self.new_away_score)

        self.site.inplay.inplay_sport_menu.click_item(self.sport_name)
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=self.sport_name)
        events = self.get_inplay_events(league_name=self.league_name_in_play_sport_tab, watch_live_page=False)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_sport_tab}" league')
        self.__class__.new_home_score = '8'
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.new_away_score)
        self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
        self.verify_event_score_template(events=events,
                                         expected_home_score=self.new_home_score,
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
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
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
            self.__class__.basketball_sport_number = sport_number + 1
            self.__class__.in_play_event_count = self.cms_config.get_inplay_event_count()
            self.__class__.sport_event_count = self.cms_config.get_sport_event_count(
                sport_number=self.basketball_sport_number)
            initial_number_of_events = self.cms_config.get_max_number_of_inplay_event(
                sport_category=self.ob_config.backend.ti.basketball.category_id)
            sport_event_count = initial_number_of_events + 100
            inplay_event_count = initial_number_of_events + 200
            self.cms_config.update_inplay_event_count(event_count=inplay_event_count)
            self.cms_config.update_inplay_sport_event_count(sport_number=self.basketball_sport_number,
                                                            event_count=sport_event_count)
            time.sleep(30)  # to avoid delays in CMS
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
            self.assertTrue(events, msg=f'No events were found under "{sport_name}" section')
            self.__class__.new_home_score = '4'
            self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                        home_score=self.new_home_score, away_score=self.new_away_score)
            self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', delimiter='42/0,',
                                                      event_id=self.event_id)
            self.verify_event_score_template(events=events,
                                             expected_home_score=self.new_home_score,
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

            wait_for_category_in_inplay_structure(category_id=self.ob_config.backend.ti.basketball.category_id)
            inplay_list_live = self.site.home.tab_content.live_now.items_as_ordered_dict
            sport_section = inplay_list_live.get(vec.siteserve.BASKETBALL_TAB)
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
                                        home_score=self.new_home_score, away_score=self.new_away_score)
            self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
            self.verify_event_score_template(events=events,
                                             expected_home_score=self.new_home_score,
                                             expected_away_score=self.new_away_score)

            live_stream_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream,
                                                       raise_exceptions=False)
            self.softAssert(self.assertTrue, live_stream_tab,
                            msg=f'Tab with internal id "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream}" '
                                f'is not configured')
            self.site.home.tabs_menu.click_button(live_stream_tab)
            self.assertTrue(self.site.home.tabs_menu.items_as_ordered_dict.get(live_stream_tab).is_selected(),
                            msg=f'"{live_stream_tab}" tab is not selected')
            sections = self.site.home.get_module_content(module_name=live_stream_tab).live_now.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No sports sections found on {vec.sb.LIVE_STREAM.upper()} tab')
            section = sections.get(vec.siteserve.BASKETBALL_TAB)
            self.assertTrue(section, msg=f'"{self.sport_name}" section not found')
            section.expand()
            if section.has_show_more_leagues_button():
                section.show_more_leagues_button.click()
            leagues = section.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name.upper()}"')
            league = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.assertTrue(league, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
            events = league.items_as_ordered_dict
            self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
            self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
            self.verify_event_score_template(events=events,
                                             expected_home_score=self.new_home_score,
                                             expected_away_score=self.new_away_score)
        else:
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')
            wait_for_category_in_inplay_sports_ribbon_home_page(category_id=self.ob_config.backend.ti.basketball.category_id)

            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            self.assertTrue(inplay_sports, msg='In Play sports are not displayed on page')
            basketball = inplay_sports.get(self.sport_name)
            self.assertTrue(basketball, msg=f'"{self.sport_name}" not found among "{inplay_sports.keys()}"')
            basketball.click()
            self.assertTrue(inplay_sports.get(self.sport_name).is_selected(),
                            msg=f'"{self.sport_name}" tab is not selected')
            module_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME
            leagues = self.site.home.get_module_content(module_name=module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            if self.league_name_in_play_live_stream_homepage in leagues.keys():
                league = leagues.get(self.league_name_in_play_live_stream_homepage)
                self.assertTrue(league, msg=f'League "{self.league_name_in_play_live_stream_homepage}" not found among leagues "{leagues.keys()}"')
                events = league.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
                if self.event_name in list(events.keys()):
                    self.__class__.new_home_score = '4'
                    self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                                home_score=self.new_home_score, away_score=self.new_away_score)
                    self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
                    self.verify_event_score_template(events=events,
                                                     expected_home_score=self.new_home_score,
                                                     expected_away_score=self.new_away_score)
            else:
                self._logger.warning(f'*** "{self.league_name_in_play_live_stream_homepage}" is not displayed, due to hard coded limitation of 4 events')

            result = self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.click_button(button_name=vec.sb.LIVE_STREAM.upper())
            self.assertTrue(result,
                            msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected')
            leagues = self.site.home.get_module_content(module_name=module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            if self.league_name_in_play_live_stream_homepage in leagues.keys():
                league = leagues.get(self.league_name_in_play_live_stream_homepage)
                events = league.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
                if self.event_name in list(events.keys()):
                    self.__class__.new_home_score = '3'
                    self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                                home_score=self.new_home_score, away_score=self.new_away_score)
                    self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
                    self.verify_event_score_template(events=events, expected_home_score=self.new_home_score,
                                                     expected_away_score=self.new_away_score)
            else:
                self._logger.info(f'*** "{self.league_name_in_play_live_stream_homepage}" is not displayed, due to hard coded limitation of 4 events')

    def test_005_go_to_basketball_landing_page_in_play_tab(self):
        """
        DESCRIPTION: Go to **Basketball Landing page > 'In Play'** tab
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='Basketball')
        in_play_tab = self.get_ribbon_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                               raise_exceptions=False)
        self.softAssert(self.assertTrue, in_play_tab,
                        msg=f'Tab with internal id "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play}" '
                            f'is not configured')
        result = self.site.basketball.tabs_menu.click_button(button_name=in_play_tab)
        self.assertTrue(result,
                        msg=f'"{in_play_tab}" tab is not selected')
        inplay_section = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(inplay_section, msg='In Play section is not found')
        league = inplay_section.get(self.league_name_in_play_tab_slp)
        self.assertTrue(league, msg=f'"{self.league_name_in_play_tab_slp}" league not found')
        league.expand()
        events = league.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_tab_slp}" league')
        self.__class__.new_home_score = '5'
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.new_away_score)
        self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
        self.verify_event_score_template(events=events,
                                         expected_home_score=self.new_home_score,
                                         expected_away_score=self.new_away_score)

    def test_006_verify_scores_on_basketball_landing_page_competitions_tab(self):
        """
        DESCRIPTION: Navigate to **Basketball Landing page > Competitions** tab
        DESCRIPTION: Select appropriate Competition to  event where scores should be checked
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        """
        self.navigate_to_page(name='sport/basketball/competitions')
        self.site.wait_content_state(state_name=self.sport_name)
        self.assertTrue(self.site.sports_page.tabs_menu.items_as_ordered_dict.get(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()).is_selected(), msg=f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}" tab is not selected')
        competitions = self.site.basketball.tab_content.all_competitions_categories.items_as_ordered_dict \
            if self.device_type == 'mobile' else self.site.basketball.tab_content.accordions_list.items_as_ordered_dict

        self.assertTrue(competitions, msg='No competitions are present on page')
        if self.brand != 'ladbrokes':
            competition_name = self.competition_name.upper()
        else:
            competition_name = self.competition_name.upper() if self.is_mobile else self.competition_name.title().replace('Usa', 'USA').replace('Nba', 'NBA')
        self.assertIn(competition_name, competitions,
                      msg=f'"{competition_name}" is not present in competitions list "{competitions.keys()}"')
        competition = competitions[competition_name]
        self.assertTrue(competition, msg=f'"{competition_name}" is not found')
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=5)
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(self.league_name_competitions_page, leagues,
                      msg=f'League "{self.league_name_competitions_page}" is not present in list of leagues "{leagues.keys()}"'
                          f' in competition "{competition_name}"')
        league = leagues[self.league_name_competitions_page]
        self.assertTrue(league, msg=f'"{self.league_name_competitions_page}" league not found')
        league.click()
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections are present on page')
        today_tab = vec.sb.TABS_NAME_TODAY if self.is_mobile else vec.sb.TABS_NAME_TODAY.title()
        self.assertIn(today_tab, sections, msg=f'"{today_tab}" is not present in sections list "{sections.keys()}" ')
        events = sections[today_tab].items_as_ordered_dict
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_competitions_page}" league')
        if self.is_us:
            new_home_score, new_away_score = self.new_away_score, self.new_home_score  # scores and odds displayed reversed for US sports
        else:
            new_home_score, new_away_score = self.new_home_score, self.new_away_score
        self.verify_event_score_template(events=events,
                                         event_name=self.event_name_competitions_tab,
                                         expected_home_score=new_home_score,
                                         expected_away_score=new_away_score)

    def test_007_navigate_to_edp_of_the_appropriate_event(self):
        """
        DESCRIPTION: Navigate to **EDP** of the appropriate event
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name
        EXPECTED: - Score corresponds to the name in response from SiteServer
        EXPECTED: ![](index.php?/attachments/get/36796)
        """
        self.navigate_to_edp(event_id=self.event_id)
        event_details_page = self.site.sport_event_details
        self.assertTrue(event_details_page.has_event_scoreboard_bar().is_displayed(), msg='Event scoreboard bar is not present')
        home_team_name = event_details_page.scoreboard_title_bar.home_team_name
        self.assertNotIn(self.new_home_score, home_team_name, msg=f'Home Score is showed in the event name "{home_team_name}"')
        away_team_name = event_details_page.scoreboard_title_bar.away_team_name
        self.assertNotIn(self.new_away_score, away_team_name,
                         msg=f'Away Score is showed in the event name "{away_team_name}"')
        actual_event_name = event_details_page.scoreboard_title_bar.event_name.replace('\n', ' ')
        expected_event_name = f'{self.team1} {self.new_home_score} {self.new_away_score} {self.team2}'
        self.assertEqual(actual_event_name, expected_event_name,
                         msg=f'Actual event name "{actual_event_name}" with team names and scores are not same as expected "{expected_event_name}"')

    def test_008_for_desktop_sports_landing_page_in_play_widget_and_live_stream_widget(self):
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
