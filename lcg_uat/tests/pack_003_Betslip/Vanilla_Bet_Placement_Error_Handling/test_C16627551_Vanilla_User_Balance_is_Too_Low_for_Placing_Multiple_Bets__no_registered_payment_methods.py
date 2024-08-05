from time import sleep

import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.login
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-48323')  # Vanilla desktop
class Test_C16627551_Vanilla_User_Balance_is_Too_Low_for_Placing_Multiple_Bets__no_registered_payment_methods(BaseBetSlipTest):
    """
    TR_ID: C16627551
    NAME: [Vanilla] User Balance is Too Low for Placing Multiple Bets (no registered payment methods)
    DESCRIPTION: This test case verifies Error Handling When User Balance is Too Low for Placing Multiple Bets
    PRECONDITIONS: 1.  The user account is NOT sufficient to cover multiple stakes (no registered payment methods)
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> sport it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event landing page
    PRECONDITIONS: NOTE: in order to check Max Allowed Bet enter extremely large stake value in 'Stake' field and tap 'Bet Now' button to see what is Max allowed bet for selection.
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

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.user_has_no_pm_0_balance)

    def test_002_add_multiple_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add multiple selection to the Bet Slip
        EXPECTED: Betslip counter is increased with number of selections
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_003_go_to_betslip_and_enter_multiples_stake_which_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Go to 'Betslip' and enter Multiples stake which won't exceed a max bet allowed
        EXPECTED: 'PLACE BET' button is changed to 'MAKE A DEPOSIT'
        """
        sections = self.get_betslip_sections(multiples=True)
        multiples_section = sections.Multiples
        stake_name, stake = list(multiples_section.items())[0]
        self.enter_stake_amount(stake=(stake.name, stake))
        self.__class__.deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(self.deposit_button.is_enabled(), msg=f'"{self.deposit_button.name}" button is not enabled')
        self.assertEqual(self.deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'\nActual button name: "{self.deposit_button.name}"'
                             f'\nis not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_004_tap_make_a_deposit(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT'
        EXPECTED: User is redirected to 'Deposit' page
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        sleep(20)
        self.assertTrue(self.site.select_deposit_method.is_displayed(),
                        msg='"Select Deposit Method page" is not displayed')
