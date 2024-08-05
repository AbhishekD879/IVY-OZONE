import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


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
class Test_C29148_Maximum_Stake_functionality_when_Overask_is_disabled_for_User(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C29148
    NAME: Maximum Stake functionality when Overask is disabled for User
    DESCRIPTION: This test case verifies Maximum Stake functionality when Overask is disabled for User
    PRECONDITIONS: To enable/disable Overask for the Customer/Event type please follow this path:
    PRECONDITIONS: Backoffice Tool -> Trader Interface -> Customer -> (Search by Username) -> Click on the Account name -> Account Rules -> Select No Intercept value in the Control column  -> click Update
    """
    keep_browser_open = True
    max_bet = 0.02
    bet_amount = 0.03
    expected_max_bet_msg = vec.betslip.MAX_STAKE.format(max_bet)
    selection_ids, selection_ids_2 = None, None
    double_stake_title = vec.betslip.DBL
    draw_stake_title = vec.sb.DRAW.title()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet,
                                                                                 max_mult_bet=self.max_bet)
        self.__class__.selection_ids = event_params.selection_ids

        event_params_2 = self.ob_config.add_UK_racing_event(max_bet=self.max_bet,
                                                            max_mult_bet=self.max_bet,
                                                            number_of_runners=2,
                                                            forecast_available=True)
        self.__class__.eventID, self.__class__.selection_ids_2 = event_params_2.event_id, event_params_2.selection_ids

    def test_001_login_to_oxygen_application_and_add_selection_to_betslip(self):
        """
        DESCRIPTION: Login to Oxygen application and add selection to betslip
        """
        self.site.login(username=tests.settings.disabled_overask_user)
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.draw_stake_title])

    def test_002_enter_stake_value_which_is_higher_then_maximum_allowed_stake_for_this_bet(self):
        """
        DESCRIPTION: Enter Stake value which is higher then maximum allowed Stake for this bet
        """
        self.place_single_bet()

    def test_003_tap_click_on_bet_now_button(self):
        """
        DESCRIPTION: Tap/Click on 'Bet now' button
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
        self.assertTrue(bet_now_button.is_enabled(timeout=1),
                        msg=f'"{bet_now_button.name}" button is disabled')

    def test_004_add_multiple_bets_to_betslip(self):
        """
        DESCRIPTION: Add multiple bets to Betslip
        """
        self.clear_betslip()
        self.open_betslip_with_selections(selection_ids=(list(self.selection_ids_2.values())[0],
                                                         self.selection_ids[self.draw_stake_title]))

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

    def test_006_add_forecasts_tricasts_to_betslip(self):
        """
        DESCRIPTION: Add Forecasts/Tricasts to Betslip
        """
        self.clear_betslip()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', forecast=True)
        self.site.open_betslip()

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: *   Bet is NOT placed
        EXPECTED: *   'Maximum stake of <currency><amount>' error message is displayed above stake section
        EXPECTED: *   Place Bet button is active
        """
        self.place_single_bet(number_of_stakes=1)

        sections = self.get_betslip_sections()
        self.assertTrue(sections, msg='No selections found')

        self.verify_user_balance(expected_user_balance=self.user_balance)

        forecast_tricast_section = sections.Singles
        for stake in list(forecast_tricast_section.values()):
            error_message = stake.wait_for_error_message()
            self.assertEqual(error_message, self.expected_max_bet_msg,
                             msg=f'\nActual message: \n"{error_message}" '
                                 f'\nis not as expected: \n"{self.expected_max_bet_msg}"')

            bet_now_button = self.get_betslip_content().bet_now_button
            self.assertTrue(bet_now_button.is_enabled(timeout=1),
                            msg=f'"{bet_now_button.name}" button is disabled')
