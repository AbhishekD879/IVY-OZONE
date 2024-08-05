import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events with diff markets
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28848_To_Edit__BMA_37026_Verify_Markets_Filtering_per_Tabs(Common):
    """
    TR_ID: C28848
    NAME: [To Edit - BMA-37026] Verify Market's Filtering per Tabs
    DESCRIPTION: This test case verifies market's filtering per tabs
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6586 - Racecard Layout Update - Markets and Selections area
    PRECONDITIONS: To retrieve an information from Site Server use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: See attribute:
    PRECONDITIONS: 'name' attribute in the market level to see market name
    """
    keep_browser_open = True
    selection_to_bet_without = 2

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event in OB TI
        """
        # four or more markets
        markets = [('win_only',), ('betting_without', {'without_runner': self.selection_to_bet_without}), ('to_finish_second',), ('insurance_2_places',),
                   ('antepost',), ('top_2_finish',)]
        event_params1 = self.ob_config.add_UK_racing_event(markets=markets, number_of_runners=3)
        self.__class__.win_only_selection_ids = list(event_params1.selection_ids['win_only'].values())
        self.__class__.betting_without_selection_ids = list(event_params1.selection_ids['betting_without'].values())
        self.__class__.win_or_each_way_selection_ids = list(event_params1.selection_ids['win_or_each_way'].values())
        self.__class__.selection_name = list(event_params1.selection_ids['win_only'].keys())[1]
        self._logger.info('*** Created Horse racing event with parameters {}'.format(event_params1))
        self.__class__.eventID1 = event_params1.event_id

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Home')

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the Sports Menu Ribbon
        EXPECTED: <Race> landing page is opened
        """
        self.navigate_to_edp(event_id=self.eventID1, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        self.__class__.markets = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list
        self.__class__.market_tabs = self.markets.items_as_ordered_dict
        tab = self.markets.open_tab(vec.sb.WIN_OR_EACH_WAY.upper())
        self.assertTrue(tab, msg=f'"{vec.sb.WIN_OR_EACH_WAY.upper()}" Tab is not opened')

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: *   Event details page is opened
        EXPECTED: *   'Win or E/W' tab is opened by default
        EXPECTED: *   Tab is expanded by default and not collapsible
        """
        # This step is not applicable as the default settings have been changed

    def test_004_verify_win_or_ew_tab(self):
        """
        DESCRIPTION: Verify 'Win or E/W' tab
        EXPECTED: *   Market with **'name' = 'Win or Each Way'** is shown (**'name'** attribute on market level)
        EXPECTED: *   All outcomes within market are shown
        EXPECTED: *   If market/outcomes within market are absent - Tab is not shown
        """
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID1)[0]
        market_name = event_resp['event']['children'][0]['market']['name']
        expected_market_name = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.market_name
        self.assertEqual(market_name, expected_market_name, msg=f'Actual Market name from ss response "{market_name}" '
                                                                f'is not equal to expected market name "{expected_market_name}"')

    def test_005_tap_win_only_tab(self):
        """
        DESCRIPTION: Tap 'Win Only' tab
        EXPECTED: 'Win Only' tab is expanded by default and not collapsible
        """
        tab = self.markets.open_tab(vec.betslip.WIN_ONLY.upper())
        self.assertTrue(tab, msg=f'"{vec.betslip.WIN_ONLY.upper()}" Tab is not opened')

    def test_006_verify_win_only_tab(self):
        """
        DESCRIPTION: Verify 'Win Only' tab
        EXPECTED: *   Market with **'name' = 'Win Only'** is shown (**'name'** attribute on market level)
        EXPECTED: *   All outcomes within market are shown
        EXPECTED: *   If market/outcomes within market are absent - Tab 'Win Only' is not shown
        """
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID1)[0]
        market_name = event_resp['event']['children'][1]['market']['name']
        expected_market_name = list(self.ob_config.horseracing_config.horse_racing_live.autotest_uk.markets.win_only.keys())[0]
        self.assertEqual(market_name, expected_market_name, msg=f'Actual Market name from ss response "{market_name}" '
                                                                f'is not equal to expected market name "{expected_market_name}"')

    def test_007_tap_betting_wo_tab(self):
        """
        DESCRIPTION: Tap 'Betting WO' tab
        EXPECTED: *   The list of all available markets is shown
        EXPECTED: *   All markets are expanded by default
        EXPECTED: *   Each market is collapsible/expandable
        """
        if self.brand == 'ladbrokes':
            tab_name = vec.racing.RACING_EDP_BETTING_WITHOUT.upper() + ' ' + self.selection_name.upper()
        else:
            tab_name = vec.sb.BETTING_WITHOUT.upper()
        tab = self.markets.open_tab(tab_name)
        self.assertTrue(tab, msg=f'"{tab_name}" Tab is not opened')

    def test_008_verify_betting_wo_tab(self):
        """
        DESCRIPTION: Verify 'Betting WO' tab
        EXPECTED: *   Markets with **'name' = 'Betting without XXXX' **are shown (e.g. 'Betting without Theatrical Style')
        EXPECTED: *   All outcomes within markets are shown
        EXPECTED: *   If market/outcomes within market are absent - Tab 'Betting WO' is not shown
        """
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID1)[0]
        market_name = event_resp['event']['children'][2]['market']['name']
        expected_market_name = list(self.ob_config.horseracing_config.horse_racing_live.autotest_uk.markets.betting_without.keys())[0] + ' ' + self.selection_name
        self.assertEqual(market_name, expected_market_name, msg=f'Actual Market name from ss response "{market_name}" '
                                                                f'is not equal to expected market name "{expected_market_name}"')

    def test_009_tap_more_markets_tab(self):
        """
        DESCRIPTION: Tap 'More Markets' tab
        EXPECTED: *   The list of all available markets is shown
        EXPECTED: *   All markets are expanded by default
        EXPECTED: *   Each market is collapsible/expandable
        """
        # More markets link is removed as per manual team confirmation
        expected_markets = [vec.sb.WIN_OR_EACH_WAY.upper(), vec.betslip.WIN_ONLY.upper(), vec.sb.BETTING_WITHOUT.upper() if self.brand == 'bma' else vec.racing.RACING_EDP_BETTING_WITHOUT.upper()]
        self.ob_config.change_selection_state(selection_id=self.win_or_each_way_selection_ids[0], displayed=False,
                                              active=False)
        self.ob_config.change_selection_state(selection_id=self.win_or_each_way_selection_ids[1], displayed=False,
                                              active=False)
        self.ob_config.change_selection_state(selection_id=self.win_or_each_way_selection_ids[2], displayed=False,
                                              active=False)
        self.ob_config.change_selection_state(selection_id=self.win_only_selection_ids[0], displayed=False,
                                              active=False)
        self.ob_config.change_selection_state(selection_id=self.win_only_selection_ids[1], displayed=False,
                                              active=False)
        self.ob_config.change_selection_state(selection_id=self.win_only_selection_ids[2], displayed=False,
                                              active=False)
        self.ob_config.change_selection_state(selection_id=self.betting_without_selection_ids[0], displayed=False,
                                              active=False)
        self.ob_config.change_selection_state(selection_id=self.betting_without_selection_ids[1], displayed=False,
                                              active=False)
        markets = list(self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict.keys())
        for market in expected_markets:
            self.assertNotIn(market, markets, msg=f'market "{market}" should not be in present in market list "{markets}"')

    def test_010_verify_more_markets_tab(self):
        """
        DESCRIPTION: Verify 'More Markets' tab
        EXPECTED: *   Markets which doesn't contain any** name = **Win or E/W', 'Win Only' or 'Betting WO appear in 'More markets' tab
        EXPECTED: *   All outcomes within markets are shown
        EXPECTED: *   If market/outcomes within market are absent - Tab 'More Markets' is not shown
        """
        # More markets link is removed as per manual team confirmation
