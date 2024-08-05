import pytest
from crlat_cms_client.utils.exceptions import CMSException
import voltron.environments.constants as vec
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.market_switcher
@pytest.mark.timeout(1200)
@pytest.mark.sports
@pytest.mark.market_switcher_bpp
@vtest
class Test_C28635_Verify_Market_selector_drop_down_on_Football_landing_page(BaseBetSlipTest):
    """
    TR_ID: C28635
    NAME: Verify Market selector drop down on Football landing page
    DESCRIPTION: This Test Case verified Market selector drop down on Football landing page
    """
    keep_browser_open = True

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        items = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        if header2:
            self.assertEqual(event.header2, header2,
                             msg=f'Actual fixture header "{event.header2}" does not equal to'
                                 f'Expected "{header2}"')
        self.assertEqual(event.header3, header3,
                         msg=f'Actual fixture header "{event.header3}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(events)[-1].template.get_available_prices())
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def place_bet_and_verify(self):
        sections = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections,
                        msg='"Sections" are not available')
        for section in sections:
            if not section.is_expanded():
                section.expand()
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(' "Events" are not available')
            for event in events:
                selections = list(event.template.items_as_ordered_dict.values())
                self.assertTrue(' "Selections" are not available')
                for selection in selections:
                    if selection.is_enabled():
                        selection.click()
                        self.__class__.is_clicked = True
                        break
                if self.is_clicked:
                    break
            if self.is_clicked:
                break

        self.__class__.is_clicked = False
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=10), msg='Quick Bet panel is not opened')
            self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet Receipt is not displayed')
            self.site.quick_bet_panel.header.close_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Adds football events with different markets
        """
        if tests.settings.backend_env != 'prod':
            all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
            self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
            status = self.cms_config.verify_and_update_market_switcher_status(sport_name='football', status=True)
            self.assertTrue(status, msg=f'The sport "football" is not checked')

            markets = [
                ('to_qualify', ),
                ('over_under_total_goals', {'over_under': 2.5}),
                ('both_teams_to_score', ),
                ('draw_no_bet', ),
                ('first_half_result', )
            ]
            self.ob_config.add_autotest_premier_league_football_event(markets=markets)
        sport_tab_from_cms = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                    self.ob_config.football_config.category_id)
        # reading markets from cms_config
        expected_markets = self.cms_config.get_sports_tab_data(sport_id=self.ob_config.football_config.category_id, tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)['marketsNames']
        self.__class__.expected_market_selector_options = [market['title'].title() for market in expected_markets]
        tab_status = self.cms_config.get_sport_tab_status(sport_id=self.ob_config.football_config.category_id, tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        self.site.login()
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        tabs = self.site.football.tabs_menu.items_as_ordered_dict
        tabs_names = [tab.upper() for tab in tabs]
        # checking the tab status for frontend and from cms
        if not tab_status and sport_tab_from_cms.upper() not in tabs_names:
            raise CMSException(f' "{sport_tab_from_cms}" tab is not enabled in CMS for football')
        expected_sport_tab = self.site.football.tabs_menu.current
        self.assertEqual(expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{expected_sport_tab}"')

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: For tablet/mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing up) on the module header opens the MS dropdown
        EXPECTED: For desktop:
        EXPECTED: • 'Market selector' is displayed next to Date Selector (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market selector' drop down
        EXPECTED: • Up and down arrows are shown next to 'Match result' in 'Market selector'
        """
        if tests.settings.backend_env == 'prod':
            today_tab = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            if not today_tab:
                self.site.football.date_tab.tomorrow.click()
                tomorrow_tab = self.site.football.tab_content.accordions_list.items_as_ordered_dict
                if not tomorrow_tab:
                    self.site.football.date_tab.future.click()
                    future_tab = self.site.football.tab_content.accordions_list.items_as_ordered_dict
                    if not future_tab:
                        raise VoltronException('No events found in football for matches tab')
        football_tab_content = self.site.football.tab_content
        self.assertTrue(football_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on Football landing page')
        market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper() if self.brand == 'ladbrokes' and \
            self.device_type == 'desktop' else vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        self.assertEqual(football_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: {football_tab_content.dropdown_market_selector.selected_market_selector_item}\n'
                             f'Expected: {market_selector_default_value}')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • To Qualify
        EXPECTED: • Total Goals Over/Under 2.5
        EXPECTED: • Both Teams to Score
        EXPECTED: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: • Draw No Bet
        EXPECTED: • 1st Half Result
        EXPECTED: **Note:**
        EXPECTED: *If any Market is not available it is skipped in the Market selector drop down list*
        """
        available_markets = self.site.football.tab_content.dropdown_market_selector.available_options
        for market in available_markets:
            self.assertIn(market.title(), self.expected_market_selector_options,
                          msg=f'Actual market: {market} is not present in '
                              f'the Expected list: {self.expected_market_selector_options}')

    def test_003_select_match_results_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Results' in the 'Market Selector' dropdown list
        EXPECTED: * The events for selected market are shown
        EXPECTED: * Values on Fixture header are changed for each event according to selected market
        EXPECTED: * Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        options = self.site.football.tab_content.dropdown_market_selector
        match_result = options.selected_market_selector_item
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.assertEqual(match_result, vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual market: "{match_result}" not same as '
                                 f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')
        else:
            self.assertEqual(match_result, vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                             msg=f'Actual market: "{match_result}" not same as '
                                 f'"{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')
        options = self.site.football.tab_content.dropdown_market_selector
        markets_dropdown_list = list(options.items_as_ordered_dict.keys())
        for market in markets_dropdown_list:
            options.select_value(value=market)
            sleep(2)
            if market.upper() in [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.first_half_result.upper()]:
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='HOME', header2='DRAW', header3='AWAY')
            elif market.upper() in [vec.siteserve.EXPECTED_MARKETS_NAMES.to_qualify.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.draw_no_bet.upper()]:
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='HOME', header3='AWAY')
            elif market.upper() == vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5.upper():
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.SB.FIXTURE_HEADER.over, header3=vec.SB.FIXTURE_HEADER.under)
            elif market.upper() == vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score.upper():
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='YES', header3='NO')
            self.place_bet_and_verify()
            options = self.site.football.tab_content.dropdown_market_selector

    def test_004_repeat_step_3_for_the_following_markets_to_qualify_total_goals_overunder_25_both_teams_to_score_to_win_and_both_teams_to_score_ladbrokes_removed_from_ox_1003_match_result_and_both_teams_to_score_ladbrokes_added_from_ox_1003_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: * To Qualify
        DESCRIPTION: * Total Goals Over/Under 2.5
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        DESCRIPTION: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        EXPECTED:
        """
        # covered in step 003

    def test_005_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_to_qualify_total_goals_overunder_25_both_teams_to_score_to_win_and_both_teams_to_score_ladbrokes_removed_from_ox_1003_match_result_and_both_teams_to_score_ladbrokes_added_from_ox_1003_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Verify Bet Placement for Single and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • To Qualify
        DESCRIPTION: • Total Goals Over/Under 2.5
        DESCRIPTION: • Both Teams to Score
        DESCRIPTION: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        DESCRIPTION: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        DESCRIPTION: • Draw No Bet
        DESCRIPTION: • 1st Half Result
        EXPECTED: Bet should be placed successfully
        """
        # covered in step 003
