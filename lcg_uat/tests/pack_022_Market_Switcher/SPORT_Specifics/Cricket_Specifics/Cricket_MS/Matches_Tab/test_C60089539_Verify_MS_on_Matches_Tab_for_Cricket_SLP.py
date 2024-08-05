import pytest
import random
import tests
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.base_test import vtest
from selenium.common.exceptions import WebDriverException
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089539_Verify_MS_on_Matches_Tab_for_Cricket_SLP(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C60089539
    NAME: Verify MS on Matches Tab for Cricket SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Cricket landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Cricket Landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WDW & WW)| - "Match Result"
    PRECONDITIONS: |Total Sixes (Over/Under)| - "Total Sixes"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [
        ('total_sixes',)
    ]
    inplay_list = []
    preplay_list = []
    multiple = False

    def verifying_tab(self, market):
        if self.device_type == 'desktop':
            for tab_name, tab in list(self.site.sports_page.date_tab.items_as_ordered_dict.items()):
                tab.click()
                no_events = self.site.sports_page.tab_content.has_no_events_label()
                if no_events or market not in list(
                        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys()):
                    self._logger.info(f'No Events available in the "{tab_name}" tab')
                    raise Exception(f'No Events available in the "{tab_name}" tab')
                else:
                    break

    def choosing_events(self):
        if self.multiple:
            self.__class__.sel_events = []
            sections = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
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
            section = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            if not section.is_expanded():
                section.expand()
            self.__class__.event = list(section.items_as_ordered_dict.values())[0]

    def verify_bet_placement(self):
        self.choosing_events()
        bet_button = random.choice(list(self.event.template.get_available_prices().values()))
        try:
            bet_button.click()
        except Exception:
            dropdown = self.site.sports_page.tab_content.dropdown_market_selector
            if dropdown.is_expanded():
                dropdown.click()
            bet_button.click()
        sleep(3)
        if self.device_type == 'mobile':
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

        self.__class__.multiple = True
        self.choosing_events()
        if self.device_type != 'mobile':
            if len(self.sel_events) < 2:
                self.site.sports_page.date_tab.tomorrow.click()
                self.choosing_events()
            if len(self.sel_events) < 2:
                self.site.sports_page.date_tab.future.click()
                self.choosing_events()
        if len(self.sel_events) < 2:
            self.__class__.multiple = False
            self.site.open_betslip()
            self.clear_betslip()
        self.sel_events.clear()
        if self.multiple:
            self.site.open_betslip()
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        else:
            self._logger.info('***Can not place multiple bet as there is only one event present***')
        self.__class__.multiple = False

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
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
                         msg=f'Actual fixture header "{event.header3}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Cricket landing page -> 'Matches' tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        if tests.settings.backend_env != 'prod':
            all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
            self.assertTrue(all_sports_status, msg='"All Sports" market switcher status is disabled')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Cricket sport')
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.cricket_config.category_id,
                                                           disp_sort_names='MR,HH,MH,WH,HL',
                                                           primary_markets='|Match Betting|,|Match Betting Head/Head|,|Total Sixes|,|Team Runs (Main)|,|Next Over Runs (Main)|,|Runs At Fall Of Next Wicket|')
            self.ob_config.add_autotest_cricket_event(markets=self.event_markets)
            self.ob_config.add_autotest_cricket_event(markets=self.event_markets)
        self.site.login()
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state(state_name='cricket')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.cricket_config.category_id)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')
        self.__class__.cricket_tab_content = self.site.contents.tab_content

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
        if tests.settings.backend_env == 'prod' and self.device_type == 'desktop':
            for tab_name, tab in list(self.site.sports_page.date_tab.items_as_ordered_dict.items()):
                tab.click()
                no_events = self.site.sports_page.tab_content.has_no_events_label()
                if no_events:
                    self._logger.info(f'No Events available in the "{tab_name}" tab')
                else:
                    break
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for cricket')
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')
        except Exception:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes}"')
        self.__class__.dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
            self.dropdown.click()
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                self.site.wait_content_state_changed()
                self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
                self.dropdown.click()

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • Total Sixes
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        sleep(2)
        try:
            self.__class__.actual_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
            self.assertIsNotNone(self.actual_list, msg="Markets list is empty")
        except Exception:
            self.__class__.actual_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes]
        if tests.settings.backend_env == 'prod':
            for market in self.actual_list:
                self.assertIn(market, self.expected_list, msg=f'Actual market: "{market} is not in'
                                                              f'Expected market List: "{self.expected_list}"')
        else:
            for market in self.expected_list:
                self.assertIn(market, self.actual_list, msg=f'Actual market: "{market} is not in'
                              f'Expected market List: "{self.actual_list}"')

    def test_003_select_match_result_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        if self.dropdown.is_expanded():
            self.dropdown.click()
        self.verifying_tab(vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default)
        if tests.settings.backend_env != 'prod':
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME,
                                                              header2=vec.sb.DRAW, header3=vec.sb.AWAY)
            self.verify_bet_placement()
        elif vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default in self.actual_list:
            items = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            events = items.items_as_ordered_dict.values()
            self.assertTrue(events, msg='"Events" are not available')
            event = items.fixture_header
            if len(event.items) > 2:
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME,
                                                                  header2=vec.sb.DRAW, header3=vec.sb.AWAY)
            else:
                self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1',
                                                                  header3='2')
            self.verify_bet_placement()
        else:
            self._logger.info(f'*** Market {vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default} is not present')

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (applicable for mobile tablet only)
        EXPECTED: 'SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type in ['mobile', 'tablet']:
            try:
                section_name, self.__class__.section = self.site.sports_page.tab_content.accordions_list.first_item
                self.__class__.has_see_all_link = self.section.group_header.has_see_all_link()
                self.assertTrue(self.has_see_all_link, msg=f'*** SEE ALL link not present in the section %s' % section_name)
            except WebDriverException:
                self._logger.info(f'*** No more than one event found')

    def test_005_click_on_see_all(self):
        """
        DESCRIPTION: Click on 'SEE ALL'
        EXPECTED: User should be navigated to competition tab where whole list of available events(Preplay/Inplay) will be displayed for that particular Tournament/League with Market switcher dropdown
        """
        if self.device_type in ['mobile', 'tablet']:
            self.site.wait_splash_to_hide()
            if self.has_see_all_link:
                dropdown = self.site.contents.tab_content.dropdown_market_selector
                if dropdown.is_expanded():
                    dropdown.collapse()
                try:
                    self.section.group_header.see_all_link.click()
                except Exception:
                    dropdown.click()
                    self.section.group_header.see_all_link.click()
                self.site.wait_content_state('CompetitionLeaguePage')
                sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No list of available events are present on competition league page')
                for section in list(sections.values()):
                    events = list(section.items_as_ordered_dict.values())
                    for event in events:
                        event_template = event.template
                        is_live = event_template.is_live_now_event
                        self.inplay_list.append(is_live) if is_live else self.preplay_list.append(is_live)
                        odds = list(event_template.items_as_ordered_dict.values())
                        for odd in odds:
                            self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                        if is_live:
                            self._logger.info(f'{event_template.event_name} is live event')
                        else:
                            self.assertTrue(event_template.event_time, msg=' "Event time" not displayed')

                if len(self.inplay_list) > 0 and len(self.preplay_list) == 0:
                    self._logger.info(msg=f'Only "In-Play" events are available ')
                elif len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
                    self._logger.info(msg=f'Only "Pre-Play" events are available ')
                else:
                    self._logger.info(msg=f'Both "In-Play" and "Pre-play" events are available ')

    def test_006_repeat_steps_3_5_for_the_following_markets_total_sixes(self):
        """
        DESCRIPTION: Repeat steps 3-5 for the following markets:
        DESCRIPTION: • Total Sixes
        """
        # Total Sixes
        self.navigate_to_page(name='sport/cricket/matches')
        market_exists = vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes in list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if not market_exists:
            self._logger.info('No events for total sixes market')
            return 'No events for total sixes market'
        else:
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes).click()
        self.verifying_tab(vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes)

        if tests.settings.backend_env != 'prod':
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.OVER.upper(),
                                                              header3=vec.sb.UNDER.upper())
            self.verify_bet_placement()
        else:
            try:
                dropdown_exists = self.site.sports_page.tab_content.dropdown_market_selector.is_displayed()
            except Exception:
                dropdown_exists = False
            if dropdown_exists:
                market_exists = vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes in list(self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
                if market_exists:
                    self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes).click()
                    self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.OVER.upper(),
                                                                      header3=vec.sb.UNDER.upper())
                    self.verify_bet_placement()
                else:
                    self._logger.info('No events for total sixes market')
        self.test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only()
        self.test_005_click_on_see_all()

    def test_007_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_total_sixes(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Total Sixes
        EXPECTED: Bet should be placed successfully
        """
        # This step covered in above steps
