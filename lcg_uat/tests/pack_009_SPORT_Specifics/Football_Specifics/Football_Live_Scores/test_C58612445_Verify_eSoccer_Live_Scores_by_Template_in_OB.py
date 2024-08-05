import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure
from voltron.utils.helpers import wait_for_category_in_inplay_sports_ribbon_home_page
from voltron.utils.helpers import wait_for_category_in_inplay_structure


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create events in OB
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C58612445_Verify_eSoccer_Live_Scores_by_Template_in_OB(BaseFallbackScoreboardTest):
    """
    TR_ID: C58612445
    NAME: Verify eSoccer Live Scores by Template in OB
    DESCRIPTION: This test case verifies that Live Scores for eSoccer are shown and updated through OB name template
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Create events using OB for Football category in eSoccer class.
    PRECONDITIONS: Use the following event name templates:
    PRECONDITIONS: **|Team A| x-y |Team B|**
    PRECONDITIONS: **|Team A (Nickname1@!)| x-y |Team B (Nickname2@!) (Bo1)||(BG)|**
    PRECONDITIONS: **Team A (Nickname1@!) x-y Team B (Nickname2@!) (Bo1)(BG)**
    PRECONDITIONS: e.g. |Test Team 1| 0-0 |Test Team 2|
    PRECONDITIONS: See templates here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Testing+Fallback
    PRECONDITIONS: **RULES:**
    PRECONDITIONS: Added possibility to use brackets in team name to specify secondary name (SN) for Football and eSports: Liverpool (FEARGGWP), where FEARGGWP is secondary name.
    PRECONDITIONS: * There can be used as much SN as you want: Liverpool (lv-pl)(FEARGGWP) (second attempt).
    PRECONDITIONS: * SN can contain same characters as base team name: `' "&!@#$^|_;:.,?~/ and alphanumeric: Liverpool (lvpl777@com)
    PRECONDITIONS: * SN should NOT start from digit! Liverpool (123lvp)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To check scores are updated just edit the scores in event name: e.g. from 0-0 to 1-0
    PRECONDITIONS: To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: - Look at the attribute 'scoreboard':
    PRECONDITIONS: - Verify score value for **'ALL'**
    PRECONDITIONS: *   **value** - to see a score for particular participant
    PRECONDITIONS: *   **role_code**' - HOME/AWAY to see home and away team
    PRECONDITIONS: - Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: TST2: 'roleCode' - TEAM_1/TEAM_2
    PRECONDITIONS: PROD: 'roleCode' - HOME/AWAY
    PRECONDITIONS: ![](index.php?/attachments/get/104229685)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Verify that scores are shown and updated on pages where scores are available:
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create live event with scores
        EXPECTED: Event is successfully created
        """
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.football_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.football_config.category_id)

        self.check_sport_presence_on_inplay(sport_name='sport/football')
        event_params = self.ob_config.add_football_event_to_italy_serie_a(score=self.score, is_live=True,
                                                                          perform_stream=True)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.event_id = event_params.event_id
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        event = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id, query_builder=self.ss_query_builder)

        sport_name_raw = self.get_sport_name_for_event(event=event[0])
        self.__class__.sport_name = sport_name_raw.title() if self.brand == 'ladbrokes' else sport_name_raw.upper()
        category_code = event[0]['event']['categoryCode'].title().replace('_', ' ')
        self.__class__.competition_name = event[0]['event']['className'].replace(category_code, '', 1).lstrip()

        self.__class__.league_name_watch_live = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                          in_play_page_watch_live=True)
        self.__class__.league_name_in_play_sport_tab = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                 in_play_page_sport_tab=True)
        self.__class__.league_name_in_play_live_stream_homepage = self.get_accordion_name_for_event_from_ss(
            event=event[0],
            in_play_tab_home_page=True)
        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                               in_play_tab_slp=True)
        self.__class__.league_name_competitions_page = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                 competition_page=True)

    def test_001_for_mobiletablet_in_play_page_from_the_sports_menu_ribboncheck_on_watch_live_and_esoccer_pages_home_page__featured_tab__in_play_module_highlight_carousel_featured_module_created_by_type_idevent_id_home_page__in_play_tab_home_page__live_stream_tab_esoccer_landing_page__in_play_module(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: * **'In-Play'** page from the Sports Menu Ribbon
        DESCRIPTION: Check on **'Watch live'** and **eSoccer** pages
        DESCRIPTION: * Home page > **'Featured' tab** :
        DESCRIPTION: * In-play module
        DESCRIPTION: * Highlight carousel
        DESCRIPTION: * Featured module (created by Type_id/Event_id)
        DESCRIPTION: * Home page > **'In Play'** tab
        DESCRIPTION: * Home page > **'Live stream'** tab
        DESCRIPTION: * **eSoccer Landing page > 'In Play'** module
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: ![](index.php?/attachments/get/104231911)
        """
        self.site.wait_content_state(state_name='HomePage')
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state(state_name='in-play')
        sleep(2)
        self.site.inplay.inplay_sport_menu.items[1].click()
        self.site.wait_content_state(state_name='in-play')
        self.site.inplay.inplay_sport_menu.items[0].click()
        sleep(2)
        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.football.category_id)
        events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_watch_live)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_watch_live}" league')
        expected_scores = self.get_scores_from_initial_data(
            category_id=str(self.ob_config.backend.ti.football.category_id),
            event_id=self.event_id)
        if self.event_name not in events.keys():
            events = self.get_inplay_events(sport_name=self.sport_name.upper(), league_name=self.league_name_watch_live)
            self.assertTrue(events, msg=f'No events were found for "{self.league_name_watch_live}" league')
        self.verify_event_score_template(events=events, expected_home_score=expected_scores.get('home', ''),
                                         expected_away_score=expected_scores.get('away', ''))
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.new_away_score)
        sleep(3)
        self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
        self.verify_event_score_template(events=events, expected_home_score=self.new_home_score,
                                         expected_away_score=self.new_away_score)

        self.site.inplay.inplay_sport_menu.click_item(self.sport_name)
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=self.sport_name)
        events = self.get_inplay_events(sport_name=self.sport_name, league_name=self.league_name_in_play_sport_tab,
                                        watch_live_page=False)
        self.assertTrue(events, msg=f'No events were found for "{self.league_name_in_play_sport_tab}" league')
        self.__class__.new_home_score = '3'
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.new_away_score)
        sleep(3)
        self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
        self.verify_event_score_template(events=events,
                                         expected_home_score=self.new_home_score,
                                         expected_away_score=self.new_away_score)

    def test_002_for_desktop_in_play_page_from_the_main_navigation_menu_at_the_universal_headercheck_on_watch_live_and_esoccer_pages_home_page__in_play_and_live_stream_module_check_in_play_tab_and_live_stream_tabs_sports_landing_page__in_play_widget_and_live_stream_widget_esoccer_landing_page__in_play_tab(self):
        """
        DESCRIPTION: **For Desktop**
        DESCRIPTION: * **'In-Play'** page from the 'Main Navigation' menu at the 'Universal Header'
        DESCRIPTION: Check on **'Watch live'** and **eSoccer** pages
        DESCRIPTION: * Home page > **'In play and live stream'** module
        DESCRIPTION: * Check 'In-play' tab and 'Live Stream' tabs
        DESCRIPTION: * Sports Landing page > 'In-Play' widget and 'Live Stream 'widget
        DESCRIPTION: * **eSoccer Landing page > 'In Play'** tab
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Each score for particular team is shown in the same row as team's name near the Price/Odds button
        EXPECTED: - Score corresponds to the ** 'value'** attribute from WS
        EXPECTED: Score for the home team is shown opposite the home team name (roleCode="HOME"/"TEAM_1")
        EXPECTED: - Score for the away team is shown opposite the away team name (roleCode="AWAY"/"TEAM_2")
        EXPECTED: ![](index.php?/attachments/get/104231911)
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        self.__class__.new_home_score = '5'
        if self.is_mobile:
            in_play_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play,
                                                   raise_exceptions=False)
            self.site.home.tabs_menu.click_button(in_play_tab)
            self.assertTrue(self.site.home.tabs_menu.items_as_ordered_dict.get(in_play_tab).is_selected(),
                            msg=f'"{in_play_tab}" tab is not selected')

            wait_for_category_in_inplay_structure(category_id=self.ob_config.backend.ti.football.category_id)

            inplay_list_live = self.site.home.tab_content.live_now.items_as_ordered_dict
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
            self.assertTrue(events,
                            msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
            self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                        home_score=self.new_home_score, away_score=self.new_away_score)
            sleep(3)
            self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id)
            self.verify_event_score_template(events=events,
                                             expected_home_score=self.new_home_score,
                                             expected_away_score=self.new_away_score)

        else:
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')
            wait_for_category_in_inplay_sports_ribbon_home_page(
                category_id=self.ob_config.backend.ti.football.category_id)

            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            football = inplay_sports.get(vec.inplay.IN_PLAY_FOOTBALL)
            self.assertTrue(football, msg=f'"{vec.inplay.IN_PLAY_FOOTBALL}" not found among "{inplay_sports.keys()}"')
            football.click()
            self.assertTrue(inplay_sports.get(vec.inplay.IN_PLAY_FOOTBALL).is_selected(),
                            msg=f'"{vec.inplay.IN_PLAY_FOOTBALL}" tab is not selected')
            module_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME
            leagues = self.site.home.get_module_content(module_name=module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{vec.inplay.IN_PLAY_FOOTBALL}"')
            if self.league_name_in_play_live_stream_homepage in leagues.keys():
                league = leagues.get(self.league_name_in_play_live_stream_homepage)
                events = league.items_as_ordered_dict
                self.assertTrue(events,
                                msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
                if self.event_name in list(events.keys()):
                    self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                                home_score=self.new_home_score, away_score=self.new_away_score)
                    sleep(3)
                    self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home',
                                                              event_id=self.event_id)
                    self.verify_event_score_template(events=events,
                                                     expected_home_score=self.new_home_score,
                                                     expected_away_score=self.new_away_score)
            else:
                self._logger.warning(
                    f'*** "{self.league_name_in_play_live_stream_homepage}" is not displayed, due to hard coded limitation of 4 events')

            self.__class__.new_home_score = '6'
            result = self.site.home.desktop_modules.inplay_live_stream_module.tabs_menu.click_button(
                button_name=vec.sb.LIVE_STREAM.upper())
            self.assertTrue(result,
                            msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected')
            leagues = self.site.home.get_module_content(module_name=module_name).accordions_list.items_as_ordered_dict
            if self.league_name_in_play_live_stream_homepage in leagues.keys():
                league = leagues.get(self.league_name_in_play_live_stream_homepage)
                events = league.items_as_ordered_dict
                self.assertTrue(events,
                                msg=f'No events were found for "{self.league_name_in_play_live_stream_homepage}" league')
                if self.event_name in list(events.keys()):
                    self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                                home_score=self.new_home_score, away_score=self.new_away_score)
                    sleep(3)
                    self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home',
                                                              event_id=self.event_id)
                    self.verify_event_score_template(events=events, expected_home_score=self.new_home_score,
                                                     expected_away_score=self.new_away_score)
            else:
                self._logger.warning(
                    f'*** "{self.league_name_in_play_live_stream_homepage}" is not displayed, due to hard coded limitation of 4 events')

    def test_003_navigate_to_edp_of_the_appropriate_event(self):
        """
        DESCRIPTION: Navigate to **EDP** of the appropriate event
        EXPECTED: - Scores are NOT shown in the event name
        EXPECTED: - Team name and scores are shown in one line
        EXPECTED: - Score corresponds to the name in response from SiteServer
        EXPECTED: ![](index.php?/attachments/get/104231912)
        """
        self.navigate_to_edp(event_id=self.event_id)
        title = self.site.sport_event_details.scoreboard_title_bar
        self.assertNotIn(self.new_home_score, title.home_team_name,
                         msg=f'Home Score is showed in the event name "{title.home_team_name}"')
        self.assertNotIn(self.new_away_score, title.away_team_name,
                         msg=f'Away Score is showed in the event name "{title.away_team_name}"')
        actual_event_name = title.event_name
        expected_event_name = f'{self.team1} {self.new_home_score} {self.new_away_score} {self.team2}'
        self.assertEqual(actual_event_name, expected_event_name,
                         msg=f'Actual event name "{actual_event_name}" '
                             f'with team names and scores are not same as expected "{expected_event_name}"')
