import random
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher_bpp
@pytest.mark.market_switcher
@vtest
class Test_C60089551_Verify_MS_on_Competitions_Tab_for_Volleyball(BaseSportTest, BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C60089551
    NAME: Verify MS on Competitions Tab for Volleyball
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Volleyball Competition page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|,|Total Points|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Volleyball Landing Page -> 'Click on Competition  Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting (WW)| - "Match Result"
    PRECONDITIONS: * |Match Set Handicap (Handicap)| - "Set Handicap"
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

    def choosing_events(self):
        self.__class__.sel_events = []
        sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        for section in sections:
            if not section.is_expanded():
                section.expand()
            for event in list(section.items_as_ordered_dict.values()):
                if len(self.sel_events) < 2:
                    self.sel_events.append(event)
                else:
                    break
            if len(self.sel_events) >= 2:
                break

    def verify_bet_placement(self, market):
        self.choosing_events()
        quick_bet = False
        if not quick_bet:
            random.choice(list(list(self.sel_events)[0].template.get_available_prices().values())).click()
            if self.device_type == 'mobile':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            self.site.open_betslip()
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
            quick_bet = True

        if quick_bet and self.device_type == 'mobile':
            random.choice(list(list(self.sel_events)[0].template.get_available_prices().values())).click()
            sleep(3)
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = self.bet_amount
            self.site.wait_content_state_changed()
            quick_bet.place_bet.click()
            bet_receipt_displayed = quick_bet.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            quick_bet.header.close_button.click()

        if len(self.sel_events) >= 2:
            for event in self.sel_events:
                sel_name, sel = random.choice(list(event.template.get_available_prices().items()))
                sel.click()
                try:
                    self.assertTrue(sel.is_selected(),
                                    msg=f'Selection "{sel_name}" is not selected from Event "{event.template.event_name}"')
                except Exception:
                    sel.click()
                    self.assertTrue(sel.is_selected(),
                                    msg=f'Selection "{sel_name}" is not selected from Event "{event.template.event_name}"')
                counter_value = int(self.site.header.bet_slip_counter.counter_value)
                if counter_value == 0 and self.device_type == 'mobile':
                    self.site.add_first_selection_from_quick_bet_to_betslip()
            self.site.open_betslip()
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        self.sel_events.clear()

    def verify_ga_tracking_for_selected_market(self, market):
        if self.device_type == 'mobile' or self.brand == 'bma':
            selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        else:
            selected_value = market
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=selected_value)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': selected_value,
                             'categoryID': '36',
                             }
        self.compare_json_response(actual_response, expected_response)

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header2):
        items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate volleybal campetition tab
        EXPECTED: Event is successfully created
        """
        self.site.login()
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='volleyball', status=True)
        self.assertTrue(status, msg=f'The sport "volleyball" is not checked')
        if tests.settings.backend_env != 'prod':
            self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.volleyball_config.category_id,
                                                           disp_sort_names='HH,MH,WH,HL,3W',
                                                           primary_markets='|Match Betting|,|Handicap Match Result|,|Match Set Handicap|,|Total Match Points|,|Set X Winner||Handicap 3-Way|')
            self.ob_config.add_volleyball_event_to_austrian_league(markets=self.event_markets)
            self.ob_config.add_volleyball_event_to_austrian_league(markets=self.event_markets)
        self.navigate_to_page(name='sport/volleyball')
        self.site.wait_content_state('volleyball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.volleyball_config.category_id)
        self.site.competition_league.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab = self.site.competition_league.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for volleyball')
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
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
                wait_for_result(lambda: dropdown.is_expanded() is not True,
                                name=f'Market switcher expanded/collapsed',
                                timeout=5)
                self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
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
        self.site.wait_splash_to_hide()
        actual_markets_list = list(
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        if actual_markets_list == ['']:
            actual_markets_list = list(
                self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())

        self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.title(),
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.match_set_handicap.title(),
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_match_points.title()]
        if tests.settings.backend_env == 'prod':
            for market in actual_markets_list:
                self.assertIn(market, self.expected_list, msg=f'Actual Market: "{market}" is not present in the '
                                                              f'Expected Markets list:"{self.expected_list}"')
        else:
            self.assertListEqual(actual_markets_list, self.expected_list,
                                 msg=f'Actual list : "{actual_markets_list}" is not same as '
                                     f'Expected list : "{self.expected_list}"')

    def test_003_select_match_result_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        try:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[1]).click()
        except Exception:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[1]).click()
        self.verify_bet_placement(market=self.expected_list[1])
        self.verify_ga_tracking_for_selected_market(market=self.expected_list[1])
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1="1", header2="2")

    def test_004_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: Fixture header is displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2
        """
        # covered in step 3

    def test_005_verify_ga_tracking_for_the_match_result(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Match Result'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Match Result"
        EXPECTED: categoryID: "36"
        EXPECTED: })
        """
        # covered in step 3

    def test_006_repeat_step_2_5_for_the_following_markets_set_handicap_total_points_except_step_4(self):
        """
        DESCRIPTION: Repeat step 2-5 for the following markets:
        DESCRIPTION: • Set Handicap
        DESCRIPTION: • Total Points (except step 4)
        """
        try:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[2]).click()
        except Exception:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[2]).click()
        self.verify_bet_placement(market=self.expected_list[2])
        self.verify_ga_tracking_for_selected_market(market=self.expected_list[2])
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1=vec.sb.OVER.upper(),
                                                      header2=vec.sb.UNDER.upper())

    def test_007_verify_text_of_the_labels_for_total_points(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points'
        EXPECTED: Fixture header is displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under
        """
        try:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[0]).click()
        except Exception:
            self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                self.expected_list[0]).click()
        self.verify_bet_placement(market=self.expected_list[0])
        self.verify_ga_tracking_for_selected_market(market=self.expected_list[0])
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1="1", header2="2")

    def test_008_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_Set_Handicap_Total_Points(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • Set Handicap
        DESCRIPTION: • Total Points
        EXPECTED: Bet should be placed successfully
        """
        # covered in step 7
