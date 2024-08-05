import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.market_switcher
@pytest.mark.timeout(900)
@pytest.mark.sports
@pytest.mark.market_switcher_bpp
@vtest
class Test_C60617098_Verify_Market_Selector_dropdown_list_on_Football_landing_page_for_Multiple_Bet_placement(BaseBetSlipTest):
    """
    TR_ID: C60617098
    NAME: Verify 'Market Selector' dropdown list on Football landing page for Multiple Bet placement
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on the Football landing page for Multiple Bet placement
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Football Landing page -> 'Matches' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following templateMarketNames:
    PRECONDITIONS: * |Match Betting| - "Match Result"
    PRECONDITIONS: * |To Qualify| - "To Qualify"
    PRECONDITIONS: * |Total Goals Over/Under| - "Total Goals Over/Under 2.5"
    PRECONDITIONS: * |Both Teams to Score| - "Both Teams to Score"
    PRECONDITIONS: * |To Win Not to Nil| - "To Win and Both Teams to Score" **Ladbrokes removed from OX 100.3**
    PRECONDITIONS: * |Match Result and Both Teams To Score| - "Match Result & Both Teams To Score" **Ladbrokes added from OX 100.3**
    PRECONDITIONS: * |Draw No Bet| - "Draw No Bet"
    PRECONDITIONS: * |First-Half Result| - "1st Half Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def place_bet_and_verify(self):
        sections = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(sections, msg='"Sections" are not available')
        selection_clicked = 0
        for section in sections:
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(events, msg='"Events" are not available')
            for event in events:
                selections = list(event.template.items_as_ordered_dict.values())
                self.assertTrue(selections, msg='"Selections" are not available')
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
            self.ob_config.add_autotest_premier_league_football_event(markets=markets)
        # reading markets from cms_config
        expected_markets = self.cms_config.get_sports_tab_data(sport_id=self.ob_config.football_config.category_id,
                                                               tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)['marketsNames']
        self.__class__.expected_market_selector_options = [market['title'].title() for market in expected_markets]
        tab_status = self.cms_config.get_sport_tab_status(sport_id=self.ob_config.football_config.category_id,
                                                          tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)

        self.site.login()
        self.site.open_sport(name='FOOTBALL')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        sport_tab_from_cms = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, self.ob_config.football_config.category_id)
        tabs = self.site.football.tabs_menu.items_as_ordered_dict
        tabs_names = [tab.upper() for tab in tabs]
        # checking the tab status for frontend and from cms
        if not tab_status and sport_tab_from_cms.upper() not in tabs_names:
            raise CMSException(f' "{sport_tab_from_cms}" tab is not enabled in CMS for football')
        expected_sport_tab = self.site.football.tabs_menu.current
        self.assertEqual(expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{expected_sport_tab}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match result' in 'Market selector' **Coral**
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
        market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()
        self.assertEqual(football_tab_content.dropdown_market_selector.selected_market_selector_item.upper(),
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: {football_tab_content.dropdown_market_selector.selected_market_selector_item}\n'
                             f'Expected: {market_selector_default_value}')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        EXPECTED: • To Qualify
        EXPECTED: • Total Goals Over/Under 2.5
        EXPECTED: • Both Teams to Score
        EXPECTED: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        EXPECTED: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: • Draw No Bet
        EXPECTED: • 1st Half Result
        EXPECTED: **Note:**
        EXPECTED: *If any Market is not available it is skipped in the Market selector drop down list*
        """
        available_markets = self.site.football.tab_content.dropdown_market_selector.available_options
        for market in available_markets:
            self.assertIn(market.title(), self.expected_market_selector_options,
                          msg=f'Actual market: {market.title()} is not present in '
                              f'the Expected list: {self.expected_market_selector_options}')

    def test_003_verify_bet_placement_for_multiple_bet_for_the_below_markets_match_result_to_qualify_total_goals_overunder_25_both_teams_to_score_to_win_and_both_teams_to_score_ladbrokes_removed_from_ox_1003_match_result_and_both_teams_to_score_ladbrokes_added_from_ox_1003_draw_no_bet_1st_half_result(self):
        """
        DESCRIPTION: Verify Bet Placement for multiple Bet for the below markets
        DESCRIPTION: • Match Result
        DESCRIPTION: • To Qualify
        DESCRIPTION: • Total Goals Over/Under 2.5
        DESCRIPTION: • Both Teams to Score
        DESCRIPTION: * To Win and Both Teams to Score **Ladbrokes removed from OX 100.3**
        DESCRIPTION: * Match Result and Both Teams To Score **Ladbrokes added from OX 100.3**
        DESCRIPTION: • Draw No Bet
        DESCRIPTION: • 1st Half Result
        EXPECTED: Bet should be placed successfully
        """
        options = self.site.football.tab_content.dropdown_market_selector
        markets_dropdown_list = list(options.items_as_ordered_dict.keys())
        for market in markets_dropdown_list:
            options.select_value(value=market)
            sleep(2)
            self.place_bet_and_verify()
            options = self.site.football.tab_content.dropdown_market_selector
