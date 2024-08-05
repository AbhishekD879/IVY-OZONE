import pytest
from tests.base_test import vtest
from time import sleep
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod : # Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher_bpp
@pytest.mark.market_switcher
@vtest
class Test_C60089588_Verify_MS_on_Competitions_Tab_for_Baseball(BaseSportTest, BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C60089588
    NAME: Verify MS on Competitions Tab for Baseball
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Baseball Competition page
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
    markets = [('run_line',), ('total_runs',)]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]

        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        self.assertEqual(event.header3, header3,
                         msg=f'Actual fixture header "{event.header3}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def select_event_place_bet(self, bet_type=None):

        if self.device_type == 'mobile' and bet_type == 'quickbet':
            list(list(self.events)[0].template.items_as_ordered_dict.values())[0].click()
            self.site.wait_for_quick_bet_panel(timeout=5)
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()

        if bet_type in ['single', 'multiple']:
            for bet_button_value, bet_button in list(list(self.events)[0].template.items_as_ordered_dict.items()):
                bet_button.click()
                sleep(2)
                if not bet_button.is_selected():
                    bet_button.click()
                if self.device_type == 'mobile' and self.site.wait_for_quick_bet_panel(timeout=5):
                    sleep(2)
                    self.site.add_first_selection_from_quick_bet_to_betslip()
                    self.site.wait_quick_bet_overlay_to_hide()
                    self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False),
                                     msg='Quick bet not closed')
            if bet_type == 'multiple':
                for bet_button_value, bet_button in list(list(self.events)[1].template.items_as_ordered_dict.items()):
                    bet_button.click()
                    sleep(2)
                    if not bet_button.is_selected():
                        bet_button.click()

            self.site.open_betslip()
            if bet_type == 'single':
                self.place_single_bet()
                self.check_bet_receipt_is_displayed(timeout=20, poll_interval=0.5)
                self.site.bet_receipt.close_button.click()
            else:
                self.place_multiple_bet()
                self.check_bet_receipt_is_displayed(timeout=20, poll_interval=0.5)
                self.site.bet_receipt.close_button.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate to baseball page
        EXPECTED: Event is successfully created
        """

        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='baseball', status=True)
        self.assertTrue(status, msg=f'The sport "baseball" is not checked')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.baseball_config.category_id,
                                                       disp_sort_names='HH,HL,WH', primary_markets='|Money Line|,|Run Line|,|Total Runs|')
        self.ob_config.add_baseball_event_to_autotest_league(markets=self.markets, min_bet=0.03)
        self.ob_config.add_baseball_event_to_autotest_league(markets=self.markets, min_bet=0.03)
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='homepage')
        self.site.login()
        self.navigate_to_page(name='sport/baseball')
        self.site.wait_content_state('baseball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.baseball_config.category_id)
        self.site.baseball.tabs_menu.click_button(expected_tab_name)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' Coral
        """

        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Baseball')
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(2)
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line,
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line}"')

    def test_002_clicktap_on_market_selector(self):

        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Money Line
        EXPECTED: • Run Line
        EXPECTED: • Total Runs
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """

        actual_list = list(
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKET_SECTIONS_TITLE.money_line,
                                        vec.siteserve.EXPECTED_MARKET_SECTIONS_TITLE.total_runs,
                                        vec.siteserve.EXPECTED_MARKET_SECTIONS_TITLE.run_line]
        self.assertListEqual(actual_list, self.expected_list,
                             msg=f'Actual List: "{actual_list} is not same as'
                                 f'Expected List: "{self.expected_list}"')

    def test_003_select_money_line_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Money Line' in the 'Market Selector' dropdown list
        EXPECTED: • Events will be displayed as per the below conditions
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[0]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')

    def test_004_repeat_step_3_for_the_following_markets_run_line_total_runs(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Run Line
        DESCRIPTION: • Total Runs
        """
        # total runs
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[1]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.SB.FIXTURE_HEADER.over,
                                                          header3=vec.SB.FIXTURE_HEADER.under)

        # run line
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_list[2]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')

    def test_005_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_money_line_run_line_total_runs(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Money Line
        DESCRIPTION: • Run Line
        DESCRIPTION: • Total Runs
        EXPECTED: Bet should be placed successfully
        """
        self.__class__.actual_markets_list = list(self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        for market in self.expected_list:
            self.site.sports_page.tab_content.dropdown_market_selector.scroll_to()
            self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()

            items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
            self.__class__.events = items.items_as_ordered_dict.values()
            self.assertTrue(self.events, msg='"Events" are not available')

            for bet_type in ['single', 'multiple', 'quickbet']:
                self.select_event_place_bet(bet_type=bet_type)
