import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark. #Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089646_Verify_Handicap_WW_MT_on_Matches_Tab_for_Darts(BaseDataLayerTest):
    """
    TR_ID: C60089646
    NAME: Verify 'Handicap WW’ MT on Matches Tab for Darts
    DESCRIPTION: This test case verifies displaying of behaviour of ‘Handicap WW market’ Template in Matches Tab
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Darts Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'rawHandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Leg Handicap| - "Handicap"
    PRECONDITIONS: * |Total 180s Over/Under (Over/Under)| - "Total 180s"
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
    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.handicap,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.total_180s_over_under]
    event_markets = [
        ('match_handicap_1', {'handicap': expected_low_sort_handicap, 'disp_order': -3}),
        ('match_handicap_2', {'handicap': 1.0, 'disp_order': 7}),
        ('total_180s_over_under', {'handicap': expected_same_sort_handicap}),
        ('total_180s_over_under_1', {'handicap': 3.0})]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Darts event with scores
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='darts', status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Darts sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.darts.category_id,
                                                       disp_sort_names='MR,HL,WH,HH',
                                                       primary_markets='|Match Betting|,|Total 180s Over/Under|,'
                                                                       '|Most 180s|,|Leg Handicap|,|Leg Winner|,'
                                                                       '|Match Betting Head/Head|,|Match Handicap|')
        created_event = self.ob_config.add_darts_event_to_darts_all_darts(markets=self.event_markets)
        self.__class__.event_name = created_event.team1 + ' v ' + created_event.team2
        self.navigate_to_page(name='sport/darts')
        self.site.wait_content_state_changed(timeout=30)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.darts_config.category_id)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Handicap' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Handicap' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Spread' in 'Market selector' Coral
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for darts')
        self.__class__.dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                self.site.wait_content_state_changed(timeout=20)
                self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Handicap
        EXPECTED: • Total 180s
        """
        actual_list = list(
            self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for item in self.expected_list:
            self.assertIn(item, actual_list,
                          msg=f'Actual List: "{actual_list} is not same as'
                              f'Expected List: "{self.expected_list}"')

    def test_003_select_handicap_in_the_market_selector_dropdown_list(self, handicap_value=expected_low_sort_handicap):
        """
        DESCRIPTION: Select 'Handicap' in the 'Market Selector' dropdown list
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
        if self.handicap_market:
            options = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
            if not self.dropdown.is_expanded():
                self.dropdown.expand()
            options.get(self.expected_list[1]).click()
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

    def test_004_verify_text_of_the_labels_for_handicap(self, label1="1", label2="2"):
        """
        DESCRIPTION: Verify text of the labels for 'Handicap'
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2.
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
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present
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

    def test_006_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        # Covered in step 5

    def test_007_verify_ga_tracking_for_the_handicap(self, market=expected_list[1]):
        """
        DESCRIPTION: Verify GA Tracking for the 'Handicap'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Handicap"
        EXPECTED: categoryID: "13"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        options = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(market).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market,
                             'categoryID': 13,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_steps_3_7_for_the_below_market_total_180s_except_step4(self):
        """
        DESCRIPTION: Repeat steps 3-7 for the below market:
        DESCRIPTION: • Total 180s (except step4)
        EXPECTED:
        """
        self.__class__.handicap_market = False
        self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict. \
            get(self.expected_list[2]).click()
        self.test_003_select_handicap_in_the_market_selector_dropdown_list(
            handicap_value=self.expected_same_sort_handicap)
        self.test_005_verify_the_standard_match_event_details()
        self.test_007_verify_ga_tracking_for_the_handicap(
            market=self.expected_list[2])

    def test_009_verify_text_of_the_labels_for_total_180s(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total 180s'
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under.
        """
        self.test_004_verify_text_of_the_labels_for_handicap(label1=vec.sb.OVER.upper(), label2=vec.sb.UNDER.upper())
