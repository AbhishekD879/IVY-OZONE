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
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60089643_Verify_MS_on_Matches_Tab_for_Ice_Hockey_SLP(BaseSportTest, BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C60089643
    NAME: Verify MS on Matches Tab for Ice Hockey SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Ice Hockey landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|,|60 Minute betting|,|Total Goals 2-way|,|Puck Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Ice Hockey Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|Money Line (WW)|- Money Line
    PRECONDITIONS: *|60 Minutes Betting (WDW)|- 60 Minute Betting
    PRECONDITIONS: *|Puck Line (Handicap)| - "Puck Line"
    PRECONDITIONS: *|Total Goals 2-way (Over/Under)| - "Total Goals 2-way"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [
        ('sixty_minutes_betting',),
        ('puck_line',),
        ('total_goals_2_way',)
    ]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None, header2=None):
        items = self.site.sports_page.tab_content.accordions_list.first_item[1]
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
                         msg=f'Actual fixture header "{event.header2}" does not equal to'
                             f'Expected "{header3}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def select_tab_with_events(self):
        if self.device_type == 'desktop' and tests.settings.backend_env == 'prod':
            self.site.ice_hockey.date_tab.today.click()
            self.section_name, section = self.site.ice_hockey.tab_content.accordions_list.first_item
            events = list(section.items_as_ordered_dict.values())
            if not section or len(events) <= 1:
                self.site.ice_hockey.date_tab.tomorrow.click()
                self.section_name, section = self.site.ice_hockey.tab_content.accordions_list.first_item
                events = list(section.items_as_ordered_dict.values())
                if not section or len(events) <= 1:
                    self.site.ice_hockey.date_tab.future.click()
                    future_tab = self.site.ice_hockey.tab_content.accordions_list.items_as_ordered_dict
                    if not future_tab:
                        raise VoltronException('No events found in ice hockey for matches tab')

    def verify_betplacement(self):
        self.section_name, usa_ahl_section = self.site.sports_page.tab_content.accordions_list.first_item
        usa_ahl_section.expand()
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
        PRECONDITIONS: Go to the IceHockey Landing Page -> 'Click on Matches Tab'
        """
        self.site.login()
        if tests.settings.backend_env != 'prod':
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='icehockey',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for IceHockey sport')
            all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                                 status=True)
            self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
            self.cms_config.verify_and_update_sport_config(
                sport_category_id=self.ob_config.backend.ti.ice_hockey.category_id,
                disp_sort_names='HH,WH,MR,HL',
                primary_markets='|Money Line|,|Total Goals 2-way|,|Puck Line|,|60 Minutes Betting|')
            event = self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets)
            self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets)
            self.__class__.eventID = event.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            full_section_name = event.ss_response['event']['categoryCode'] + self.get_accordion_name_for_event_from_ss(
                event=event_resp[0])
            self.__class__.section_name = full_section_name.replace('ICE_HOCKEY', '')
            self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.ice_hockey_config.category_id)
        current_tab_name = self.site.sports_page.tabs_menu.current
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
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Ice Hockey')
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
        EXPECTED: • Money Line
        EXPECTED: • Puck Line
        EXPECTED: • 60 Minute Betting
        EXPECTED: • Total Goals 2-way
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        self.__class__.actual_markets_list = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if len(self.actual_markets_list) == 1:
            self.__class__.actual_markets_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.actual_markets_list, msg=f'"Market Selector" dropdown list not opened')
        expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                         vec.siteserve.EXPECTED_MARKETS_NAMES.sixty_minutes_betting,
                         vec.siteserve.EXPECTED_MARKETS_NAMES.puck_line,
                         vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_2_way]
        if tests.settings.backend_env == 'prod':
            for market in self.actual_markets_list:
                self.assertIn(market, expected_list, msg=f'Actual Market: "{market}" is not present in the '
                                                         f'Expected Markets list:"{expected_list}"')
        else:
            self.assertListEqual(self.actual_markets_list, expected_list,
                                 msg=f'Actual list : "{self.actual_markets_list}" is not same as '
                                     f'Expected list : "{expected_list}"')

    def test_003_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (applicable for mobile tablet only)
        EXPECTED: 'SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type in ['mobile', 'tablet']:
            try:
                section_name, self.__class__.section = self.site.sports_page.tab_content.accordions_list.first_item
                has_see_all_link = self.section.group_header.has_see_all_link()
                self.assertTrue(has_see_all_link, msg=f'*** SEE ALL link not present in the section %s' % section_name)
            except WebDriverException:
                self._logger.info(f'*** No more than one event found')

    def test_004_click_on_see_all(self):
        """
        DESCRIPTION: Click on 'SEE ALL'
        EXPECTED: User should be navigated to competition tab where whole list of available events(Preplay/Inplay) will be displayed for that particular Tournament/League with Market switcher dropdown
        """
        if self.device_type in ['mobile', 'tablet']:
            try:
                self.site.wait_splash_to_hide()
                self.section.group_header.see_all_link.click()
                self.site.wait_content_state('CompetitionLeaguePage')
                sections = self.site.competition_league.tab_content.accordions_list.has_items
                self.assertTrue(sections, msg='No list of available events are present on competition league page')
            except WebDriverException:
                self._logger.info(f'*** No more than one event found')
            self.navigate_to_page(name='sport/ice-hockey')
            self.site.wait_content_state('IceHockey')

    def test_005_select_money_line_in_the_market_selector_dropdown_list(self, market='Money Line', bet_button_qty=2, header1='1', header2=None, header3='2'):
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
                                                              header2=header2,
                                                              header3=header3)
            self.select_tab_with_events()
            self.verify_betplacement()

    def test_006_repeat_step_3_for_the_following_markets_puck_line_60_minute_betting_total_goals_2_way(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Puck Line
        DESCRIPTION: • 60 Minute Betting
        DESCRIPTION: • Total Goals 2-way
        """
        self.test_005_select_money_line_in_the_market_selector_dropdown_list(market='Puck Line', bet_button_qty=2,
                                                                             header1='1', header3='2')
        self.test_005_select_money_line_in_the_market_selector_dropdown_list(market='60 Minutes Betting', bet_button_qty=3,
                                                                             header1='1', header2='TIE', header3='2')
        self.test_005_select_money_line_in_the_market_selector_dropdown_list(market='Total Goals 2-way', bet_button_qty=2,
                                                                             header1='OVER', header3='UNDER')

    def test_007_verify_bet_placements_for_single_multiple_and_quick_bet_for_the_below_markets_money_line_puck_line_60_minute_betting_total_goals_2_way(self):
        """
        DESCRIPTION: Verify Bet Placements for single, multiple and Quick bet for the below markets
        DESCRIPTION: • Money Line
        DESCRIPTION: • Puck Line
        DESCRIPTION: • 60 Minute Betting
        DESCRIPTION: • Total Goals 2-way
        EXPECTED: Bet should be placed successfully
        """
        # Covered in the previous steps
