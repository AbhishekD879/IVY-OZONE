import random
import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from selenium.common.exceptions import WebDriverException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089554_Verify_MS_on_Matches_Tab_for_Boxing_SLP(BaseBetSlipTest):
    """
    TR_ID: C60089554
    NAME: Verify MS on Matches Tab for Boxing SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Boxing  landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Boxing  landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Fight Betting (WDW)| - "Fight Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    multiple = False
    status = False
    number_of_events = 0
    HOME = '1'
    AWAY = '2'

    def verifying_tab(self, market):
        if self.device_type == 'desktop':
            for tab_name, tab in list(self.site.sports_page.date_tab.items_as_ordered_dict.items()):
                tab.click()
                no_events = self.site.sports_page.tab_content.has_no_events_label()
                if no_events or market not in list(
                        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys()):
                    self._logger.info(f'No Events available in the "{tab_name}" tab')
                else:
                    break

    def choosing_events(self):
        current_page = self.site.sports_page
        if self.multiple:
            self.__class__.sel_events = []
            sections = list(current_page.tab_content.accordions_list.items_as_ordered_dict.values())
            for section in sections:
                if not section.is_expanded():
                    section.expand()
                for event in list(section.items_as_ordered_dict.values()):
                    if len(self.sel_events) < 2:
                        sel_name, sel = random.choice(list(event.template.get_available_prices().items()))
                        sel.click()
                        try:
                            self.assertTrue(sel.is_selected(),
                                            msg=f'Selection "{sel_name}" is not selected from Event "{event.template.event_name}"')
                        except Exception:
                            sel.click()
                            self.assertTrue(sel.is_selected(),
                                            msg=f'Selection "{sel_name}" is not selected from Event "{event.template.event_name}"')
                        self.sel_events.append(event)
                        if len(self.sel_events) == 1 and self.device_type == 'mobile':
                            self.site.add_first_selection_from_quick_bet_to_betslip()
                    else:
                        break
                if len(self.sel_events) >= 2:
                    break
        else:
            section = list(current_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            if not section.is_expanded():
                section.expand()
            self.__class__.event = list(section.items_as_ordered_dict.values())[0]

    def verify_bet_placement(self):
        self.choosing_events()
        quick_bet = False
        if not quick_bet:
            random.choice(list(self.event.template.get_available_prices().values())).click()
            if self.device_type == 'mobile':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            self.site.open_betslip()
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
            quick_bet = True

        if quick_bet and self.device_type == 'mobile':
            random.choice(list(self.event.template.get_available_prices().values())).click()
            sleep(3)
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            self.site.wait_content_state_changed()
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()

        self.multiple = True
        self.choosing_events()
        if self.device_type != 'mobile':
            if len(self.sel_events) < 2:
                self.site.sports_page.date_tab.tomorrow.click()
                self.choosing_events()
            if len(self.sel_events) < 2:
                self.site.sports_page.date_tab.future.click()
                self.choosing_events()
        self.sel_events.clear()
        if self.multiple:
            self.site.open_betslip()
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        else:
            self._logger.info('***Can not place multiple bet as there is only one event present***')

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None, header2=None):
        current_page = self.site.sports_page
        items = list(current_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
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

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Boxing landing page -> 'Matches' tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        if tests.settings.backend_env != 'prod':
            all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                         status=True)
            self.assertTrue(all_sports_status, msg='"All Sports" market switcher status is disabled')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='boxing',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Boxing sport')
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.boxing_config.category_id,
                                                           disp_sort_names='MR',
                                                           primary_markets='|Fight Betting|')
            self.ob_config.add_autotest_boxing_event()
            self.ob_config.add_autotest_boxing_event()
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.boxing_config.category_id)
        self.site.login()
        self.navigate_to_page(name='sport/boxing')
        self.site.wait_content_state_changed()
        sport_title = self.site.boxing.header_line.page_title.text
        self.assertEqual(sport_title.upper(), vec.sb.BOXING.upper(),
                         msg=f'Actual page is "{sport_title}",instead of "{vec.sb.BOXING}"')
        self.site.boxing.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed(timeout=10)
        current_tab_name = self.site.boxing.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Fight Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Fight Betting' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Fight Betting' in 'Market selector' **Coral**
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
            has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
            self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Boxing')

        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
            dropdown.click()
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(2)
                self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
                dropdown.click()
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.upper(),
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.upper()}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Fight Betting
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        try:
            actual_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        except Exception:
            actual_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting]
        if tests.settings.backend_env != 'prod':
            self.assertEqual(self.expected_list, actual_list, msg=f'Actual market List: "{self.expected_list} is not same as'
                             f'Expected market List: "{actual_list}"')
        else:
            for market in self.expected_list:
                self.assertIn(market, actual_list, msg=f'Actual market: "{market} is not in'
                                                       f'Expected market List: "{actual_list}"')

    def test_003_select_fight_betting_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Fight Betting' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.verifying_tab(self.expected_list[0])
        if tests.settings.backend_env != 'prod' or self.expected_list[0] in list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys()):
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[0]).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=self.HOME,
                                                              header2=vec.sb.DRAW,
                                                              header3=self.AWAY)
            self.verify_bet_placement()

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (applicable for mobile tablet only)
        EXPECTED: SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type in ['mobile', 'tablet']:
            try:
                sections = self.site.boxing.tab_content.accordions_list.items_as_ordered_dict
                section_name, self.__class__.section = list(sections.items())[0]
                has_see_all_link = self.section.group_header.has_see_all_link()
                self.assertTrue(has_see_all_link, msg=f'*** SEE ALL link present in the section %s' % section_name)
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

    def test_006_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_market_fight_betting(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below market
        DESCRIPTION: • Fight Betting
        EXPECTED: Bet should be placed successfully
        """
        # covered in step 3
