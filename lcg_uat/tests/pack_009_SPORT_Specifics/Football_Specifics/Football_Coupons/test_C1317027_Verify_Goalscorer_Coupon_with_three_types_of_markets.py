import pytest
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.football
@pytest.mark.back_button
@pytest.mark.coupons
@pytest.mark.fixture_header
@pytest.mark.goalscorer
@pytest.mark.bet_placement
@pytest.mark.cms
@pytest.mark.quick_bet
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.mobile_only
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-3330')
@pytest.mark.login
@vtest
class Test_C1317027_Verify_Goalscorer_Coupon_with_three_types_of_markets(BaseCouponsTest):
    """
    TR_ID: C1317027
    VOL_ID: C9697683
    NAME: Verify Goalscorer Coupon with three types of markets
    DESCRIPTION: This test case verifies Goalscorer Coupons
    PRECONDITIONS: 1. The Football event with First Goalscorer / Last Goalscorer  / Anytime Goalscorer markets (templateMarketName='First Goalscorer', templateMarketName="Last Goalscorer", templateMarketName="Anytime Goalscorer") are available
    PRECONDITIONS: 2. In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 3. The following market templates are used: |First Goalscorer| |Last Goalscorer| |Anytime Goalscorer|
    PRECONDITIONS: 4. List of Coupons depends on TI tool configuration data for Coupons. All available Coupons from OB response will be displayed on the page
    PRECONDITIONS: 5. For testing purposes the following Classes and Types should be used:
    PRECONDITIONS: - Football England - Premier League, Championship, League One, League Two
    PRECONDITIONS: - Football UEFA Club Competitions - UEFA Champions League, UEFA Europa League
    PRECONDITIONS: Note: The ‘New’ badge on Coupons page is CMS configurable (‘System-configuration’ -> ‘FOOTBALLCOUPONSNEWBADGE’ > check/uncheck ‘enableCouponNewBadge’ check box)
    PRECONDITIONS: **User is navigated to Coupon tab on Football and Goalscorer coupon is available**
    """
    keep_browser_open = True
    leagues = None
    event = None
    autotest_league = tests.settings.football_autotest_competition_league
    autotest_league2 = tests.settings.football_autotest_competition_league_2
    goalscorer_coupon = vec.coupons.GOALSCORER_COUPON
    markets = [
        ('anytime_goalscorer', {'cashout': False}),
        ('first_goalscorer', {'cashout': False}),
        ('last_goalscorer', {'cashout': False})
    ]
    bet_amount = 0.01
    expected_market_types = ['1ST', 'LAST', 'ANYTIME']
    market_first_goalscorer = 'first_goalscorer'
    player1 = 'Player 1'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add 'Football' events and additional market
        DESCRIPTION: The ‘New’ badge on Coupons page is CMS configurable ‘System-configuration’
        """
        self.site.login()
        self.__class__.user_balance = self.site.header.user_balance

        # League1 with 2 events
        # event1
        event_params1 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        event_id = event_params1.event_id
        first_goalscorer_id = self.ob_config.market_ids[event_id][self.market_first_goalscorer]
        self.ob_config.add_event_to_coupon(market_id=first_goalscorer_id, coupon_name=self.goalscorer_coupon)

        # event2
        event_params2 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        event_id2 = event_params2.event_id
        first_goalscorer_id2 = self.ob_config.market_ids[event_id2][self.market_first_goalscorer]
        self.ob_config.add_event_to_coupon(market_id=first_goalscorer_id2, coupon_name=self.goalscorer_coupon)

        # League2 2 with 2 events
        # event3
        event_params3 = self.ob_config.add_football_event_to_autotest_league2(markets=self.markets)
        self.__class__.event_id3, self.__class__.team3_1, self.__class__.team3_2, self.__class__.selection_ids3 = \
            event_params3.event_id, event_params3.team1, event_params3.team2, event_params3.selection_ids
        self.__class__.event_name3 = self.team3_1 + ' v ' + self.team3_2
        anytime_goalscorer_id3 = self.ob_config.market_ids[self.event_id3]['anytime_goalscorer']

        self.__class__.first_goalscorer_id3 = self.ob_config.market_ids[self.event_id3][self.market_first_goalscorer]
        last_goalscorer_id3 = self.ob_config.market_ids[self.event_id3]['last_goalscorer']

        self.ob_config.add_event_to_coupon(market_id=anytime_goalscorer_id3, coupon_name=self.goalscorer_coupon)
        self.ob_config.add_event_to_coupon(market_id=self.first_goalscorer_id3, coupon_name=self.goalscorer_coupon)
        self.ob_config.add_event_to_coupon(market_id=last_goalscorer_id3, coupon_name=self.goalscorer_coupon)

        # event4
        event_params4 = self.ob_config.add_football_event_to_autotest_league2(markets=self.markets)
        event_id4, team4_1, team4_2 = \
            event_params4.event_id, event_params4.team1, event_params4.team2
        self.__class__.event_name4 = team4_1 + ' v ' + team4_2
        anytime_goalscorer_id4 = self.ob_config.market_ids[event_id4]['anytime_goalscorer']

        first_goalscorer_id4 = self.ob_config.market_ids[event_id4][self.market_first_goalscorer]
        last_goalscorer_id4 = self.ob_config.market_ids[event_id4]['last_goalscorer']

        self.ob_config.add_event_to_coupon(market_id=anytime_goalscorer_id4, coupon_name=self.goalscorer_coupon)
        self.ob_config.add_event_to_coupon(market_id=first_goalscorer_id4, coupon_name=self.goalscorer_coupon)
        self.ob_config.add_event_to_coupon(market_id=last_goalscorer_id4, coupon_name=self.goalscorer_coupon)

        self.cms_config.new_coupon_badge_switcher(status=True)

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

        self.navigate_to_page(name='sport/football/coupons')
        self.site.wait_content_state('Football')
        result = self.site.football.tabs_menu.current
        self.assertTrue(result, msg=f'"{self.coupon_tab_name}" tab was not opened')

        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=self.goalscorer_coupon)

    def test_001_select_goalscorer_coupon(self):
        """
        DESCRIPTION: Select 'Goalscorer' coupon
        EXPECTED: - When events are not available for a coupon “No events found” text is shown
        EXPECTED: - When events are available for a coupon:
        EXPECTED: * Market Selector is NOT shown
        """
        self.assertFalse(self.site.coupon.tab_content.has_dropdown_market_selector(expected_result=False),
                         msg='Market selector is present on page')

    def test_002_verify_competition_section_displaying(self):
        """
        DESCRIPTION: Verify competition section displaying
        EXPECTED: - First competition is expanded by default;
        EXPECTED: - All competitions are collapsible, expandable.
        """
        leagues = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No competitions found on Coupon page')
        if self.brand != 'ladbrokes':
            _, league = list(leagues.items())[0]
            self.assertTrue(league.is_expanded(), msg=f'First league is not expanded by default')

            for league_name, league in leagues.items():
                self.assertTrue(league.is_expanded(), msg=f'League "{league_name}" is not expanded')
                league.collapse()
                self.assertFalse(league.is_expanded(), msg=f'League "{league_name}" is not collapsible')
                league.expand()
                self.assertTrue(league.is_expanded(), msg=f'League "{league_name}" is not expandable')

        self.assertIn(self.autotest_league, leagues,
                      msg=f'"{self.autotest_league}" league not found in list "{leagues}"')
        self.assertIn(self.autotest_league2, leagues,
                      msg=f'"{self.autotest_league2}" league not found in list "{leagues}"')

        if self.brand != 'ladbrokes':
            self.assertTrue(leagues.get(self.autotest_league).is_expanded(),
                            msg=f'League "{self.autotest_league}" is not expanded')

            self.assertTrue(leagues.get(self.autotest_league2).is_expanded(),
                            msg=f'League 2"{self.autotest_league2}" is expanded')

        events = leagues.get(self.autotest_league2).items_as_ordered_dict
        self.assertIn(self.event_name4.upper(), events,
                      msg=f'"{self.event_name4.upper()}" event not found in list "{events}"')

        # Took first event from autotest_league2
        self.__class__.event = list(events.items())[0][1]
        # because we have incorrect sorting of events sometimes

    def test_003_verify_event_section_displaying(self):
        """
        DESCRIPTION: Verify event section displaying
        EXPECTED: - First event section(2nd level of accordion) within first Competitions accordion is expanded by default
        EXPECTED: - All other event sections are collapsed by default
        EXPECTED: - Event section is expandable / collapsible with "Show more" button
        EXPECTED: - 'SEE ALL' link is shown
        """
        self.assertTrue(self.event.is_expanded(), msg=f'Event "{self.event_name4.upper()}" is not expanded')
        self.event.collapse()
        self.assertFalse(self.event.is_expanded(), msg=f'Event "{self.event_name4.upper()}" is not collapsible')
        self.event.expand()
        self.assertTrue(self.event.is_expanded(), msg=f'Event "{self.event_name4.upper()}" is not expandable')
        self.assertTrue(self.event.has_show_more_button(),
                        msg=f'"SHOW MORE" button is not present for event "{self.event_name4.upper()}"')
        self.assertTrue(self.event.has_see_all_link(),
                        msg=f'"SEE ALL" link is not present for event "{self.event_name4.upper()}"')

    def test_004_click_on_the_see_all_link(self):
        """
        DESCRIPTION: Click on the 'SEE ALL' link
        EXPECTED: User is redirected to the event details page
        """
        self.event.see_all_link.click()
        self.site.wait_content_state(state_name='EventDetails')
        self.site.back_button_click()
        self.site.wait_content_state('CouponPage')

    def test_005_verify_goalscorer_markets_collection_tab(self):
        """
        DESCRIPTION: Verify Goalscorer markets collection tab
        EXPECTED: * 'Goalscorer' market headers are displayed:
        EXPECTED: - Date and time of event is displayed
        EXPECTED: - '1st'
        EXPECTED: - 'Last'
        EXPECTED: - 'Anytime'
        EXPECTED: * Available selections are displayed in the grid, odds of each are shown in correct market section (1st, Last, Anytime)
        EXPECTED: * Selection name(footballer name), footballer team are displayed for each selection (if available)
        EXPECTED: * If some markets are not created or do not contain at least 1 available selection - their header is not displayed
        EXPECTED: * Odds on 'Odds/Prices' buttons are displayed in fractional format by default
        EXPECTED: * Maximum 5 selections are displayed within event section
        EXPECTED: * 'Show more' button is present if there are more than 5 selections within events section
        """
        leagues = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='No leagues found on Coupon page')

        self.assertIn(self.autotest_league2, leagues,
                      msg=f'"{self.autotest_league2}" league not found in list "{leagues}"')

        events = leagues.get(self.autotest_league2).items_as_ordered_dict
        self.assertIn(self.event_name3.upper(), events,
                      msg=f'"{self.event_name3.upper()}" event not found in list "{events}"')
        self.__class__.event = events.get(self.event_name3.upper())
        if not self.event.is_expanded():
            # TODO BMA
            self._logger.warning(f'*** First event "{self.event_name3}" is not expanded by default '
                                 f'because of incorrect order of events')
            self.event.expand()
            self.assertTrue(self.event.is_expanded(), msg=f'Event "{self.event}" is not collapsible')
            events = leagues.get(self.autotest_league2).items_as_ordered_dict
            self.__class__.event = events.get(self.event_name3.upper())

        self.assertEqual(self.site.coupon.name, self.goalscorer_coupon,
                         msg=f'Coupon name in subheader "{self.site.coupon.name}" '
                         f'is not the same as expected "{self.goalscorer_coupon}"')
        actual_market_types = [self.event.fixture_header.header1, self.event.fixture_header.header2,
                               self.event.fixture_header.header3]
        self.assertEqual(actual_market_types, self.expected_market_types,
                         msg=f'Actual markets "{actual_market_types}" '
                         f'are not the same as expected "{self.expected_market_types}"')

        self.assertEqual(len(self.event.table.players), 5,
                         msg=f'Incorrect players count is displayed: "{len(self.event.table.players)}" '
                         f'Expected count: "5"')
        self.assertTrue(self.event.has_show_more_button(), msg='"Show more" button is not present')

    def test_006_verify_show_more_button(self):
        """
        DESCRIPTION: Verify 'Show more' button
        EXPECTED: All available selections are present after clicking / tapping 'Show more' button
        """
        self.event.show_more_button.click()

        result = wait_for_result(lambda: len(self.event.table.items_as_ordered_dict) > 5, timeout=7,
                                 name='All available selections are present after clicking "SHOW MORE" button')
        self.assertTrue(result,
                        msg=f'Actual players cont is displayed after click "SHOW MORE" button: '
                        f'"{len(self.event.table.items_as_ordered_dict)}". Expected count should be > 5')

    def test_007_verify_selection_attribute_for_player_in_ss_response(self):
        """
        DESCRIPTION: Verify selection attribute for player in SS response
        EXPECTED: 1. First team's name in event's name is (Home) and second is (Away)
        EXPECTED: 2. OutcomeMeaningMinorCode:
        EXPECTED: - H (Home team)
        EXPECTED: - A (Away team)
        EXPECTED: - N (No score)
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.backend.ti.football.category_id)
        self.__class__.ss_event_details = ss_req.ss_event_to_outcome_for_event(event_id=self.event_id3,
                                                                               query_builder=self.ss_query_builder)
        self.__class__.ss_first_scorer_player_team1 = []
        self.__class__.ss_first_scorer_player_team2 = []

        ss_event_markets = self.ss_event_details[0]['event']['children']
        for market in ss_event_markets:
            if market['market']['id'] == self.first_goalscorer_id3:
                self.__class__.market_outcomes1 = market['market']['children']

        for outcome in self.market_outcomes1:
            if outcome['outcome'].get('outcomeMeaningMinorCode') and \
                    outcome['outcome']['outcomeMeaningMinorCode'] == 'H':
                self.ss_first_scorer_player_team1.append(outcome['outcome']['name'])
                continue
            if outcome['outcome'].get('outcomeMeaningMinorCode') and \
                    outcome['outcome']['outcomeMeaningMinorCode'] == 'A':
                self.ss_first_scorer_player_team2.append(outcome['outcome']['name'])
                continue

        items = self.event.table.items_as_ordered_dict
        home_team1 = [player.player_name for player in items.values() if player.team_name == self.team3_1]
        away_team2 = [player.player_name for player in items.values() if player.team_name == self.team3_2]

        self.assertEqual(home_team1, self.ss_first_scorer_player_team1,
                         msg=f'Selection names {home_team1} '
                         f'is not the same as expected {self.ss_first_scorer_player_team1}')

        self.assertEqual(away_team2, self.ss_first_scorer_player_team2,
                         msg=f'Selection names {away_team2} '
                         f'is not the same as expected {self.ss_first_scorer_player_team2}')

    def test_008_verify_ordering_of_selections(self):
        """
        DESCRIPTION: Verify ordering of selections
        EXPECTED: * Selections are ordered by odds in first available market (e.g. 1st/Last/Anytime) in ascending order (lowest to highest)
        EXPECTED: * If odds of selections are the same -> display alphabetically by footballer name (in ascending order)
        EXPECTED: * If prices are absent for selections - display alphabetically by footballer name (in ascending order)
        """
        event_ordering = [selection.player_name for selection in self.event.table.items]
        self.assertListEqual(event_ordering, sorted(event_ordering),
                             msg=f'Player Names in event "{event_ordering}" '
                             f'and sorted alphabetically player names list "{sorted(event_ordering)}" differ')

    def test_009_in_ti_change_price_for_one_of_the_selections_with_enabled_liveserve_updates_see_preconditions__navigate_to_application_and_observe_changes(
            self):
        """
        DESCRIPTION: In TI: Change price for one of the selections with enabled liveServe updates (see Preconditions) > Navigate to application and observe changes
        EXPECTED: - Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds they will change their color to:
        EXPECTED: * blue color if price has decreased
        EXPECTED: * pink color if price has increased
        """
        selection_to_change = self.selection_ids3[self.market_first_goalscorer][self.player1]
        outcomes = self.event.table.items_as_ordered_dict
        selection_name, selection = list(outcomes.items())[0]
        expected_new_price = '7/1'

        self._logger.info(f'*** Price change for event "{self.event_name3}" with selection name "{selection_name}" '
                          f'with selection id "{self.selection_ids3}"')
        self.ob_config.change_price(selection_id=selection_to_change, price=expected_new_price)

        result = wait_for_result(lambda: selection.bet_button.outcome_price_text == expected_new_price,
                                 name=f'Price to change from {selection.bet_button.outcome_price_text} '
                                 f'to {expected_new_price}',
                                 timeout=25)
        self.assertTrue(result, msg=f'Price for {selection_name} outcome was not changed.')

    def test_010_in_ti_suspend_marketone_of_the_selections_with_enabled_liveserve_updates_see_preconditions__navigate_to_application_and_observe_changes(
            self):
        """
        DESCRIPTION: In TI: Suspend market/one of the selections with enabled liveServe updates (see Preconditions) > Navigate to application and observe changes
        EXPECTED: - ***If market is suspended:*** All Price/Odds buttons under specific market column are displayed immediately as greyed out and become disabled for selected market but still displaying the prices
        EXPECTED: - ***If some selections are suspended:***
        EXPECTED: Price/Odds button of changed outcome are displayed immediately as greyed out and become disabled
        EXPECTED: The rest outcomes and market tabs are not changed
        """
        selection_to_change = self.selection_ids3[self.market_first_goalscorer][self.player1]
        self.ob_config.change_selection_state(selection_id=selection_to_change, displayed=True, active=False)
        selections = self.event.table.items_as_ordered_dict
        self.assertFalse(selections[self.player1].bet_button.is_enabled(timeout=25, expected_result=False),
                         msg=f'Price is not suspended for market '
                         f'"{self.market_first_goalscorer}" and player "{self.player1}"')

    def test_011_add_selections_to_the_quickbet_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the QuickBet/Betslip
        EXPECTED: Added selection(s) is/are displayed within the 'Quick Bet' (for 1 selection)/'Betslip' (for more than 1 selection)
        """
        selections = self.event.table.items_as_ordered_dict
        selection_name, selection = list(selections.items())[1]
        selection.bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True), msg='Quick Bet is not present')

    def test_012_enter_stake_for_a_bet_manually_or_using_quick_stakes_buttons_tap_place_bet__in_quick_betbet_now_in_betslip(
            self):
        """
        DESCRIPTION: Enter 'Stake' for a bet manually or using 'Quick Stakes' buttons> Tap 'Place Bet'  in 'Quick Bet'/'Bet Now' in Betslip
        EXPECTED: - Bet is successfully placed
        EXPECTED: - 'Quick Bet'/Betslip is replaced with 'Bet Receipt' view, displaying bet information
        EXPECTED: - Balance is decreased accordingly
        """
        quick_bet = self.site.quick_bet_panel
        quick_bet.selection.content.amount_form.input.value = str(self.bet_amount)
        quick_bet.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance)
