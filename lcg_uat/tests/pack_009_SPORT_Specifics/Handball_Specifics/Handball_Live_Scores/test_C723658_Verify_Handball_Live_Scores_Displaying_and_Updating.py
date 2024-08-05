import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_009_SPORT_Specifics.BaseFallbackScoreboardTest import BaseFallbackScoreboardTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.helpers import wait_for_category_in_inplay_module_from_ws, get_in_play_module_from_ws
from voltron.utils.helpers import wait_for_category_in_inplay_sports_ribbon
from voltron.utils.helpers import wait_for_category_in_inplay_structure
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot update scores for prod and hl
# @pytest.mark.hl
@pytest.mark.sports
@pytest.mark.handball
@pytest.mark.module_ribbon
@pytest.mark.liveserv_updates
@pytest.mark.in_play
@pytest.mark.featured
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.live_scores
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-54910')
@vtest
class Test_C723658_Verify_Handball_Live_Scores_Displaying_and_Updating(BaseBetSlipTest, BaseFeaturedTest, BaseFallbackScoreboardTest):
    """
    TR_ID: C723658
    NAME: Verify Handball Live Scores Displaying and Updating
    DESCRIPTION: This test case verifies live scores displaying when score was changed for HOME player.
    PRECONDITIONS: 1) In order to have a Scores Handball event should be BIP event
    PRECONDITIONS: 2) To verify new received data use Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: SCBRD
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *   **categoryCode** = "HANDBALL"
    PRECONDITIONS: *   **value** - to see update with score
    PRECONDITIONS: *   **role_code=HOME**  - to determine HOME team
    PRECONDITIONS: 3) Live Scores are received in event name from BetGenius or can be created manually in Openbet TI in next format:
    PRECONDITIONS: "|Team A Name|" ScoreA-ScoreB "|Team B Name|"
    """
    keep_browser_open = True
    home_score_expected = '25'
    away_score_expected = '18'
    new_home_score = '30'
    new_away_score = '20'
    sport_name = 'Handball'
    score = {'current': f'{home_score_expected}-{away_score_expected}'}
    widget_section_name = 'In-Play LIVE Handball'
    events_from_hours_delta = -5

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        number_of_events = cms_config.get_max_number_of_inplay_event(
            sport_category=cls.sport_category)
        if number_of_events != cls.initial_number_of_events:
            cms_config.update_inplay_event_count(
                sport_category=cls.sport_category, event_count=int(cls.initial_number_of_events))

    def get_featured_section(self, module_name):
        self.wait_for_featured_module(name=module_name)
        featured_modules = self.site.home.get_module_content(
            module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)) \
            .accordions_list.items_as_ordered_dict
        self.assertTrue(featured_modules, msg='*** No modules present on page')
        module_events_section = featured_modules[module_name]
        return module_events_section

    def test_000_preconditions(self):
        """
        DESCRIPTION: Go to OB and create Handball live event with name:
        DESCRIPTION: |Team A Name| ScoreA-ScoreB |Team B Name|
        EXPECTED: Event is successfully created
        """
        self.__class__.sport_category = self.ob_config.backend.ti.handball.category_id
        self.check_sport_configured(self.sport_category)
        event_params = self.ob_config.add_handball_event_to_croatian_premijer_liga(
            score=self.score, is_live=True, img_stream=True)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.event_id = event_params.event_id
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        self.__class__.initial_number_of_events = self.cms_config.get_max_number_of_inplay_event(
            sport_category=self.sport_category)
        self.cms_config.update_inplay_event_count(
            sport_category=self.sport_category, event_count=((int(self.initial_number_of_events)) + 10))

        event = self.ss_req.ss_event_to_outcome_for_event(event_id=event_params.event_id,
                                                          query_builder=self.ss_query_builder)

        self.__class__.league_name_in_play_module_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                  in_play_module_slp=True)
        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                               in_play_tab_slp=True)
        self.__class__.league_name_in_play_page_sport_tab = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                      in_play_page_sport_tab=True)
        self.__class__.league_name_in_play_tab_homepage = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                    in_play_tab_home_page=True)
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        self.__class__.delimiter = '42/20,' if self.is_mobile else '42'

    def test_001_open_handball_in_play_tab(self):
        """
        DESCRIPTION: Open 'Handball' -> 'In-Play' tab
        EXPECTED: 'In Play' tab is opened
        """
        self.navigate_to_page(name='sport/handball')
        self.site.wait_content_state(state_name=self.sport_name)
        if self.device_type == 'mobile':
            wait_for_category_in_inplay_module_from_ws(category_id=self.ob_config.backend.ti.handball.category_id,
                                                       delimiter=f'42/{self.ob_config.backend.ti.handball.category_id},')

            self.__class__.sections = self.site.handball.tab_content.in_play_module.items_as_ordered_dict
            self.__class__.league_name = self.league_name_in_play_module_slp
        else:
            modules = self.cms_config.get_initial_data().get('modularContent', [])
            modules_name = [module.get('id') for module in modules]
            self.softAssert(self.assertIn, self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play, modules_name,
                            msg=f'In-play tab isn\'t shown on Homepage')
            in_play_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play)
            self.site.handball.tabs_menu.click_button(in_play_tab)
            self.assertEqual(self.site.handball.tabs_menu.current, in_play_tab,
                             msg=f'"{in_play_tab}" tab is not active')
            self.__class__.league_name = self.league_name_in_play_tab_slp
            self.__class__.sections = self.site.handball.tab_content.accordions_list.items_as_ordered_dict

        self.assertTrue(self.sections, msg=f'No sections found on "In-Play" section')

    def test_002_verify_handball_event_with_score_available(self, section=None):
        """
        DESCRIPTION: Verify Handball event with score available
        EXPECTED: *  'LIVE' label is displayed
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   Set score is shown between price/odds buttons and event name
        EXPECTED: *   Set score is shown vertically
        EXPECTED: **For desktop:**
        EXPECTED: *   Set score is shown below event name
        EXPECTED: *   Set score is shown horizontally next to 'LIVE' label
        """
        self.__class__.section = section if section else self.sections.get(self.league_name)
        self.assertTrue(self.section,
                        msg=f'"{self.league_name}" section not found on "{self.sport_name}" page')

        if self.device_type != 'mobile':
            self.section.expand()
            self.assertTrue(self.section.is_expanded(), msg=f'"{self.league_name}" section is not expanded')

        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.league_name}"')
        event = events.get(self.event_name)
        self.assertTrue(event, msg=f'Event "{self.event_name}" is not found among events "{events.keys()}"')

        self.__class__.home_score_actual = event.score_table.match_score.home_score
        self.assertTrue(self.home_score_actual, msg=f'Home score is not shown for "{self.event_name}"')

        self.__class__.away_score_actual = event.score_table.match_score.away_score
        self.assertTrue(self.away_score_actual, msg=f'Away score is not shown for "{self.event_name}"')

        if self.device_type == 'mobile':
            is_live = event.is_live_now_event
            self.softAssert(self.assertTrue, is_live, msg='"LIVE" label is not shown on the screen')

    def test_003_verify_score_correctness_for_home_team(self):
        """
        DESCRIPTION: Verify score correctness for Home team
        EXPECTED: Score corresponds to the **events.[i].comments.teams.home.score'** attribute from the WS,
        EXPECTED: where [i] - number of event that contains particular class
        """
        self.softAssert(self.assertEqual, self.home_score_expected, self.home_score_actual,
                        msg=f'Actual score value: "{self.home_score_actual}"'
                        f' for Home team is not the same as expected: "{self.home_score_expected}"')

    def test_004_verify_score_correctness_for_away_team(self):
        """
        DESCRIPTION: Verify score correctness for Away team
        EXPECTED: Score corresponds to the **events.[i].comments.teams.home.score'** attribute from the WS,
        EXPECTED: where [i] - number of event that contains particular class
        """
        self.softAssert(self.assertEqual, self.away_score_expected, self.away_score_actual,
                        msg=f'Actual score value: "{self.away_score_actual}"'
                        f' for Away team is not the same as expected: "{self.away_score_expected}"')

    def test_005_trigger_the_following_situation_the_score_is_changed_for_home_team(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: the score is changed for HOME team
        EXPECTED: * Score immediately starts displaying new value for Home player
        EXPECTED: * Update is received in WS and corresponds to **event.scoreboard.ALL.value** where **role_code=HOME**
        """
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.new_home_score, away_score=self.away_score_expected)
        self.wait_for_score_update_from_inplay_ms(score=self.new_home_score, team='home', event_id=self.event_id, delimiter=self.delimiter)
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.league_name}"')
        event = events.get(self.event_name)
        self.assertTrue(event, msg=f'Event "{self.event_name}" is not found among events "{events.keys()}"')

        result = wait_for_result(
            lambda: event.score_table.match_score.home_score == self.new_home_score,
            timeout=3, name='Home team score changed to expected')
        self.assertTrue(result, msg=f'Actual score value is:'
                                    f'"{self.section.items_as_ordered_dict[self.event_name].score_table.match_score.home_score}"'
                                    f' for Home team is not the same as expected: "{self.new_home_score}"')

    def test_006_verify_score_change_for_home_player_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Score change for HOME player for sections in a collapsed state
        EXPECTED: If section is collapsed and Score was changed, after expanding the section - updated Score will be shown there
        """
        self.section.collapse()
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.home_score_expected, away_score=self.away_score_expected)
        self.section.expand()
        self.wait_for_score_update_from_inplay_ms(score=self.home_score_expected, team='home', event_id=self.event_id,
                                                  delimiter=self.delimiter)
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.league_name}"')
        event = events.get(self.event_name)
        self.assertTrue(event, msg=f'Event "{self.event_name}" is not found among events "{events.keys()}"')

        result = wait_for_result(
            lambda: event.score_table.match_score.home_score == self.home_score_expected,
            timeout=3,
            name='Home team score changed to expected')
        self.assertTrue(result, msg=f'Actual score value: "{event.score_table.match_score.home_score}"'
                                    f' for Home team is not the same as expected: "{self.home_score_expected}"')

    def test_007_trigger_the_following_situation_the_score_is_changed_for_away_team(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: the score is changed for AWAY team
        EXPECTED: * Score immediately starts displaying new value for Away player
        EXPECTED: * Update is received in WS and corresponds to event.scoreboard.ALL.value where role_code=AWAY
        """
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.home_score_expected, away_score=self.new_away_score)
        self.wait_for_score_update_from_inplay_ms(score=self.new_away_score, team='away', event_id=self.event_id, delimiter=self.delimiter)
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.league_name}"')
        event = events.get(self.event_name)
        self.assertTrue(event, msg=f'Event "{self.event_name}" is not found among events "{events.keys()}"')

        result = wait_for_result(
            lambda: event.score_table.match_score.away_score == self.new_away_score,
            timeout=3,
            name='Away team score changed to expected')
        self.assertTrue(result, msg=f'Actual score value is: "{event.score_table.match_score.away_score}"'
                                    f' for Away team is not the same as expected: "{self.new_away_score}"')

    def test_008_verify_score_change_for_away_player_for_sections_in_a_collapsed_state(self):
        """
        DESCRIPTION: Verify Score change for AWAY player for sections in a collapsed state
        EXPECTED: If section is collapsed and Score was changed, after expanding the section - updated Score will be shown there
        """
        self.section.collapse()
        self.ob_config.change_score(event_id=self.event_id, team1_name=self.team1, team2_name=self.team2,
                                    home_score=self.home_score_expected, away_score=self.away_score_expected)
        self.section.expand()
        self.wait_for_score_update_from_inplay_ms(score=self.away_score_expected, team='away', event_id=self.event_id, delimiter=self.delimiter)
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.league_name}"')
        event = events.get(self.event_name)
        self.assertTrue(event, msg=f'Event "{self.event_name}" is not found among events "{events.keys()}"')

        result = wait_for_result(
            lambda: self.away_score_expected == event.score_table.match_score.away_score,
            timeout=3,
            name='Away team score changed to expected')
        self.assertTrue(result, msg=f'Actual score value is: "{event.score_table.match_score.away_score}"'
                                    f' for Away team is not the same as expected: "{self.away_score_expected}"')

    def test_009_go_to_in_play_page_handball_sorting_type_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to 'In Play' page, 'Handball' sorting type and repeat steps #2-4
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='in-play/handball')
            self.site.wait_content_state(state_name='in-play')

            wait_for_category_in_inplay_sports_ribbon(category_id=self.ob_config.backend.ti.handball.category_id)

            sections = self.site.inplay.tab_content.live_now.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No sections found for "{self.sport_name}"')

            section = sections.get(self.league_name_in_play_page_sport_tab)
            self.assertTrue(section, msg=f'"{self.league_name_in_play_page_sport_tab}" section not found')
            section.expand()

            self.test_002_verify_handball_event_with_score_available(section=section)
            self.test_003_verify_score_correctness_for_home_team()
            self.test_004_verify_score_correctness_for_away_team()

    def test_010_go_to_in_play_tab_on_module_selector_ribbon_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to 'In Play' tab on Module Selector Ribbon and repeat steps #2-4
        """
        self.__class__.delimiter = '42'
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state(state_name='Homepage')

            wait_for_category_in_inplay_structure(category_id=self.ob_config.backend.ti.handball.category_id)

            sport_sections = self.site.home.tab_content.live_now.items_as_ordered_dict
            self.assertTrue(sport_sections, msg='*** No sport sections are present on page')

            sport_section = sport_sections.get(self.sport_name.upper())
            self.assertTrue(sport_section, msg=f'"{self.sport_name.upper()}" sport section not found')

            sport_section.expand()
            self.assertTrue(sport_section.is_expanded(),
                            msg=f'"{self.sport_name}" section is not expanded')

            if sport_section.has_show_more_leagues_button():
                sport_section.show_more_leagues_button.click()

            leagues = sport_section.items_as_ordered_dict
            self.assertTrue(leagues, msg=f'No leagues found for "{self.sport_name.upper()}"')

            if self.brand == 'ladbrokes':
                section = leagues.get(self.league_name_in_play_tab_homepage)
                self.assertTrue(section, msg=f'"{self.league_name_in_play_tab_homepage}" league not found')
            else:
                section = leagues.get(self.league_name_in_play_tab_homepage)
                self.assertTrue(section, msg=f'"{self.league_name_in_play_tab_homepage}" league not found')

            self.test_002_verify_handball_event_with_score_available(section=section)
            self.test_003_verify_score_correctness_for_home_team()
            self.test_004_verify_score_correctness_for_away_team()

    def test_011_go_to_in_play_widget_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to 'In Play' widget and repeat steps #2-4
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='sport/handball')
            # Widget has a specific carousel scroll that can not be automated because it does not exist when
            # the mouse is not hovering on it. In this case, this will be only the first event: if this is our event -
            # it will be checked according to the scenario
            widgets = self.site.handball.in_play_widget.items_as_ordered_dict
            self.assertTrue(widgets, msg='No sections found on Football page')
            self.assertIn(self.widget_section_name, widgets.keys(),
                          msg=f'{self.widget_section_name} not found in {widgets.keys()}')

            widget = widgets[self.widget_section_name]
            slides = widget.content.items
            self.assertTrue(slides, msg='No events found on Handball widget')
            slide = slides[0]
            event_name = slide.in_play_card.first_participant.text

            if event_name == self.team1:
                live_label = slide.in_play_card.in_play_score.game_status._we.text
                self.assertEqual('LIVE', live_label, msg='"LIVE" label is not shown on the screen')

                home_score = slide.in_play_card.in_play_score.left_score._we.text
                away_score = slide.in_play_card.in_play_score.right_score._we.text
                self.assertEqual(self.home_score_expected, home_score,
                                 msg=f'Actual score value {home_score}'
                                     f' for Home team is not the same as expected {self.home_score_expected}')
                self.assertEqual(self.away_score_expected, away_score,
                                 msg=f'Actual score value {away_score}'
                                     f' for Away team is not the same as expected {self.away_score_expected}')

    def test_012_go_to_featured_tab_and_repeat_steps_2_4(self):
        """
        DESCRIPTION: Go to Featured tab and repeat steps #2-4
        """
        # For avoiding duplication of events on Homepage in 'In-Play' and 'Featured' sections, the Live events are not
        # displayed in Featured module. For Desktop only, according to BMA-38673.
        self.__class__.delimiter = '42/0'
        if self.device_type == 'mobile':
            type_id = self.ob_config.backend.ti.handball.handball_croatia.dukat_premijer_liga.type_id

            module_name = self.cms_config.add_featured_tab_module(
                select_event_by='Type', id=type_id, events_time_from_hours_delta=self.events_from_hours_delta,
                show_all_events=True)['title'].upper()

            self.site.wait_content_state(state_name='HomePage')
            self.site.home.get_module_content(
                module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

            inplay_module = get_in_play_module_from_ws()
            self.assertTrue(inplay_module, 'Failed to get inplay module in featured structure changed response in WS')

            section_list = self.site.home.tab_content.in_play_module.items_as_ordered_dict
            self.assertTrue(section_list, msg='*** No sections present on page')

            if vec.siteserve.HANDBALL_TAB.upper() not in section_list.keys():
                section = self.get_featured_section(module_name=module_name)
            else:
                section_to_check = section_list[vec.siteserve.HANDBALL_TAB.upper()]
                section_events = section_to_check.items_as_ordered_dict
                self.assertTrue(section_events, msg='*** No events present on page')

                if self.event_name not in section_events.keys():
                    section = self.get_featured_section(module_name=module_name)
                else:
                    section = section_to_check

            self.test_002_verify_handball_event_with_score_available(section=section)
            self.test_003_verify_score_correctness_for_home_team()
            self.test_004_verify_score_correctness_for_away_team()
