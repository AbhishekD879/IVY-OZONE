import pytest
import tests
import random
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.environments.constants.base.markets_abbreviation import MarketAbbreviation


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
@pytest.mark.timeout(900)
class Test_C60673618_Verify_MS_on_Matches_Tab_for_Basketball_SLP_Multiple_Bet_Placement(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C60673618
    NAME: Verify MS on Matches Tab for Basketball SLP Multiple Bet Placement
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Basketball landing page
    PRECONDITIONS: Precondition:
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing Page -> 'Click on Matches
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
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
    event_markets = [
        ('Match Result', {}),
        ('Handicap', {}),
        ('Handicap 2_way', {})
    ]

    # CMS Markets Config for Created Market in OB(Stg/tst only)
    cms_markets_names = [
        {
            "templateMarketName": "Match Result",
            "title": "Match Result",
            "aggregated": False
        },
        {
            "templateMarketName": "Handicap",
            "title": "Handicap",
            "aggregated": False
        },
        {
            "templateMarketName": "Handicap 2_way",
            "title": "Handicap 2_way",
            "aggregated": False
        }
    ]

    def choose_events_for_aggregate_markets(self):
        current_page = self.site.sports_page
        sections = list(current_page.tab_content.accordions_list.items_as_ordered_dict.values())
        event_objects = list()
        for section in sections:
            if not section.is_expanded():
                section.expand()
            for event in list(section.items_as_ordered_dict.values()):
                event_objects.append(event)
        return event_objects

    def choosing_events(self):
        current_page = self.site.sports_page
        sections = list(current_page.tab_content.accordions_list.items_as_ordered_dict.values())
        none_aggregated_events = list()
        for section in sections:
            if not section.is_expanded():
                section.expand()
            for event in list(section.items_as_ordered_dict.values()):
                event_ = next((event for button in list(event.template.get_available_prices().values()) if
                               button.name.upper() not in ['N/A', 'SUSP']), None)
                if (event_ != None):
                    none_aggregated_events.append(event_)
                if len(none_aggregated_events) == 2:
                    break
            if len(none_aggregated_events) == 2:
                break
        return none_aggregated_events

    def select_active_events(self, all_events,
                             index_of_market):  # selecting two active events for aggregated markets to place multiple bet
        event1 = None
        event2 = None
        for event in all_events:
            market_section_objects = event.aggregated_template.get_market_sections
            bet_buttons = [button for button_name, button in
                           market_section_objects[index_of_market].get_bet_buttons.items() if
                           button_name.upper() not in ['N/A', 'SUSP']]
            if len(bet_buttons) == 0:
                continue
            else:
                if event1 == None:
                    event1 = event
                else:
                    event2 = event
                    break
        return [event1, event2]

    def click_random_bet_button(self, event, aggregated=False, index_of_market=None):
        if aggregated:
            market_section_objects = event.aggregated_template.get_market_sections
            bet_button_objects = list(market_section_objects[index_of_market].get_bet_buttons.values())
        else:
            bet_button_objects = list(event.template.get_available_prices().values())
        bet_button = next((button for button in bet_button_objects if
                           button.name.upper() not in ['N/A', 'SUSP']), None)  # getting active bet buttons
        bet_button.click()

    def verify_bet_placement(self, market, aggregated=False, market_names=[]):
        if aggregated:
            all_events = self.choose_events_for_aggregate_markets()
            # to place single bet, quick bet, multiple bet in every market for each aggregated market
            for index in range(len(market_names)):
                event1, event2 = self.select_active_events(all_events=all_events, index_of_market=index)
                # placing_single_bet
                if event1 != None:
                    self.click_random_bet_button(event1, aggregated=aggregated, index_of_market=index)
                    if self.device_type == 'mobile':
                        self.site.add_first_selection_from_quick_bet_to_betslip()
                    self.site.open_betslip()
                    self.place_single_bet()
                    self.check_bet_receipt_is_displayed()
                    self.site.close_betreceipt()
                else:
                    self._logger.info(f'there is no events for "{market_names[index]}"')
                    continue

                # placing quick bet
                if self.device_type == 'mobile':
                    self.click_random_bet_button(event1, aggregated=aggregated, index_of_market=index)
                    quick_bet = self.site.quick_bet_panel
                    quick_bet.selection.content.amount_form.input.value = self.bet_amount
                    self.site.wait_content_state_changed()
                    quick_bet.place_bet.click()
                    bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
                    self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
                    quick_bet.header.close_button.click()

                # placing multiple bet
                if event2 == None:
                    self._logger.info(f'there is no events for "{market_names[index]} to place multiple bet"')
                    continue
                self.click_random_bet_button(event1, aggregated=aggregated, index_of_market=index)
                if self.device_type == 'mobile':
                    self.site.add_first_selection_from_quick_bet_to_betslip()
                self.click_random_bet_button(event2, aggregated=aggregated, index_of_market=index)
                self.site.open_betslip()
                self.place_multiple_bet(number_of_stakes=1)
                self.check_bet_receipt_is_displayed()
                self.site.close_betreceipt()
            return

        none_aggregated_events = self.choosing_events()
        if len(none_aggregated_events) == 0:
            raise SiteServeException(f'events are not available for {market}')

        # single bet placement
        event, event2 = none_aggregated_events
        quick_bet = False
        if not quick_bet:
            random.choice(list(event.template.get_available_prices().values())).click()
            if self.device_type == 'mobile':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            self.site.open_betslip()
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
            quick_bet = True

        # quick bet
        if quick_bet and self.device_type == 'mobile':
            random.choice(list(event.template.get_available_prices().values())).click()
            sleep(3)
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            self.site.wait_content_state_changed()
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()

        # multiple bet
        if event2 == None:
            self._logger.info(f'there is no enough events for "{market} to place multiple bet"')
        else:
            self.click_random_bet_button(event)
            if self.device_type == 'mobile':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            self.click_random_bet_button(event2)
            self.site.open_betslip()
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None, header2=None,
                                                     aggregated=None, markets_qty=None):
        current_page = self.site.sports_page
        items = list(current_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        market_abbr = MarketAbbreviation.FIXTURE_HEADERS_MARKETS_ABBREVIATION
        cms_header1 = market_abbr.get(header1.lower().replace(' ', ''), None)
        header1 = [header1.upper(), cms_header1.upper()] if cms_header1 != None else [header1.upper()]
        self.assertIn(event.header1.upper(), header1,
                      msg=f'Actual fixture header "{event.header1}" does not equal to'
                          f'Expected "{header1}"')
        if header2:
            cms_header2 = market_abbr.get(header2.lower().replace(' ', ''), None)
            header2 = [header2.upper(), cms_header2.upper()] if cms_header2 != None else [header2.upper()]
            self.assertIn(event.header2.upper(), header2,
                          msg=f'Actual fixture header "{event.header2}" does not equal to'
                              f'Expected "{header2}"')
        cms_header3 = market_abbr.get(header3.lower().replace(' ', ''), None)
        header3 = [header3.upper(), cms_header3.upper()] if cms_header3 != None else [header3.upper()]
        self.assertIn(event.header3.upper(), header3,
                      msg=f'Actual fixture header "{event.header2}" does not equal to'
                          f'Expected "{header3}"')
        if aggregated:
            markets_count = list(events)[0].aggregated_template.get_aggregated_markets_count
            self.assertEqual(markets_count, markets_qty, f'Actual Number of Aggregate Markets is "{markets_count}"'
                                                         f'is not same as Expected Number of Aggregated Markets "{markets_qty}"')
        else:
            bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
            self.assertEqual(bet_buttons, bet_button_qty,
                             msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                                 f'Expected Buttons: "{bet_button_qty}".')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events  with scores
        EXPECTED: Event is successfully created
        """
        self.__class__.markets_fixture_headers = {'MATCH RESULT': ['HOME', 'DRAW'],
                                                  'TOTAL POINT': ['OVER', 'UNDER'],
                                                  'HANDICAP': ['1', '2'],
                                                  'HANDICAP 2-WAY': ['1', '2'],
                                                  'SPREAD': ['1', '2']
                                                  }
        matches_tab_enabled = self.cms_config.get_sport_tab_status(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.basketball_config.category_id)

        matches_tab_data = self.cms_config.get_sports_tab_data(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.basketball_config.category_id)

        is_market_switcher_enabled = self.cms_config.get_system_configuration_item('MarketSwitcher').get('basketball')

        if not is_market_switcher_enabled:
            raise CmsClientException('Market Switcher is Not Enabled for Basketball')

        self.__class__.cms_markets = matches_tab_data.get('marketsNames', None)

        if not self.cms_markets:
            raise CmsClientException('No One Market added for Market Switcher')

        self.__class__.expected_display_names = list()
        expected_none_aggregated_market_names = list()
        self.__class__.expected_aggregate_market_names = list()

        for market in self.cms_markets:
            self.expected_display_names.append(market.get('title').strip().title())
            self.expected_aggregate_market_names.append(market.get('title').strip().title()) if ',' in market.get(
                'templateMarketName') else expected_none_aggregated_market_names.append(
                market.get('title').strip().title())

        self.site.login()
        if tests.settings.backend_env != 'prod':
            self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball', status=True)
            self.cms_config.verify_and_update_sport_config(
                sport_category_id=self.ob_config.basketball_config.category_id,
                disp_sort_names='MR,WH,HL',
                primary_markets='|Match Betting|,|Handicap 2-way|,'
                                '|Total Match Points|',
                marketsNames=self.cms_markets_names
            )
            for i in range(0, 2):
                self.ob_config.add_basketball_event_to_us_league(markets=self.event_markets)

        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.basketball_config.category_id)
        self.navigate_to_page("sport/basketball")
        self.site.wait_content_state('basketball')
        tabs = self.site.contents.tabs_menu.items_as_ordered_dict
        if expected_tab_name not in tabs and not matches_tab_enabled:
            raise CmsClientException('Matches tab is not enabled')
        self.assertIn(expected_tab_name, list(tabs.keys()), f'expected tab {expected_tab_name} is not in {tabs}')
        tabs.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        if current_tab_name != expected_tab_name:
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
            current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' **Coral**
        """
        if tests.settings.backend_env == 'prod' and self.device_type == 'desktop':
            for tab_name, tab in list(self.site.sports_page.date_tab.items_as_ordered_dict.items()):
                tab.click()
                no_events = self.site.sports_page.tab_content.has_no_events_label()
                if no_events:
                    self._logger.info(f'No Events available in the "{tab_name}" tab')
                else:
                    break
        else:
            has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
            self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Basketball')

        dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                self.site.wait_content_state_changed(timeout=20)
                self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertIn(selected_value.title(), self.expected_display_names,
                      msg=f'Actual selected value: "{selected_value.title()}" is not in'
                          f'Market Selections: "{self.expected_display_names}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Money Line
        EXPECTED: • Total Points
        EXPECTED: • Handicap (Handicap in lads and Spread in Coral)
        EXPECTED: • Home Team Total Points
        EXPECTED: • Away Team Total Points
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        actual_list = list(
            self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if tests.settings.backend_env != 'prod':
            for item in actual_list:
                self.assertIn(item.title(), self.expected_display_names,
                              msg=f'Actual List item: "{item.title()}" is not present in Expected List: "{self.expected_display_names}"')

    def test_003_verify_bet_placement_for_multiple_bet_for_the_below_markets_money_line_total_points_handicap_handicap_in_lads_and_spread_in_coral_home_team_total_points_away_team_total_points(
            self):
        """
        DESCRIPTION: Verify Bet Placement for multiple Bet for the below markets
        DESCRIPTION: • Money Line
        DESCRIPTION: • Total Points
        DESCRIPTION: • Handicap (Handicap in lads and Spread in Coral)
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        EXPECTED: Bet should be placed successfully
        """
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict
        actual_markets = dropdown.keys()
        for market_name in actual_markets:
            dropdown.get(market_name).click()
            if market_name.title() in self.expected_aggregate_market_names:
                fixture_markets = next((cms_market.get('templateMarketName') for cms_market in self.cms_markets if
                                        cms_market.get('title').title() == market_name.title()), None).upper().split(
                    ',')
                if len(fixture_markets) == 2:
                    self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=0,
                                                                      header1=fixture_markets[0],
                                                                      header3=None,
                                                                      header2=fixture_markets[1],
                                                                      aggregated=True,
                                                                      markets_qty=2)
                else:
                    self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=0,
                                                                      header1=fixture_markets[0],
                                                                      header2=fixture_markets[1],
                                                                      header3=fixture_markets[2],
                                                                      aggregated=True,
                                                                      markets_qty=3)
                self.verify_bet_placement(market_name, aggregated=True, market_names=fixture_markets)

            elif market_name.upper() in list(self.markets_fixture_headers.keys()):
                # none aggregated markets
                fixture_headers = self.markets_fixture_headers[market_name.upper()]
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2,
                                                                  header1=fixture_headers[0],
                                                                  header3=fixture_headers[1])
                self.verify_bet_placement(market=market_name)
            dropdown = self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict
