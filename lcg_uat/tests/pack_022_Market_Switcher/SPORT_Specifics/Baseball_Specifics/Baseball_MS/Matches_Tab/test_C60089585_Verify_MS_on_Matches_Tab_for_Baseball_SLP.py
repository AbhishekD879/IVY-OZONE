import random
import pytest
import tests
import voltron.environments.constants as vec
from selenium.common.exceptions import WebDriverException
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.frequent_blocker
@vtest
class Test_C60089585_Verify_MS_on_Matches_Tab_for_Baseball_SLP(BaseSportTest, BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C60089585
    NAME: Verify MS on Matches Tab for Baseball SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Baseball landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|,|Run Line|,|Total Runs|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Baseball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line| - "Money Line"
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
    event_markets = [('run_line',), ('total_runs',)]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None, header2=None):
        items = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
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

    def select_tab_with_events(self):
        if self.device_type == 'desktop' and tests.settings.backend_env == 'prod':
            self.site.baseball.date_tab.today.click()
            today_tab = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict
            self.section_name = list(today_tab.keys())[0]
            section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
                self.section_name)
            events = list(section.items_as_ordered_dict.values())
            if not today_tab or len(events) <= 1:
                self.site.baseball.date_tab.tomorrow.click()
                tomorrow_tab = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict
                self.section_name = list(tomorrow_tab.keys())[0]
                section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
                    self.section_name)
                events = list(section.items_as_ordered_dict.values())
                if not tomorrow_tab or len(events) <= 1:
                    self.site.baseball.date_tab.future.click()
                    future_tab = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict
                    if not future_tab:
                        raise VoltronException('No events found in base ball for matches tab')

    def verify_betplacement(self):
        if tests.settings.backend_env == 'prod':
            self.section_name = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.keys())[0]
        usa_ahl_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
            self.section_name)
        events = list(usa_ahl_section.items_as_ordered_dict.values())
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
        self.site.wait_splash_to_hide(10)
        if self.dropdown.is_expanded():
            self.dropdown.click()
        bet_button.click()
        if self.device_type == 'mobile':
            # single betplacement through quick bet
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet panel is not opened')
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            self.site.wait_content_state_changed()
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()
        else:
            self.site.open_betslip()
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        # Multiple betplacement
        if len(events) >= 2:
            bet_button = random.choice(list(bet_buttons.values()))
            self.site.wait_splash_to_hide(10)
            if self.dropdown.is_expanded():
                self.dropdown.click()
            bet_button.click()
            if self.device_type == 'mobile':
                self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet panel is not opened')
                self.site.add_first_selection_from_quick_bet_to_betslip()
            bet_button = random.choice(list(event2_bet_buttons.values()))
            self.site.wait_splash_to_hide(10)
            if self.dropdown.is_expanded():
                self.dropdown.click()
            bet_button.click()
            self.site.open_betslip()
            self.place_multiple_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        else:
            raise Exception('can not place a multiple bet as there is only one event present')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Baseball Landing Page -> 'Click on Matches Tab'
        """
        self.site.login()
        if tests.settings.backend_env != 'prod':
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='baseball',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for Base ball sport')
            all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                                 status=True)
            self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
            baseball_category_id = self.ob_config.baseball_config.category_id
            self.cms_config.verify_and_update_sport_config(sport_category_id=baseball_category_id,
                                                           disp_sort_names='HH,HL,WH',
                                                           primary_markets='|Money Line|,|Run Line|,|Total Runs|')
            event = self.ob_config.add_baseball_event_to_autotest_league(markets=self.event_markets)
            self.ob_config.add_baseball_event_to_autotest_league(markets=self.event_markets)
            self.__class__.eventID = event.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            full_section_name = event.ss_response['event']['categoryCode'] + self.get_accordion_name_for_event_from_ss(event=event_resp[0])
            self.__class__.section_name = full_section_name.replace('BASEBALL', '')
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

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' Coral
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Baseball')
        self.__class__.dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type == 'desktop':
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                sleep(2)
                self.assertFalse(self.dropdown.is_expanded(), msg=f'"Dropdown Arrow" is not pointing downwards')
        else:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            sleep(2)
            self.assertFalse(self.dropdown.is_expanded(), msg=f'"Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line,
                         msg=f'Actual market value: "{selected_value.upper()}" is not same as'
                             f'Expected market value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: * Money Line
        EXPECTED: * Total Runs
        EXPECTED: * Run Line
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        self.__class__.actual_markets_list = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if len(self.actual_markets_list) == 1:
            self.__class__.actual_markets_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.actual_markets_list, msg=f'"Market Selector" dropdown list not opened')
        expected_list = [vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line.title(),
                         vec.siteserve.EXPECTED_MARKET_SECTIONS.total_runs.title(),
                         vec.siteserve.EXPECTED_MARKET_SECTIONS.run_line.title()]
        if tests.settings.backend_env == 'prod':
            for market in self.actual_markets_list:
                self.assertIn(market, expected_list, msg=f'Actual Market: "{market}" is not present in the '
                                                         f'Expected Markets list:"{expected_list}"')
        else:
            self.assertListEqual(self.actual_markets_list, expected_list,
                                 msg=f'Actual list : "{self.actual_markets_list}" is not same as '
                                     f'Expected list : "{expected_list}"')

    def test_003_select_money_line_in_the_market_selector_dropdown_list(self, market='Money Line', bet_button_qty=2, header1='1', header3='2'):
        """
        DESCRIPTION: Select 'Money Line' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        if tests.settings.backend_env != 'prod' or market in self.actual_markets_list:
            try:
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    market).click()
            except Exception:
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    market).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=bet_button_qty, header1=header1,
                                                              header3=header3)
            self.select_tab_with_events()
            self.verify_betplacement()

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (applicable for mobile tablet only)
        EXPECTED: 'SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type in ['mobile', 'tablet']:
            try:
                sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
                section_name, self.__class__.section = list(sections.items())[0]
                has_see_all_link = self.section.group_header.has_see_all_link()
                self.assertTrue(has_see_all_link, msg=f'*** SEE ALL link not present in the section %s' % section_name)
            except WebDriverException:
                self._logger.info(f'*** No more than one event found')

    def test_005_click_on_see_all(self):
        """
        DESCRIPTION: Click on 'SEE ALL'
        EXPECTED: User should be navigated to competition tab where whole list of available events(Preplay/Inplay) will be displayed for that particular Tournament/League with Market switcher dropdown
        """
        if self.device_type in ['mobile', 'tablet']:
            try:
                self.site.wait_splash_to_hide()
                self.section.group_header.see_all_link.click()
                self.site.wait_content_state('CompetitionLeaguePage')
                sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No list of available events are present on competition league page')
            except WebDriverException:
                self._logger.info(f'*** No more than one event found')
            self.navigate_to_page(name='sport/baseball')
            self.site.wait_content_state(state_name='Baseball')

    def test_006_repeat_step_3_for_the_following_markets_total_runs_run_line(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: * Total Runs
        DESCRIPTION: * Run Line
        """
        self.test_003_select_money_line_in_the_market_selector_dropdown_list(market='Total Runs', bet_button_qty=2,
                                                                             header1='OVER', header3='UNDER')
        self.test_003_select_money_line_in_the_market_selector_dropdown_list(market='Run Line',
                                                                             bet_button_qty=2,
                                                                             header1='1', header3='2')

    def test_007_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_money_line_total_runs_run_line(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: * Money Line
        DESCRIPTION: * Total Runs
        DESCRIPTION: * Run Line
        EXPECTED: Bet should be placed successfully
        """
        # Covered in the previous steps
