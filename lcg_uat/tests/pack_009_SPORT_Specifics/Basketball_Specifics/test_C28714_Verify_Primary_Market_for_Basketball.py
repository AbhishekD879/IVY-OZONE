import tests
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create events
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28714_Verify_Primary_Market_for_Basketball(BaseSportTest):
    """
    TR_ID: C28714
    NAME: Verify Primary Market for Basketball
    DESCRIPTION: This test case verifies Primary Market for 'Basketball' Sport
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Outright events are NOT shown on 'Today', 'Tomorrow', 'Future' tabs
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * Go to Basketball landing page
    """
    keep_browser_open = True
    expected_events = []
    outright_events = []

    def verify_event_attributes(self, event_id, market_pattern):
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]
        self.__class__.market = event_resp['event']['children'][0]
        actual_market_name = self.market['market']['name']
        self.assertEqual(actual_market_name, market_pattern,
                         msg='Actual market name is not equal with expected market name')
        outcomes = self.market['market']['children']
        home = outcomes[0]['outcome']['outcomeMeaningMinorCode']
        self.assertEqual(home, 'H', msg='Actual outcomeMeaningMinorCode is not equal with expected "H"')
        away = outcomes[1]['outcome']['outcomeMeaningMinorCode']
        self.assertEqual(away, 'A', msg='Actual outcomeMeaningMinorCode is not equal with expected "A"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events
        """
        self.__class__.basketball_category_id = self.ob_config.backend.ti.basketball.category_id
        self.__class__.section_name = tests.settings.basketball_autotest_league
        event1 = self.ob_config.add_basketball_event_to_autotest_league()
        self.__class__.eventID1 = event1.event_id
        self.__class__.market_pattern = self.ob_config.backend.ti.basketball.basketball_autotest.autotest_league.market_name

    def test_001_verify_todays_matches_page_for_desktop(self):
        """
        DESCRIPTION: Verify Today's Matches page for **Desktop**
        EXPECTED: * Today's Matches page is opened
        EXPECTED: * Events are grouped by **classId** and typeId
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining accordions are collapsed by default
        EXPECTED: * If no events to show, the message No events found is displayed
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state('Basketball')
        if self.device_type == 'mobile':
            basketball_sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(basketball_sections, msg='No section found on Basketball page')
        else:
            current_tab = self.site.contents.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                             msg=f'Default tab: "{current_tab}" opened '
                                 f'is not as expected: "{self.expected_sport_tabs.events}"')
        self.verify_section_collapse_expand()

    def test_002_verify_list_of_events__on_matches___today_tab_for_desktop__on_matches_tab_on_mobile(self):
        """
        DESCRIPTION: Verify list of events
        DESCRIPTION: - on Matches -> Today tab for **Desktop**
        DESCRIPTION: - on Matches tab on **Mobile**
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Money Line"**
        EXPECTED: *   **dispSortName="HH"**
        """
        self.verify_event_attributes(event_id=self.eventID1, market_pattern=self.market_pattern)
        sort_code = self.market['market']['dispSortName']
        self.assertEqual(sort_code, 'HH', msg='Actual sort code is not equal with expected sort code')

    def test_003_verify_priceodds_button_for_2_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 2-Way Market
        EXPECTED: For **Money Line** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home **'Win'**
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'Win'**
        """
        # covered in above step

    def test_004_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap '**In-Play**' tab
        EXPECTED: **'In-Play' **tab is opened
        """
        event2 = self.ob_config.add_basketball_event_to_autotest_league(is_live=True)
        self.__class__.eventID2 = event2.event_id

        event3 = self.ob_config.add_basketball_outright_event_to_autotest_league(is_live=True)
        self.__class__.eventID3 = event3.event_id
        event4 = self.ob_config.add_basketball_event_to_autotest_league(is_upcoming=True)
        self.__class__.eventID4 = event4.event_id

        event5 = self.ob_config.add_basketball_outright_event_to_autotest_league(is_upcoming=True)
        self.__class__.eventID5 = event5.event_id
        if self.device_type == 'mobile':
            self.navigate_to_page('sport/basketball/live')
            in_play_module = self.site.inplay.tab_content
            self.assertTrue(in_play_module, msg='There is no "In Play" module on the page')
            self.verify_section_collapse_expand()
        else:
            modules = self.cms_config.get_initial_data().get('modularContent', [])
            modules_name = [module.get('id') for module in modules]
            if self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play in modules_name:
                in_play_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play)
                self.site.contents.tabs_menu.click_button(in_play_tab)
                current_tab = self.site.contents.tabs_menu.current
                self.assertEqual(current_tab, in_play_tab,
                                 msg=f'Current tab: "{current_tab}" opened is not as expected: "{in_play_tab}"')
            else:
                self._logger.warning('In-play tab isn\'t shown on Homepage')

    def test_005_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: 1) Events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Money Line"**
        EXPECTED: *   **dispSortName="HH"**
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        self.__class__.market_pattern1 = self.ob_config.backend.ti.basketball.basketball_autotest.autotest_league.outright_market_name
        self.verify_event_attributes(event_id=self.eventID2, market_pattern=self.market_pattern)
        sort_code = self.market['market']['dispSortName']
        self.assertEqual(sort_code, 'HH', msg='Actual sort code is not equal with expected sort code')

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID3)[0]
        market = event_resp['event']['children'][0]
        actual_market_name = market['market']['name']
        self.assertEqual(actual_market_name, self.market_pattern1,
                         msg='Actual market name is not equal with expected market name')
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            self.verify_section_collapse_expand()
        self.verify_event_attributes(event_id=self.eventID4, market_pattern=self.market_pattern)
        sort_code = self.market['market']['dispSortName']
        self.assertEqual(sort_code, 'HH', msg='Actual sort code is not equal with expected sort code')

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID5)[0]
        market = event_resp['event']['children'][0]
        actual_market_name = market['market']['name']
        self.assertEqual(actual_market_name, self.market_pattern1,
                         msg='Actual market name is not equal with expected market name')

    def test_006_repeat_step_4_for_events_that_are_not_outrights(self):
        """
        DESCRIPTION: Repeat step №4 for events that are not Outrights
        EXPECTED:
        """
        # covered in above step

    def test_007_repeat_steps_1_3_step_3_only_for_tomorrow_and_future_tabs_for_desktop_for_tomorrow_tab_for_desktop_only_future_tab_for_desktop_only_competition_tab_mobile_only_competition_detailed_page_mobile_where_applicable_live_stream_pagetab___live_now_and_upcoming_filters_highlights_carousel_module_created_on_homepage_landing_page_featured_tab_module_created_by_typeid_live_stream_widget(
            self):
        """
        DESCRIPTION: Repeat steps №1-3 (step 3 only for Tomorrow and Future tabs for Desktop) for:
        DESCRIPTION: * 'Tomorrow' tab (for desktop only)
        DESCRIPTION: * 'Future' tab (for desktop only)
        DESCRIPTION: * 'Competition' tab (mobile only)
        DESCRIPTION: * 'Competition Detailed' page (mobile, where applicable)
        """
        tomorrow = self.get_date_time_formatted_string(days=1)
        event_params6 = self.ob_config.add_basketball_event_to_autotest_league(
            start_time=tomorrow)
        self.__class__.eventID6 = event_params6.event_id
        future = self.get_date_time_formatted_string(days=3)
        event_params7 = self.ob_config.add_basketball_event_to_autotest_league(
            start_time=future)
        self.__class__.eventID7 = event_params7.event_id
        if self.device_type == 'desktop':
            self.navigate_to_page(name='sport/basketball')
            self.site.wait_content_state('Basketball')
            current_tab = self.site.contents.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                             msg=f'Default tab: "{current_tab}" opened '
                                 f'is not as expected: "{self.expected_sport_tabs.events}"')
            self.site.sports_page.date_tab.tomorrow.click()
            self.verify_event_attributes(event_id=self.eventID6, market_pattern=self.market_pattern)
            sort_code = self.market['market']['dispSortName']
            self.assertEqual(sort_code, 'HH', msg='Actual sort code is not equal with expected sort code')
            self.verify_section_collapse_expand()
            self.site.sports_page.date_tab.future.click()

            self.verify_event_attributes(event_id=self.eventID7, market_pattern=self.market_pattern)
            sort_code = self.market['market']['dispSortName']
            self.assertEqual(sort_code, 'HH', msg='Actual sort code is not equal with expected sort code')
            self.verify_section_collapse_expand()
        else:
            self.__class__.competitions_tab_name = self.get_sport_tab_name(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                self.basketball_category_id)
            self.assertTrue(self.competitions_tab_name, msg='competition tab is not available')
            self.site.basketball.tabs_menu.click_button(self.competitions_tab_name.upper())
            self.verify_event_attributes(event_id=self.eventID7, market_pattern=self.market_pattern)
            sort_code = self.market['market']['dispSortName']
            self.assertEqual(sort_code, 'HH', msg='Actual sort code is not equal with expected sort code')
            self.verify_section_collapse_expand()

    def test_008_repeat_steps_2_3_and_5_6_for_in_play_tab___live_now_and_upcoming_filters_in_play_sport_page___live_now_and_upcoming_filters_in_play_widget_on_desktop(
            self):
        """
        DESCRIPTION: Repeat steps №2-3 and №5-6 for:
        DESCRIPTION: * In-Play tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play Sport page -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play widget on Desktop
        """
        self.navigate_to_page(name='in-play/basketball')
        self.site.wait_content_state(state_name='in-play')
        self.test_005_verify_list_of_events()
        # In Play Sport page -> 'Live Now' and 'Upcoming 'filters covered in above steps
