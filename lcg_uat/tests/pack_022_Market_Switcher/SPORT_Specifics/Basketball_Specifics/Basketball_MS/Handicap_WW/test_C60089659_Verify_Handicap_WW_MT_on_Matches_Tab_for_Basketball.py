import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089659_Verify_Handicap_WW_MT_on_Matches_Tab_for_Basketball(BaseDataLayerTest):
    """
    TR_ID: C60089659
    NAME: Verify 'Handicap WW’ MT on Matches Tab for Basketball
    DESCRIPTION: This test case verifies displaying behaviour of ‘Handicap WW market’ Template in Matches Tab
    PRECONDITIONS: Precondition:
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'rawHandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    markets = [
        ('total_points_1', {'handicap': 2}),
        ('handicap_2_way',),
        ('handicap_2_way_2', {'handicap': 3}),
        ('home_team_total_points',),
        ('home_team_total_points_2', {'handicap': 3}),
        ('away_team_total_points',),
        ('away_team_total_points_2', {'handicap': 3})]

    expected_handicap_value_to_display = 5

    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.total_points,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points,
                     ]

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the basketball Landing page -> 'Matches tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
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
        event = self.ob_config.add_basketball_event_to_basketball_autotest_handicap(markets=self.markets, disp_order=2)
        self.__class__.event_name = event.team1 + ' v ' + event.team2
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state('basketball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.basketball_config.category_id)
        self.site.basketball.tabs_menu.click_button(expected_tab_name)
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
        EXPECTED: • 'Total Points' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Total Points' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Total Points' in 'Market selector' Coral
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Basketball')
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.dropdown.click()
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                self.site.wait_content_state_changed(timeout=30)
                self.assertFalse(self.dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.total_points.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.total_points}"')
        except VoltronException:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.money_line.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.money_line}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Total Points
        EXPECTED: • Handicap (Handicap in Lads and Spread in Coral)
        EXPECTED: • Home Team Total Points
        EXPECTED: • Away Team Total Points
        """
        if self.brand == 'bma':
            self.expected_list[1] = 'Spread'
        self.__class__.actual_list = list(self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        actual_list = [element.title() for element in self.actual_list]
        for item in self.expected_list:
            self.assertIn(item, actual_list, msg=f'Actual List: "{item} is not same as Expected List: '
                                                 f'"{actual_list}"')

    def test_003_select_total_points_in_the_market_selector_dropdown_list(self,
                                                                          market=vec.siteserve.EXPECTED_MARKETS_NAMES.total_points.title()):
        """
        DESCRIPTION: Select 'Total Points' in the 'Market Selector' dropdown list
        EXPECTED: • Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value markets (with odds) will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        EXPECTED: Note- When multiple markets are created for the any handicap market , then user should be able to see one market for each market type in landing page and in EDP page whole list will be displayed with all the different handicap values for that particular market.
        """
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        self.site.wait_content_state_changed()
        self.__class__.leagues = list(
            self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
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
                    else:
                        odd1, odd2 = handicap[0].split('\n')[0], handicap[1].split('\n')[0]
                        self.assertGreater(float(odd1), 0,
                                           msg=f'Odd1 "{odd1}" is not positive for Handicap market as per dispsort value')
                        self.assertGreater(float(odd2), 0,
                                           msg=f'Odd2 "{odd2}" is not positive for Handicap market as per dispsort value')

    def test_004_verify_text_of_the_labels_for_total_points(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points'
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under.
        """
        fixture = self.leagues[0].fixture_header
        self.assertEqual(fixture.header1, vec.sb.FIXTURE_HEADER.over,
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{vec.sb.FIXTURE_HEADER.over}"')
        self.assertEqual(fixture.header3, vec.sb.FIXTURE_HEADER.under,
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{vec.sb.FIXTURE_HEADER.under}"')
        for league in self.leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                self.assertFalse(event_template.is_live_now_event, msg=f'Event: "{event}" is an "In-Play" Event')
                self.assertTrue(event_template.event_name, msg=' "Event Name" not displayed')
                self.assertTrue(event_template.event_time, msg=' "Event time" not displayed')
                self.assertTrue(event_template.has_markets, msg='There is no "More" markets link')
                self._logger.info(f'Only preplay events found in league:"{league}"')

    def test_005_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present
        """
        # this step is covered in test_004

    def test_006_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        # this step is covered in test_004

    def test_007_verify_ga_tracking_for_the_total_points(self,
                                                         market=vec.siteserve.EXPECTED_MARKETS_NAMES.total_points.title()):
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
        self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market,
                             'categoryID': 6,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_steps_3_7_for_the_below_market_home_team_total_points_away_team_total_points_handicap_except_step_4(
            self):
        """
        DESCRIPTION: Repeat steps 3-7 for the below market:
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        DESCRIPTION: • Handicap (except step 4)
        EXPECTED:
        """
        # for home team total points
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(
            market=self.actual_list[2])
        self.test_007_verify_ga_tracking_for_the_total_points(
            market=self.actual_list[2])

        # for away team total points
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(
            market=self.actual_list[3])
        self.test_007_verify_ga_tracking_for_the_total_points(
            market=self.actual_list[3])

        # for handicap
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(
            market=self.expected_list[1])
        self.test_007_verify_ga_tracking_for_the_total_points(
            market=self.expected_list[1])

    def test_009_verify_text_of_the_labels_for_handicap(self):
        """
        DESCRIPTION: Verify text of the labels for 'Handicap'
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2.
        """
        fixture = self.leagues[0].fixture_header
        self.assertEqual(fixture.header1, '1',
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{1}"')
        self.assertEqual(fixture.header3, '2',
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{2}"')
