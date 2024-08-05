import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29053_Place_a_Bet_on_several_selections_when_user_is_Logged_In(BaseBetSlipTest):
    """
    TR_ID: C29053
    NAME: Place a Bet on several selections when user is Logged In
    """
    keep_browser_open = True

    def check_bet_receipt(self, betslip_info, each_way=False, sp=False, freebet=False, forecast_tricast=False, **kwargs):
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        for section_name, section in betreceipt_sections.items():
            receipts = section.items_as_ordered_dict
            self.assertTrue(receipts, msg='No Receipt legs found')
            market_type = []
            if section_name != vec.betslip.SINGLE:
                self.__class__.bet_id = section.bet_id
                self._logger.info(f'*** Bet receipt id "{self.bet_id}" and name type "{section_name}"')
                total_stake = section.total_stake
                betslip_bet = betslip_info[section.multiple_bet_type]['bet_amount'] * section.bet_multiplier
                self.assertAlmostEqual(float(total_stake),
                                       betslip_bet,
                                       delta=0.015,
                                       msg=f'Total stake "{total_stake}" is not the same as on betslip "{betslip_bet}" '
                                       f'within 0.015 delta')
                est_returns = section.estimate_returns
                betslip_est_returns = betslip_info[section.multiple_bet_type]['estimate_returns']
                if betslip_est_returns == 'N/A':
                    self.assertEqual(est_returns, betslip_est_returns,
                                     msg=f'Estimate return on Bet Receipt "{est_returns}" doesn\'t match estimate returns '
                                         f'on Bet Slip "{betslip_est_returns}"')
                else:
                    self.assertAlmostEqual(float(est_returns), betslip_est_returns,
                                           delta=0.015,
                                           msg=f'Estimate return on Bet Receipt "{est_returns}" doesn\'t match estimate returns '
                                               f'on Bet Slip "{betslip_est_returns}" within 0.015 delta')
                self._logger.info(f'*** Total stake: "{total_stake}", est returns: "{est_returns}"')
            for receipt_name, receipt in receipts.items():
                receipt_type = receipt.__class__.__name__
                self._logger.info(f'*** Receipt name "{receipt_name}" has type "{receipt_type}"')
                if receipt_type == 'ReceiptSingles':
                    # TODO: fix comparison of stake values on betslip and betreceipt:
                    # TODO:(now stake 1 on betslip can be compared to stake 2 on receipt)
                    outcome_name = receipt_name
                    event_name = receipt.event_name
                    result = event_name == betslip_info[outcome_name]['event_name'].strip()
                    result_wa = event_name in betslip_info[outcome_name]['event_name'].strip()  # workaround for PROD incident BMA-52751 (repro only on some racing events)
                    self.assertTrue(result or result_wa,
                                    msg='Event name on bet receipt "%s" is not the same as on Bet Slip "%s"'
                                        % (event_name, betslip_info[outcome_name]['event_name'].strip()))
                    self.__class__.bet_id = receipt.bet_id
                    self.assertTrue(self.bet_id is not None, msg='Bet id on Bet Receipt is empty')

                    odds = receipt.odds if not sp else 'SP'
                    if not forecast_tricast:
                        self.assertEqual(odds, betslip_info[outcome_name]['odds'],
                                         msg='Odds on bet receipt "%s" is not the same as on BetSlip "%s"'
                                             % (odds, betslip_info[outcome_name]['odds']))

                    market = normalize_name(receipt.event_market_name.replace(' /', '').replace('Match Betting','Match Result'))
                    market_type.append(market)
                    self.assertEqual(market, betslip_info[outcome_name]['market_name'].replace('Match Betting','Match Result'),
                                     msg='Market name on bet receipt "%s" is not the same as on Bet Slip "%s"'
                                         % (market, betslip_info[outcome_name]['market_name']))
                    if each_way:
                        ew_terms = receipt.ew_terms
                        self.assertTrue(ew_terms is not None and ew_terms != '',
                                        msg='Each way terms is not found in bet receipt')
                    total_stake = receipt.free_bet_stake if freebet else receipt.total_stake
                    self.assertTrue(float(total_stake) is not None, msg='Total stake is None')
                    est_returns = 'N/A' if receipt.estimate_returns == 'N/A' else float(receipt.estimate_returns)
                    if betslip_info[outcome_name]['estimate_returns'] != 'N/A':
                        self.assertAlmostEqual(est_returns, betslip_info[outcome_name]['estimate_returns'], delta=0.015,
                                               msg='Estimate return on Bet Receipt "%s" is not the same as '
                                                   'on Bet Slip "%s"' % (
                                                   est_returns, betslip_info[outcome_name]['estimate_returns']))
                    self._logger.info('*** Name: "%s", bet id: "%s", event name: "%s", event market: "%s", '
                                      'odds: "%s", total stake: "%s", est returns: "%s"'
                                      % (outcome_name, self.bet_id, event_name,
                                         market_type, odds, total_stake, est_returns))
                elif receipt_type == 'ReceiptMultiples':
                    self._logger.info(f'*** Multiples section header: {receipt.name}')
                    market_type.append(normalize_name(receipt.market_type[:-2]))
                    self._logger.info(f'*** Market type "{market_type}"')
                    self._logger.info(f'*** Multiples receipt leg items: {receipt.event_description}')

            stake_name = kwargs.get('stake_name')
            if stake_name:
                betslip_markets = betslip_info[stake_name]['market_name']
            else:
                betslip_markets = [bet['market_name'] for bet_name, bet in betslip_info.items()
                                   if bet_name not in ['Patent', 'Treble', 'Double', 'Single Stakes About (3)', 'Trixie', 'Round Robin', 'Flag', 'Single Stakes About',
                                                       'Double Stakes About', 'total_stake', 'total_estimate_returns']]
            market_type = ['Match Result' if ui_market == 'Match Betting' else ui_market for ui_market in market_type]
            betslip_markets = ['Match Result' if ui_market == 'Match Betting' else ui_market for ui_market in betslip_markets]
            self.assertListEqual(sorted(market_type), sorted(betslip_markets),
                                 msg=f'Markets on betreceipt "{sorted(market_type)}" and betslip '
                                 f'"{sorted(betslip_markets)}" are not the same')
            footer = self.site.bet_receipt.footer
            total_stake = footer.total_stake
            total_est_returns = footer.total_estimate_returns
            self.__class__.total_stake_betreceipt = float(total_stake.replace(',', ''))
            self._logger.info(f'*** Total stake {self.total_stake_betreceipt}, total est returns {total_est_returns}')
            self.assertEqual(betslip_info['total_stake'], self.total_stake_betreceipt,
                             msg=f'Total stake on betslip {betslip_info["total_stake"]} doesn\'t match with total '
                             f'stake on betreceipt {self.total_stake_betreceipt}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Login into app
        EXPECTED: Event is created
        EXPECTED: User is logged in
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.football_selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'Found Football event with outcomes "{self.football_selection_ids}"')

            self.__class__.racing_selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.horseracing_config.category_id)
            self._logger.info(f'Found Racing event with outcomes "{self.racing_selection_ids}"')
            self.__class__.selection_ids = (list(self.football_selection_ids.values())[0],
                                            list(self.racing_selection_ids.values())[0])

        else:
            football_event = self.ob_config.add_autotest_premier_league_football_event()

            racing_event = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '1/2'})

            self.__class__.selection_ids = (football_event.selection_ids[football_event.team1],
                                            list(racing_event.selection_ids.values())[0])

        self.site.login()

    def test_001_add_several_selections_to_the_bet_slip_and_open_betslip(self):
        """
        DESCRIPTION: Add several selections to the Bet Slip
        EXPECTED: Betslip counter is increased
        EXPECTED: Open Betslip
        EXPECTED: Added selections are displayed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_enter_valid_stakes_in_stake_fields_and_click_on_bet_now_button(self):
        """
        DESCRIPTION: Enter valid stakes in 'Stake' fields
        EXPECTED: Click on 'Bet Now' button
        EXPECTED: 1.  Bets are placed successfully
        EXPECTED: 2.  User 'Balance' is decreased by values entered in 'Stake' field
        EXPECTED: 3.  Bet Slip is replaced with a Bet Receipt view
        """
        self.__class__.betslip_info = self.place_and_validate_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()

    def test_003_verify_bet_receipt_for_few_selections(self):
        """
        DESCRIPTION: Verify Bet Receipt for few selections
        EXPECTED: 1. Bet Receipt header and back button are present
        EXPECTED: 2. Bet Receipt contains the following information:
        EXPECTED: Bet Receipt details for each selection:
        EXPECTED: *   header 'Singles' with the total number of single bets - i.e. Singles (1)
        EXPECTED: *   the outcome name made by the customer
        EXPECTED: *   Outcome name contains handicap value near the name (if such are available for outcomes)
        EXPECTED: *   the market type user has bet on - i.e. Win or Each Way
        EXPECTED: *   the event name to which the outcome belongs to
        EXPECTED: *   the Bet ID. The Bet ID is start with O and contain numeric values - i.e. O/0123828/0000155
        EXPECTED: *   'i' icon
        EXPECTED: *   Odds of the selection (for <Race> with 'SP' price - N/A)
        EXPECTED: *   Unit Stake and 'E/W' label (if 'Each Way' option was selected)
        EXPECTED: *   Stake
        EXPECTED: *   Free Bet Stake (if Free bet was selected)
        EXPECTED: *   Total Stake = Stake + Free Bet Stake
        EXPECTED: *   Est. Returns (for <Race> with 'SP' price - N/A)
        EXPECTED: Total Bet Receipt details:
        EXPECTED: *   Stake
        EXPECTED: *   Free Bet Stake  (if Free bet was selected)
        EXPECTED: *   Total Stake = Stake + Free Bet Stake
        EXPECTED: *   Total Est. Returns (for <Race> with 'SP' price - N/A)
        EXPECTED: 3. 'Reuse Selection' and 'Done' buttons
        EXPECTED: All information corresponds to the information about just placed bet
        """
        self.check_bet_receipt_is_displayed()
        self.check_bet_receipt(betslip_info=self.betslip_info)
        self.site.bet_receipt.close_button.click()

    def test_004_go_to_settings_switch_odds_format_to_decimal_and_go_back_to_bet_receipt_page(self):
        """
        DESCRIPTION: Go to Settings, switch Odds format to Decimal and go back to Bet Receipt page
        EXPECTED: Odds are shown in Decimal format
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

    def test_005_add_again_selections_to_the_bet_slip_and_open_betslip(self):
        """
        DESCRIPTION: Tap 'Reuse Selection' button on Bet Receipt page
        EXPECTED: User is returned to the Betslip to initiate bet placement again on the same selections
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_006_place_bet_and_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify 'Done' button on Bet Receipt page
        EXPECTED: Bet Slip slider closes
        EXPECTED: User stays on the same age
        """
        self.__class__.betslip_info = self.place_and_validate_single_bet(number_of_stakes=2)
        self.check_bet_receipt_is_displayed()
        self.check_bet_receipt(betslip_info=self.betslip_info)
