import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.login
@vtest
class Test_C29057_User_Balance_is_Too_Low_for_Placing_Multiple_Bets(BaseBetSlipTest):
    """
    TR_ID: C29057
    NAME: User Balance is Too Low for Placing Multiple Bets
    DESCRIPTION: This test case verifies Error Handling When User Balance is Too Low for Placing Multiple Bets
    DESCRIPTION: AUTOTEST C2491007
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User's balance is not sufficient to cover any stake, no registered payment methods
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find a few selections to the Bet Slip
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            event_params_2 = self.ob_config.add_autotest_premier_league_football_event()
            event_params_3 = self.ob_config.add_autotest_premier_league_football_event()

            self.__class__.selection_ids = (event_params.selection_ids[event_params.team1],
                                            event_params_2.selection_ids[event_params_2.team1],
                                            event_params_3.selection_ids[event_params_3.team1])
        else:
            selection_ids = []
            events = self.get_active_events_for_category(number_of_events=3)
            for event in events:
                for market in event['event']['children']:
                    if market['market']['templateMarketName'] == 'Match Betting' and market['market'].get('children'):
                        selection_ids.append(market['market']['children'][0]['outcome']['id'])
                        break

            self.__class__.selection_ids = tuple(selection_ids)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.wait_content_state("Home")
        balance = self.site.header.user_balance
        self.assertEqual(balance, 0.00, msg=f'{balance} not equal to {0.00}')

    def test_001_add_few_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add few selections to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_enter_multiples_stake_which_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Enter Multiples stake which won't exceed a max bet allowed
        EXPECTED: 'Bet Now' (from OX 99 'Place Bet') button is enabled
        """
        sections = self.get_betslip_sections(multiples=True)
        multiples_section = sections.Multiples
        stake_name, stake = list(multiples_section.items())[0]
        self.enter_stake_amount(stake=(stake.name, stake))
        deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(deposit_button.is_enabled(), msg=f'"{deposit_button.name}" button is not enabled')
        self.assertEqual(deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'\nActual button name: "{deposit_button.name}"'
                             f'\nis not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_003_tap_on_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: Tap on 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: Betslip is closed
        EXPECTED: User is navigated to 'Deposit' page, 'Add Credit/Debit Cards' tab for Coral brand
        EXPECTED: User is navigated to Account One system for Ladbrokes brand
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        wait_for_result(lambda: self.site.deposit.is_displayed(),
                        name='Deposit page is not loaded',
                        timeout=20)
        self.assertTrue(self.site.select_deposit_method.is_displayed(), msg='User is not navigated to the deposit page')
        if self.brand == 'ladbrokes' and tests.settings.backend_env == 'tst2':
            self.assertTrue(self.site.select_deposit_method.debit_card_button.is_displayed(),
                            msg='"Master Card" button is not displayed"')
        else:
            self.assertTrue(self.site.select_deposit_method.master_card_button.is_displayed(),
                            msg='"Master Card" button is not displayed"')
            self.assertTrue(self.site.select_deposit_method.visa_button.is_displayed(),
                            msg='"Visa Card" button is not displayed')
            self.assertTrue(self.site.select_deposit_method.maestro_button.is_displayed(),
                            msg='"Maestro Card" button is not displayed')
