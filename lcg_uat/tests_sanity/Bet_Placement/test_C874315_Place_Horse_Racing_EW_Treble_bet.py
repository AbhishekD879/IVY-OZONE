import pytest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.login
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.next_races
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.sanity
@vtest
class Test_C874315_Place_Horse_Racing_EW_Treble_bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C874315
    NAME: Place Horse Racing EW Treble bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Multiple E/W bet on Horse Racing
    DESCRIPTION: Note: according to BMA-47237 event time is displayed twice in My Bets section
    PRECONDITIONS: Steps:
    PRECONDITIONS: - Open the app
    PRECONDITIONS: - Log in with user
    PRECONDITIONS: - Navigate to Horse Racing Page from the Menu
    """
    runner_names = []
    market_names_edp = []
    expected_currency = '£'
    keep_browser_open = True
    selection_ids = []
    number_of_stakes = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Find / create event for test
        DESCRIPTION: Navigate to HR page from menu
        EXPECTED: User is logged in
        EXPECTED: Event is found / created
        EXPECTED: Navigated to racing page
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)
        for event in events:
            market = next((market for market in event['event']['children'] if market['market']['templateMarketName'] == 'Win or Each Way'), None)
            outcomes_resp = market['market']['children']
            selection = next((i for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']),
                                None)
            if not selection:
                continue
            self.selection_ids.append(selection['outcome']['id'])
            self.runner_names.append(selection['outcome']['name'])
            self.market_names_edp.append(f"Win or Each Way {market['market']['eachWayFactorNum']}/{market['market']['eachWayFactorDen']} odds - places {','.join([str(i) for i in range(1, int(market['market']['eachWayPlaces']) + 1)])}")
            if len(self.selection_ids) == 3:
                break
        if len(self.selection_ids) < 3:
            raise SiteServeException('Enough Events are not available to place treble bet.')

    def test_001_add_3_horse_racing_selections_to_betslip_from_different_events(self):
        """
        DESCRIPTION: Add 3 Horse racing selections to Betslip from different events (e.g. from the "NEXT RACES" module (**CORAL**)/"NEXT RACES" tab (**LADBROKES**))
        EXPECTED: The selections are added to Betslip
        """
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_add_a_stake_eg_1_to_the_treble_acca_tick_the_each_way_checkbox(self):
        """
        DESCRIPTION: Add a Stake (e.g. 1£) to the Treble ACCA, tick the "Each Way" checkbox and then click on "PLACE BET" button
        EXPECTED: The bet is successfully placed
        """
        self.__class__.bet_info = self.place_and_validate_multiple_bet(multiples=True, each_way=True,
                                                                       number_of_stakes=self.number_of_stakes)
        self.check_bet_receipt_is_displayed()

    def test_003_verify_the_bet_confirmation_eg_bet_receipt_details(self):
        """
        DESCRIPTION: Verify the Bet Confirmation (e.g. bet receipt details)
        EXPECTED: Correct information is displayed in bet receipt:
        EXPECTED: - sign ![](index.php?/attachments/get/53866838)
        EXPECTED: with text 'Bet Placed Successfully' at the left side and date/time when the bet was placed at the right side
        EXPECTED: - 'Your Bets: (1)' text
        EXPECTED: - Bet Type ('Treble (X2)')
        EXPECTED: - Bet ID
        EXPECTED: - Selections name
        EXPECTED: - Markets name
        EXPECTED: - Events name
        EXPECTED: - Each Way conditions
        EXPECTED: - 'X Lines at £X.XX per line' text
        EXPECTED: - 'Cash Out' label (if available)
        EXPECTED: - Stake
        EXPECTED: - Est. Returns (**CORAL**)/Potential Returns(**LADBROKES**) (N/A if SP price)
        EXPECTED: - Total Stake
        EXPECTED: - Estimated Returns (CORAL)/Total Potential Returns(LADBROKES)
        EXPECTED: - 'REUSE SELECTIONS' and 'GO BETTING' buttons
        EXPECTED: - Currency is correct
        EXPECTED: - The balance is correctly updated
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/53866871)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/53866872)
        """
        bet_receipt = self.site.bet_receipt
        self.assertEqual(bet_receipt.receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{bet_receipt.receipt_header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        actual_date_time = bet_receipt.receipt_header.bet_datetime
        self.assertRegex(actual_date_time, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet data and time: "{actual_date_time}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        your_bets = f'{vec.betslip.YOUR_BETS}: ({self.number_of_stakes})'
        self.assertEqual(bet_receipt.receipt_sub_header.bet_counter_text,
                         your_bets,
                         msg=f'Actual bet count: {bet_receipt.receipt_sub_header.bet_counter_text} is '
                             f'not the same as expected: "{your_bets}"')

        sections = bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        section = sections.get(vec.betslip.TBL, None)
        self.assertTrue(section, msg=f'"{vec.betslip.TBL}" not found')
        self.assertEqual(f'(x{section.bet_multiplier})', '(x2)', msg='Incorrect number of bets')

        est_returns = 'N/A' if section.estimate_returns == 'N/A' else section.total_estimate_returns_currency
        if self.bet_info['total_estimate_returns'] != 'N/A':
            self.assertEqual(est_returns, self.expected_currency,
                             msg=f'Currency is not "{self.expected_currency}" and is "{est_returns}" instead.')

        total_stake_currency = section.total_stake_currency
        self.assertEqual(total_stake_currency, self.expected_currency,
                         msg=f'Currency is not "{self.expected_currency}" and is "{total_stake_currency}" instead.')

        self.check_bet_receipt(betslip_info=self.bet_info, each_way=True)

        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Reuse Selection button is not displayed')
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='Go Betting button is not displayed, Bet was not placed')

    def test_004_click_on_the_go_betting_button(self):
        """
        DESCRIPTION: Click on the 'GO BETTING' button
        EXPECTED: The customer is redirected to Horse Racing Page
        """
        self.site.bet_receipt.close_button.click()

    def test_005_click_on_my_bets_button_from_the_header_coral_my_account_my_bets_ladbrokes(self):
        """
        DESCRIPTION: Click on
        DESCRIPTION: -'My Bets' button from the header (**CORAL**)
        DESCRIPTION: -'My Account'-> 'My Bets' (**LADBROKES**)
        EXPECTED: My Bets page is opened
        """
        self.site.open_my_bets_open_bets()

    def test_006_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: Correct information is displayed in bet history:
        EXPECTED: - Bet Type (TREBLE(EACH WAY))
        EXPECTED: - Selections name with odds (@1/4)
        EXPECTED: - Markets name
        EXPECTED: - Each Way conditions
        EXPECTED: - Event name and event off time
        EXPECTED: - Event time and date
        EXPECTED: - 'WATCH LIVE' (**CORAL**)/'WATCH' (**LADBROKES**) label (if available)
        EXPECTED: - Sign that redirects to the event detail page ![](index.php?/attachments/get/53866895)
        EXPECTED: - Unit Stake
        EXPECTED: - Total Stake
        EXPECTED: - Est. Returns (**CORAL**)/Potential Returns(**LADBROKES**) (N/A if SP price)
        EXPECTED: - Currency is correct
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/53866943)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/53866945)
        """
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=f'{vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE} ({vec.bet_history.EWE.upper()})')
        self.assertEqual(bet.bet_type, f'{vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE} (EACH WAY)',
                         msg=f'Bet type "{bet.bet_type}" is not the same as expected TREBLE (EACH WAY)')

        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')

        market_names_open_bets = []
        outcome_names = []
        for betleg_name, betleg in bet_legs.items():
            market_names_open_bets.append(betleg.market_name)
            # It can be failed here because of odds change for 1 of 3 events
            # e.g. was 1/1 but now is 10/11(almost 1/1)
            self.softAssert(self.assertEqual, betleg.odds_value, self.bet_info[betleg.outcome_name]['odds'],
                            msg=f'"{betleg.odds_value}" is not the same as expected '
                                f'"{self.bet_info[betleg.outcome_name]["odds"]}"')
            outcome_names.append(betleg.outcome_name)
            self.assertTrue(betleg.event_time, msg='Can not find event time')

        if bet.est_returns.stake_value != 'N/A':
            actual_est_returns = float(bet.est_returns.stake_value)
            expected_est_returns = float(self.bet_info['total_estimate_returns'])
            delta = 0.03
            self.assertAlmostEqual(actual_est_returns, expected_est_returns, delta=delta,
                                   msg=f'Actual Estimated returns: "{actual_est_returns}" '
                                       f'does not match with excepted: "{expected_est_returns}" with delta "{delta}"')
        self.assertListEqual(market_names_open_bets, self.market_names_edp,
                                 msg=f'"{market_names_open_bets}" market name on Open Bets'
                                     f'is not the same as on edp: "{self.market_names_edp}"')

        self.assertListEqual(outcome_names, self.runner_names,
                             msg=f'Selection name "{outcome_names}" is not the same as '
                                 f'expected "{self.runner_names}"')
        self.assertEqual(bet.stake.currency, self.expected_currency,
                         msg=f'Stake currency "{bet.stake.currency}" is not the same as expected "{self.expected_currency}"')
        if self.bet_info['total_estimate_returns'] != 'N/A':
            self.assertEqual(bet.est_returns.currency, self.expected_currency,
                             msg=f'Estimate returns currency "{bet.est_returns.currency}" is not the same as '
                                 f'expected "{self.expected_currency}"')

    def test_007_click_on_user_menu_logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: Customer is logged out
        """
        self.site.logout()
