import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.timeout(1200)
@pytest.mark.market_switcher
@vtest
class Test_C60089613_Verify_pre_selected_Handicap_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Ice_Hockey(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089613
    NAME: Verify pre selected ‘Handicap WW’ MT is saved when switching b/w T/T/F on Matches Tab for Ice Hockey
    DESCRIPTION: This test case verifies that previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future in Matches tab in Ice Hockey Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Ice Hockey Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) 1) The set of markets should be created in OB system with different 'HandicapValue' (2,2.5,3)etc using the following Market Template Names:
    PRECONDITIONS: *|Puck Line (Handicap)| - "Puck Line"
    PRECONDITIONS: *|Total Goals 2-way (Over/Under)| - "Total Goals 2-way"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    handicap_market = True
    expected_low_sort_handicap = 2.5
    expected_same_sort_handicap = 1.5
    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.puck_line,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_2_way]
    event_markets = [
        ('puck_line_2', {'handicap': expected_low_sort_handicap, 'disp_order': -3}),
        ('puck_line_3', {'handicap': 1.0, 'disp_order': 7}),
        ('total_goals_2_way', {'handicap': expected_same_sort_handicap}),
        ('total_goals_2_way_2', {'handicap': 3.0}), ]

    def verify_market_event_fixture(self, eventID=None, section_name=None, expected_tab=None,
                                    market_selector_default_value=expected_list[0]):
        self.assertEqual(self.site.ice_hockey.date_tab.current_date_tab, expected_tab,
                         msg=f'Current active date tab: "{self.site.ice_hockey.date_tab.current_date_tab}" '
                             f'expected: "{expected_tab}"')

        market_selector_default_value = market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' else market_selector_default_value
        self.assertEqual(self.site.ice_hockey.tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.site.ice_hockey.tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')

        section = self.site.ice_hockey.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
        self.assertTrue(section, msg=f'Section "{section_name}" not found')
        event = self.get_event_from_league(event_id=eventID, section_name=section_name)
        events = section.items_as_ordered_dict.values()
        self.assertTrue(event, msg=f'Events are not shown')
        expected_default_fixture_value = ['1', '2'] if self.handicap_market else ['OVER', 'UNDER']
        default_fixture_value = list(section.fixture_header.items_as_ordered_dict.keys())
        self.assertEqual(default_fixture_value, expected_default_fixture_value,
                         msg=f'Actual fixture header "{default_fixture_value}" does not '
                             f'equal to expected "{expected_default_fixture_value}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 2,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "2"')
        name, odds_from_page = list(section.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index], expected_odds_format="fraction")

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Ice Hockey event with required markets
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='icehockey',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for IceHockey sport')
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.ice_hockey.category_id,
            disp_sort_names='HH,WH,MR,HL',
            primary_markets='|Money Line|,|Total Goals 2-way|,|Puck Line|,|60 Minutes Betting|')
        # Today tab event
        event_params = self.ob_config.add_ice_hockey_event_to_ice_hockey_autotest_handicap(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        # Tomorrow Tab Event
        tomorrow = self.get_date_time_formatted_string(days=1)
        event_params_tomorrow = self.ob_config.add_ice_hockey_event_to_ice_hockey_autotest_handicap(
            markets=self.event_markets, start_time=tomorrow)
        self.__class__.event_name_tomorrow = event_params_tomorrow.team1 + ' v ' + event_params_tomorrow.team2
        self.__class__.eventID_tomorrow = event_params_tomorrow.event_id
        event_resp_tomorrow = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_tomorrow,
                                                                        query_builder=self.ss_query_builder)
        self.__class__.section_name_tomorrow = self.get_accordion_name_for_event_from_ss(event=event_resp_tomorrow[0])

        # Future Tab Event
        future = self.get_date_time_formatted_string(days=7)
        event_params_future = self.ob_config.add_ice_hockey_event_to_ice_hockey_autotest_handicap(
            markets=self.event_markets, start_time=future)
        self.__class__.event_name_future = event_params_future.team1 + ' v ' + event_params_future.team2
        self.__class__.eventID_future = event_params_future.event_id
        event_resp_future = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_future,
                                                                      query_builder=self.ss_query_builder)
        self.__class__.section_name_future = self.get_accordion_name_for_event_from_ss(event=event_resp_future[0])

        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        wait_for_result(lambda: self.site.ice_hockey.tabs_menu.current is not None,
                        name=f'Matches Tab is displayed',
                        timeout=15)
        current_tab_name = self.site.ice_hockey.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Expected tab: "{self.expected_sport_tabs.matches}", Actual Tab: "{current_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • Primary market is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Puck Line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Puck Line' in 'Market selector' **Coral**
        """
        self.__class__.ice_hockey_tab_content = self.site.ice_hockey.tab_content
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.puck_line.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as '
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.puck_line}"')
            market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.puck_line
        except VoltronException:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.money_line.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.money_line}"')
        self.assertTrue(self.ice_hockey_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on IceHockey landing page')
        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value
        self.assertEqual(self.ice_hockey_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.ice_hockey_tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        self.dropdown.click()
        wait_for_result(lambda: self.dropdown.is_expanded() is not True,
                        name=f'Market switcher expanded/collapsed',
                        timeout=10)
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing upwards')
        if self.brand == 'bma' and self.device_type == 'desktop':
            self.assertTrue(self.dropdown.has_up_arrow, msg='Market selector up arrow is not displayed')
            self.assertTrue(self.dropdown.has_down_arrow, msg='Market selector down arrow is not displayed')
        elif self.device_type == 'mobile' or self.brand == 'ladbrokes':
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_002_select_puck_line_in_the_market_selector_dropdown_list(self, handicap_value=expected_low_sort_handicap):
        """
        DESCRIPTION: Select 'Puck Line' in the 'Market Selector' dropdown list
        EXPECTED: • Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        """
        if self.handicap_market:
            options = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
            if not self.dropdown.is_expanded():
                self.dropdown.expand()
            options.get(self.expected_list[0]).click()
        self.site.wait_content_state_changed(timeout=5)

        self.__class__.leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')

        for league in self.leagues:
            self.__class__.events = list(league.items_as_ordered_dict.values())
            self.assertTrue(self.events, msg='Events not found')
            for event in self.events:
                event_template = event.template
                if self.event_name == event_template.event_name:
                    handicap = event_template.items_names
                    handicap_values = list(event_template.items_as_ordered_dict.values())
                    for val in handicap_values:
                        self.assertEqual(val.handicap_value.text_color_value, vec.colors.HANDICAP_COLOR,
                                         msg=' Handicap Value is not in blue color')
                    val = 0
                    for value in handicap:
                        actual_value = value.split('\n')[0]
                        self.assertIn(str(handicap_value), actual_value,
                                      msg=f'{handicap_value} value is not displayed as per dispsort value ')
                        if self.handicap_market:
                            if val == 0:
                                self.assertNotIn('-', actual_value,
                                                 msg=' "Negetive value" present in button')
                                val += 1
                            else:
                                self.assertIn('-', actual_value,
                                              msg=' "Negetive value" not present in button')
                        else:
                            self.assertNotIn('-', actual_value,
                                             msg=' "Negetive value" present in button')

    def test_003_verify_text_of_the_labels_for_puck_line_in_matches_tab(self, label1="1", label2="2"):
        """
        DESCRIPTION: Verify text of the labels for 'Puck Line' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label Over & Under.
        """
        leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        fixture = leagues[0].fixture_header
        self.assertEqual(fixture.header1, label1,
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{label1}"')
        self.assertEqual(fixture.header3, label2,
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{label2}"')

    def test_004_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        dropdown = self.site.contents.tab_content.dropdown_market_selector
        if dropdown.is_expanded():
            dropdown.click()
            wait_for_result(lambda: dropdown.is_expanded() is not True,
                            name=f'Market switcher expanded/collapsed',
                            timeout=5)
        leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.__class__.events = list(leagues.items_as_ordered_dict.values())
        for event in self.events:
            event_template = event.template
            self.assertFalse(event_template.is_live_now_event, msg=f'Event: "{event}" is an "In-Play" Event')

    def test_005_verify_ga_tracking_for_the_puck_line(self, market=expected_list[0]):
        """
        DESCRIPTION: Verify GA Tracking for the 'Puck Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: 'Puck Line'
        EXPECTED: categoryID: "22"
        EXPECTED: })
        """
        dropdown = self.site.contents.tab_content.dropdown_market_selector
        dropdown.scroll_to()
        options = self.ice_hockey_tab_content.dropdown_market_selector.items_as_ordered_dict
        if not dropdown.is_expanded():
            dropdown.expand()
        options.get(market).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market,
                             'categoryID': 22,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_006_switch_to_the_tomorrow_tab(self, market_selector_default_value=expected_list[0]):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Puck Line)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note: If events are not present for 'Puck Line' market and if events are present for 'Total Goals 2-way' market then 'Total Goals 2-way' will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display
        """
        self.site.ice_hockey.date_tab.tomorrow.click()
        self.verify_market_event_fixture(eventID=self.eventID_tomorrow, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.tomorrow,
                                         market_selector_default_value=market_selector_default_value)

    def test_007_repeat_steps_45(self, market=expected_list[0]):
        """
        DESCRIPTION: Repeat steps 4,5
        EXPECTED:
        """
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_puck_line(market=market)

    def test_008_repeat_steps_456_for_the_future_tab(self, market=expected_list[0]):
        """
        DESCRIPTION: Repeat steps 4,5,6 for the 'Future' tab
        EXPECTED:
        """
        self.site.ice_hockey.date_tab.future.click()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_puck_line(market=market)
        self.verify_market_event_fixture(eventID=self.eventID_future, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.future, market_selector_default_value=market)

    def test_009_switch_back_to_today_tab(self, market_selector_default_value=expected_list[0]):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        self.site.ice_hockey.date_tab.today.click()
        self.verify_market_event_fixture(eventID=self.eventID, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.today,
                                         market_selector_default_value=market_selector_default_value)

    def test_010_repeat_steps_2_9_for_the_below_markets_total_goals_2_wayexcept_validating_the_labels_from_step_9(self):
        """
        DESCRIPTION: Repeat steps 2-9 for the below markets
        DESCRIPTION: • Total Goals 2-way(except validating the labels from step 9)
        EXPECTED:
        """
        self.__class__.handicap_market = False
        self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_list[1]).click()
        self.test_002_select_puck_line_in_the_market_selector_dropdown_list(handicap_value=self.expected_same_sort_handicap)
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_puck_line(market=self.expected_list[1])
        self.test_006_switch_to_the_tomorrow_tab(market_selector_default_value=self.expected_list[1])
        self.test_007_repeat_steps_45(market=self.expected_list[1])
        self.test_008_repeat_steps_456_for_the_future_tab(market=self.expected_list[1])
        self.test_009_switch_back_to_today_tab(market_selector_default_value=self.expected_list[1])

    def test_011_verify_text_of_the_labels_for_total_goals_2_way_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Goals 2-way' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under
        """
        self.test_003_verify_text_of_the_labels_for_puck_line_in_matches_tab(label1=vec.sb.OVER.upper(), label2=vec.sb.UNDER.upper())
