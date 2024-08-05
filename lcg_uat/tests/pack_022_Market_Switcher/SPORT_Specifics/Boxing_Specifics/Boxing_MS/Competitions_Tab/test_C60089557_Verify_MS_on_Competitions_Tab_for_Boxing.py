import pytest
import voltron.environments.constants as vec
import tests
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089557_Verify_MS_on_Competitions_Tab_for_Boxing(BaseBetSlipTest):
    """
    TR_ID: C60089557
    NAME: Verify MS on Competitions Tab for Boxing
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Boxing Competitions page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Boxing Competitions page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Fight Betting(WDW)| - "Fight Betting"
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
    Home = '1'
    Away = '2'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Boxing Landing page -> 'Competition' tab
        """
        if tests.settings.backend_env != 'prod':
            all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                         status=True)
            self.assertTrue(all_sports_status, msg='"All Sports" market switcher status is disabled')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='boxing',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Boxing sport')
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.boxing_config.category_id,
                                                           disp_sort_names='MR', primary_markets='|Fight Betting|')
            self.ob_config.add_autotest_boxing_event()
            self.ob_config.add_autotest_boxing_event()
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
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
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Boxing')
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        sleep(3)
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'"Dropdown arrow" is not pointing downwards')
            dropdown.click()
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
                dropdown.click()
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.upper()}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Fight Betting
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        actual_list = list(
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting]
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
        try:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_list[0]).click()
        except Exception:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[0]).click()
        leagues = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(leagues, msg='"Leagues" are not available')
        for league in leagues:
            header = league.fixture_header
            self.assertEqual(header.header1, self.Home,
                             msg=f'Actual fixture header "{header.header1}" does not equal to'
                             f'Expected "{self.Home}"')
            self.assertEqual(header.header2, vec.sb.DRAW,
                             msg=f'Actual fixture header "{header.header2}" does not equal to'
                             f'Expected "{vec.sb.DRAW}"')
            self.assertEqual(header.header3, self.Away,
                             msg=f'Actual fixture header "{header.header3}" does not equal to'
                             f'Expected "{self.Away}"')
            events = league.items_as_ordered_dict.values()
            self.assertTrue(events, msg='"Events" are not available')
            for event in events:
                self.site.wait_content_state_changed()
                bet_buttons = list(event.template.get_available_prices().values())
                self.assertEqual(len(bet_buttons), 3, msg=f'Actual Buttons: "{len(bet_buttons)}" are not same as'
                                 'Expected Buttons: "3".')
                self.site.wait_content_state_changed()
                bet_buttons[0].click()
                self.__class__.number_of_events = self.number_of_events + 1
                if not self.multiple:
                    if self.device_type == 'mobile':
                        self.site.wait_for_quick_bet_panel(timeout=10)
                        self.site.quick_bet_panel.selection.content.amount_form.input.value = 0.03
                        self.site.quick_bet_panel.place_bet.click()
                        self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(timeout=10),
                                        msg='Bet Receipt is not shown')
                        self.site.quick_bet_panel.header.close_button.click()
                        self.site.wait_content_state_changed(timeout=15)
                        self.__class__.multiple = True
                        bet_buttons[0].click()
                        self.site.wait_for_quick_bet_panel(timeout=10)
                        self.site.quick_bet_panel.add_to_betslip_button.click()
                        self.site.wait_content_state_changed()
                    else:
                        singles_section = self.get_betslip_sections().Singles
                        stake_name, stake = list(singles_section.items())[0]
                        self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts={stake_name: 0.03})
                        self.get_betslip_content().bet_now_button.click()
                        self.check_bet_receipt_is_displayed()
                        self.site.wait_content_state_changed(timeout=15)
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
                break
        if not self.number_of_events >= 2:
            raise Exception("Multiple betplacement not happened as the number of events are less than 2")

    def test_004_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_market_fight_betting(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below market
        DESCRIPTION: • Fight Betting
        EXPECTED: Bet should be placed successfully
        """
        # covered in step 3
