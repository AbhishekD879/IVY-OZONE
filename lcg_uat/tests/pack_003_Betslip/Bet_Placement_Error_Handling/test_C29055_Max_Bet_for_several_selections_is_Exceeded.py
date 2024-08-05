import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot create events on prod / looking for specific events is too complicated
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.max_min_bet
@pytest.mark.ob_smoke
@pytest.mark.bet_placement
@pytest.mark.slow
@pytest.mark.desktop
@pytest.mark.timeout(800)
@pytest.mark.login
@vtest
class Test_C29055_Max_Bet_for_several_selections_is_Exceeded(BaseBetSlipTest):
    """
    TR_ID: C29055
    NAME: Max Bet for several selections is Exceeded
    DESCRIPTION: This test case verifies Error Handling When Max Bet for several selections is Exceeded
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. The user's account balance is sufficient to cover the max bet stake
    PRECONDITIONS: 3. Overask is turned off for used user
    PRECONDITIONS: 4. App is loaded
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races>  it is possible to place a bet from:
    PRECONDITIONS: - 'NEXT 4' module
    PRECONDITIONS: - event landing page
    """
    keep_browser_open = True
    max_bet = 0.02
    expected_max_bet_msg = vec.betslip.MAX_STAKE.format(max_bet)
    increased_max_bet = 0.03
    selection_ids_2 = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        EXPECTED: Test events are available
        EXPECTED: User is logged in
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet, max_mult_bet=self.max_bet)
        self.__class__.selection_ids, self.__class__.team1, self.__class__.eventID =\
            event_params.selection_ids, event_params.team1, event_params.event_id
        event_params = self.ob_config.add_UK_racing_event(max_bet=self.max_bet, max_mult_bet=self.max_bet, number_of_runners=1)
        self.__class__.selection_ids_2, self.__class__.eventID_2 = event_params.selection_ids, event_params.event_id
        self.site.login(username=tests.settings.disabled_overask_user)

    def test_001_add_few_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add few selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1], list(self.selection_ids_2.values())[0]))

    def test_002_enter_extremely_large_stake_values_in_stake_field_click_bet_now(self):
        """
        DESCRIPTION: Enter extremely large stake values in 'Stake' field
        DESCRIPTION: Click 'Bet Now'
        EXPECTED: Bet is NOT placed
        EXPECTED: Error notification is displayed above stake section (Text: 'Maximum stake is <currency><amount>')
        EXPECTED: Place Bet button is active
        """
        self.__class__.bet_amount = self.increased_max_bet
        self.place_single_bet()
        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            error = stake.wait_for_error_message()
            self.assertEqual(error, self.expected_max_bet_msg,
                             msg=f'Actual message "{error}" != Expected "{self.expected_max_bet_msg}"')
        self.assertTrue(self.get_betslip_content().bet_now_button.is_enabled(timeout=3),
                        msg='Bet button is not active, but was expected to be')

    def test_003_enter_correct_stakes_which_is_equivalent_to_max_bet_which_is_displayed_on_error_message_above_each_selection_and_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Enter correct stakes which is equivalent to max bet and tap on 'Place Bet' button
        EXPECTED: Bet is placed
        EXPECTED: User balance is decreased by value entered in stake field
        """
        self.__class__.bet_amount = self.max_bet

        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            stake.amount_form.input.value = self.bet_amount

        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.user_balance - (self.bet_amount * 2))

    def test_004_enter_a_stakes_but_make_sure_max_bets_are_changed_via_liveserv_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Enter a stakes but make sure Max Bets are changed via LiveServ -> tap on 'Bet Now' button.
        EXPECTED: Max Bet amount can be changed.
        EXPECTED: 1.  In case if entered stakes are still higher then 'max bet' -> results will be the same as in steps # 3
        EXPECTED: 2.  In case if entered stakes are less then 'max bet' -> bets will be placed
        """
        self.site.bet_receipt.footer.click_done()
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_add_few_selection_to_the_bet_slip()

        self.ob_config.change_min_max_bet_limits(id=self.selection_ids[self.team1], level='selection',
                                                 max_mult_bet=self.max_bet * 2, max_bet=self.max_bet * 2)
        self.ob_config.change_min_max_bet_limits(id=list(self.selection_ids_2.values())[0], level='selection',
                                                 max_mult_bet=self.max_bet * 2, max_bet=self.max_bet * 2)

        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.user_balance - (self.bet_amount * 2))

    def test_005_set_back_default_max_bet_limits(self):
        """
        DESCRIPTION: Set back default max bet limits
        """
        self.ob_config.change_min_max_bet_limits(id=self.selection_ids[self.team1], level='selection',
                                                 max_mult_bet=self.max_bet, max_bet=self.max_bet)
        self.ob_config.change_min_max_bet_limits(id=list(self.selection_ids_2.values())[0], level='selection',
                                                 max_mult_bet=self.max_bet, max_bet=self.max_bet)

    def test_006_add_two_or_more_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more selections from different events to the Bet Slip
        EXPECTED: Selections are added
        """
        self.site.bet_receipt.close_button.click()
        self.site.logout()
        self.site.login(username=tests.settings.disabled_overask_user)
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1], list(self.selection_ids_2.values())[0]))

    def test_007_repeat_steps_3_6_for_multiples_section(self):
        """
        DESCRIPTION: Repeat steps # 3 - 6 for 'Multiples' section
        EXPECTED:
        """
        self.__class__.bet_amount = self.increased_max_bet
        self.place_multiple_bet(number_of_stakes=1)

        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        stake_name, stake = list(multiples_section.items())[0]
        error = stake.wait_for_error_message()
        self.assertEqual(error, self.expected_max_bet_msg,
                         msg=f'Actual message "{error}" != Expected "{self.expected_max_bet_msg}"')

        self.__class__.bet_amount = self.max_bet
        self.place_multiple_bet(number_of_stakes=1)

        self.check_bet_receipt_is_displayed()
        self.verify_user_balance(expected_user_balance=self.user_balance - self.bet_amount)

        for event_id in (self.eventID, self.eventID_2):
            self.ob_config.change_min_max_bet_limits(id=event_id, max_mult_bet=self.increased_max_bet, max_bet=self.increased_max_bet)
        self.__class__.bet_amount = self.max_bet
        self.test_006_add_two_or_more_selections_from_different_events_to_the_bet_slip()
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

        self.verify_user_balance(expected_user_balance=self.user_balance - self.bet_amount)
