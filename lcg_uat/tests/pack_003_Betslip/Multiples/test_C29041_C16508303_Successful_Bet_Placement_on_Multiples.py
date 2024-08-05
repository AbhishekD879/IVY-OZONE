import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod We can't get info about bet from TI on prod
# @pytest.mark.hl We can't get info about bet from TI on prod
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.bet_receipt
@pytest.mark.slow
@pytest.mark.timeout(700)
@pytest.mark.login
@vtest
class Test_C29041_C16508303_Successful_Bet_Placement_on_Multiples(BaseBetSlipTest):
    """
    TR_ID: C29041
    TR_ID: C16508303
    NAME: Successful Bet Placement on Multiples
    DESCRIPTION: This test case verifies placing a bet on Multiples
    DESCRIPTION: NOTE: For checking information in IMS system  navigate by link
    DESCRIPTION: http://backoffice-tst2.coral.co.uk/ti/bet
    DESCRIPTION: and set up fields 'Placed At'(date of placing bet) and 'Receipt' (ex.  "O/0123364/0000141" from bet receipt of placed bet) with proper values
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test football events
        """
        self.__class__.selection_id_1 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
        self.__class__.selection_id_2 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]
        self.__class__.selection_id_3 = list(self.ob_config.add_autotest_premier_league_football_event().selection_ids.values())[0]

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        DESCRIPTION: Login with user with positive balance
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username, async_close_banners=False)

    def test_002_add_several_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1,
                                                         self.selection_id_2))

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        """
        # Done in prev. step
        pass

    def test_004_open_betslip_multiplessection(self):
        """
        DESCRIPTION: Open Betslip->'Multiples' section
        EXPECTED: Multiples are displayed
        """
        # Done in next step
        pass

    def test_005_enter_stake_for_one_of_available_multiples(self):
        """
        DESCRIPTION: Enter Stake for one of available Multiples
        EXPECTED: Est. Returns, Total Stake and Total Est. Returns fields are calculated
        """
        self.__class__.user_balance = self.get_balance_by_page('betslip')
        self.__class__.number_of_stakes = 1
        self.__class__.betslip_info = self.place_and_validate_multiple_bet(number_of_stakes=self.number_of_stakes)

    def test_006_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: Multiple Bet is placed successfully (the one which had entered Stake, the rest Multiples are ignored)
        EXPECTED: User balance is decreased by Total Stake
        EXPECTED: Bet Receipt page is shown with the correct information about placed bet
        """
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.user_balance - self.bet_amount * self.number_of_stakes)
        self.check_bet_receipt(self.betslip_info)
        betreceipt_section = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertEqual(betreceipt_section.__len__(), 1, msg='There is more than one item in Bet Receipt')
        for section_name, section in betreceipt_section.items():
            self.__class__.bet_id = section.bet_id
        self.__class__.ti_bet_info = self.ob_config.get_bet_info(username=self.username, bet_id=self.bet_id)

    def test_007_tap_done_button(self):
        """
        DESCRIPTION: Tap 'Done' button
        EXPECTED: User is returned to the main view she/he was before placing the bet (Sport / Race Landing page, Homepage)
        """
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('Homepage')

    def test_008_check_placed_bet_correctness_in_openbet_system(self):
        """
        DESCRIPTION: Check placed bet correctness in Openbet system
        EXPECTED: Information should be correct in Openbet system
        """
        bets = [bet for bet_name, bet in self.betslip_info.items()
                if bet_name not in ['Patent', 'Treble', 'Double', 'Trixie', 'Round Robin', 'Flag',
                                    'Single Stakes About', 'Double Stakes About', 'total_stake', 'total_estimate_returns']]
        markets = [bet['market_name'] for bet in bets]
        events = [bet['event_name'].replace(' v ', ' vs ') for bet in bets]
        ti_events = [event.replace(' v ', ' vs ').replace('|', '').replace('\n', '') for event in self.ti_bet_info.events]
        outcomes = [bet['outcome_name'] for bet in bets]
        ti_markets = [market.replace('|', '') for market in self.ti_bet_info.markets]
        ti_bets = [bet.replace('|', '').replace('\n', '') for bet in self.ti_bet_info.bets]
        self.assertListEqual(sorted(ti_markets), sorted(markets),
                             msg=f'Markets on openbet "{sorted(ti_markets)}" and betslip '
                                 f'"{sorted(markets)}" are not the same')
        self.assertListEqual(sorted(ti_events), sorted(events),
                             msg=f'Event on openbet "{sorted(ti_events)}" and betslip '
                                 f'"{sorted(events)}" are not the same')
        self.assertListEqual(sorted(ti_bets), sorted(outcomes),
                             msg=f'Bets on openbet "{sorted(ti_bets)}" and betslip '
                                 f'"{sorted(outcomes)}" are not the same')
        self.assertAlmostEqual(float(self.ti_bet_info.est_returns), self.betslip_info['total_estimate_returns'], delta=0.015,
                               msg=f'Estimate return on openbet "{float(self.ti_bet_info.est_returns)}" doesn\'t match'
                                   f' estimate returns on Bet Slip "{self.betslip_info["total_estimate_returns"]}" within 0.015 delta')
        self.assertAlmostEqual(float(self.ti_bet_info.stake), self.betslip_info['total_stake'], delta=0.015,
                               msg=f'Estimate return on Bet Receipt "{float(self.ti_bet_info.stake)}" doesn\'t match '
                                   f'estimate returns on Bet Slip "{self.betslip_info["total_stake"]}" within 0.015 delta')

    def test_009_add_several_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip
        """
        self.expected_betslip_counter_value = 3
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1,
                                                         self.selection_id_2,
                                                         self.selection_id_3))

    def test_010_enter_stake_for_all_available_multiples(self):
        """
        DESCRIPTION: Enter Stake for all available Multiples
        EXPECTED: Est. Returns, Total Stake and Total Est. Returns fields are calculated
        """
        self.user_balance = self.get_balance_by_page('betslip')
        self.__class__.betslip_info = self.place_and_validate_multiple_bet()

    def test_011_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: Multiple Bets is placed successfully
        EXPECTED: User balance is decreased by Total Stake
        EXPECTED: Bet Receipt page is shown with the correct information about placed bet
        """
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.user_balance - self.betslip_info['total_stake'])
        self.check_bet_receipt(self.betslip_info)

    def test_012_check_placed_bet_correctness_in_openbet_system(self):
        """
        DESCRIPTION: Check placed bet correctness in Openbet system
        EXPECTED: Information should be correct in Openbet system
        """
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        for section_name, section in betreceipt_sections.items():
            bet_id = section.bet_id
            self._logger.debug(f'*** Bet receipt id "{bet_id}" and name type "{section_name}"')
            ti_bet_info = self.ob_config.get_bet_info(username=self.username, bet_id=bet_id)

            unit_stake = float(ti_bet_info.stake)
            receipt_unit_stake = float(section.total_stake) / section.bet_multiplier
            est_returns = ti_bet_info.est_returns
            receipt_est_returns = section.estimate_returns
            ti_bets = [bet.replace('|', '').replace('\n', '') for bet in ti_bet_info.bets]
            self.assertAlmostEqual(receipt_unit_stake, unit_stake,
                                   delta=0.015,
                                   msg=f'Unit stake "{unit_stake}" is not the same as on bet receipt {receipt_unit_stake}')
            self.assertAlmostEqual(est_returns, receipt_est_returns,
                                   delta=0.015,
                                   msg=f'Est. returns "{est_returns}" is not the same as on bet receipt {receipt_est_returns}')
            self.assertListEqual(sorted(ti_bets), sorted(section.items_names),
                                 msg=f'Bets on betreceipt "{sorted(ti_bets)}" and betslip '
                                     f'"{sorted(section.items_names)}" are not the same')
            receipt_markets = []
            receipt_events = []
            for receipt_name, receipt in section.items_as_ordered_dict.items():
                receipt_markets.append(receipt.market_type[:-2])
                receipt_events.append(receipt.event_description.replace(' v ', ' vs '))

            ti_markets = [market.replace('|', '') for market in ti_bet_info.markets]
            ti_events = [event.replace('|', '').replace(' v ', ' vs ').replace('\n', '') for event in ti_bet_info.events]

            self.assertListEqual(sorted(ti_markets), sorted(receipt_markets),
                                 msg=f'Markets on betreceipt "{sorted(ti_markets)}" and betslip '
                                     f'"{sorted(receipt_markets)}" are not the same')
            self.assertListEqual(sorted(ti_events), sorted(receipt_events),
                                 msg=f'Events on betreceipt "{sorted(ti_events)}" and betslip '
                                     f'"{sorted(receipt_events)}" are not the same')
