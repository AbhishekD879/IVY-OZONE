import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089629_Verify_Handicap_WW_MT_in_Competitions_Tab_for_Volleyball(BaseDataLayerTest):
    """
    TR_ID: C60089629
    NAME: Verify ‘Handicap WW’ MT in Competitions Tab for Volleyball
    DESCRIPTION: This test case verifies behaviour of ‘Handicap WW market’ Template in Competition Tab
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Total Points|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Volleyball Landing Page -> 'Click on Competition Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Set Handicap (Handicap)| - "Set Handicap"
    PRECONDITIONS: * |Total Match Points (Over/Under)| - "Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    handicap_market = False
    preplay_list = []
    inplay_list = []
    markets = [('total_match_points', {'handicap': 2}),
               ('total_match_points_2', {'handicap': 3}),
               ('match_set_handicap_2', {'handicap': 3})]
    total_match_points_expected_handicap_value = 2
    match_set_handicap_expected_handicap_value = 5

    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.total_match_points]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate volleybal landing page
        EXPECTED: Event is successfully created
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='volleyball', status=True)
        self.assertTrue(status, msg=f'The sport "volleyball" is not checked')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.volleyball_config.category_id,
                                                       disp_sort_names='HH,MH,WH,HL,3W',
                                                       primary_markets='|Match Betting|,|Handicap Match Result|,|Match Set Handicap|,|Total Match Points|,|Set X Winner||Handicap 3-Way|')
        event = self.ob_config.add_volleyball_event_to_austrian_league_avl_set_handicap(markets=self.markets, disp_order=2)
        self.__class__.event_name = event.team1 + ' v ' + event.team2
        self.navigate_to_page(name='sport/volleyball')
        self.site.wait_content_state('volleyball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.volleyball_config.category_id)
        self.site.competition_league.tabs_menu.click_button(expected_tab_name)
        current_tab = self.site.competition_league.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Set Handicap' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Set Handicap' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Set Handicap' in 'Market selector' Coral
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for volleyball')
        self.__class__.dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                wait_for_result(lambda: self.dropdown.is_expanded() is not True,
                                name=f'Market switcher expanded/collapsed',
                                timeout=5)
                self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap.upper(),
                             msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap.upper()}"')
        except VoltronException:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap).click()

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Set Handicap
        EXPECTED: • Total Points
        """
        actual_list = list(self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for selector in self.expected_list:
            self.assertIn(selector, actual_list,
                          msg=f'Actual List: "{actual_list} is not same as'
                              f'Expected List: "{self.expected_list}"')

    def test_003_select_total_points_in_the_market_selector_dropdown_list(self, market=expected_list[1], handicap_value=total_match_points_expected_handicap_value):
        """
        DESCRIPTION: Select 'Total Points' in the 'Market Selector' dropdown list
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
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        self.__class__.leagues = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
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
                    for value in handicap:
                        actual_value = value.split('\n')[0]
                        self.assertIn(str(handicap_value), actual_value,
                                      msg=f'{handicap_value} value is not displayed as per dispsort value ')
                        if self.handicap_market:
                            if int(float(actual_value)) >= 0:
                                self.assertNotIn('-', actual_value,
                                                 msg=' "Negative value" present in button')
                            else:
                                self.assertIn('-', actual_value,
                                              msg=' "Negative value" not present in button')
                        else:
                            self.assertNotIn('-', actual_value,
                                             msg=' "Negative value" present in button')

    def test_004_verify_displaying_of_preplayinplay_or_both_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay/Inplay or both events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • Set Handicap (Preplay and Inplay market)
        EXPECTED: • Total Points (Preplay and Inplay market)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        for league in self.leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                is_live = event_template.is_live_now_event
                self.inplay_list.append(is_live) if is_live else self.preplay_list.append(is_live)
                odds = list(event_template.items_as_ordered_dict.values())
                for odd in odds:
                    self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                self.assertTrue(event_template.event_name,
                                msg=' "Event Name" not displayed')
                if is_live:
                    self._logger.info(f'{event_template.event_name} is live event')
                else:
                    self.assertTrue(event_template.event_time,
                                    msg=' "Event time" not displayed')
                if event_template.has_markets():
                    self._logger.info(f'{event_template.event_name} has more markets')
                else:
                    self._logger.info(f'{event_template.event_name} has no more markets')

        if len(self.inplay_list) > 0 and len(self.preplay_list) == 0:
            self._logger.info(msg=f'Only "In-Play" events are available ')
        elif len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
            self._logger.info(msg=f'Only "Pre-Play" events are available ')
        else:
            self._logger.info(msg=f'Both "In-Play" and "Pre-play" events are available ')

    def test_005_verify_text_of_the_labels_for_total_points(self, header_1=vec.sb.FIXTURE_HEADER.over, header_2=vec.sb.FIXTURE_HEADER.under):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points'
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under.
        """
        fixture = self.leagues[0].fixture_header
        self.assertEqual(fixture.header1, header_1,
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{header_1}"')
        self.assertEqual(fixture.header3, header_2,
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{header_2}"')

    def test_006_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        # covered in step 4

    def test_007_verify_ga_tracking_for_the_total_points(self, market=expected_list[1]):
        """
        DESCRIPTION: Verify GA Tracking for the 'Total Points'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Total points"
        EXPECTED: categoryID: "36"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        options = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(market).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market,
                             'categoryID': '36',
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_steps_3_7_for_the_below_market_set_handicapstep5(self):
        """
        DESCRIPTION: Repeat steps 3-7 for the below market:
        DESCRIPTION: • Set Handicap(step5)
        """
        self.__class__.handicap_market = True
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.\
            get(self.expected_list[0]).click()
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(market=self.expected_list[0], handicap_value=self.match_set_handicap_expected_handicap_value)
        self.test_004_verify_displaying_of_preplayinplay_or_both_events()
        self.test_007_verify_ga_tracking_for_the_total_points(market=self.expected_list[0])

    def test_009_verify_text_of_the_labels_for_set_handicap(self):
        """
        DESCRIPTION: Verify text of the labels for 'Set Handicap'
        EXPECTED: Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2.
        """
        self.test_005_verify_text_of_the_labels_for_total_points(header_1='1', header_2='2')
