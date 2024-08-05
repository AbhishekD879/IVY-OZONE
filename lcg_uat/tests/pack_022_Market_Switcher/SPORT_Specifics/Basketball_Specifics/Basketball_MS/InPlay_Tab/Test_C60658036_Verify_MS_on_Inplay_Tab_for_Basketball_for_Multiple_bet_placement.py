import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep
from tests.base_test import vtest
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.in_play
@vtest
class Test_C60658036_Verify_MS_on_Inplay_Tab_for_Basketball_for_Multiple_bet_placement(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C60658036
    NAME: Verify MS on Inplay Tab for Basketball for Multiple bet placement
    DESCRIPTION: This test case verifies 'Market Selector' drop down displaying for Basketball on in-Play page (SLP-Basketball ->Inplay Tab) and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Basketball ->Inplay Tab and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB using the following market Templates:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    """
    keep_browser_open = True
    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER.upper()
    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.main_markets,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.money_line,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.half_total_points,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.quarter_total_points]
    event_markets = [
        ('total_points',),
        ('handicap_2_way',),
        ('half_total_points',),
        ('quarter_total_points',)]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events  with scores
        EXPECTED: Event is successfully created
        """
        self.get_active_events_for_category(category_id=self.ob_config.backend.ti.basketball.category_id,in_play_event=True)
        self.__class__.section_name = tests.settings.basketball_us_league
        if tests.settings.backend_env != 'prod':
            all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                           status=True)
            self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sport')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
            self.cms_config.verify_and_update_sport_config(
                sport_category_id=self.ob_config.backend.ti.basketball.category_id,
                disp_sort_names='HL,WH,HH',
                primary_markets='|Money Line|,|Total Points|,'
                                '|Home team total points|,|Away team total points|,'
                                '|Half Total Points|,|Quarter Total Points|,'
                                '|Handicap 2-way|')
            for index in range(0, 2):
                self.ob_config.add_basketball_event_to_us_league(markets=self.event_markets, is_live=True)
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.main_markets
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        self.site.login(username=tests.settings.betplacement_user)
        expected_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play
        self.site.basketball.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        expected_tab_name = self.get_sport_tab_name(expected_tab, self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        if tests.settings.backend_env != 'prod':
            self.assertEqual(current_tab_name, expected_tab_name,
                             msg=f'Actual tab: "{current_tab_name}" is not same as'
                                 f'Expected tab: "{expected_tab_name}".')

    def place_bet_and_verify(self):
        if self.brand == 'bma':
            sections = list(self.site.basketball.tab_content.accordions_list.items_as_ordered_dict.values())
        else:
            sections = list(self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections, msg='"Sections" are not available')
        selection_clicked = 0
        for section in sections:
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(' "Events" are not available')
            for event in events:
                selections = list(event.template.items_as_ordered_dict.values())
                self.assertTrue(' "Selections" are not available')
                for selection in selections:
                    if selection.is_enabled():
                        selection.click()
                        if self.device_type == 'mobile' and selection_clicked == 0:
                            self.site.add_first_selection_from_quick_bet_to_betslip()
                        selection_clicked += 1
                        sleep(3)
                        break
                if selection_clicked == 2:
                    break
            if selection_clicked == 2:
                break
        if selection_clicked == 2:
            self.site.open_betslip()
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        else:
            raise VoltronException('Not more than one event present to place multiple bet')

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: **Mobile:**
        EXPECTED:  The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED:  'Main Markets' option is selected by default
        EXPECTED:  'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: **Desktop:**
        EXPECTED:  The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED:  'Main Markets' option is selected by default
        EXPECTED:  'Change Market' button is placed next to  'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED:  'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(self.live_now_switcher)
            actual_btn = self.site.inplay.tab_content.grouping_buttons.current
            self.assertEqual(actual_btn, self.live_now_switcher, msg=f'"{self.live_now_switcher}" is not selected')
        self.__class__.basketball_tab_content = self.site.inplay.tab_content
        self.assertTrue(self.basketball_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on basketball landing page')

        if self.brand == 'bma':
            actual = self.site.basketball.tab_content.dropdown_market_selector.value
        else:
            actual = self.site.inplay.tab_content.selected_market
        self.assertEqual(actual.strip(), self.market_selector_default_value,
                         msg=f'Selected market selector "{actual}" is not the same as '
                             f'expected "{self.market_selector_default_value}"')
        self.__class__.dropdown = self.site.basketball.tab_content.dropdown_market_selector
        if self.device_type == 'desktop':
            if self.brand == "bma":
                self.assertFalse(self.dropdown.is_expanded(),
                                 msg='chevron (pointing down) arrow not displayed')
            else:
                self.assertTrue(self.dropdown.change_market_button, msg=f'"Change Market" button is not displayed')
                self.assertFalse(self.dropdown.is_expanded(),
                                 msg='chevron (pointing down) arrow not displayed')
        else:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change Market" button is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(),
                             msg='chevron (pointing down) arrow not displayed')

    def test_002_click_on_the_change_market_button_to_verify_options_available_for_basketball_in_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click on the 'Change Market' button to verify options available for Basketball in the Market selector dropdown
        EXPECTED: Market selector drop down becomes expanded (with chevron/arrow pointing upwards) with the below listed markets:
        EXPECTED:  Main Markets
        EXPECTED:  Money Line
        EXPECTED:  Total Points
        EXPECTED:  Handicap (Handicap in Lads and Spread in coral)
        EXPECTED:  Current Half Total Points
        EXPECTED:  Current Quarter Total Points
        EXPECTED: If any Market is not available it is not displayed in the Market selector drop-down list*
        """
        if self.brand == 'bma':
            available_markets = self.site.basketball.tab_content.dropdown_market_selector.available_options
            available_markets = [market.strip() for market in available_markets]
            available_markets[3] = "Handicap"
        else:
            available_markets = self.site.inplay.tab_content.dropdown_market_selector.available_options
        self.assertEqual(available_markets, self.expected_market_selector_options,
                         msg=f'Incorrect list/order of markets in Market Selector drop-down.\n'
                             f'Actual: {available_markets}\nExpected: {self.expected_market_selector_options}')

        for market_name in available_markets:
            sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found')
            us_autotest_section = sections.get(list(sections.keys())[0])
            self.assertTrue(us_autotest_section, msg=f'Section "{list(sections.keys())[0]}" not found')
            market_dropdown = self.site.basketball.tab_content.dropdown_market_selector
            if self.brand == 'bma' and market_name == "Handicap":
                market = available_markets.index(market_name)
                available_markets[market] = market_name = "Spread"
            if self.device_type != 'mobile' and self.brand == 'bma':
                market_dropdown.click()
                list(self.site.basketball.tab_content.dropdown_market_selector.options)[
                    available_markets.index(market_name)].click()
            elif self.device_type != 'mobile' and self.brand != 'bma':
                list(self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict.values())[
                    available_markets.index(market_name)].click()
            else:
                market_dropdown.click_item(market_name)
            self.place_bet_and_verify()

    def test_003_verify_bet_placement_for_multiple_bet_for_the_below_markets_money_line_total_points_handicap_handicap_in_lads_and_spread_in_coral_current_half_total_points_current_quarter_total_points(self):
        """
        DESCRIPTION: Verify Bet Placement for multiple Bet for the below markets
        DESCRIPTION:  Money Line
        DESCRIPTION:  Total Points
        DESCRIPTION:  Handicap (Handicap in Lads and Spread in coral)
        DESCRIPTION:  Current Half Total Points
        DESCRIPTION:  Current Quarter Total Points
        EXPECTED: Bet should be placed successfully
        """
        # covered in step 2
