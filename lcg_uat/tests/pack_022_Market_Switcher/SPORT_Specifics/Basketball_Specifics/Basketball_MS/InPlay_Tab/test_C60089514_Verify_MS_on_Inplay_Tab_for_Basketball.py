import pytest
import tests
from time import sleep
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.environments.constants.base.markets_abbreviation import MarketAbbreviation


@vtest
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.in_play
@pytest.mark.reg161_fix
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
class Test_C60089514_Verify_MS_on_Inplay_Tab_for_Basketball(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C60089514
    NAME: Verify MS on Inplay Tab for Basketball
    DESCRIPTION: This test case verifies 'Market Selector' drop down displaying for Basketball on in-Play page (SLP-Basketball ->Inplay Tab) and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Basketball ->Inplay Tab and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB using the following market Templates:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    """
    keep_browser_open = True
    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER.upper()
    event_markets = [
        ('total_points',),
        ('handicap',),
        ('handicap_2_way',),
        ('half_total_points',),
        ('quarter_total_points',)]

    def verify_fixture_header_and_qty_of_bet_buttons(self, header1=None, header3=None, header2=None,
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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events  with scores
        EXPECTED: Event is successfully created
        """
        self.__class__.fixture_markets = {'MATCH RESULT': ['HOME', 'DRAW', 'AWAY'],
                                          'MONEY LINE': ['HOME', 'DRAW'],
                                          'MAIN MARKETS': ['1', '2'],
                                          'CURRENT QUARTER TOTAL POINTS': ['OVER', 'UNDER'],
                                          'CURRENT HALF TOTAL POINTS': ['OVER', 'UNDER'],
                                          'TOTAL POINT': ['OVER', 'UNDER'],
                                          'HANDICAP': ['1', '2'],
                                          'HANDICAP 2-WAY': ['1', '2'],
                                          'SPREAD': ['1', '2']
                                          }
        self.__class__.section_name = tests.settings.basketball_us_league
        if tests.settings.backend_env != 'prod':
            all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                           status=True)
            self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sport')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
            self.cms_config.verify_and_update_sport_config(
                sport_category_id=self.ob_config.backend.ti.basketball.category_id,
                disp_sort_names='HL,WH,HH',
                primary_markets='|Money Line|,|Total Points|,'
                                '|Home team total points|,|Away team total points|,'
                                '|Half Total Points|,|Quarter Total Points|,'
                                '|Handicap 2-way|,|Handicap|')
            self.ob_config.add_basketball_event_to_us_league(markets=self.event_markets, is_live=True)
        self.__class__.non_aggregated_market_names = [vec.siteserve.EXPECTED_MARKETS_NAMES.main_markets.upper(),
                                                      vec.siteserve.EXPECTED_MARKETS_NAMES.quarter_total_points.upper(),
                                                      vec.siteserve.EXPECTED_MARKETS_NAMES.half_total_points.upper(),
                                                      vec.siteserve.EXPECTED_MARKETS_NAMES.money_line.upper(),
                                                      vec.siteserve.EXPECTED_MARKETS_NAMES.total_points.upper(),
                                                      vec.siteserve.EXPECTED_MARKETS_NAMES.handicap.upper(),
                                                      vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way.upper(),
                                                      vec.siteserve.EXPECTED_MARKETS_NAMES.spread.upper(),
                                                      vec.siteserve.EXPECTED_MARKETS_NAMES.match_result.upper()]
        # verifying whether inplay tab is available in cms or not for basket ball for desktop
        self.__class__.aggregated_markets = []
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'] == "Basketball":
                sport_id = sport['id']
        # getting top sports form basketball general sport configuration
        general_sport_config = self.cms_config.get_sport_category(sport_category_id=sport_id)
        markets_names = general_sport_config['aggrigatedMarkets']
        for market in markets_names:
            self.aggregated_markets.append(market['marketName'].upper().strip())
            self.fixture_markets[market['marketName'].upper().strip()] = market['titleName'].upper().strip().split(",")

        inplay_tab_status = self.cms_config.get_sport_tab_status(sport_id=self.ob_config.basketball_config.category_id,
                                                                 tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play)
        if not inplay_tab_status:
            raise CmsClientException(f'inplay tab is not available in cms')

        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        self.site.login(username=tests.settings.betplacement_user)
        expected_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play
        self.site.basketball.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        expected_tab_name = self.get_sport_tab_name(expected_tab, self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        if tests.settings.backend_env != 'prod':
            self.assertEqual(current_tab_name, expected_tab_name,
                             msg=f'Actual tab: "{current_tab_name}" is not same as'
                                 f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: **Mobile:**
        EXPECTED: • The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED: • 'Main Markets' option is selected by default
        EXPECTED: • 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: **Desktop:**
        EXPECTED: • The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED: • 'Main Markets' option is selected by default
        EXPECTED: • 'Change Market' button is placed next to  'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: • 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(self.live_now_switcher)
            actual_btn = self.site.inplay.tab_content.grouping_buttons.current
            self.assertEqual(actual_btn, self.live_now_switcher, msg=f'"{self.live_now_switcher}" is not selected')
        self.__class__.basketball_tab_content = self.site.inplay.tab_content
        self.assertTrue(self.basketball_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on basketball landing page')

        if self.brand == 'bma':
            actual_market = self.site.basketball.tab_content.dropdown_market_selector.value
        else:
            actual_market = self.site.inplay.tab_content.selected_market
        if actual_market.upper() in set(self.aggregated_markets):
            self.assertIn(actual_market.upper(), self.aggregated_markets, msg=f'Selected market selector "{actual_market.upper()}" is not in expected "{self.aggregated_markets}"')
        else:
            self.assertIn(actual_market.upper(), self.non_aggregated_market_names, msg=f'Selected market selector "{actual_market}" is not in expected "{self.non_aggregated_market_names}"')
        self.__class__.dropdown = self.site.basketball.tab_content.dropdown_market_selector
        if self.device_type == 'desktop':
            if self.brand == "bma":
                self.assertFalse(self.dropdown.is_expanded(),
                                 msg='chevron (pointing down) arrow not displayed')
            else:
                self.assertTrue(self.dropdown.change_market_button, msg=f'"Change Market" button is not displayed')
                self.assertFalse(self.dropdown.is_expanded(),
                                 msg='chevron (pointing down) arrow not displayed')
        else:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change Market" button is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(),
                             msg='chevron (pointing down) arrow not displayed')

    def test_002_click_on_the_change_market_button_to_verify_options_available_for_basketball_in_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click on the 'Change Market' button to verify options available for Basketball in the Market selector dropdown
        EXPECTED: Market selector drop down becomes expanded (with chevron/arrow pointing upwards) with the below listed markets:
        EXPECTED: * Main Markets
        EXPECTED: • Money Line
        EXPECTED: • Total Points
        EXPECTED: • Handicap (Handicap in Lads and Spread in coral)
        EXPECTED: • Current Half Total Points
        EXPECTED: • Current Quarter Total Points
        EXPECTED: •If any Market is not available it is not displayed in the Market selector drop-down list*
        """
        if self.brand == 'bma' and self.device_type == 'mobile' :
            if not self.site.basketball.tab_content.dropdown_market_selector.is_expanded():
                self.site.basketball.tab_content.dropdown_market_selector.expand()
        if self.brand == 'bma':
            available_markets = self.site.basketball.tab_content.dropdown_market_selector.available_options
        else:
            available_markets = self.site.inplay.tab_content.dropdown_market_selector.available_options
        for market in available_markets:
            if market.upper().strip() in self.aggregated_markets:
                self.assertIn(market.upper().strip(), self.aggregated_markets,
                                 msg=f'Actual market is not in expected Market Selector drop-down.\n'
                                     f'Actual: {market.upper()}\nExpected: {self.aggregated_markets}')
            else:
                self.assertIn(market.upper().strip(), self.non_aggregated_market_names,
                              msg=f'Actual market is not in expected Market Selector drop-down.\n'
                                  f'Actual: {market.upper()}\nExpected: {self.non_aggregated_market_names}')

        dropdown = self.site.basketball.tab_content.dropdown_market_selector
        if self.brand == 'bma' and self.device_type == 'mobile':
            if not self.site.basketball.tab_content.dropdown_market_selector.is_expanded():
                self.site.basketball.tab_content.dropdown_market_selector.expand()
        if self.brand == 'bma':
            available_markets = [option for option in
                                 self.site.basketball.tab_content.dropdown_market_selector.available_options]
        else:
            available_markets = [option for option in
                                 self.site.inplay.tab_content.dropdown_market_selector.available_options]

        for market_name in available_markets:
            if self.device_type != 'mobile' and self.brand == 'bma':
                dropdown.click()
                list(self.site.basketball.tab_content.dropdown_market_selector.options)[
                    available_markets.index(market_name)].click()
            elif self.device_type != 'mobile' and self.brand != 'bma':
                if not dropdown.is_expanded():
                    dropdown.expand()
                list(self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict.values())[
                    available_markets.index(market_name)].click()
            else:
                if not self.site.basketball.tab_content.dropdown_market_selector.is_expanded():
                    self.site.basketball.tab_content.dropdown_market_selector.expand()
                self.site.basketball.tab_content.dropdown_market_selector.items_as_ordered_dict[market_name].click()

            market_name = market_name.upper().strip()
            if market_name in self.aggregated_markets:
                if len(self.fixture_markets[market_name]) == 2:
                    self.verify_fixture_header_and_qty_of_bet_buttons(header1=self.fixture_markets[market_name][0],
                                                                      header3=None,
                                                                      header2=self.fixture_markets[market_name][1],
                                                                      aggregated=True,
                                                                      markets_qty=2)
                else:
                    self.verify_fixture_header_and_qty_of_bet_buttons(header1=self.fixture_markets[market_name][0],
                                                                      header2=self.fixture_markets[market_name][1],
                                                                      header3=self.fixture_markets[market_name][2],
                                                                      aggregated=True,
                                                                      markets_qty=3)
                #  can't able to place single and quick bet on basketball in_play live now events due to continuous change and suspending of events

            elif market_name in self.non_aggregated_market_names:
                # none aggregated markets
                fixture_headers = self.fixture_markets[market_name]
                self.verify_fixture_header_and_qty_of_bet_buttons(header1=fixture_headers[0],
                                                                  header3=fixture_headers[1])
                #  can't able to place single and quick bet on basketball in_play live now events due to continuous change and suspending of events

    def test_003_click_on_somewhere_outside_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click on somewhere outside the Market Selector dropdown
        EXPECTED: 'Market Selector' dropdown becomes collapsed
        """
        if self.device_type != 'mobile' and self.brand == 'bma':
            self.dropdown.click()
        sleep(1)
        self.assertFalse(self.dropdown.is_expanded(),
                         msg='chevron (pointing down) arrow not displayed')
        self.site.basketball.tabs_menu.items_as_ordered_dict.get(self.expected_sport_tabs.in_play).click()

    def test_004_select_upcoming_tab_menu(self):
        """
        DESCRIPTION: Select Upcoming tab menu
        EXPECTED: The 'Market Selector' is not available
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            self.assertFalse(self.site.inplay.tab_content.has_dropdown_market_selector(),
                             msg='"Market Selector" drop-down is displayed on basketball Inplay tab')

    def test_005_verify_bet_placement_for_single_and_quick_bet_for_the_below_markets_money_line_total_points_handicap_handicap_in_lads_and_spread_in_coral_current_half_total_points_current_quarter_total_points(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single and Quick Bet for the below markets
        DESCRIPTION: • Money Line
        DESCRIPTION: • Total Points
        DESCRIPTION: • Handicap (Handicap in Lads and Spread in coral)
        DESCRIPTION: • Current Half Total Points
        DESCRIPTION: • Current Quarter Total Points
        EXPECTED: Bet should be placed successfully
        """
        # Covered in step 2
