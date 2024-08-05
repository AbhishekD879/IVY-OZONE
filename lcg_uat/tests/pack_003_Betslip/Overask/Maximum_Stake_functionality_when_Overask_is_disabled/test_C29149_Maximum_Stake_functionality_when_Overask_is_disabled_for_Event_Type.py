import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.max_min_bet
@pytest.mark.bet_placement
@pytest.mark.forecast_tricast
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29149_Maximum_Stake_functionality_when_Overask_is_disabled_for_Event_Type(BaseBetSlipTest):
    """
    TR_ID: C29149
    NAME: This test case verifies Maximum Stake functionality when Overask is disabled for Event type
    DESCRIPTION: This test case verifies Maximum Stake functionality when Overask is disabled for Event type
    PRECONDITIONS: To enable/disable Overask for type event lease follow this path:
    PRECONDITIONS: Backoffice tool -> Events hierarchy -> Type -> Bet Intercept -> Check/Uncheck option
    """
    keep_browser_open = True
    min_bet = 0.01
    max_bet = 0.03
    bet_amount = 0.04
    expected_max_bet_msg = vec.betslip.MAX_STAKE.format(max_bet)
    selection_ids, selection_ids_2, selection_ids_3 = None, None, None
    double_stake_title = vec.betslip.DBL
    draw_stake_title = vec.sb.DRAW.title()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Disable Overask for event type
        """
        self.__class__.selection_ids = \
            self.ob_config.add_football_event_to_special_league(min_bet=self.min_bet, max_bet=self.max_bet,
                                                                max_mult_bet=self.max_bet).selection_ids
        self.__class__.selection_ids_2 = \
            self.ob_config.add_football_event_to_special_league(min_bet=self.min_bet, max_bet=self.max_bet,
                                                                max_mult_bet=self.max_bet).selection_ids
        self.__class__.selection_ids_3 = \
            self.ob_config.add_autotest_premier_league_football_event(min_bet=self.min_bet, max_bet=self.max_bet,
                                                                      max_mult_bet=self.max_bet).selection_ids

    def test_001_login_with_user_who_has_enabled_overask_and_add_selection_for_event_with_disabled_overask(self):
        """
        DESCRIPTION: Login with user who has enabled Overask functionality and add selection for event with disabled Overask for its type
        """
        self.site.login(username=tests.settings.overask_enabled_user)
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.draw_stake_title])

    def test_002_enter_stake_value_which_is_higher_then_maximum_allowed_stake_for_this_bet(self):
        """
        DESCRIPTION: Enter Stake value which is higher then maximum allowed Stake for this bet
        """
        self.place_single_bet()

    def test_003_tap_click_on_bet_now_button(self):
        """
        DESCRIPTION: Tap/click on 'Bet now' button
        EXPECTED: *   Bet is NOT placed
        EXPECTED: *   'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: *   Place Bet button is active
        """
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.draw_stake_title)
        self.assertTrue(stake, msg=f'No stake with name "{self.draw_stake_title}" found')

        self.verify_user_balance(expected_user_balance=self.user_balance)

        error_message = stake.wait_for_error_message()
        self.assertEqual(error_message, self.expected_max_bet_msg,
                         msg=f'\nActual message: \n"{error_message}" '
                             f'\nis not as expected: \n"{self.expected_max_bet_msg}"')

        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=3),
                        msg=f'"{bet_now_button.name}" button is disabled')

    def test_004_add_multiples_to_betslip_for_event_type_with_disabled_overask(self):
        """
        DESCRIPTION: Add Multiples to Betslip for Event type with disabled Overask
        """
        self.clear_betslip()
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.draw_stake_title],
                                                         self.selection_ids_2[self.draw_stake_title]))

    def test_005_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: *   Bet is NOT placed
        EXPECTED: *   'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: *   Place Bet button is active
        """
        self.place_multiple_bet()

        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        stake = multiples_section.get(self.double_stake_title)
        self.assertTrue(stake, msg=f'No stake with name "{self.double_stake_title}" found')

        self.verify_user_balance(expected_user_balance=self.user_balance)

        error_message = stake.wait_for_error_message()
        self.assertEqual(error_message, self.expected_max_bet_msg,
                         msg=f'\nActual message: \n"{error_message}" '
                             f'\nis not as expected: \n"{self.expected_max_bet_msg}"')

        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=1),
                        msg=f'"{bet_now_button.name}" button is disabled')

    def test_006_add_multiples_for_different_event_types_one_of_which_has_enabled_overask_and_the_second_one_is_disabled(self):
        """
        DESCRIPTION: Add Multiples for different event types, one of which has enabled overask functionality, and the second one - disabled
        """
        self.clear_betslip()
        self.open_betslip_with_selections(selection_ids=(self.selection_ids_3[self.draw_stake_title],
                                                         self.selection_ids_2[self.draw_stake_title]))

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: Overask review is started / Max Bet error message is displayed depending on OB response
        EXPECTED: OB response is located in PlaceBet call
        """
        self.place_multiple_bet()
        try:
            overask_warning = self.get_betslip_content().overask.has_overask_warning()
            self.assertTrue(overask_warning, msg='Overask warning message is not shown')
        except VoltronException:
            self._logger.warning('*** Overask review has not been started')
            multiples_section = self.get_betslip_sections(multiples=True).Multiples
            stake = multiples_section.get(self.double_stake_title)
            self.assertTrue(stake, msg=f'No stake with name "{self.double_stake_title}" found')

            error_message = stake.wait_for_error_message()
            self.assertEqual(error_message, self.expected_max_bet_msg,
                             msg=f'\nActual message: \n"{error_message}" '
                                 f'\nis not as expected: \n"{self.expected_max_bet_msg}"')
