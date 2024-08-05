import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  We can't get info about bet from TI on prod
# @pytest.mark.hl  We can't get info about bet from TI on prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C29040_Bet_Receipt_for_Multiple_Bets(BaseBetSlipTest):
    """
    TR_ID: C29040
    NAME: Bet Receipt for Multiple Bets
    DESCRIPTION: This test case verifies Bet Receipt information for Multiple Bets
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement for selections from different events (multiples)
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: In order to check the potential payout value for multiple bets please go to Dev Tools->Network->All->buildBet->payout:
    PRECONDITIONS: For Win Only bets the value with the legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: For each way bets the sum of the value for legType="P" and the value for legType="W" should be used
    PRECONDITIONS: <potential="#.#" legType="W"/>
    PRECONDITIONS: <potential="#.#" legType="P"/>
    PRECONDITIONS: For <Sport>  it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event details page
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: *   For checking information in OB admin system navigates to queries > customers > fill in 'username' field in 'Customer Search Criteria' section > click 'Find Customers' button > choose your customer from 'Result' table > put receipt number e.g. "O/0123364/0000141" in 'Receipt like' field in 'Bet Search Criteria' section > click 'Find Bet' button > check the correctness of placed bet
    PRECONDITIONS: *   It is NOT possible to place a bet on 'Unnamed favorite' Racing selections with checked 'Each Way' option (ticket BMA-3935, to be changed with ticket BMA-6736 (Remove the E/W text and checkbox from Betslip for Favourite selections))
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load Oxygen app
        PRECONDITIONS: 2. Make sure the user is logged into their account
        PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
        PRECONDITIONS: 4. Make bet placement for selections from different events (multiples)
        PRECONDITIONS: 5. Make sure Bet is placed successfully
        """
        self.__class__.selection_id_1 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
        self.__class__.selection_id_2 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username, timeout_wait_for_dialog=10)
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))
        self.__class__.favourites_enabled = self.get_favourites_enabled_status()
        self.__class__.brand_is_coral = self.brand == 'bma'
        self.__class__.user_balance = self.get_balance_by_page('betslip')
        self.__class__.number_of_stakes = 1
        self.__class__.betslip_info = self.place_and_validate_multiple_bet(number_of_stakes=self.number_of_stakes)

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_bet_now_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Bet Now' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.user_balance - self.bet_amount)

    def test_002_verify_bet_receipt_layout(self):
        """
        DESCRIPTION: Verify Bet Receipt layout
        EXPECTED: * Bet Receipt header and subheader
        EXPECTED: * Card with multiples information
        EXPECTED: * 'Reuse Selections' and 'Go Betting' buttons
        EXPECTED: * Player Bets clickable banner (only for events from the following leagues: Football: England - Premier League, Spain - La Liga, Italy - Serie A, UEFA Champions League; Basketball: NBA; American Football: NFL) **NOTE:** Only for Mobile view
        """
        # Done in next steps

    def test_003_verify_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * 'User Balance' button
        """
        self.__class__.bet_receipt = self.site.bet_receipt
        if self.device_type == 'mobile':
            self.assertTrue(self.bet_receipt.close_button.is_displayed(),
                            msg='"X" button not displayed on BET RECEIPT header')
            self.assertEqual(self.bet_receipt.bet_receipt_header_name, vec.betslip.BET_RECEIPT,
                             msg=f'Page title "{self.bet_receipt.bet_receipt_header_name}" is '
                                 f'not the same as expected "{vec.betslip.BET_RECEIPT}"')

    def test_004_verify_bet_receipt_subheader(self):
        """
        DESCRIPTION: Verify Bet Receipt subheader
        EXPECTED: Bet Receipt subheader contains the following elements:
        EXPECTED: * 'Check' icon and 'Bet Placed Successfully' text
        EXPECTED: * Date and time in the next format: i.e. 19/09/2019, 11:57 and aligned by the right side
        EXPECTED: * Bet count in the next format: 'Your Bets:(X)' where 'X' is the number of bets placed in for that receipt
        EXPECTED: * Favorites icon for Football selection only (Coral)
        """
        self.assertTrue(self.bet_receipt.receipt_header.check_icon.is_displayed(), msg='"Check" icon is not displayed')
        self.assertEqual(self.bet_receipt.receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.bet_receipt.receipt_header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        actual_date_time = self.bet_receipt.receipt_header.bet_datetime
        self.assertRegex(actual_date_time, vec.regex.BET_DATA_TIME_FORMAT,
                         msg=f'Bet data and time: "{actual_date_time}" '
                             f'do not match expected pattern: {vec.regex.BET_DATA_TIME_FORMAT}')
        your_bets = f'{vec.betslip.YOUR_BETS}: ({self.number_of_stakes})'
        self.assertEqual(self.bet_receipt.receipt_sub_header.bet_counter_text, your_bets,
                         msg=f'Actual bet count: {self.bet_receipt.receipt_sub_header.bet_counter_text} is '
                             f'not the same as expected: "{your_bets}"')
        self.assertEqual(self.favourites_enabled,
                         self.bet_receipt.receipt_sub_header.has_add_all_to_favourites_button(expected_result=self.favourites_enabled),
                         msg=f'"Favourite all" icon presence status is not "{self.favourites_enabled}" for Football event')

    def test_005_verify_multiples_information(self):
        """
        DESCRIPTION: Verify Multiples information
        EXPECTED: Bet Receipt contains information about just placed Multiple bets:
        EXPECTED: Bet Receipt contains information about just placed Multiple bets:
        EXPECTED: Bet Receipt details for each multiple selections:
        EXPECTED: * Boosted bet section (in case of bet has been boosted)
        EXPECTED: * 'Multiples Type' text on each card (i.e. Double)
        EXPECTED: * Odds (for <Race> with 'SP' price - N/A) in the next format: i.e. @1/2 or @N/A
        EXPECTED: * Bet ID (Coral)/Receipt No (Ladbrokes). It starts with O and contains numeric values - i.e. O/0123828/0000155
        EXPECTED: * The outcome name
        EXPECTED: * Outcome name contains handicap value near the name (if such are available for outcomes)
        EXPECTED: * Market type user has bet on - i.e. Win or Each Way and Event name to which the outcome belongs to. Should display in the next format: Market Name/Event Name
        EXPECTED: * 'CashOut' label if available
        EXPECTED: * 'Promo' icon if available (Ladbrokes only)
        EXPECTED: * 'Favourites' icon for Football stakes (Coral only)
        EXPECTED: *  'Win Alerts' toggle (Wrapper only)
        EXPECTED: *  Total Stake (Coral)/Stake for this bet (Ladbrokes)
        EXPECTED: *  Free Bet Amount  (if Free bet was selected)
        EXPECTED: *  Est. Returns (Coral)/Potentials Returns (Ladbrokes) (for <Race> with 'SP' price - N/A)
        EXPECTED: Total Bet Receipt details:
        EXPECTED: * Total Stake
        EXPECTED: * Est. Returns (Coral)/Potentials Returns (Ladbrokes) (for <Race> with 'SP' price - N/A)
        """
        self.check_bet_receipt(self.betslip_info)
        self.assertTrue(self.bet_receipt.cash_out_label.is_displayed(), msg='"CashOut" label is not displayed')
        receipt_sections = self.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='Bet receipt sections not found')
        receipts = receipt_sections['Double'].items_as_ordered_dict
        self.assertTrue(receipts, msg='Receipts not found in bet receipt section')
        for event in list(receipts.values()):
            self.assertEqual(self.favourites_enabled, event.has_favourite_icon(expected_result=self.favourites_enabled),
                             msg=f'"Favourites" icon presence status is not "{self.favourites_enabled}"')

    def test_006_verify_buttons_displaying(self):
        """
        DESCRIPTION: Verify buttons displaying
        EXPECTED: * 'Reuse Selections' and 'Go Betting' buttons are displayed
        EXPECTED: * Buttons are located in the bottom area of Bet Receipt
        """
        self.assertTrue(self.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Reuse Selection button is not displayed')
        self.assertTrue(self.bet_receipt.footer.has_done_button(),
                        msg='Go Betting button is not displayed, Bet was not placed')

    def test_007_check_placed_bets_correctness_in_ob_adminsystem_send_to_uat_receipt_number_eg_o01233640000141(self):
        """
        DESCRIPTION: Check placed bets correctness in OB admin system (send to UAT receipt number e.g. "O/0123364/0000141")
        EXPECTED: Information on Bet Receipt should correspond to data in OB admin system
        """
        betreceipt_sections = self.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='Bet receipt sections not found')
        for section_name, section in betreceipt_sections.items():
            bet_id = section.bet_id
            self._logger.debug(f'*** Bet receipt id "{bet_id}" and name type "{section_name}"')
            ti_bet_info = self.ob_config.get_bet_info(username=self.username, bet_id=bet_id)

            unit_stake = float(ti_bet_info.stake)
            receipt_unit_stake = float(section.total_stake) / section.bet_multiplier
            est_returns = ti_bet_info.est_returns
            receipt_est_returns = section.estimate_returns
            self.assertAlmostEqual(receipt_unit_stake, unit_stake,
                                   delta=0.015,
                                   msg=f'Unit stake "{unit_stake}" is not the same as on bet receipt {receipt_unit_stake}')
            self.assertAlmostEqual(est_returns, receipt_est_returns,
                                   delta=0.015,
                                   msg=f'Est. returns "{est_returns}" is not the same as on bet receipt {receipt_est_returns}')
            ti_bets = [normalize_name(bet) for bet in ti_bet_info.bets]
            self.assertListEqual(sorted(ti_bets), sorted(section.items_names),
                                 msg=f'Bets on betreceipt "{sorted(ti_bets)}" and betslip '
                                     f'"{sorted(section.items_names)}" are not the same')
            receipt_markets = []
            receipt_events = []
            for receipt_name, receipt in section.items_as_ordered_dict.items():
                receipt_markets.append(receipt.market_type[:-2])
                receipt_events.append(receipt.event_description)
            ti_markets = [normalize_name(market) for market in ti_bet_info.markets]
            self.assertListEqual(sorted(ti_markets), sorted(receipt_markets),
                                 msg=f'Markets on betreceipt "{sorted(ti_markets)}" and betslip '
                                     f'"{sorted(receipt_markets)}" are not the same')
            ti_events = [normalize_name(event) for event in ti_bet_info.events]
            self.assertListEqual(sorted(ti_events), sorted(receipt_events),
                                 msg=f'Events on betreceipt "{sorted(ti_events)}" and betslip '
                                     f'"{sorted(receipt_events)}" are not the same')
