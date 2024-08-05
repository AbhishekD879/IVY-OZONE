import pytest
import random
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from voltron.utils.helpers import do_request, get_response_url
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.desktop
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089569_Verify_MS_on_Competitions_Tab_Match_Result_Most_180s_for_Darts(BaseBetSlipTest):
    """
    TR_ID: C60089569
    NAME: Verify MS on Competitions Tab for Darts
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Darts Competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Darts Competition page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting(WW/WDW)| - "Match Result"
    PRECONDITIONS: * |Leg Handicap (Handicap)| - "Handicap"
    PRECONDITIONS: * |Total 180s Over/Under (Over/Under)| - "Total 180s"
    PRECONDITIONS: * |Most 180s (WDW)| - "Most 180s"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    market_selector_options = [('match_handicap',),
                               ('most_180s',)]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
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

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))

        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def place_bet_and_verify(self):
        darts_section = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = list(darts_section.items_as_ordered_dict.values())
        self.assertTrue(events, msg=f'Events is not found')
        if len(events) >= 2:
            event1, event2 = events[0], events[1]
            bet_buttons = event1.template.get_available_prices()
            self.assertTrue(bet_buttons, msg='No selections found')
            event2_bet_buttons = event2.template.get_available_prices()
            self.assertTrue(event2_bet_buttons, msg='No selections found')
        else:
            bet_buttons = events[0].template.get_available_prices()
            self.assertTrue(bet_buttons, msg='No selections found')

        # single betplacement
        bet_button = random.choice(list(bet_buttons.values()))
        # self.site.wait_splash_to_hide(10)
        if self.drop_down.is_expanded():
            self.drop_down.click()
        bet_button.click()
        if self.device_type == 'mobile':
            sleep(3)
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

        # single betplacement through quick bet
        if self.device_type == 'mobile':
            bet_button = random.choice(list(bet_buttons.values()))
            # self.site.wait_splash_to_hide(10)
            if self.drop_down.is_expanded():
                self.drop_down.click()
            bet_button.click()
            sleep(3)
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            self.site.wait_content_state_changed()
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()

        # Multiple betplacement
        if len(events) >= 2:
            bet_button = random.choice(list(bet_buttons.values()))
            self.site.wait_splash_to_hide(10)
            if self.drop_down.is_expanded():
                self.drop_down.click()
            bet_button.click()
            if self.device_type == 'mobile':
                sleep(3)
                self.site.add_first_selection_from_quick_bet_to_betslip()
            bet_button = random.choice(list(event2_bet_buttons.values()))
            # self.site.wait_splash_to_hide(10)
            if self.drop_down.is_expanded():
                self.drop_down.click()
            bet_button.click()
            self.site.open_betslip()
            self.place_multiple_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        else:
            self._logger.info('*** can not place a multiple bet as there is only one event present***')

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Dart Landing page -> 'Matches tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        competition_tab_data = self.cms_config.get_sports_tab_data(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            sport_id=self.ob_config.darts_config.category_id)
        self.__class__.expected_market_selector_options = [market.get('title').upper() for market in competition_tab_data.get('marketsNames')]
        self.site.login()
        self.__class__.expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                                   self.ob_config.darts_config.category_id)
        if tests.settings.backend_env != 'prod':
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='darts', status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Darts sport')
            all_sports_status = \
                self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
            self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.darts.category_id,
                                                           disp_sort_names='MR,HL,WH,HH',
                                                           primary_markets='|Match Betting|,|Total 180s Over/Under|,'
                                                                           '|Most 180s|,|Leg Handicap|,|Leg Winner|,'
                                                                           '|Match Betting Head/Head|,|Match Handicap|')

            event = self.ob_config.add_darts_event_to_darts_all_darts(markets=self.market_selector_options)
            self.__class__.event_name1 = event.team2 + ' v ' + event.team1
            event2 = self.ob_config.add_darts_event_to_darts_all_darts(markets=self.market_selector_options)
            self.__class__.event_name2 = event2.team2 + ' v ' + event2.team1

        self.navigate_to_page(name='sport/darts')
        self.site.wait_content_state(state_name='Darts')
        self.site.darts.tabs_menu.click_button(self.expected_tab_name)
        self.assertEqual(self.site.darts.tabs_menu.current, self.expected_tab_name,
                         msg=f'"{self.expected_tab_name}" tab is not active')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Darts')
        self.__class__.drop_down = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.drop_down.change_button, msg=f'"Change button" is not displayed')
            self.drop_down.click()
            self.assertFalse(self.drop_down.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.drop_down.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.drop_down.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.drop_down.click()
                wait_for_result(lambda: self.drop_down.is_expanded() is not True,
                                name=f'Market switcher expanded/collapsed',
                                timeout=5)
                self.assertFalse(self.drop_down.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.assertEqual(selected_value, vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')
        else:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • Most 180s
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        self.__class__.actual_markets_list = list(
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if self.actual_markets_list == ['']:
            self.actual_markets_list = list(
                self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for market_name in self.actual_markets_list:
            self.assertIn(market_name.upper(), self.expected_market_selector_options,
                          msg=f'Actual market_name: "{self.actual_markets_list} is not in'
                              f'Expected market_name: "{self.expected_market_selector_options}"')

    def test_003_select_match_result_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        options = self.site.competition_league.tab_content.dropdown_market_selector
        markets_dropdown_list = list(self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict)
        self.__class__.leauge_name = \
            list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0].sport_name
        for market_name in markets_dropdown_list[0:2]:
            try:
                self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    market_name).click()
            except Exception:
                self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    market_name).click()
            sleep(2)
            # Match Result
            if market_name == vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default:
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')
            # Most 180s
            elif market_name == vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s:
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='TIE', header3='2')
            self.place_bet_and_verify()
            options = self.site.competition_league.tab_content.dropdown_market_selector

    def test_004_repeat_step_3_for_the_following_markets_most_180s(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Most 180s
        """
        # This step is covered into step 3

    def test_005_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_most_180s(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Most 180s
        EXPECTED: Bet should be placed successfully
        """
        # This step is covered into step 3
