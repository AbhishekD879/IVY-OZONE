import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Events with specific markets cannot be created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60089622_Verify_pre_selected_Handicap_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Snooker(BaseDataLayerTest):
    """
    TR_ID: C60089622
    NAME: Verify pre selected ‘Handicap WW’ MT is saved when switching b/w T/T/F on Matches Tab for Snooker
    DESCRIPTION: This test case verifies that previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future in Matches Tab
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Handicap|,|Total Frames|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Handicap(Handicap)|-"Handicap"
    PRECONDITIONS: |Total Frames Over/Under (Over/Under)|-"Total Frames"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    preplay_list = []
    inplay_list = []
    markets = [('match_handicap',), ('total_frames_over_under',)]
    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKET_SECTIONS.handicap.title(),
                                        vec.siteserve.EXPECTED_MARKET_SECTIONS.total_frames.title()]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None):
        items = list(self.site.snooker.tab_content.accordions_list.items_as_ordered_dict.values())[0]
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
        PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='snooker',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Snooker sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.snooker.category_id,
                                                       disp_sort_names='HH,MH,WH,HL',
                                                       primary_markets='|Match Result|,|Match Betting|,|Handicap Match Result|,'
                                                                       '|Total Frames Over/Under|,|Match Handicap|')
        self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.markets)
        tomorrow = self.get_date_time_formatted_string(days=1)
        self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.markets, start_time=tomorrow)
        future = self.get_date_time_formatted_string(days=7)
        self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.markets, start_time=future)
        event = self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.markets, disp_order=2)
        self.__class__.event_name = event.team1 + ' v ' + event.team2

        self.navigate_to_page(name='sport/snooker')
        self.site.wait_content_state('Snooker')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.snooker_config.category_id)
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
        EXPECTED: • 'Handicap' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Handicap' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Handicap' in 'Market selector' **Coral**
        """
        self.__class__.snooker_tab_content = self.site.snooker.tab_content
        self.assertTrue(self.snooker_tab_content.has_dropdown_market_selector(), msg='"Market selector" is not '
                                                                                     'available for Snooker')
        dropdown = self.snooker_tab_content.dropdown_market_selector
        if self.brand == 'bma':
            self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
            self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
        else:
            dropdown.click()
            sleep(2)
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        selected_value = dropdown.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')

    def test_002_select_handicap_in_the_market_selector_dropdown_list(self,
                                                                      market=vec.siteserve.EXPECTED_MARKET_SECTIONS.handicap.title()):
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
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            market).click()
        self.__class__.leagues = list(
            self.site.snooker.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')
        for league in self.leagues:
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
                    if market == 'Handicap':
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

    def test_003_verify_text_of_the_labels_for_handicap_in_matches_tabtoday(self):
        """
        DESCRIPTION: Verify text of the labels for 'Handicap' in Matches Tab(Today)
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')

    def test_004_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        leagues = list(
            self.snooker_tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(leagues, msg='Leagues not found')
        for league in leagues:
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
        self.assertFalse(len(self.inplay_list) > 0, msg='Inplay events are displayed in Matches Tab. It should not')
        if len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
            self._logger.info(msg=f'Only "Pre-Play" events are available ')

    def test_005_verify_ga_tracking_for_the_handicap(self,
                                                     market_name=vec.siteserve.EXPECTED_MARKET_SECTIONS.handicap.title()):
        """
        DESCRIPTION: Verify GA Tracking for the 'Handicap'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Handicap"
        EXPECTED: categoryID: "32"
        EXPECTED: })
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
                             'categoryID': 32,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_006_switch_to_the_tomorrow_tab(self, bet_button_qty=2, header1='1', header3='2'):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Handicap)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note:
        EXPECTED: If events are not present for Handicap market and if events are present for Total Frames market then Total Frames will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        self.site.snooker.date_tab.tomorrow.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=bet_button_qty, header1=header1,
                                                          header3=header3)

    def test_007_repeat_steps_345(self):
        """
        DESCRIPTION: Repeat steps 3,4,5
        EXPECTED: As per steps
        """
        self.test_003_verify_text_of_the_labels_for_handicap_in_matches_tabtoday()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_handicap(
            market_name=vec.siteserve.EXPECTED_MARKET_SECTIONS.handicap.title())

    def test_008_repeat_steps_345_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4,5 for the 'Future' tab
        EXPECTED: As per steps
        """
        self.site.snooker.date_tab.future.click()
        self.test_003_verify_text_of_the_labels_for_handicap_in_matches_tabtoday()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_handicap(
            market_name=vec.siteserve.EXPECTED_MARKET_SECTIONS.handicap.title())

    def test_009_switch_back_to_today_tab(self, bet_button_qty=2, header1='1', header3='2'):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        self.site.snooker.date_tab.today.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=bet_button_qty, header1=header1,
                                                          header3=header3)

    def test_010_repeat_steps_2_9_for_the_below_markets_total_frames_except_step3(self):
        """
        DESCRIPTION: Repeat steps 2-9 for the below markets
        DESCRIPTION: • 'Total Frames (Except Step3)
        EXPECTED: As per steps
        """
        self.test_002_select_handicap_in_the_market_selector_dropdown_list(
            market=self.expected_market_selector_options[1])
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_handicap(market_name=self.expected_market_selector_options[1])
        self.test_006_switch_to_the_tomorrow_tab(bet_button_qty=2, header1='OVER', header3='UNDER')
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_handicap(market_name=self.expected_market_selector_options[1])
        self.site.snooker.date_tab.future.click()
        self.test_004_verify_displaying_of_preplay_events()
        self.test_005_verify_ga_tracking_for_the_handicap(market_name=self.expected_market_selector_options[1])
        self.test_009_switch_back_to_today_tab(bet_button_qty=2, header1='OVER', header3='UNDER')

    def test_011_verify_text_of_the_labels_for_total_frames_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Frames' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under
        """
        # Covered in Step#10

    def test_012_verify_ga_tracking_for_the_total_frames(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Total Frames'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Total Frames"
        EXPECTED: categoryID: "32"
        EXPECTED: })
        """
        # Covered in step#10
