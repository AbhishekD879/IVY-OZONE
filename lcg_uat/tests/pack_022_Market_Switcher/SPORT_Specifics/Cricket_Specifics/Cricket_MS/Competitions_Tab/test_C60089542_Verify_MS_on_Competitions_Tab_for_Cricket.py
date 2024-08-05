import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089542_Verify_MS_on_Competitions_Tab_for_Cricket(BaseBetSlipTest):
    """
    TR_ID: C60089542
    NAME: Verify MS on Competitions Tab for Cricket
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Cricket Competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Cricket landing page -> 'Competitions' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WDW & WW)| - "Match Result"
    PRECONDITIONS: |Total Sixes (Over/Under)| - "Total Sixes"
    PRECONDITIONS: |Next Over Runs (Main) (Over/Under)| - "Next Over Runs"
    PRECONDITIONS: |Team Runs (Main) (Over/Under)| - "Team Runs"
    PRECONDITIONS: |Runs At Fall Of Next Wicket (Over/Under)| - "Runs At Fall Of Next Wicket"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [
        ('total_sixes',),
        ('team_runs',),
        ('next_over_runs',),
        ('runs_at_fall_of_next_wicket',)]

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
        bet_buttons = len(list(events)[-1].template.get_available_prices())
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def place_bet_and_verify(self, bet_type=None):
        if self.device_type == 'mobile' and bet_type == 'quickbet':
            list(list(self.events)[0].template.items_as_ordered_dict.values())[0].click()
            self.site.wait_for_quick_bet_panel(timeout=5)
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()
        if bet_type in ['single', 'multiple']:
            for bet_button_value, bet_button in list(list(self.events)[0].template.items_as_ordered_dict.items()):
                bet_button.click()
                if not bet_button.is_selected():
                    bet_button.click()
                if self.device_type == 'mobile' and self.site.wait_for_quick_bet_panel(timeout=5):
                    self.site.add_first_selection_from_quick_bet_to_betslip()
                    self.site.wait_quick_bet_overlay_to_hide()
                    self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False),
                                     msg='Quick bet not closed')
            if bet_type == 'multiple':
                for bet_button_value, bet_button in list(list(self.events)[1].template.items_as_ordered_dict.items()):
                    bet_button.click()
                    if not bet_button.is_selected():
                        bet_button.click()
            self.site.open_betslip()
            if bet_type == 'single':
                self.place_single_bet()
                self.check_bet_receipt_is_displayed()
                self.site.bet_receipt.close_button.click()
            else:
                self.place_multiple_bet()
                self.check_bet_receipt_is_displayed()
                self.site.bet_receipt.close_button.click()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Cricket Landing page -> 'Click on Competitions Tab'
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" market switcher status is disabled')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Cricket sport')
        if tests.settings.backend_env != 'prod':
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.cricket_config.category_id,
                                                           disp_sort_names='MR,HH,WH,HL',
                                                           primary_markets='|Match Betting|,|Match Betting Head/Head|,|Total Sixes|,'
                                                                           '|Team Runs (Main)|,|Next Over Runs (Main)|,'
                                                                           '|Runs At Fall Of Next Wicket|')
            self.ob_config.add_autotest_cricket_event(markets=self.event_markets)
            self.ob_config.add_autotest_cricket_event(markets=self.event_markets)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.cricket_config.category_id)
        self.site.login()
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='cricket')
        try:
            self.site.competition_league.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        except Exception:
            self.device.refresh_page()
            self.site.wait_content_state(state_name='cricket')
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab_name = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{expected_tab_name}"')

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
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Cricket')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(),
                             vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')
        except Exception:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes}"')
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
            dropdown.click()
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(2)
                self.site.wait_content_state_changed()
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
                dropdown.click()

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • Total Sixes
        EXPECTED: • Next Over Runs
        EXPECTED: • Team Runs
        EXPECTED: • Runs At Fall Of Next Wicket
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        sleep(2)
        try:
            self.__class__.actual_list = self.site.competition_league.tab_content.dropdown_market_selector.available_options
            self.assertIsNotNone(self.actual_list, msg="Markets list is empty")
        except Exception:
            self.__class__.actual_list = self.site.competition_league.tab_content.dropdown_market_selector.available_options
        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.next_over_runs,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.team_runs,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.runs_at_fall_of_next_wicket]
        if tests.settings.backend_env == 'prod':
            for market in self.actual_list:
                self.assertIn(market, self.expected_list, msg=f'Actual Market: "{market}" is not present in the '
                                                              f'Expected Markets list:"{self.expected_list}"')
        else:
            self.assertListEqual(self.actual_list, self.expected_list,
                                 msg=f'Actual list : "{self.actual_list}" is not same as '
                                     f'Expected list : "{self.expected_list}"')

    def test_003_select_match_result_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        try:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[0]).click()
        except Exception:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[0]).click()
        if tests.settings.backend_env != 'prod':
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME,
                                                              header2=vec.sb.DRAW, header3=vec.sb.AWAY)
        elif vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default in self.actual_list:
            items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            events = items.items_as_ordered_dict.values()
            self.assertTrue(events, msg='"Events" are not available')
            event = items.fixture_header
            if len(event.items) > 2:
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME,
                                                                  header2=vec.sb.DRAW, header3=vec.sb.AWAY)
            else:
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1',
                                                                  header3='2')

    def test_004_repeat_step_3_for_the_following_markets_total_sixes_next_over_runs_team_runs_runs_at_fall_of_next_wicket(
            self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Total Sixes
        DESCRIPTION: • Next Over Runs
        DESCRIPTION: • Team Runs
        DESCRIPTION: • Runs At Fall Of Next Wicket
        """
        for market in self.actual_list:
            if market != vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default:
                self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    market).click()
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.OVER.upper(),
                                                                  header3=vec.sb.UNDER.upper())

    def test_005_Verify_Bet_Placement_for_Single_multiple_and_Quick_Bet_for_the_below_markets(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Total Sixes
        DESCRIPTION: • Next Over Runs
        DESCRIPTION: • Team Runs
        DESCRIPTION: • Runs At Fall Of Next Wicket
        EXPECTED: Bet should be placed successfully
        """
        self.__class__.actual_list = list(
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for market in self.expected_list:
            if market in self.actual_list:
                try:
                    self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
                except Exception:
                    self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                        market).click()
                self.site.wait_content_state('cricket')
                items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
                self.__class__.events = items.items_as_ordered_dict.values()
                self.assertTrue(self.events, msg='"Events" are not available')
                no_of_events = len(self.events)
                for bet_type in ['single', 'multiple', 'quickbet']:
                    if bet_type == 'multiple' and no_of_events < 2:
                        break
                    else:
                        self.place_bet_and_verify(bet_type=bet_type)
