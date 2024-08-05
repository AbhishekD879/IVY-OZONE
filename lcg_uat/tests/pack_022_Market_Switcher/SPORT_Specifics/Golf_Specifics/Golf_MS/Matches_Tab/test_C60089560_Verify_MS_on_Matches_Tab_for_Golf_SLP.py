import pytest
import random
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from selenium.common.exceptions import WebDriverException
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.sports_specific
@pytest.mark.golf_specific
@pytest.mark.adhoc_suite
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.frequent_blocker
@vtest
class Test_C60089560_Verify_MS_on_Matches_Tab_for_Golf_SLP(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C60089560
    NAME: Verify MS on Matches Tab for Golf SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Golf landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |3 Ball Betting| - "3 Ball Betting"
    PRECONDITIONS: * |2 Ball Betting| - "2 Ball Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    multiple = False
    event_markets = [
        ('2_ball_betting',)
    ]

    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting
                                        ]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        current_page = self.site.sports_page
        items = list(self.golf_tab_content.accordions_list.items_as_ordered_dict.values())[0]
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
        section_name = list(current_page.tab_content.accordions_list.items_as_ordered_dict)
        sections = self.site.golf.tab_content.accordions_list.items_as_ordered_dict
        golf_section = sections.get(section_name[0])
        name, odds_from_page = list(golf_section.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index],
                                   expected_odds_format="fraction")

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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Golf events  with scores
        EXPECTED: Event is successfully created
        """
        if tests.settings.backend_env != 'prod':
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='golf',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Golf sport')
            all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                                 status=True)
            self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
            self.ob_config.add_golf_event_to_golf_all_golf(markets=self.event_markets)
            self.ob_config.add_golf_event_to_golf_all_golf(markets=self.event_markets)
        self.site.login()
        self.navigate_to_page(name='sport/golf')
        self.site.wait_content_state('golf')

        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.golf_config.category_id)

        self.site.golf.tabs_menu.click_button(vec.SB.TABS_NAME_EVENTS.upper())

        self.__class__.remove_empty_if_any = [val for val in self.site.golf.tab_content.dropdown_market_selector.available_options if val!='' ]
        list_empty = []
        if len(self.remove_empty_if_any) == 0 :
            self.remove_empty_if_any = list_empty.append(
                self.site.golf.tab_content.dropdown_market_selector.selected_market_selector_item)

        self.__class__.market_selector_default_value = self.remove_empty_if_any[0]
        current_tab_name = self.site.contents.tabs_menu.current
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
        EXPECTED: • '3 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '3 Ball Betting' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to '3 Ball Betting' in 'Market selector' **Coral**
        """
        self.__class__.golf_tab_content = self.site.golf.tab_content
        self.assertTrue(self.golf_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on Golf landing page')

        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value

        dropdown = self.golf_tab_content.dropdown_market_selector
        self.assertEqual(dropdown.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{dropdown.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')
        if self.device_type == 'desktop':
            if self.brand == "bma":
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                self.assertTrue(dropdown.is_expanded(),
                                msg='chevron (pointing down) arrow not displayed')
        else:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • 3 Ball Betting
        EXPECTED: • 2 Ball Betting
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        self.__class__.available_markets = self.remove_empty_if_any
        for market in self.expected_market_selector_options:
            if market not in self.available_markets:
                raise VoltronException(f"{market} market is not available")

    def test_003_select_3_ball_betting_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select '3 Ball Betting' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        # 3 Ball Betting:
        self.site.golf.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_market_selector_options[0]).click()
        self.golf_tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.market_selector_default_value)
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='2',
                                                          header3='3')
        self.verify_bet_placement()

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_tablet_only(self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (applicable for mobile tablet only)
        EXPECTED: SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type in ['mobile', 'tablet']:
            try:
                sections = self.golf_tab_content.accordions_list.items_as_ordered_dict
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

    def test_006_repeat_step_3_for_the_following_markets_2_ball_betting(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • 2 Ball Betting
        EXPECTED: As per step
        """
        self.navigate_to_page(name='sport/golf')
        self.site.wait_content_state('golf')
        self.site.golf.tabs_menu.click_button(vec.SB.TABS_NAME_EVENTS.upper())
        # 2 Ball Betting:
        self.site.golf.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_market_selector_options[1]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='TIE',
                                                            header3='2')
        self.verify_bet_placement()


    def test_007_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_2_ball_betting_3_ball_betting(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • 2 Ball Betting
        DESCRIPTION: • 3 Ball Betting
        EXPECTED: Bet should be placed successfully
        """
        # Covered in step#3 & 6
