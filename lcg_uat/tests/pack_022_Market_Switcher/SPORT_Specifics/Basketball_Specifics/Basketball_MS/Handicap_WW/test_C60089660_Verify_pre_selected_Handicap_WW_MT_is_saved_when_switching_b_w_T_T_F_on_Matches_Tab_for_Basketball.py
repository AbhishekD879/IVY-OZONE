import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from voltron.utils.exceptions.siteserve_exception import VoltronException
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Events with specific markets cannot be created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.slow
@vtest
class Test_C60089660_Verify_pre_selected_Handicap_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Basketball(BaseDataLayerTest):
    """
    TR_ID: C60089660
    NAME: Verify pre selected ‘Handicap WW’ MT is saved when switching b/w T/T/F on Matches Tab for Basketball
    DESCRIPTION: This test case verifies that previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Basketball Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'rawHandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    markets = [
        ('total_points_1', {'handicap': 2}),
        ('handicap_2_way',),
        ('handicap_2_way_2', {'handicap': 3}),
        ('home_team_total_points',),
        ('home_team_total_points_2', {'handicap': 3}),
        ('away_team_total_points',),
        ('away_team_total_points_2', {'handicap': 3}),
        ('half_total_points',),
        ('half_total_points_2', {'handicap': 3}),
        ('quarter_total_points',),
        ('quarter_total_points_2', {'handicap': 3})]

    expected_handicap_value_to_display = 5

    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.total_points,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points,
                     ]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None):
        items = list(self.site.basketball.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        self.assertEqual(event.header3, header3,
                         msg=f'Actual fixture header "{event.header2}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Basketball Landing page -> 'Matches' tab
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.basketball.category_id,
            disp_sort_names='HL,WH,HH',
            primary_markets='|Money Line|,|Total Points|,'
                            '|Home team total points|,|Away team total points|,'
                            '|Half Total Points|,|Quarter Total Points|,'
                            '|Handicap 2-way|')
        self.ob_config.add_basketball_event_to_basketball_autotest_handicap(markets=self.markets, disp_order=2)
        tomorrow = self.get_date_time_formatted_string(days=1)
        self.ob_config.add_basketball_event_to_basketball_autotest_handicap(markets=self.markets, start_time=tomorrow)
        future = self.get_date_time_formatted_string(days=7)
        self.ob_config.add_basketball_event_to_basketball_autotest_handicap(markets=self.markets, start_time=future)
        event = self.ob_config.add_basketball_event_to_basketball_autotest_handicap(markets=self.markets, disp_order=2)
        self.__class__.event_name = event.team1 + ' v ' + event.team2

        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state('basketball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.sports_page.tabs_menu.current
        if current_tab_name != expected_tab_name:
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
            current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Total Points' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Total Points' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Total Points' in 'Market selector' **Coral**
        """
        self.__class__.basketball_tab_content = self.site.basketball.tab_content
        self.assertTrue(self.basketball_tab_content.has_dropdown_market_selector(), msg='"Market selector" is not '
                                                                                        'available for basketball')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.total_points.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.total_points}"')
        except VoltronException:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.money_line.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')
        dropdown = self.basketball_tab_content.dropdown_market_selector
        if self.brand == 'bma':
            self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
            self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
        else:
            dropdown.click()
            sleep(2)
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_002_select_total_points_in_the_market_selector_dropdown_list(self, market=vec.siteserve.EXPECTED_MARKETS_NAMES.total_points):
        """
        DESCRIPTION: Select 'Total Points' in the 'Market Selector' dropdown list
        EXPECTED: • Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        """
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            market).click()
        self.__class__.leagues = list(
            self.site.basketball.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')
        for league in self.leagues:
            if not league.is_expanded():
                league.expand()
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                if self.event_name == event_template.event_name:
                    handicap = event_template.items_names
                    handicap_values = list(event_template.items_as_ordered_dict.values())
                    for val in handicap_values:
                        self.assertEqual(val.handicap_value.text_color_value, vec.colors.HANDICAP_COLOR,
                                         msg=' "Handicap Value" is not in blue color')
                    if market in ['Handicap', 'Spread']:
                        odd1, odd2 = handicap[0].split('\n')[0], handicap[1].split('\n')[0]
                        self.assertGreater(float(odd1), 0,
                                           msg=f'Odd1 "{odd1}" is not positive for Handicap market as per dispsort value')
                        self.assertLess(float(odd2), 0,
                                        msg=f'Odd2 "{odd2}" is not negative for Handicap market as per dispsort value')
                    elif market == "Total Frames":
                        odd1, odd2 = handicap[0].split('\n')[0], handicap[1].split('\n')[0]
                        self.assertGreater(float(odd1), 0,
                                           msg=f'Odd1 "{odd1}" is not positive for Handicap market as per dispsort value')
                        self.assertGreater(float(odd2), 0,
                                           msg=f'Odd2 "{odd2}" is not positive for Handicap market as per dispsort value')

    def test_003_verify_text_of_the_labels_for_total_points_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        """
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.OVER.upper(), header3=vec.sb.UNDER.upper())

    def test_004_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.__class__.events = list(leagues.items_as_ordered_dict.values())
        for event in self.events:
            event_template = event.template
            odds = list(event_template.items_as_ordered_dict.values())
            for odd in odds:
                self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
            self.assertFalse(event_template.is_live_now_event,
                             msg=f'Event: "{event}" is an "In-Play" Event')
            self.assertTrue(event_template.event_name,
                            msg=' "Event Name" not displayed')
            self.assertTrue(event_template.event_time,
                            msg=' "Event time and date " are not displayed')
            if event_template.has_markets():
                self._logger.info(f'{event_template.event_name} has more markets')
            else:
                self._logger.info(f'{event_template.event_name} has no more markets')

    def test_005_verify_ga_tracking_for_the_total_points(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.total_points):
        """
        DESCRIPTION: Verify GA Tracking for the 'Total Points'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Total Points"
        EXPECTED: categoryID: "6"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        options = self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if not dropdown.is_expanded():
            dropdown.expand()
        options.get(market_name).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market_name)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market_name,
                             'categoryID': 6,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_006_switch_to_the_tomorrow_tab(self, bet_button_qty=2, header1=vec.sb.OVER.upper(), header3=vec.sb.UNDER.upper()):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Total Points)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        EXPECTED: Note: If events are not present for Total Points market and if events are present for either Home Team Total Points/Away Team Total Points/Handicap  markets then those markets will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        self.site.basketball.date_tab.tomorrow.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=bet_button_qty, header1=header1,
                                                          header3=header3)

    def test_007_repeat_steps_45(self):
        """
        DESCRIPTION: Repeat steps 4,5
        """
        self.site.contents.scroll_to_top()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(
            market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.total_points)

    def test_008_repeat_steps_456_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 4,5,6 for the 'Future' tab
        """
        self.site.basketball.date_tab.future.click()
        self.site.contents.scroll_to_top()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(
            market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.total_points)

    def test_009_switch_back_to_today_tab(self, bet_button_qty=2, header1=vec.sb.OVER.upper(), header3=vec.sb.UNDER.upper()):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under
        """
        self.site.basketball.date_tab.today.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=bet_button_qty, header1=header1,
                                                          header3=header3)

    def test_010_repeat_steps_2_9_for_the_below_markets_home_team_total_points_away_team_total_points_handicap_except_step_3(self):
        """
        DESCRIPTION: Repeat steps 2-9 for the below markets
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        DESCRIPTION: • Handicap (except step 3)
        """
        # Home Team Total Points
        self.expected_list[2] = vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points \
            if self.brand == 'bma' else vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points.replace('P', 'p')
        self.test_002_select_total_points_in_the_market_selector_dropdown_list(market=self.expected_list[2])
        self.test_003_verify_text_of_the_labels_for_total_points_in_matches_tab()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[2])
        self.test_006_switch_to_the_tomorrow_tab(bet_button_qty=2, header1=vec.sb.OVER.upper(), header3=vec.sb.UNDER.upper())
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[2])
        self.site.basketball.date_tab.future.click()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[2])
        self.test_009_switch_back_to_today_tab(bet_button_qty=2, header1=vec.sb.OVER.upper(), header3=vec.sb.UNDER.upper())

        # Away Team Total Points
        self.test_002_select_total_points_in_the_market_selector_dropdown_list(
            market=self.expected_list[3])
        self.test_003_verify_text_of_the_labels_for_total_points_in_matches_tab()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[3])
        self.test_006_switch_to_the_tomorrow_tab(bet_button_qty=2, header1=vec.sb.OVER.upper(),
                                                 header3=vec.sb.UNDER.upper())
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[3])
        self.site.basketball.date_tab.future.click()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[3])
        self.test_009_switch_back_to_today_tab(bet_button_qty=2, header1=vec.sb.OVER.upper(),
                                               header3=vec.sb.UNDER.upper())

        # Handicap
        self.expected_list[1] = 'Spread' \
            if self.brand == 'bma' else vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way
        self.test_002_select_total_points_in_the_market_selector_dropdown_list(
            market=self.expected_list[1])
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[1])
        self.test_006_switch_to_the_tomorrow_tab(bet_button_qty=2, header1='1', header3='2')
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[1])
        self.site.basketball.date_tab.future.click()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_total_points(market_name=self.expected_list[1])
        self.test_009_switch_back_to_today_tab(bet_button_qty=2, header1='1', header3='2')

    def test_011_verify_text_of_the_labels_for_handicap_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Handicap' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        # Covered in Step#10
