import pytest
import voltron.environments.constants as vec
import random
import tests
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089548_Verify_MS_on_Matches_Tab_for_Volleyball_SLP(BaseBetSlipTest):
    """
    TR_ID: C60089548
    NAME: Verify MS on Matches Tab for Volleyball SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Volleyball landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|,|Total Points|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Volleyball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting (WW)| - "Match Result"
    PRECONDITIONS: * |Set Handicap (Handicap)| - "Set Handicap"
    PRECONDITIONS: * |Total Match Points (Over/Under)| - "Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [
        ('match_set_handicap',),
        ('total_match_points',)]
    inplay_list = []
    preplay_list = []
    bet_amount = 0.1

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header2):
        first_accordion = self.site.contents.tab_content.accordions_list.first_item[1]
        events = first_accordion.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = first_accordion.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        self.assertEqual(event.header3, header2,
                         msg=f'Actual fixture header "{event.header3}" does not equal to'
                             f'Expected "{header2}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def place_bet_and_verify(self):
        volleyball_section = self.site.contents.tab_content.accordions_list.first_item[1]
        events = list(volleyball_section.n_items_as_ordered_dict().values())
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
            self.site.wait_splash_to_hide(10)
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
            sleep(5)
            bet_button.click()
            if self.device_type == 'mobile':
                sleep(3)
                self.site.add_first_selection_from_quick_bet_to_betslip()
            bet_button = random.choice(list(event2_bet_buttons.values()))
            self.site.wait_splash_to_hide(10)
            sleep(5)
            bet_button.click()
            self.site.open_betslip()
            self.place_multiple_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        else:
            self._logger.info('*** can not place a multiple bet as there is only one event present***')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Volleyball Landing Page -> 'Click on Matches Tab'
        """
        self.__class__.expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                                   self.ob_config.volleyball_config.category_id)
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.volleyball_config.category_id)
            for event in events:
                market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
                if not market:
                    continue
                class_name = event['event']['className'].split(' ')
                self.__class__.section_name = (class_name[-1] + ' - ' + event['event']['typeName']).upper()
        else:
            self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
            self.cms_config.verify_and_update_market_switcher_status(sport_name='volleyball', status=True)
            self.ob_config.add_volleyball_event_to_austrian_league(markets=self.event_markets)
            self.ob_config.add_volleyball_event_to_austrian_league(markets=self.event_markets)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.volleyball_config.category_id)
        self.site.login()
        self.navigate_to_page(name='sport/volleyball')
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')
        if tests.settings.backend_env == 'prod':
            today_tab = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
            if not today_tab:
                self.site.contents.tab_content.date_tab.tomorrow.click()
                tomorrow_tab = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
                if not tomorrow_tab:
                    self.site.contents.tab_content.date_tab.future.click()
                    future_tab = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
                    if not future_tab:
                        raise VoltronException('No events found in football for matches tab')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' Coral
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for volleyball')

        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                self.site.wait_content_state_changed(timeout=20)
                self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result,
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • Set Handicap
        EXPECTED: • Total Points
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        self.__class__.actual_markets_list  = list(
            self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_points]
        if self.actual_markets_list == ['']:
            self.actual_markets_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for market in self.actual_markets_list:
            self.assertIn(market, self.expected_list,
                          msg=f'Actual List: "{self.actual_markets_list}" is not same as'
                              f'Expected List: "{self.expected_list}"')

    def test_003_select_match_results_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Results' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        market = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        if tests.settings.backend_env != 'prod' or market in self.actual_markets_list:
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                market).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1="1", header2="2")
            self.device.refresh_page()
            self.place_bet_and_verify()

    def test_004_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2
        """
        # covered in step 3

    def test_005_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (applicable for mobile tablet only)
        EXPECTED: 'SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type == 'mobile':
            section_name, self.__class__.section = self.site.contents.tab_content.accordions_list.first_item
            self.assertTrue(self.section, msg=' "Sections" are not avaialbe')
            events = list(self.section.items_as_ordered_dict.values())
            if len(events) >= 1:
                self.__class__.has_see_all_link = self.section.group_header.has_see_all_link()
                self.assertTrue(self.has_see_all_link, msg=f'*** SEE ALL link present in the section %s' % section_name)
            else:
                self.__class__.has_see_all_link = None
                self._logger.info(msg=' "SEE ALL" link is not available')
        if self.device_type == 'mobile':
            if self.dropdown.is_expanded():
                self.dropdown.click()

    def test_006_click_on_see_all(self):
        """
        DESCRIPTION: Click on 'SEE ALL'
        EXPECTED: User should be navigated to competition tab where whole list of available events(Preplay/Inplay) will be displayed for that particular Tournament/League with Market switcher dropdown
        """
        if self.device_type == 'mobile':
            if self.has_see_all_link:
                self.section.group_header.see_all_link.click()
                self.site.wait_content_state('CompetitionLeaguePage')
                sections = self.site.competition_league.tab_content.accordions_list.n_items_as_ordered_dict()
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

    def test_007_repeat_step_2_6_for_the_following_markets_set_handicap_total_points_except_step_4(self):
        """
        DESCRIPTION: Repeat step 2-6 for the following markets:
        DESCRIPTION: • Set Handicap
        DESCRIPTION: • Total Points (except step 4)
        EXPECTED:
        """
        if self.device_type == 'mobile':
            self.site.back_button_click()
            self.site.wait_content_state_changed()

        self.actual_markets_list = list(
            self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if self.actual_markets_list == ['']:
            self.actual_markets_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        market = vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if tests.settings.backend_env != 'prod' or market in self.actual_markets_list:
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                market).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1="1", header2="2")
        if self.dropdown.is_expanded():
            self.dropdown.click()
        self.place_bet_and_verify()
        self.test_005_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only()
        if self.device_type == 'mobile':
            if self.dropdown.is_expanded():
                self.dropdown.click()
            self.test_006_click_on_see_all()

    def test_008_verify_text_of_the_labels_for_total_points_(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points '
        EXPECTED: Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under
        """
        if self.device_type == 'mobile':
            self.site.back_button_click()
            self.site.wait_content_state_changed()

        self.actual_markets_list = list(
            self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if self.actual_markets_list == ['']:
            self.actual_markets_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        market = vec.siteserve.EXPECTED_MARKETS_NAMES.total_points
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if tests.settings.backend_env != 'prod' or market in self.actual_markets_list:
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                market).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.OVER.upper(),
                                                          header2=vec.sb.UNDER.upper())
        if self.dropdown.is_expanded():
            self.dropdown.click()
        self.place_bet_and_verify()
        self.test_005_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only()
        if self.device_type == 'mobile':
            if self.dropdown.is_expanded():
                self.dropdown.click()
            self.test_006_click_on_see_all()

    def test_008_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_set_handicap_total_points(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Set Handicap
        DESCRIPTION: • Total Points
        EXPECTED: Bet should be placed successfully
        """
        # Covered in previous steps
