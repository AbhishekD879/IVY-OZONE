import json
import pytest
import voltron.environments.constants as vec

from json import JSONDecodeError
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt

from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.pages.shared import get_device
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.helpers import wait_for_category_in_inplay_ls_structure
from voltron.utils.helpers import wait_for_category_in_inplay_sports_ribbon_home_page
from voltron.utils.helpers import wait_for_category_in_inplay_structure


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't be run on prod/hl, specific event required
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@pytest.mark.football
@pytest.mark.desktop
@pytest.mark.slow
@vtest
class Test_C874381_Verify_Football_Scores_displaying_and_updating(BaseFallbackScoreboardTest, BaseFeaturedTest):
    """
    TR_ID: C874381
    NAME: Verify Football Scores displaying and updating
    DESCRIPTION: This test case verifies the Football Scores displaying and updating for BIP events
    DESCRIPTION: AUTOTEST [C50107450] - mobile - (just on tst2 endpoints)
    DESCRIPTION: AUTOTEST [C50107451] - desktop
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: * In order to have Football Scores, the event should be BIP. In OB system/TI make the following settings:
    PRECONDITIONS: * Set 'Bet in Play List': True in 'Flag' section on event level
    PRECONDITIONS: * Set the valid 'Start Time' for event
    PRECONDITIONS: * Set 'Is Off':'Yes' on the event level
    PRECONDITIONS: * Set 'Bet In Running':'Yes' on market level
    PRECONDITIONS: Links to OB system:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+OpenBet+System
    PRECONDITIONS: * [How to generate Live Scores for Football using Amelco][1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+generate+Live+Score+updates+on+Tennis+and+Football+sports
    PRECONDITIONS: * [How to generate Live Scores for Football using TI][2]
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/SPI/Testing+Fallback
    PRECONDITIONS: * [How to configure Fallback Scoreboard in CMS][3]
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Fallback+CMS+Configs
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To verify Football data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX", where XX - Category ID; XXX - Type ID
    PRECONDITIONS: Look at the attribute:
    PRECONDITIONS: *   **categoryCode** = "FOOTBALL"
    PRECONDITIONS: *   **score** : X,
    PRECONDITIONS: where X - score from main match time for particular team;
    PRECONDITIONS: *   **extraTimeScore** : X,
    PRECONDITIONS: where X - score from extra time period for particular team;
    PRECONDITIONS: *   **penaltyScore** : X,
    PRECONDITIONS: where X - score due to penalty for particular team;
    PRECONDITIONS: *   **role_code**='HOME'/'AWAY' - to determine HOME and AWAY teams
    PRECONDITIONS: *   **period_code**='FIRST_HALF/HALF_TIME/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF''** - to look at the scorers for the specific time
    PRECONDITIONS: *   **state**='R' - set in running state
    PRECONDITIONS: *   **state**='S' - set in stopped state
    PRECONDITIONS: ![](index.php?/attachments/get/6051048)
    PRECONDITIONS: 2) To verify new received data (updated scores) use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: 'SCBRD'
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **period_code**='FIRST_HALF/HALF_TIME/SECOND_HALF/EXTRA_TIME_FIRST_HALF/EXTRA_TIME_HALF_TIME/EXTRA_TIME_SECOND_HALF''** - to look at the scorers for the specific time
    PRECONDITIONS: *   **role_code**='HOME'/'AWAY' - to determine HOME and AWAY teams
    PRECONDITIONS: *   **value** - to see a score for particular team
    PRECONDITIONS: ![](index.php?/attachments/get/6051050)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Navigate to 'In-Play' page
    PRECONDITIONS: 3. Select the 'Football' tab
    """
    keep_browser_open = True
    scores_updated = False
    module_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME
    new_home_score = '5'
    new_away_score = '4'
    expected_home_score = None
    expected_away_score = None

    def ws_socres_verication(self, web_socket_id: str, delimiter: str = '42'):
        logs = get_device().get_performance_log()
        for entry in logs[::-1]:
            try:
                payload_data = entry[1]['message']['message']['params']['response']['payloadData']
                if payload_data.startswith(delimiter):
                    message = json.loads(payload_data.split(delimiter)[1])
                    if message[0] == web_socket_id:
                        if message[1]['type'] == 'SCBRD':
                            return message[1]['event']['scoreboard']['ALL']
            except (KeyError, IndexError, AttributeError, JSONDecodeError):
                continue

    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def scores_verification(self):
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        score_event = events.get(self.live_event_name)
        home_score_actual = score_event.score_table.match_score.home_score
        self.assertEqual(home_score_actual, self.expected_home_score,
                         msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.expected_home_score}"')
        away_score_actual = score_event.score_table.match_score.away_score
        self.assertEqual(away_score_actual, self.expected_away_score,
                         msg=f'Away score "{away_score_actual}"  is not the same as in response: "{self.expected_away_score}"')

    def create_events(self):
        self.check_fallback_scoreboard_is_configured_for_sport(category_id=self.ob_config.football_config.category_id)
        self.check_bip_score_is_configured_for_sport(category_id=self.ob_config.football_config.category_id)
        self.__class__.widget_section_name = 'In-Play LIVE Football'
        # Simple event
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self._logger.info(f'*** Create Football event "{self.event_name}"')

        # Score event
        live_event = self.ob_config.add_autotest_premier_league_football_event(is_live=True, score=self.score, perform_stream=True)
        self.__class__.team1 = live_event.team1
        self.__class__.team2 = live_event.team2
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=live_event.event_id, query_builder=self.ss_query_builder,
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
        self.__class__.sport_name = self.get_sport_title(category_id=self.ob_config.football_config.category_id).upper()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load the application and navigate to 'In-Play' page > 'Football' tab
        EXPECTED: 'Football' tab on the 'In-Play' page is opened
        """
        if not self.scores_updated:
            self.create_events()
            self.__class__.expected_home_score = self.home_score_expected
            self.__class__.expected_away_score = self.away_score_expected
        else:
            self.__class__.expected_home_score = self.new_home_score
            self.__class__.expected_away_score = self.new_away_score

        self.check_sport_presence_on_inplay(sport_name='/football')
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')
        self.site.inplay.inplay_sport_menu.click_item(vec.siteserve.FOOTBALL_TAB)
        self.site.wait_content_state(state_name='InPlay')
        self.__class__.sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found')

    def test_001_verify_scores_displaying_for_the_event_which_has_scores_available(self):
        """
        DESCRIPTION: Verify scores displaying for the event which has Scores available
        EXPECTED: * Match score is shown
        EXPECTED: * Each score for a particular team is shown near team name
        """
        section_name = self.league_name_in_play_sport_tab
        self.__class__.section = self.sections.get(section_name)
        self.assertTrue(self.section, msg=f'"{section_name}" section not found on page')
        if not self.section.is_expanded():
            self.section.expand()
            self.assertTrue(self.section.is_expanded(), msg=f'"{section_name}" section is not expanded')
        self.scores_verification()

    def test_002__trigger_updating_of_scores_verify_reflection_of_updated_scores_on_the_page(self):
        """
        DESCRIPTION: * Trigger updating of Scores.
        DESCRIPTION: * Verify reflection of updated Scores on the page.
        EXPECTED: * New Score replace the old one
        EXPECTED: * New Score is received in 'SCBRD' response in WS
        """
        # this step will be done in step9

    def test_003_verify_event_which_doesnt_have_scores_available(self):
        """
        DESCRIPTION: Verify event which doesn't have Scores available
        EXPECTED: * Only 'LIVE' label is shown below the team name
        EXPECTED: * Scores are NOT displayed
        """
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        event = events.get(self.event_name)
        self.softAssert(self.assertTrue, event,
                        msg=f'Event {self.event_name} was not found in the list of events {list(events.keys())}')
        self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
        self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

    def test_004_repeat_steps_1_3_for__homepage___featured_tabsection_mobile__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-3 for:
        DESCRIPTION: - Homepage -> 'Featured' tab/section **Mobile**
        DESCRIPTION: - Homepage -> 'In-Play' tab
        DESCRIPTION: - Homepage -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play' page -> 'Watch Live' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' tab
        DESCRIPTION: - Sports Landing page -> 'In-Play' module **Mobile**
        DESCRIPTION: - 'In-Play & Live Stream ' section on Homepage **Desktop**
        EXPECTED:
        """
        # Homepage -> 'In-Play' tab
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state('Homepage')
            wait_for_category_in_inplay_structure(category_id=self.ob_config.football_config.category_id)
            score_event = self.get_event_for_homepage_inplay_tab(
                event_name=self.live_event_name,
                sport_name=self.sport_name,
                league_name=self.league_name_in_play_live_stream_homepage,
                raise_exceptions=False)
            self.softAssert(self.assertTrue, score_event, msg=f'Event "{self.live_event_name}" not found for "In-Play tab"')
            home_score_actual = score_event.score_table.match_score.home_score
            self.assertEqual(home_score_actual, self.expected_home_score,
                             msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.expected_home_score}"')

            away_score_actual = score_event.score_table.match_score.away_score
            self.assertEqual(away_score_actual, self.expected_away_score,
                             msg=f'Away score "{away_score_actual}"  is not the same as in response: "{self.expected_away_score}"')

            event = self.get_event_for_homepage_inplay_tab(
                event_name=self.event_name,
                sport_name=self.sport_name,
                league_name=self.league_name_in_play_live_stream_homepage,
                raise_exceptions=False)
            self.softAssert(self.assertTrue, event, msg=f'Event "{self.event_name}" not found for "In-Play tab"')
            self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
            self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')
        else:
            self.navigate_to_page(name='/')
            self.site.wait_content_state('Homepage')
            wait_for_category_in_inplay_sports_ribbon_home_page(category_id=self.ob_config.backend.ti.football.category_id)
            inplay_sports = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            inplay_football_tab = inplay_sports.get(vec.inplay.IN_PLAY_FOOTBALL)
            self.assertTrue(inplay_football_tab, msg=f'"{vec.inplay.IN_PLAY_FOOTBALL}" tab not found')
            inplay_football_tab.click()
            self.assertTrue(inplay_football_tab.is_selected(),
                            msg=f'"{vec.inplay.IN_PLAY_FOOTBALL}" tab is not selected')
            leagues = self.site.home.get_module_content(module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.softAssert(self.assertTrue, self.section,
                            msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found in "{leagues.keys()}"')
            self.scores_verification()
            self.test_003_verify_event_which_doesnt_have_scores_available()

        # Homepage -> 'In-Play' module **Mobile**
        if self.device_type == 'mobile':
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')
            resp = get_in_play_module_from_ws()
            self.softAssert(self.assertTrue, resp, msg='Inplay module is not configured for Homepage Featured tab')
            sports_name = [sport_segment.get('categoryName') for sport_segment in resp['data']]
            sport_number = sports_name.index(self.sport_name.title())
            self.__class__.sport_number = sport_number + 1
            self.__class__.in_play_event_count = self.cms_config.get_inplay_event_count()
            self.__class__.sport_event_count = self.cms_config.get_sport_event_count(
                sport_number=self.sport_number)
            initial_number_of_events = self.cms_config.get_max_number_of_inplay_event(
                sport_category=self.ob_config.backend.ti.football.category_id)
            sport_event_count = initial_number_of_events + 30
            inplay_event_count = initial_number_of_events + 90
            self.cms_config.update_inplay_event_count(event_count=inplay_event_count)
            self.cms_config.update_inplay_sport_event_count(sport_number=self.sport_number,
                                                            event_count=sport_event_count)

            sleep(10)  # to avoid delays in CMS
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Homepage', timeout=15)

            sections = self.site.home.tab_content.in_play_module.items_as_ordered_dict
            ui_sport_name = self.sport_name.title() if not self.brand == 'ladbrokes' else self.sport_name
            self.assertIn(ui_sport_name, sections.keys(), msg=f'"{ui_sport_name}" container is not displayed')
            self.__class__.section = sections.get(ui_sport_name)
            self.assertTrue(self.section, msg=f'"{ui_sport_name}" not found in "{sections.keys()}"')
            self.scores_verification()
            self.test_003_verify_event_which_doesnt_have_scores_available()

        # 'In-Play' page -> 'Watch Live' tab
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state('in-play')
        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.football.category_id)

        events = self.get_inplay_events(sport_name=self.sport_name, league_name=self.league_name_watch_live, watch_live_page=True)
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event "{self.live_event_name}" was not found in the list of events "{events.keys()}"')
        score_event = events.get(self.live_event_name)
        home_score_actual = score_event.score_table.match_score.home_score
        self.assertEqual(home_score_actual, self.expected_home_score,
                         msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.expected_home_score}"')
        away_score_actual = score_event.score_table.match_score.away_score
        self.assertEqual(away_score_actual, self.expected_away_score,
                         msg=f'Away score "{away_score_actual}"  is not the same as in response: "{self.expected_away_score}"')

        # Sports Landing page -> 'In-Play' tab
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
        self.site.football.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
        self.site.wait_content_state('Football')

        wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.football.category_id)
        events = self.get_inplay_events(league_name=self.league_name_in_play_tab_slp, watch_live_page=False)
        self.assertTrue(events, msg='There is no Events on the page')
        self.softAssert(self.assertTrue, self.live_event_name in events,
                        msg=f'Event {self.live_event_name} was not found in the list of events {events.keys()}')
        score_event = events.get(self.live_event_name)
        home_score_actual = score_event.score_table.match_score.home_score
        self.assertEqual(home_score_actual, self.expected_home_score,
                         msg=f'Home score "{home_score_actual}" is not the same as in response: "{self.expected_home_score}"')
        away_score_actual = score_event.score_table.match_score.away_score
        self.assertEqual(away_score_actual, self.expected_away_score,
                         msg=f'Away score "{away_score_actual}" is not the same as in response: "{self.expected_away_score}"')
        event = events.get(self.event_name)
        self.softAssert(self.assertTrue, event,
                        msg=f'Event "{self.event_name}" was not found in the list of events "{events.keys()}"')
        self.assertTrue(event.is_live_now_event, msg='"LIVE" label is not shown on the screen')
        self.assertFalse(event.has_stream_icon(expected_result=False), msg='"Watch Live" icon is found')

        # Sports Landing page -> 'In-Play' module **Mobile**
        if self.device_type != 'desktop':
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name='Football')
            wait_for_category_in_inplay_ls_structure(category_id=self.ob_config.backend.ti.football.category_id)
            if self.device_type == 'mobile':
                self.softAssert(self.assertTrue, self.site.football.tab_content.has_inplay_module(),
                                msg='In Play module is not enabled for Cricket landing page')
                inplay_section = self.site.football.tab_content.in_play_module.items_as_ordered_dict
            else:
                self.site.football.tabs_menu.click_button(vec.inplay.BY_IN_PLAY.upper())
                active_tab = self.site.football.tabs_menu.current
                self.assertEqual(active_tab, vec.inplay.BY_IN_PLAY.upper(),
                                 msg=f'In-Play tab is not active, active is "{active_tab}"')
                inplay_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict

            self.assertTrue(inplay_section, msg='In-Play module has no any sections')
            self.__class__.section = inplay_section.get(self.league_name_in_play_module_slp)
            self.assertTrue(self.section, msg=f'"{self.league_name_in_play_module_slp}" not found in leagues: "{inplay_section.keys()}"')
            self.scores_verification()
            self.test_003_verify_event_which_doesnt_have_scores_available()

        # 'In-Play & Live Stream ' section on Homepage **Desktop**
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            self.site.wait_content_state(state_name='Homepage')
            inplay_live_stream = self.site.home.desktop_modules.inplay_live_stream_module
            if self.brand == 'bma':
                football = vec.sb.FOOTBALL.upper()
            else:
                football = vec.sb.FOOTBALL
            inplay_live_stream.menu_carousel.items_as_ordered_dict.get(football).click()
            in_play_tabs = inplay_live_stream.tabs_menu
            in_play_tabs.click_button(vec.sb.LIVE_STREAM.upper())

            self.assertEqual(in_play_tabs.current, vec.sb.LIVE_STREAM.upper(),
                             msg=f'"{vec.sb.LIVE_STREAM.upper()}" tab is not selected. Actual "{in_play_tabs.current}"')

            leagues = self.site.home.get_module_content(module_name=self.module_name).accordions_list.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name}"')
            self.__class__.section = leagues.get(self.league_name_in_play_live_stream_homepage)
            self.assertTrue(self.section, msg=f'"{self.league_name_in_play_live_stream_homepage}" league not found')
            self.scores_verification()

    def test_005_desktopnavigate_to_football_landing_page__matches_tab_and_verify_scorestimer_for_in_play_widget(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Football landing page > 'Matches' tab and verify scores/timer for 'In-play' widget
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' player respectively
        EXPECTED: * Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        if self.device_type == 'desktop':
            self.site.open_sport(name=self.sport_name)
            self.site.wait_content_state(state_name='Football')
            self.site.football.tabs_menu.click_button(vec.SB.TABS_NAME_MATCHES.upper())
            sections = self.site.football.in_play_widget.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Football page')
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
            self.assertEqual(self.expected_home_score, home_score,
                             msg=f'Actual score value "{home_score}"'
                             f' for Home team is not the same as expected "{self.expected_home_score}"')
            self.assertEqual(self.expected_away_score, away_score,
                             msg=f'Actual score value "{away_score}"'
                             f' for Away team is not the same as expected "{self.expected_away_score}"')

    def test_006_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps: 2-3
        """
        # Covered in step 5

    def test_007_desktopnavigate_to_football_landing_page__matches_tab_and_verify_scorestimer_for_live_stream_widget_if_available(self):
        """
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Navigate to Football landing page > 'Matches' tab and verify scores/timer for 'Live Stream' widget (if available)
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
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state(state_name='Football')
            event = self.site.football.live_stream_widget
            self.softAssert(self.assertTrue, self.live_event_name in event.name,
                            msg=f'Event "{self.live_event_name}" was not found')
            home_score = event.left_score
            away_score = event.right_score
            self.assertEqual(self.expected_home_score, home_score,
                             msg=f'Actual score value "{home_score}"'
                             f' for Home team is not the same as expected "{self.expected_home_score}"')
            self.assertEqual(self.expected_away_score, away_score,
                             msg=f'Actual score value "{away_score}"'
                             f' for Away team is not the same as expected "{self.expected_away_score}"')
            self.site.logout()

    def test_008_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps: 2-3
        """
        # Covered in step 7

    def test_009_repeat_steps_updated_scores(self):
        """
        DESCRIPTION: Repeat steps:
        """
        self.__class__.scores_updated = True
        self.ob_config.change_score(event_id=self.live_event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.new_away_score)
        self.test_000_preconditions()
        self.test_001_verify_scores_displaying_for_the_event_which_has_scores_available()
        ws_scores = self.ws_socres_verication(web_socket_id=self.live_event_id)
        self.assertEqual(ws_scores[0]['value'], self.expected_home_score,
                         msg=f'Home score "{ws_scores[0]["value"]}" is not the same as in response: "{self.expected_home_score}"')
        self.assertEqual(ws_scores[1]['value'], self.expected_away_score,
                         msg=f'Away score "{ws_scores[1]["value"]}"  is not the same as in response: "{self.expected_away_score}"')

        self.test_003_verify_event_which_doesnt_have_scores_available()
        self.test_004_repeat_steps_1_3_for__homepage___featured_tabsection_mobile__homepage___in_play_tab__homepage___in_play_module_mobile__in_play_page___watch_live_tab__sports_landing_page___in_play_tab__sports_landing_page___in_play_module_mobile__in_play__live_stream_section_on_homepage_desktop()
        self.test_005_desktopnavigate_to_football_landing_page__matches_tab_and_verify_scorestimer_for_in_play_widget()
        self.test_007_desktopnavigate_to_football_landing_page__matches_tab_and_verify_scorestimer_for_live_stream_widget_if_available()
