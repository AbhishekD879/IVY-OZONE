import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from time import sleep
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.in_play
@pytest.mark.market_switcher
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.timeout(900)
@pytest.mark.desktop
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60673620_Verify_Market_Selector_drop_down_displaying_for_Football_on_in_Play_page_for_multiple_bet_placement(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C60673620
    NAME: Verify 'Market Selector' drop down displaying for Football on in-Play page for multiple bet placement
    DESCRIPTION: This test case verifies 'Market Selector' drop down displaying for Football on in-Play page for multiple bet placement
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following marketTemplates:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |Next Team to Score| - "Next Team to Score"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 1.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 3.5"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 4.5"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Penalty Shoot-Out Winner| - "Penalty Shoot-Out Winner"
    PRECONDITIONS: * |Extra-Time Result| - "Extra Time Result"
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    PRECONDITIONS: 3) To check the available options in 'Market Selector' use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::XX::LIVE_EVENT"
    PRECONDITIONS: where:
    PRECONDITIONS: XX - Category ID
    PRECONDITIONS: ![](index.php?/attachments/get/10272745)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the 'In-Play' page
    PRECONDITIONS: 3. Choose the 'Football' tab
    """
    keep_browser_open = True
    expected_market_selector_options = vec.siteserve.EXPECTED_MARKETS_NAMES
    bet_amount = 0.2

    def place_bet_and_verify(self):
        sections = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections,
                        msg='"Sections" are not available')
        for section in sections:
            if not section.is_expanded():
                section.expand()
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(events, msg='"Events" are not available')
            for event in events:
                selections = list(event.template.items_as_ordered_dict.values())
                self.assertTrue(selections, msg='"Selections" are not available')
                for selection in selections:
                    if selection.is_enabled():
                        selection.click()
                        self.__class__.is_clicked = True
                        break
                if self.is_clicked:
                    break
            if self.is_clicked:
                break
        self.__class__.is_clicked = False
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=10), msg='Quick Bet panel is not opened')
            self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet Receipt is not displayed')
            self.site.quick_bet_panel.header.close_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Adds football events with different markets
        """
        if tests.settings.backend_env != 'prod':
            markets = [
                ('to_qualify', ),
                ('over_under_total_goals', {'over_under': 2.5}),
                ('both_teams_to_score', ),
                ('draw_no_bet', ),
                ('first_half_result', )
            ]
            self.ob_config.add_autotest_premier_league_football_event(markets=markets)

        self.site.login()
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        expected_sport_tab = self.site.football.tabs_menu.current
        sport_tab_from_cms = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, self.ob_config.football_config.category_id)
        self.assertEqual(expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{expected_sport_tab}"')

    def test_001_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: **Mobile:**
        EXPECTED: * The 'Market Selector' is displayed below the 'Life Now (n)' header
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: **Desktop:**
        EXPECTED: * The 'Market Selector' is displayed below the 'Life Now' (n) switcher
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change Market' button is placed next to  'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: * 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        """
        if tests.settings.backend_env == 'prod':
            today_tab = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            if not today_tab:
                self.site.football.date_tab.tomorrow.click()
                tomorrow_tab = self.site.football.tab_content.accordions_list.items_as_ordered_dict
                if not tomorrow_tab:
                    self.site.football.date_tab.future.click()
                    future_tab = self.site.football.tab_content.accordions_list.items_as_ordered_dict
                    if not future_tab:
                        raise VoltronException('No events found in football for matches tab')
        football_tab_content = self.site.football.tab_content
        self.assertTrue(football_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on Football landing page')

    def test_002_click_on_the_changechange_marketmarket_button_to_verify_options_available_for_football_in_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click on the 'Change'/'Change Market'/'Market' button to verify options available for Football in the Market selector dropdown
        EXPECTED: Market selector drop down becomes expanded (with chevron/arrow pointing upwards) with the options in the order listed below:
        EXPECTED: * Main Markets
        EXPECTED: * Match Result
        EXPECTED: * Next Team to Score
        EXPECTED: * Both Teams to Score
        EXPECTED: * Match Result & Both Teams To Score
        EXPECTED: * Total Goals Over/Under 1.5
        EXPECTED: * Total Goals Over/Under 2.5
        EXPECTED: * Total Goals Over/Under 3.5
        EXPECTED: * Total Goals Over/Under 4.5
        EXPECTED: * To Qualify
        EXPECTED: * Penalty Shoot-Out Winner
        EXPECTED: * Extra Time Result
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        EXPECTED: *If any Market is not available it is not displayed in the Market selector drop-down list*
        """
        available_markets = self.site.football.tab_content.dropdown_market_selector.available_options
        for market in available_markets:
            self.assertIn(market, self.expected_market_selector_options,
                          msg=f'Actual market: {market} is not present in '
                              f'the Expected list: {self.expected_market_selector_options}')

    def test_003_verify_bet_placement_for_multiple_selections_for_the_below_markets_match_result_next_team_to_score_both_teams_to_score_match_result__both_teams_to_score_total_goals_overunder_15_total_goals_overunder_25_total_goals_overunder_35_total_goals_overunder_45_to_qualify_penalty_shoot_out_winner_extra_time_result_draw_no_bet_1st_half_result_on_inplay_tab(self):
        """
        DESCRIPTION: Verify Bet Placement for multiple selections for the below markets on inplay tab
        DESCRIPTION: * Match Result
        DESCRIPTION: * Next Team to Score
        DESCRIPTION: * Both Teams to Score
        DESCRIPTION: * Match Result & Both Teams To Score
        DESCRIPTION: * Total Goals Over/Under 1.5
        DESCRIPTION: * Total Goals Over/Under 2.5
        DESCRIPTION: * Total Goals Over/Under 3.5
        DESCRIPTION: * Total Goals Over/Under 4.5
        DESCRIPTION: * To Qualify
        DESCRIPTION: * Penalty Shoot-Out Winner
        DESCRIPTION: * Extra Time Result
        DESCRIPTION: * Draw No Bet
        DESCRIPTION: * 1st Half Result
        EXPECTED: Bet should be placed successfully
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.basketball_config.category_id)
        result = self.site.football.tabs_menu.click_button(in_play_tab)
        self.assertTrue(result, msg=f'"{in_play_tab}" tab was not opened')
        if self.device_type == 'desktop':
            markets_dropdown_list = self.site.inplay.tab_content.dropdown_market_selector.available_options
            for market in markets_dropdown_list:
                self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict[market].click()
                sleep(2)
                self.place_bet_and_verify()
        else:
            if self.brand == 'bma':
                options = self.site.football.tab_content.dropdown_market_selector
                markets_dropdown_list = list(options.items_as_ordered_dict.keys())
                for market in markets_dropdown_list:
                    options.select_value(value=market)
                    sleep(2)
                    self.place_bet_and_verify()
                    options = self.site.football.tab_content.dropdown_market_selector
            else:
                markets_dropdown_list = self.site.inplay.tab_content.dropdown_market_selector.available_options
                for market in markets_dropdown_list:
                    self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
                    sleep(2)
                    self.place_bet_and_verify()
