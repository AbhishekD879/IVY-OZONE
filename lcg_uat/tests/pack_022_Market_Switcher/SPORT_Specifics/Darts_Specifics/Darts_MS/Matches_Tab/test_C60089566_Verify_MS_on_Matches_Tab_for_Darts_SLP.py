import pytest
import random
import tests
import voltron.environments.constants as vec
from selenium.common.exceptions import WebDriverException
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60089566_Verify_MS_on_Matches_Tab_for_Darts_SLP(BaseBetSlipTest):
    """
    TR_ID: C60089566
    NAME: Verify MS on Matches Tab for Darts SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Darts landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Darts landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting(WW/WDW)| - "Match Result"
    PRECONDITIONS: * |Leg Handicap| - "Handicap"
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
    market_selector_options = [
        ('match_handicap',),
        ('total_180s_over_under',),
        ('most_180s',)
    ]
    inplay_list = []
    preplay_list = []

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        items = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())[0]
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

        if bet_button_qty == 2 and tests.settings.backend_env == 'prod':
            bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict))
        else:
            bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def verify_chevron_display(self):
        dropdown = self.site.darts.tab_content.dropdown_market_selector
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
                sleep(2)
                self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def verify_betplacement(self):
        if self.device_type == 'desktop':
            for tab_name, tab in list(self.site.darts.date_tab.items_as_ordered_dict.items()):
                tab.click()
                no_events = self.site.sports_page.tab_content.has_no_events_label()
                if no_events:
                    self._logger.info(f'No Events available in the "{tab_name}" tab')
                    continue
                else:
                    break
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.section_name, self.__class__.section = list(sections.items())[0]
        darts_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
            self.section_name)
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
        self.site.wait_splash_to_hide(10)
        if self.dropdown.is_expanded():
            self.dropdown.click()
        bet_button.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet panel is not opened')
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()
        # single betplacement through quick bet
        if self.device_type == 'mobile':
            bet_button = random.choice(list(bet_buttons.values()))
            self.site.wait_splash_to_hide(10)
            if self.dropdown.is_expanded():
                self.dropdown.click()
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
        # if len(events) >= 2:
        #     bet_button = random.choice(list(bet_buttons.values()))
        #     self.site.wait_splash_to_hide(10)
        #     if self.dropdown.is_expanded():
        #         self.dropdown.click()
        #     bet_button.click()
        #     if self.device_type == 'mobile':
        #         self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet panel is not opened')
        #         self.site.add_first_selection_from_quick_bet_to_betslip()
        #     bet_button = random.choice(list(event2_bet_buttons.values()))
        #     self.site.wait_splash_to_hide(10)
        #     if self.dropdown.is_expanded():
        #         self.dropdown.click()
        #     bet_button.click()
        #     self.site.open_betslip()
        #     self.place_multiple_bet()
        #     self.check_bet_receipt_is_displayed()
        #     self.site.close_betreceipt()
        # else:
        #     self._logger.info('*** can not place a multiple bet as there is only one event present***')

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Dart Landing page -> 'Matches tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='darts',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Darts sport')

        if tests.settings.backend_env != 'prod':
            all_sport_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                        status=True)
            self.assertTrue(all_sport_status, msg='"All Sport" Market switcher is disabled')
            self.cms_config.verify_and_update_sport_config(
                sport_category_id=self.ob_config.backend.ti.darts.category_id,
                disp_sort_names='MR,HL,WH,HH',
                primary_markets='|Match Betting|,|Total 180s Over/Under|,'
                                '|Most 180s|,|Leg Handicap|,|Leg Winner|,'
                                '|Match Betting Head/Head|,|Match Handicap|')
            self.ob_config.add_darts_event_to_darts_all_darts(markets=self.market_selector_options)
            self.__class__.section_name = 'DARTS - CHAMPIONSHIP LEAGUE'

        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.darts_config.category_id)

        self.site.login()
        self.navigate_to_page(name='sport/darts')
        self.site.wait_content_state(state_name='Darts')
        self.site.darts.tabs_menu.click_button(expected_tab_name)
        self.assertEqual(self.site.darts.tabs_menu.current, expected_tab_name,
                         msg=f'"{expected_tab_name}" tab is not active')

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
        if self.device_type == 'desktop':
            for tab_name, tab in list(self.site.darts.date_tab.items_as_ordered_dict.items()):
                tab.click()
                no_events = self.site.sports_page.tab_content.has_no_events_label()
                if no_events:
                    self._logger.info(f'No Events available in the "{tab_name}" tab')
                    continue
                else:
                    break
        self.__class__.actual_markets_list = list(self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.actual_markets_list, msg=' "Market selector" is not available for dart')
        self.__class__.dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        self.verify_chevron_display()
        selected_value = self.site.darts.tab_content.dropdown_market_selector.selected_market_selector_item
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.assertEqual(selected_value, vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()}"')
        else:
            self.assertEqual(selected_value, vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • Most 180s
        EXPECTED: • Handicap
        EXPECTED: • Total 180s
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        drop_down_list = self.site.darts.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(drop_down_list, msg=f'"Market Selector" dropdown list not opened')
        self.__class__.expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                                                           vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s,
                                                           vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way,
                                                           vec.siteserve.EXPECTED_MARKETS_NAMES.total_180s_over_under
                                                           ]
        actual_list = list(
            self.site.darts.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if tests.settings.backend_env == 'prod':
            pass
        else:
            self.assertListEqual(actual_list, self.expected_market_selector_options,
                                 msg=f'Actual List: "{actual_list} is not same as'
                                     f'Expected List: "{self.expected_market_selector_options}"')

        self.device.refresh_page()
        self.site.wait_content_state_changed()
        self.verify_betplacement()

    def test_003_select_match_result_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_market_selector_options[0]).click()
        if tests.settings.backend_env != 'prod':
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='TIE', header3='2')
        else:
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (applicable for mobile tablet only)
        EXPECTED: 'SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type in ['mobile', 'tablet']:
            try:
                sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
                section_name, self.section = list(sections.items())[0]
                self.__class__.has_see_all_link = self.section.group_header.has_see_all_link()
                self.assertTrue(self.has_see_all_link,
                                msg=f'*** SEE ALL link not present in the section %s' % section_name)
            except WebDriverException:
                self._logger.info(f'*** No more than one event found')

    def test_005_click_on_see_all(self):
        """
        DESCRIPTION: Click on 'SEE ALL'
        EXPECTED: User should be navigated to competition tab where whole list of available events(Preplay/Inplay) will be displayed for that particular Tournament/League with Market switcher dropdown
        """
        if self.device_type == 'mobile':
            self.site.wait_splash_to_hide()
            if self.has_see_all_link:
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
                            self.assertTrue(event_template.event_time,
                                            msg=' "Event time" not displayed')

                if len(self.inplay_list) > 0 and len(self.preplay_list) == 0:
                    self._logger.info(msg=f'Only "In-Play" events are available ')
                elif len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
                    self._logger.info(msg=f'Only "Pre-Play" events are available ')
                else:
                    self._logger.info(msg=f'Both "In-Play" and "Pre-play" events are available ')

    def test_006_repeat_step_3_for_the_following_markets_most_180s_handicap_total_180s(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Most 180s
        DESCRIPTION: • Handicap
        DESCRIPTION: • Total 180s
        """
        if self.device_type == 'mobile':
            self.site.back_button_click()
            self.site.wait_content_state_changed()
        # most 180s
        market = 'Most 180s'
        if tests.settings.backend_env != 'prod' or market in self.actual_markets_list:
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header3='2')
            self.verify_betplacement()

        # total 180s
        market = 'Most 180s'
        if tests.settings.backend_env != 'prod' or market in self.actual_markets_list:
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header3='2')
            self.verify_betplacement()

        # Handicap
        market = 'Handicap'
        if tests.settings.backend_env != 'prod' or market in self.actual_markets_list:
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')
        self.verify_betplacement()

    def test_007_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_most_180s_handicap_total_180s(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Most 180s
        DESCRIPTION: • Handicap
        DESCRIPTION: • Total 180s
        EXPECTED: Bet should be placed successfully
        """
        #  covered in step 002 & 006
