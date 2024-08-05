import random
import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException

import tests
import voltron.environments.constants as vec
from selenium.common.exceptions import WebDriverException
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.sports_specific
@pytest.mark.snooker_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C60089575_Verify_MS_on_Matches_Tab_for_Snooker_SLP(BaseBetSlipTest):
    """
    TR_ID: C60089575
    NAME: Verify MS on Matches Tab for Snooker SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown in Matches tab for Snooker landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|,|Handicap|,|Total Frames|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WW)| - "Match Result"
    PRECONDITIONS: |Match Handicap (Handicap)| - "Handicap"
    PRECONDITIONS: |Total Frames Over/Under (Over/Under)| - "Total Frames"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [('total_frames_over_under',), ('match_handicap',)]

    def get_sport_tab_name_for_desktop(self, name):
        """
        :param name: field from CMS API - Sport Tabs Page
        :param category_id: sport category id
        :param raise_exceptions: whether raise exception on fail or not
        :return: field label for internal tab name
        """
        tabs_data = self.cms_config.get_sport_config(category_id=self.ob_config.snooker_config.category_id).get('tabs')
        if not tabs_data:
            raise CmsClientException(f'No tabs found for sport category id: "{self.ob_config.snooker_config.category_id}"')

        sport_tab_name = next((tab.get('label').upper() for tab in tabs_data if tab.get('name') == name), None)

        if not sport_tab_name:
            available_tabs = [tab.get('name') for tab in tabs_data]
            raise CmsClientException(f'"{name}" is not present in "{available_tabs}" for category "{self.ob_config.snooker_config.category_id}"')
        return sport_tab_name

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None, header2=None):
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
                         msg=f'Actual fixture header "{event.header2}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def verify_tab(self, market):
        if self.device_type == 'desktop' and tests.settings.backend_env == 'prod':
            count = 0
            for tab_name, tab in list(self.site.snooker.date_tab.items_as_ordered_dict.items()):
                tab.click()
                no_events = self.site.sports_page.tab_content.has_no_events_label()
                if no_events:
                    count = +1
                if no_events or market not in list(self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys()):
                    self._logger.info(f'No Events available in the "{tab_name}" tab')
                else:
                    break
            if count == 3:
                raise SiteServeException('There are not available events avaliable in matches tab for sport snooker in all date tabs')

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
        self.dropdown.scroll_to_we()
        if self.dropdown.is_expanded():
            self.dropdown.click()
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
            self.dropdown.scroll_to_we()
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
        PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
        """
        self.site.login()
        if tests.settings.backend_env != 'prod':
            all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                         status=True)
            self.assertTrue(all_sports_status, msg='Market switcher is disabled for All Sports')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='snooker',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Snooker sport')
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.snooker.category_id,
                                                           disp_sort_names='HH,MH,WH,HL',
                                                           primary_markets='|Match Result|,|Match Betting|,|Handicap Match Result|,'
                                                                           '|Total Frames Over/Under|,|Match Handicap|')
            event = self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.markets)
            self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.markets)
            self.__class__.section_name = event.ss_response['event']['categoryCode'] + ' - ' + event.ss_response['event']['typeName'].upper()

        self.navigate_to_page(name='sport/snooker')
        self.site.wait_content_state('Snooker')

        if self.device_type == 'desktop':
            expected_tab_name = self.get_sport_tab_name_for_desktop(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        else:
            expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                        self.ob_config.snooker_config.category_id)

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
        EXPECTED: • 'Mach betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Match betting' in 'Market selector' Coral
        """
        self.verify_tab(market=vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result.title())
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Snooker')
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
            self.assertFalse(self.dropdown.is_expanded(), msg=f'"Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result,
                         msg=f'Actual market value: "{selected_value.upper()}" is not same as'
                             f'Expected market value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • Handicap
        EXPECTED: • Total Frames
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        self.__class__.actual_markets_list = list(
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if self.actual_markets_list == ['']:
            self.__class__.actual_markets_list = list(
                self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertTrue(self.actual_markets_list, msg=f'"Market Selector" dropdown list not opened')

        matches_tab_data = self.cms_config.get_sports_tab_data(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.snooker_config.category_id)

        cms_markets = matches_tab_data.get('marketsNames')

        expected_list = [market.get('title').strip().title() for market in cms_markets]

        if tests.settings.backend_env == 'prod':
            for market in self.actual_markets_list:
                self.assertIn(market, expected_list, msg=f'Actual Market: "{market}" is not present in the '
                                                         f'Expected Markets list:"{expected_list}"')
        else:
            self.assertListEqual(self.actual_markets_list, expected_list,
                                 msg=f'Actual list : "{self.actual_markets_list}" is not same as '
                                     f'Expected list : "{expected_list}"')
        self.verify_betplacement()

    def test_003_select_handicap_in_the_market_selector_dropdown_list(self, market='Handicap', bet_button_qty=2,
                                                                      header1='1', header3='2'):
        """
        DESCRIPTION: Select 'Handicap' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.verify_tab(market=market)
        if tests.settings.backend_env != 'prod' or market in self.actual_markets_list:
            self.__class__.dropdown = self.site.sports_page.tab_content.dropdown_market_selector
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                market).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=bet_button_qty, header1=header1,
                                                              header3=header3)
            self.verify_betplacement()

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (applicable for mobile tablet only)
        EXPECTED: SEE All' option will be displayed when more than one event is there for that particular Tournament/League
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

    def test_006_repeat_step_3_for_the_following_markets_handicap_total_frames(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Handicap
        DESCRIPTION: • Total Frames
        """
        # Did for Handicap market in the 3rd step itself
        self.navigate_to_page(name='sport/snooker')
        self.site.wait_content_state('Snooker')
        self.test_003_select_handicap_in_the_market_selector_dropdown_list(market='Total Frames', bet_button_qty=2,
                                                                           header1='OVER', header3='UNDER')

    def test_007_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_handicap_total_frames(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Handicap
        DESCRIPTION: • Total Frames
        EXPECTED: Bet should be placed successfully
        """
        # Covered in the previous steps
