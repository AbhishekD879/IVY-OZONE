import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089612_Verify_Handicap_WW_MT_on_Matches_Tab_for_Ice_Hockey(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089612
    NAME: Verify 'Handicap WW’ MT on Matches Tab for Ice Hockey
    DESCRIPTION: This test case verifies displaying of ‘Handicap WW market’ Template is beaviour in Matches tab
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Ice Hockey Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'HandicapValue' (2,2.5,3)etc  using the following Market Template Names:
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
        event_params = self.ob_config.add_ice_hockey_event_to_ice_hockey_autotest_handicap(markets=self.event_markets)
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        current_tab_name = self.site.ice_hockey.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Expected tab: "{self.expected_sport_tabs.matches}", Actual Tab: "{current_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • Primary Market is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Puck Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Puck Line' in 'Market selector' Coral
        """
        self.__class__.ice_hockey_tab_content = self.site.ice_hockey.tab_content
        sections = self.site.ice_hockey.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No Leagues present for IceHockey')
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
            market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.assertTrue(self.ice_hockey_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on IceHockey landing page')
        market_selector_default_value = market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else market_selector_default_value
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

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets:
        EXPECTED: *Puck Line
        EXPECTED: *Total Goals 2-way
        """
        actual_list = list(self.ice_hockey_tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for item in self.expected_list:
            self.assertIn(item, actual_list, msg=f'Actual List: "{actual_list} is not same as Expected List: '
                                                 f'"{self.expected_list}"')

    def test_003_select_puck_line_in_the_market_selector_dropdown_list(self, handicap_value=expected_low_sort_handicap):
        """
        DESCRIPTION: Select 'Puck Line' in the 'Market Selector' dropdown list
        EXPECTED: Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        EXPECTED: Note- When multiple markets are created for the any handicap market , then user should be able to see one market for each market type in landing page and in EDP page whole list will be displayed with all the different handicap values for that particular market.
        """
        if self.handicap_market:
            options = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
            if not self.dropdown.is_expanded():
                self.dropdown.expand()
            options.get(self.expected_list[0]).click()
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

    def test_004_verify_text_of_the_labels_for_puck_line(self, label1="1", label2="2"):
        """
        DESCRIPTION: Verify text of the labels for 'Puck Line'
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels  '1' & '2'
        """
        fixture = self.leagues[0].fixture_header
        self.assertEqual(fixture.header1, label1,
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{label1}"')
        self.assertEqual(fixture.header3, label2,
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{label2}"')

    def test_005_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: Team names, date, time, watch signposting, "XX More" markets link are present
        """
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

    def test_006_verify_ga_tracking_for_the_puck_line(self, market=expected_list[0]):
        """
        DESCRIPTION: Verify GA Tracking for the 'Puck Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Puck Line"
        EXPECTED: categoryID: "22"
        EXPECTED: })
        """
        self.dropdown.scroll_to()
        options = self.ice_hockey_tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(market).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market,
                             'categoryID': 22,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_007_repeat_steps_3_7_for_the_below_markettotal_goals_2_wayexcept_step4(self):
        """
        DESCRIPTION: Repeat steps 3-7 for the below market:
        DESCRIPTION: Total Goals 2-way
        DESCRIPTION: (Except step4)
        """
        self.__class__.handicap_market = False
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        self.ice_hockey_tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_list[1]).click()
        self.test_003_select_puck_line_in_the_market_selector_dropdown_list(handicap_value=self.expected_same_sort_handicap)
        self.test_005_verify_the_standard_match_event_details()
        self.test_006_verify_ga_tracking_for_the_puck_line(market=self.expected_list[1])

    def test_008_verify_text_of_the_labels_for_total_goals_2_way(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Goals 2-way
        EXPECTED: Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels 'Over' & 'Under'
        """
        self.test_004_verify_text_of_the_labels_for_puck_line(label1=vec.sb.OVER.upper(), label2=vec.sb.UNDER.upper())
