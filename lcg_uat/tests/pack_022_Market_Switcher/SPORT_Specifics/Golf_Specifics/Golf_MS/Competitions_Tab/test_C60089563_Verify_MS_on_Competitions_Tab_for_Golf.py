import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.frequent_blocker
@vtest
class Test_C60089563_Verify_MS_on_Competitions_Tab_for_Golf(BaseBetSlipTest):
    """
    TR_ID: C60089563
    NAME: Verify MS on Competitions Tab for Golf
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Golf Competitions page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf Competitions page -> 'Matches' tab
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
    status = False
    event_markets = [('2_ball_betting',)]
    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting]

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
                         msg=f'Actual fixture header "{event.header2}" does not equal to'
                             f'Expected "{header3}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def bet_placement_single_multiple_quickBet(self):
        leagues = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        for league in leagues:
            events = league.items_as_ordered_dict.values()
            self.assertTrue(events, msg='"Events" are not available')
            for event in events:
                self.site.wait_content_state_changed()
                bet_buttons = list(event.template.items_as_ordered_dict.values())
                self.assertEqual(len(bet_buttons), 3, msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                                                          'Expected Buttons: "3".')
                self.site.wait_content_state_changed(timeout=15)
                bet_buttons[0].click()
                self.site.wait_content_state_changed()
                if not self.multiple:
                    if self.device_type == 'mobile':
                        self.site.wait_for_quick_bet_panel(timeout=10)
                        self.site.quick_bet_panel.selection.content.amount_form.input.value = 0.03
                        self.site.quick_bet_panel.place_bet.click()
                        self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(timeout=10),
                                        msg='Bet Receipt is not shown')
                        self.site.quick_bet_panel.header.close_button.click()
                        self.site.wait_content_state_changed()
                        self.__class__.multiple = True
                        bet_buttons[0].click()
                        self.site.wait_for_quick_bet_panel(timeout=10)
                        self.site.quick_bet_panel.add_to_betslip_button.click()
                        self.site.wait_content_state_changed(timeout=15)
                    else:
                        singles_section = self.get_betslip_sections().Singles
                        stake_name, stake = list(singles_section.items())[0]
                        self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts={stake_name: 0.03})
                        self.get_betslip_content().bet_now_button.click()
                        self.check_bet_receipt_is_displayed()
                        self.site.wait_content_state_changed()
                        self.__class__.multiple = True
                        bet_buttons[0].click()
                else:
                    self.site.open_betslip()
                    try:
                        singles_section = self.get_betslip_sections(multiples=True).Multiples
                    except Exception:
                        self.site.close_betslip()
                        bet_buttons[0].click()
                        self.site.open_betslip()
                        singles_section = self.get_betslip_sections(multiples=True).Multiples
                    stake_name, stake = list(singles_section.items())[0]
                    self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts={stake_name: 0.03})
                    self.get_betslip_content().bet_now_button.click()
                    self.check_bet_receipt_is_displayed()
                    self.__class__.status = True
                    break
            if self.status:
                self.__class__.multiple = False
                self.site.bet_receipt.close_button.click()
                self.device.refresh_page()
                self.site.wait_content_state_changed()
                break

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Golf Landing page -> 'Competition' tab
        """
        if tests.settings.backend_env != 'prod':
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='golf',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for golf sport')
            all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                                 status=True)
            self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
            self.ob_config.add_golf_event_to_golf_all_golf(markets=self.event_markets)
        self.site.login()
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.golf_config.category_id)
        self.site.wait_content_state('Homepage')
        self.navigate_to_page("sport/golf")
        self.site.wait_content_state(state_name='Golf')
        competitions_tab = self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name)
        self.assertTrue(competitions_tab, msg='"COMPETITIONS" tab is not displayed')
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
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
        EXPECTED: • '2 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '3 Ball Betting' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to '3 Ball Betting' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Golf Leauge')
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'"Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                wait_for_result(lambda: dropdown.is_expanded() is not True,
                                name=f'Market switcher expanded/collapsed',
                                timeout=5)
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • 3 Ball Betting
        EXPECTED: • 2 Ball Betting
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        actual_list = list(
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertListEqual(actual_list, self.expected_list,
                             msg=f'Actual List: "{actual_list} is not same as'
                                 f'Expected List: "{self.expected_list}"')

    def test_003_select_3_ball_betting_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select '3 Ball Betting' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[0]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='2',
                                                          header3='3')
        self.bet_placement_single_multiple_quickBet()

    def test_004_repeat_step_3_for_the_following_markets_2_ball_betting(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • 2 Ball Betting
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[1]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='TIE',
                                                          header3='2')
        self.bet_placement_single_multiple_quickBet()

    def test_005_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_2_ball_betting_3_ball_betting(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • 2 Ball Betting
        DESCRIPTION: • 3 Ball Betting
        EXPECTED: Bet should be placed successfully
        """
        # covered in steps 3 & 4
