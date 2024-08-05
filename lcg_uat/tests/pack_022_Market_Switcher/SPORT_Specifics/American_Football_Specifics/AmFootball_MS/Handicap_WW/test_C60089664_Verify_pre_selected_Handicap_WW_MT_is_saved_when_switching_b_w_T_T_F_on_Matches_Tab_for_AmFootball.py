import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from voltron.utils.helpers import normalize_name
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089664_Verify_pre_selected_Handicap_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_AmFootball(BaseDataLayerTest, BaseSportTest):
    """
    TR_ID: C60089664
    NAME: Verify pre selected ‘Handicap WW’ MT is saved when switching b/w T/T/F on Matches Tab for Am.Football
    DESCRIPTION: This test case verifies that previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on American Football Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the American Football Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'rawHandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    handicap_market = True
    device_name = tests.desktop_default
    preplay_list = []
    inplay_list = []
    expected_low_sort_handicap = 2.5
    expected_same_sort_handicap = 1.5
    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.total_points]
    event_markets = [
        ('handicap_2_way_2', {'handicap': expected_low_sort_handicap, 'disp_order': -3}),
        ('handicap_2_way_3', {'handicap': 1.0, 'disp_order': 7}),
        ('total_points', {'handicap': expected_same_sort_handicap}),
        ('total_points_1', {'handicap': 3.0}), ]

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the American Football -> 'Click on Matches Tab'
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='americanfootball', status=True)
        self.assertTrue(status, msg=f'The sport "americanfootball" is not checked')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(self.ob_config.american_football_config.category_id,
                                                       disp_sort_names='HH,WH,MR,HL',
                                                       primary_markets='|Money Line|,|Handicap 2-way|,|60 Minute Betting|,|Total Points|')
        event_params = self.ob_config.add_american_football_event_to_autotest_handicap(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        event_tomorrow = \
            self.ob_config.add_american_football_event_to_autotest_handicap(markets=self.event_markets, is_tomorrow=True)
        self.__class__.eventID_tomorrow = event_tomorrow.event_id

        event_future = \
            self.ob_config.add_american_football_event_to_autotest_handicap(markets=self.event_markets,
                                                                            start_time=self.get_date_time_formatted_string(days=14))
        self.__class__.eventID_future = event_future.event_id

        self.site.wait_content_state('Homepage')
        self.navigate_to_page("sport/american-football")
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.american_football_config.category_id)
        self.site.wait_content_state_changed(timeout=30)
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

        self.__class__.grouping_buttons = self.site.contents.tab_content.grouping_buttons
        current_tab = self.grouping_buttons.current
        self.assertEqual(current_tab.upper(), vec.sb.TABS_NAME_TODAY.upper(),
                         msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                             f'Expected tab: "{vec.sb.TABS_NAME_TODAY.upper()}".')

    def test_001_verify_displaying_of_the_market_selector(self, market=expected_list[0]):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Handicap' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Handicap' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Spread' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for American Football League')

        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.brand == 'bma':
            self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
            self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            market = 'Spread'
            self.dropdown.click_item(market)
            sleep(1)
        else:
            self.dropdown.click_item(market)
            sleep(1)
            self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item

        if self.handicap_market:
            if self.brand == 'bma':
                self.assertEqual(selected_value, 'Spread',
                                 msg=f'Actual selected value: "{selected_value}" is not same as'
                                     f'Expected selected value: "Spread"')
            else:
                self.assertEqual(selected_value.upper(), market.upper(),
                                 msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                     f'Expected selected value: "{market.upper()}"')
        else:
            self.assertEqual(selected_value.upper(), market.upper(),
                             msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                 f'Expected selected value: "{market.upper()}"')

    def test_002_select_handicap_in_the_market_selector_dropdown_listhandicap_in_lads_and_spread_in_coral(self, market=expected_list[0], dispsort=expected_low_sort_handicap):
        """
        DESCRIPTION: Select 'Handicap' in the 'Market Selector' dropdown list
        DESCRIPTION: (Handicap in Lads and Spread in Coral)
        EXPECTED: • Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        EXPECTED: Note- When multiple markets are created for the any handicap market , then user should be able to see one market for each market type in landing page and in EDP page whole list will be displayed with all the different handicap values for that particular market.
        """
        self.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        if self.handicap_market and self.brand == 'bma':
            market = 'Spread'
        self.dropdown.click_item(market)
        self.site.wait_content_state_changed(timeout=20)

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
                        self.assertIn(str(dispsort), actual_value,
                                      msg=f'{dispsort} value is not displayed as per dispsort value ')
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

    def test_003_verify_text_of_the_labels_for_handicap_in_matches_tabtodayhandicap_in_lads_and_spread_in_coral(self, label1="1", label2="2"):
        """
        DESCRIPTION: Verify text of the labels for 'Handicap' in Matches Tab(Today)
        DESCRIPTION: (Handicap in Lads and Spread in Coral)
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label 1& 2.
        """
        if len(self.leagues) > 0:
            fixture = self.leagues[0].fixture_header
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
        if len(self.leagues) > 0:
            for league in self.leagues:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(self.events, msg='Events not found')
                for event in events:
                    event_template = event.template
                    odds = list(event_template.items_as_ordered_dict.values())
                    for odd in odds:
                        self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                    self.assertFalse(event_template.is_live_now_event,
                                     msg=f'Event: "{event}" is an "In-Play" Event')

    def test_005_verify_ga_tracking_for_the_handicap(self, market=expected_list[0]):
        """
        DESCRIPTION: Verify GA Tracking for the 'Handicap'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Handicap"
        EXPECTED: categoryID: "1"
        EXPECTED: })
        """
        if len(self.leagues) > 0:
            self.dropdown = self.site.contents.tab_content.dropdown_market_selector
            if not self.dropdown.is_expanded():
                self.dropdown.expand()
            if self.handicap_market and self.brand == 'bma':
                market = 'Spread'
                self.dropdown.click_item(market)
            self.dropdown.click_item(market)
            actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
            expected_response = {'event': 'trackEvent',
                                 'eventCategory': 'market selector',
                                 'eventAction': 'change market',
                                 'eventLabel': market,
                                 'categoryID': 1,
                                 }
            self.compare_json_response(actual_response, expected_response)

    def test_006_switch_to_the_tomorrow_tab(self, market=expected_list[0]):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: handicap)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note:
        EXPECTED: If events are not present for 'Handicap' market and if events are present for 'Total Points' market then 'Total Points' will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        if self.brand == 'bma':
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.upper(),
                                        vec.sb.TABS_NAME_FUTURE.upper(),
                                        vec.sb.TABS_NAME_TODAY.upper()]
        else:
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.title(),
                                        vec.sb.TABS_NAME_FUTURE.title(),
                                        vec.sb.TABS_NAME_TODAY.title()]
        self.grouping_buttons.items_as_ordered_dict.get(self.days_list[0]).click()
        self.site.wait_content_state_changed()
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            if self.handicap_market:
                if self.brand == 'bma':
                    self.assertEqual(selected_value, 'Spread',
                                     msg=f'Actual selected value: "{selected_value}" is not same as'
                                         f'Expected selected value: "Spread"')
                else:
                    self.assertEqual(selected_value.upper(), market.upper(),
                                     msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                         f'Expected selected value: "{market.upper()}"')
            else:
                self.assertEqual(selected_value.upper(), market.upper(),
                                 msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                     f'Expected selected value: "{market.upper()}"')
        else:
            self._logger.info(msg=' "Market Selector" is not displayed in "tomorrow".')

    def test_007_repeat_steps_345(self, label1="1", label2="2", market=expected_list[0]):
        """
        DESCRIPTION: Repeat steps 3,4,5
        """
        self.__class__.leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(self.leagues) > 0:
            self.assertTrue(self.leagues, msg='Leagues not found')
            self.test_003_verify_text_of_the_labels_for_handicap_in_matches_tabtodayhandicap_in_lads_and_spread_in_coral(label1=label1, label2=label2)
            self.test_004_verify_displaying_of_preplay_events()
            self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
            self.site.wait_content_state_changed()
            self.test_005_verify_ga_tracking_for_the_handicap(market=market)
        else:
            no_events = self.site.contents.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_008_repeat_steps_345_for_the_future_tab(self, market=expected_list[0], label1="1", label2="2"):
        """
        DESCRIPTION: Repeat steps 3,4,5 for the 'Future' tab
        EXPECTED:
        """
        self.grouping_buttons.items_as_ordered_dict.get(self.days_list[1]).click()
        self.site.wait_content_state_changed()
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Rugby Leauge')
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            if self.handicap_market:
                if self.brand == 'bma':
                    self.assertEqual(selected_value, 'Spread',
                                     msg=f'Actual selected value: "{selected_value}" is not same as'
                                         f'Expected selected value: "Spread"')
                else:
                    self.assertEqual(selected_value.upper(), market.upper(),
                                     msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                         f'Expected selected value: "{market.upper()}"')
            else:
                self.assertEqual(selected_value.upper(), market.upper(),
                                 msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                     f'Expected selected value: "{market.upper()}"')

        else:
            self._logger.info(msg=' "Market Selector" is not displayed in "Future".')
        self.test_007_repeat_steps_345(market=market, label1=label1, label2=label2)

    def test_009_switch_back_to_today_tab(self, market=expected_list[0], label1="1", label2="2"):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        self.grouping_buttons.items_as_ordered_dict.get(self.days_list[2]).click()
        self.site.wait_content_state_changed()
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            if self.handicap_market:
                if self.brand == 'bma':
                    self.assertEqual(selected_value, 'Spread',
                                     msg=f'Actual selected value: "{selected_value}" is not same as'
                                         f'Expected selected value: "Spread"')
                else:
                    self.assertEqual(selected_value.upper(), market.upper(),
                                     msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                         f'Expected selected value: "{market.upper()}"')
            else:
                self.assertEqual(selected_value.upper(), market.upper(),
                                 msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                     f'Expected selected value: "{market.upper()}"')
        else:
            self._logger.info(msg=' "Market Selector" is not displayed in "Today".')
        self.__class__.leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        self.test_003_verify_text_of_the_labels_for_handicap_in_matches_tabtodayhandicap_in_lads_and_spread_in_coral(label1=label1, label2=label2)

    def test_010_repeat_step_1_9_for_the_below_markettotal_pointsexcept_step3(self, market=expected_list[1], label1=vec.sb.OVER.upper(), label2=vec.sb.UNDER.upper()):
        """
        DESCRIPTION: Repeat step 1-9 for the below market
        DESCRIPTION: Total Points(Except step(3)
        """
        self.__class__.handicap_market = False
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        self.test_001_verify_displaying_of_the_market_selector(market=self.expected_list[1])
        self.test_002_select_handicap_in_the_market_selector_dropdown_listhandicap_in_lads_and_spread_in_coral(market=self.expected_list[1], dispsort=self.expected_same_sort_handicap)
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_handicap(market=self.expected_list[1])
        self.__class__.grouping_buttons = self.site.contents.tab_content.grouping_buttons
        self.test_006_switch_to_the_tomorrow_tab(market=self.expected_list[1])
        self.test_007_repeat_steps_345(market=market, label1=label1, label2=label2)
        self.test_008_repeat_steps_345_for_the_future_tab(market=self.expected_list[1], label1=label1, label2=label2)
        self.test_009_switch_back_to_today_tab(market=self.expected_list[1], label1=label1, label2=label2)

    def test_011_verify_text_of_the_labels_for_total_points_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        """
        self.test_003_verify_text_of_the_labels_for_handicap_in_matches_tabtodayhandicap_in_lads_and_spread_in_coral(label1=vec.sb.OVER.upper(), label2=vec.sb.UNDER.upper())
