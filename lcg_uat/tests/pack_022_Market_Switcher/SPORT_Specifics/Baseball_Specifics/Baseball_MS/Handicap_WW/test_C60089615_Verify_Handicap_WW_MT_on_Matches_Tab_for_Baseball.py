import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from voltron.utils.helpers import normalize_name
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.siteserve_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Cannot create events on prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089615_Verify_Handicap_WW_MT_on_Matches_Tab_for_Baseball(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089615
    NAME: Verify 'Handicap WW’ MT on Matches Tab for Baseball
    DESCRIPTION: This test case verifies displaying behaviour of ‘Handicap WW market’ Template in Matches Tab
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Run Line|,|Total Runs|, |Away Total Runs|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Baseball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'HandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Run Line (Handicap)| - "Run Line"
    PRECONDITIONS: * |Total Runs (Over/Under)| - "Total Runs"
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
    expected_list = ["Total Runs", "Run Line"]
    event_markets = [
        ('run_line_2', {'handicap': expected_low_sort_handicap, 'disp_order': -3}),
        ('run_line_3', {'handicap': 1.0, 'disp_order': 7}),
        ('total_runs', {'handicap': expected_same_sort_handicap}),
        ('total_runs_1', {'handicap': 3.0}), ]

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Baseball Landing Page -> 'Click on Matches Tab'
        """
        self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='baseball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for Baseball sport')
        baseball_category_id = self.ob_config.baseball_config.category_id
        self.cms_config.verify_and_update_sport_config(sport_category_id=baseball_category_id,
                                                       disp_sort_names='HH,HL,WH',
                                                       primary_markets='|Money Line|,|Run Line|,|Total Runs|')
        event_params = self.ob_config.add_baseball_event_to_autotest_handicap(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self.__class__.market_selector_default_value = self.expected_list[0]
        self.navigate_to_page(name='sport/baseball')
        self.site.wait_content_state(state_name='Baseball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.baseball_config.category_id)
        current_tab_name = self.site.sports_page.tabs_menu.current
        if current_tab_name != expected_tab_name:
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
            current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Total Points' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Total Runs' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Total Runs' in 'Market selector' Coral
        """
        baseball_tab_content = self.site.baseball.tab_content
        self.assertTrue(baseball_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on Baseball landing page')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), self.expected_list[0].upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{self.expected_list[0]}"')
        except VoltronException:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.money_line.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.money_line}"')
        self.__class__.dropdown = self.site.baseball.tab_content.dropdown_market_selector
        self.dropdown.click()
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing upwards')
        if self.brand == 'bma' and self.device_type == 'desktop':
            self.assertTrue(self.dropdown.has_up_arrow, msg='Market selector up arrow is not displayed')
            self.assertTrue(self.dropdown.has_down_arrow, msg='Market selector down arrow is not displayed')
        elif self.device_type == 'mobile' or self.brand == 'ladbrokes':
            # sleep provided as it takes some time to close the market switcher dropdown
            sleep(2)
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Total Runs
        EXPECTED: • Run Line
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        actual_list = list(self.site.baseball.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for item in self.expected_list:
            self.assertIn(item, actual_list, msg=f'Actual List: "{actual_list} is not same as Expected List: '
                                                 f'"{self.expected_list}"')

    def test_003_select_run_line_in_the_market_selector_dropdown_list(self, handicap_value=expected_low_sort_handicap, market_name=expected_list[1]):
        """
        DESCRIPTION: Select 'Run Line' in the 'Market Selector' dropdown list
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

        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market_name).click()
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
                                      msg=f'{handicap_value} value is not displayed as per dispsort value {actual_value}')
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

    def test_004_verify_text_of_the_labels_for_run_line(self, label1="1", label2="2"):
        """
        DESCRIPTION: Verify text of the labels for 'Run Line'
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels '1' & '2'
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
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present in the landing page
        """
        self.assertIn(self.event.first_player, self.event_name,
                      msg=f'First player name "{self.event.first_player}" is not present in "{self.event_name}"')
        self.assertIn(self.event.second_player, self.event_name,
                      msg=f'Second player name "{self.event.second_player}" is not present in "{self.event_name}"')
        self.assertTrue(self.event.has_set_number(), msg=f'"Date/Time" not displayed for the event "{self.event_name}')
        self.assertTrue(self.event.has_markets(),
                        msg=f'More Markets link not displayed for the event "{self.event_name}')

    def test_006_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        sections = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in sections.items():
            if not section.is_expanded():
                section.expand()
            events_list = section.items_as_ordered_dict
            for event_name, event in events_list.items():
                self.assertFalse(event.is_live_now_event, msg='"LIVE" label present on the event "{event_name}"')

    def test_007_verify_ga_tracking_for_the_run_line(self, market=expected_list[1]):
        """
        DESCRIPTION: Verify GA Tracking for the 'Run Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Run Line"
        EXPECTED: categoryID: "5"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        options = self.site.baseball.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(market).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market,
                             'categoryID': 5,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_steps_3_7_for_the_below_market_total_runs_expect_step_4(self):
        """
        DESCRIPTION: Repeat steps 3-7 for the below market:
        DESCRIPTION: * Total Runs (expect step 4)
        """
        self.__class__.handicap_market = False
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        self.site.baseball.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_list[0]).click()
        sleep(2)
        self.test_003_select_run_line_in_the_market_selector_dropdown_list(handicap_value=self.expected_same_sort_handicap, market_name=self.expected_list[0])
        self.test_005_verify_the_standard_match_event_details()
        self.test_007_verify_ga_tracking_for_the_run_line(market=self.expected_list[0])

    def test_009_verify_text_of_the_labels_for_above_markets(self):
        """
        DESCRIPTION: Verify text of the labels for above markets
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under
        """
        self.test_004_verify_text_of_the_labels_for_run_line(label1="OVER", label2="UNDER")
