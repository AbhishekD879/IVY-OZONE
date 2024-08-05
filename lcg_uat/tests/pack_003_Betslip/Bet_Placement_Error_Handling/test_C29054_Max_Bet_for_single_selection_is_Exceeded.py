import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.max_min_bet
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29054_Max_Bet_for_single_selection_is_Exceeded(BaseBetSlipTest):
    """
    TR_ID: C29054
    NAME: Max Bet for single selection is Exceeded
    DESCRIPTION: This test case verifies bet slip error handling in case when user's individual Max bet for selected market is exceeded
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  The user's account balance is sufficient to cover the max bet stake
    PRECONDITIONS: 3. Overask is turned off for used user
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'NEXT 4' module
    PRECONDITIONS: - event landing page
    """
    keep_browser_open = True
    max_bet = 0.02
    extremely_large_bet_amount = 50

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login as a user with disabled overask
        EXPECTED: Test events are available
        EXPECTED: User is logged in
        """
        self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet).selection_ids
        self.__class__.selection_ids_2 = self.ob_config.add_UK_racing_event(max_bet=self.max_bet, number_of_runners=1).selection_ids
        self.site.login(username=tests.settings.disabled_overask_user)

    def test_001_add_sport_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add Sport selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])

    def test_002_enter_extremely_large_stake_value_in_stake_field_click_bet_now(self):
        """
        DESCRIPTION: Enter extremely large stake value in 'Stake' field
        DESCRIPTION: Click 'Bet Now'
        EXPECTED: Error notification is displayed above stake section (Text: 'Maximum stake is <currency><amount>')
        EXPECTED: Place Bet button is active
        """
        self.__class__.bet_amount = self.extremely_large_bet_amount
        self.place_single_bet()
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        error = stake.wait_for_error_message(timeout=10)
        expected_msg = vec.betslip.MAX_STAKE.format(self.max_bet)
        self.assertEqual(error, expected_msg,
                         msg=f'Actual message "{error}" != Expected "{expected_msg}"')
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(),
                        msg='Bet button is not active, but was expected to be')

    def test_003_enter_correct_stake_which_is_equivalent_to_max_bet_and_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Enter correct stake which is equivalent to max bet and tap on 'Bet Now' button
        EXPECTED: Bet is placed
        EXPECTED: User balance is decreased by value entered in stake field
        """
        self.__class__.bet_amount = self.max_bet

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        stake.amount_form.input.value = self.bet_amount

        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.user_balance - self.bet_amount)

    def test_004_repeat_steps_for_racing(self):
        """
        DESCRIPTION: Repeat previous steps for Racing selection
        """
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids_2.values())[0])
        self.test_002_enter_extremely_large_stake_value_in_stake_field_click_bet_now()
        self.test_003_enter_correct_stake_which_is_equivalent_to_max_bet_and_tap_on_bet_now_button()
