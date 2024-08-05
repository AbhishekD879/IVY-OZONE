import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60089633_Verify_MS_on_Competitions_Tab_for_Rugby_League(BaseBetSlipTest):
    """
    TR_ID: C60089633
    NAME: Verify MS on Competitions Tab for Rugby League
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Rugby League Competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Rugby League Landing page -> 'Competition' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting (WDW)| - "Match Result"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap 2-way"
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
        ('handicap_2_way', ),
        ('total_match_points', )]

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
                         msg=f'Actual fixture header "{event.header3}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def place_bet_and_verify(self):
        sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections,
                        msg='"Sections" are not available')
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
                        selection_clicked += 1
                        sleep(3)
                        if self.device_type == 'mobile' and selection_clicked == 1:
                            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=10), msg='Quick Bet panel is not opened')
                            self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
                            self.site.quick_bet_panel.place_bet.click()
                            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet Receipt is not displayed')
                            self.site.quick_bet_panel.header.close_button.click()
                        elif self.device_type == 'desktop' and selection_clicked == 1:
                            self.place_single_bet()
                            self.check_bet_receipt_is_displayed()
                            self.site.close_betreceipt()
                        elif self.device_type == 'mobile' and selection_clicked == 2:
                            self.site.add_first_selection_from_quick_bet_to_betslip()
                            sleep(3)
                            break
                        elif self.device_type == 'desktop' and selection_clicked == 2:
                            sleep(3)
                            break
                        elif selection_clicked == 3:
                            break
                if selection_clicked == 3:
                    break
            if selection_clicked == 3:
                break

        if selection_clicked == 3:
            self.site.open_betslip()
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        else:
            raise VoltronException('Not more than one event present to place multiple bet')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Rugby League Landing page -> 'Competition' tab
        """
        if tests.settings.backend_env != 'prod':
            all_sports = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
            self.assertTrue(all_sports, msg='"Allsports" is not enabled')
            status = self.cms_config.verify_and_update_market_switcher_status(sport_name='rugbyleague', status=True)
            self.assertTrue(status, msg='"rugby league" is not enabled')
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.rugby_league_config.category_id,
                                                           disp_sort_names='MR,WH,HL',
                                                           primary_markets='|Match Betting|,|Handicap 2-way|,'
                                                                           '|Total Match Points|')
            for i in range(2):
                self.ob_config.add_rugby_league_event_to_rugby_league_all_rugby_league(markets=self.event_markets)

        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.rugby_league_config.category_id)
        self.site.login()
        self.navigate_to_page("sport/rugby-league")
        self.site.wait_content_state(state_name='rugby-league')
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Accordions for the leagues should open with the initial load of the page
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Rugby Leauge')
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
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • Handicap 2 way(Handicap in coral and Handicap 2 way in Lads)
        EXPECTED: • Total Points
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        self.__class__.actual_market_list = list(self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.__class__.expected_market_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                                               vec.siteserve.EXPECTED_MARKETS_NAMES.rugby_handicap,
                                               vec.siteserve.EXPECTED_MARKETS_NAMES.total_points]

        for market in self.actual_market_list:
            self.assertIn(market, self.expected_market_list,
                          msg=f'Market "{market}" is not in expected market list')

    def test_003_select_match_results_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Results' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        if vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list[0]).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=vec.sb.HOME, header2=vec.sb.DRAW, header3=vec.sb.AWAY)
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default} is not in the actual market list')

    def test_004_repeat_step_3_for_the_following_markets_handicap_2_way_total_points(self):
        """
        DESCRIPTION: Repeat step 3 for the following markets:
        DESCRIPTION: • Handicap 2 way
        DESCRIPTION: • Total Points
        """
        # TODO: https://jira.egalacoral.com/browse/BMA-57952
        # Handicap 2 way market depends on above story
        # if vec.siteserve.EXPECTED_MARKETS_NAMES.rugby_handicap in self.actual_market_list:
        #     self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list[1]).click()
        #     self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')
        #     self.place_bet_and_verify()
        # else:
        #     self._logger.info(msg=f'Market {vec.siteserve.EXPECTED_MARKETS_NAMES.rugby_handicap} is not in the actual market list')

        # Total Points
        if vec.siteserve.EXPECTED_MARKETS_NAMES.total_points in self.actual_market_list:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(self.expected_market_list[2]).click()
            self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.OVER.upper(), header3=vec.sb.UNDER.upper())
            self.place_bet_and_verify()
        else:
            self._logger.info(msg=f'Market {vec.siteserve.EXPECTED_MARKETS_NAMES.total_points} is not in the actual market list')

    def test_005_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_handicap_2_wayhandicap_in_coral_and_handicap_2_way_in_lads_total_points(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Handicap 2 way(Handicap in coral and Handicap 2 way in Lads)
        DESCRIPTION: • Total Points
        EXPECTED: Bet should be placed successfully
        """
        # covered in step 3 and 4
