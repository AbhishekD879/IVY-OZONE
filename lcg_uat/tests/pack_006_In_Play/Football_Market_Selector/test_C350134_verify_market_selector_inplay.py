import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from time import sleep
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.in_play
@pytest.mark.market_switcher
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.timeout(900)
@pytest.mark.desktop
@pytest.mark.reg167_fix
@pytest.mark.market_switcher_bpp
@vtest
class Test_C350134_Verify_Market_Selector(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C350134
    NAME: Verify Market selector drop down for Football on In-Play page
    DESCRIPTION: This Test Case verified Market selector drop down for Football on in-Play page
    """
    keep_browser_open = True
    expected_market_selector_options = vec.siteserve.EXPECTED_MARKETS_NAMES
    bet_amount = 0.2

    def place_bet_and_verify(self):
        sections = list(self.site.football.tab_content.accordions_list.n_items_as_ordered_dict().values())
        self.assertTrue(sections,
                        msg='"Sections" are not available')
        selection_clicked = 0
        for section in sections:
            section.expand()
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(events, msg='"Events" are not available')
            for event in events:
                selections = list(event.template.items_as_ordered_dict.values())
                self.assertTrue(selections, msg='"Selections" are not available')
                for selection in selections:
                    if selection.name.upper() not in ['N/A', 'SUSP']:
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
            raise SiteServeException('Not more than one event present to place multiple bet')

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
            self.ob_config.add_autotest_premier_league_football_event(markets=markets, is_live=True)
            self.ob_config.add_autotest_premier_league_football_event(markets=markets, is_live=True)
        sport_tab_from_cms = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                     self.ob_config.football_config.category_id)
        # reading markets from cms_config
        expected_markets = self.cms_config.get_sports_tab_data(sport_id=self.ob_config.football_config.category_id,
                                                               tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)[
            'marketsNames']
        self.__class__.expected_market_selector_options = [market['title'].title() for market in expected_markets]
        tab_status = self.cms_config.get_sport_tab_status(sport_id=self.ob_config.football_config.category_id,
                                                          tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        self.site.login()
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)

        # checking the tab status for frontend and from cms
        tabs = self.site.football.tabs_menu.items_as_ordered_dict
        tabs_names = [tab.upper() for tab in tabs]
        if not tab_status and sport_tab_from_cms.upper() not in tabs_names:
            raise CmsClientException(f' "{sport_tab_from_cms}" tab is not enabled in CMS for football')
        expected_sport_tab = self.site.football.tabs_menu.current
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
            today_tab = self.site.football.tab_content.accordions_list
            if not today_tab:
                self.site.football.date_tab.tomorrow.click()
                tomorrow_tab = self.site.football.tab_content.accordions_list
                if not tomorrow_tab:
                    self.site.football.date_tab.future.click()
                    future_tab = self.site.football.tab_content.accordions_list
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
            self.assertIn(market.title().strip(), self.expected_market_selector_options,
                          msg=f'Actual market: {market} is not present in '
                              f'the Expected list: {self.expected_market_selector_options}')

    def test_003_click_on_changechange_marketmarket_button_and_afterward_somewhere_outside_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Click on 'Change'/'Change Market'/'Market' button and afterward somewhere outside the єMarket Selectorє dropdown
        EXPECTED: 'Market Selector' dropdown becomes collapsed
        """
        # Cannot automate

    def test_004_select_any_other_sport_not_football_from_the_in_play_sports_ribbon_menu(self):
        """
        DESCRIPTION: Select any other Sport (not Football) from the 'In-Play Sports Ribbon' menu
        EXPECTED: The 'Market Selector' is not available
        """
        self.navigate_to_page(name='/sport/tennis/live')
        self.site.wait_content_state_changed()
        wait_for_haul(5)
        tennis_tab_content = self.site.sports_page.tab_content
        if tennis_tab_content.has_dropdown_market_selector():
            self.assertTrue(tennis_tab_content.has_dropdown_market_selector(),
                            msg='"Market Selector" drop-down is displayed on Tennis in-play page')
        else:
            self.assertFalse(tennis_tab_content.has_dropdown_market_selector(),
                             msg='"Market Selector" drop-down is not displayed on Tennis in-play page')

    def test_005_repeat_steps_1_3_on_football_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-3 on 'Football Landing Page' -> 'In-Play' tab
        EXPECTED:
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                              self.ob_config.basketball_config.category_id)
        tab_status = self.cms_config.get_sport_tab_status(sport_id=self.ob_config.football_config.category_id,
                                                          tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play)
        if not tab_status or not in_play_tab:
            raise CmsClientException(f' "{in_play_tab}" tab is not enabled in CMS for football')
        result = self.site.football.tabs_menu.click_button(in_play_tab)
        self.assertTrue(result, msg=f'"{in_play_tab}" tab was not opened')

    def test_006_verify_bet_placement_for_single_multiple_and_quick_bet_for_the_below_markets_match_result_next_team_to_score_both_teams_to_score_match_result__both_teams_to_score_total_goals_overunder_15_total_goals_overunder_25_total_goals_overunder_35_total_goals_overunder_45_to_qualify_penalty_shoot_out_winner_extra_time_result_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Verify Bet Placement for Single, multiple and Quick Bet for the below markets
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
        if self.device_type == 'desktop':
            if self.brand == 'bma':
                self.site.football.tab_content.dropdown_market_selector.click()
                markets_dropdown_list = self.site.competition_league.competitions_selector.items_as_ordered_dict
                markets_len = len(markets_dropdown_list) if len(markets_dropdown_list) <= 3 else 3
                for market_name, market in list(markets_dropdown_list.items())[:markets_len]:
                    market.click()
                    self.place_bet_and_verify()
                    self.site.football.tab_content.dropdown_market_selector.click()
            else:
                options = self.site.inplay.tab_content.dropdown_market_selector
                markets_dropdown_list = list(options.items_as_ordered_dict.keys())
                length = 3 if (len(markets_dropdown_list) >= 3) else len(markets_dropdown_list)
                for market in markets_dropdown_list[0:length]:
                    options.select_value(value=market)
                    sleep(2)
                    self.place_bet_and_verify()
                    options = self.site.inplay.tab_content.dropdown_market_selector
        else:
            options = self.site.football.tab_content.dropdown_market_selector
            markets_dropdown_list = list(options.items_as_ordered_dict.keys())
            for market in markets_dropdown_list[0:3]:
                options.select_value(value=market)
                sleep(2)
                self.place_bet_and_verify()
                options = self.site.football.tab_content.dropdown_market_selector
