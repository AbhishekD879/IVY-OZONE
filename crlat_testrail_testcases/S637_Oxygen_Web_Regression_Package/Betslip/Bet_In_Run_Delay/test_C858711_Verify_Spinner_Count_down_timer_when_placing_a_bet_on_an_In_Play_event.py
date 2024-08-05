import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C858711_Verify_Spinner_Count_down_timer_when_placing_a_bet_on_an_In_Play_event(Common):
    """
    TR_ID: C858711
    NAME: Verify  Spinner + Count down timer when placing a bet on an In-Play event
    DESCRIPTION: Verify Spinner + Count down timer is displaying on clicking on 'Place bet' button on an In-Play event
    PRECONDITIONS: - 'BIR Delay' should be configured for events in OB
    PRECONDITIONS: - The highest set 'BIR Delay' value (applicable to a <Sport> selection) is used in "confirmationExpectedAt" attribute in "placeBet" response
    PRECONDITIONS: - In-Play events are available in application
    PRECONDITIONS: - Make sure you have a user account with positive balance
    PRECONDITIONS: - User is logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Application is opened
        """
        pass

    def test_002_add_a_selection_to_the_betslip_from_any_in_play_sport_event__open_betslip(self):
        """
        DESCRIPTION: Add a selection to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selection is displayed within Betslip
        """
        pass

    def test_003_enter_any_stake_value_using_keyboard(self):
        """
        DESCRIPTION: Enter any Stake value using keyboard
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        pass

    def test_004_in_ti_add_bir_delay_value_applicable_to_an_added_in_play_sport_selection(self):
        """
        DESCRIPTION: In TI: Add 'BIR Delay' value applicable to an added In-Play <Sport> selection
        EXPECTED: 'BIR Delay' is added
        """
        pass

    def test_005_in_application_tap_login__place_bet_buttoncoral_login__place_betladbrokes_login_and_place_bet(self):
        """
        DESCRIPTION: In application: Tap 'Login & Place Bet' button
        DESCRIPTION: Coral: 'Login & Place Bet'
        DESCRIPTION: Ladbrokes: 'Login and Place bet
        EXPECTED: 'Log In' pop-up is opened
        """
        pass

    def test_006_log_in_with_user_with_positive_balance_that_will_cover_stake_amount_entered_in_step_3_and_no_pop_ups_are_expected_after_login(self):
        """
        DESCRIPTION: Log in with user with positive balance that will cover Stake amount (entered in Step 3) and **NO** pop-ups are expected after login
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value)
        EXPECTED: - Once time is up, the bet is successfully processed
        EXPECTED: Place Bet response:
        EXPECTED: ![](index.php?/attachments/get/122292571)
        EXPECTED: Inplay event:
        EXPECTED: ![](index.php?/attachments/get/122292691)
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_008_add_several_selections_to_the_betslip_from_any_in_play_sport_event__open_betslip(self):
        """
        DESCRIPTION: Add several selections to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selections are displayed within Betslip
        """
        pass

    def test_009_enter_stake_value_for_single_selections_using_keyboard(self):
        """
        DESCRIPTION: Enter Stake value for single selections using keyboard
        EXPECTED: Entered values are displayed in 'Stake' fields
        """
        pass

    def test_010_in_ti_add_different_bir_delay_values_applicable_to_added_in_play_sport_selections(self):
        """
        DESCRIPTION: In TI: Add different 'BIR Delay' values applicable to added In-Play <Sport> selections
        EXPECTED: 'BIR Delay' values are added
        """
        pass

    def test_011_in_application_tap_log_in__bet_buttonfrom_ox99button_namecoral_login__place_betladbrokes_login_and_place_bet(self):
        """
        DESCRIPTION: In application: Tap 'Log In & Bet' button
        DESCRIPTION: **From OX99**
        DESCRIPTION: Button name:
        DESCRIPTION: Coral: 'Login & Place Bet'
        DESCRIPTION: Ladbrokes: 'Login and Place bet
        EXPECTED: 'Log In' pop-up is opened
        """
        pass

    def test_012_log_in_with_user_with_positive_balance_that_will_cover_stake_amount_entered_in_step_9_and_no_pop_ups_are_expected_after_login(self):
        """
        DESCRIPTION: Log in with user with positive balance that will cover Stake amount (entered in Step 9) and **NO** pop-ups are expected after login
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value)
        EXPECTED: - Once time is up, the bet is successfully processed
        """
        pass

    def test_013_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_014_add_several_selections_to_the_betslip_from_any_in_play_sport_event__open_betsliptry_with_multiple_bets(self):
        """
        DESCRIPTION: Add several selections to the Betslip from any In-Play <Sport> event > Open Betslip
        DESCRIPTION: Try with multiple bets
        EXPECTED: Added selections are displayed within Betslip
        """
        pass

    def test_015_enter_stake_value_for_multiple_selections_using_keyboard(self):
        """
        DESCRIPTION: Enter Stake value for multiple selections using keyboard
        EXPECTED: 
        """
        pass

    def test_016_in_ti_add_different_bir_delay_values_applicable_to_added_in_play_sport_selections(self):
        """
        DESCRIPTION: In TI: Add different 'BIR Delay' values applicable to added In-Play <Sport> selections
        EXPECTED: 'BIR Delay' values are added
        """
        pass

    def test_017_in_application_tap_log_in__bet_buttonfrom_ox99button_namecoral_login__place_betladbrokes_login_and_place_bet(self):
        """
        DESCRIPTION: In application: Tap 'Log In & Bet' button
        DESCRIPTION: **From OX99**
        DESCRIPTION: Button name:
        DESCRIPTION: Coral: 'Login & Place Bet'
        DESCRIPTION: Ladbrokes: 'Login and Place bet
        EXPECTED: 'Log In' pop-up is opened
        """
        pass

    def test_018_log_in_with_user_with_positive_balance_that_will_cover_stake_amount_entered_in_step_15_and_no_pop_ups_are_expected_after_login(self):
        """
        DESCRIPTION: Log in with user with positive balance that will cover Stake amount (entered in Step 15) and **NO** pop-ups are expected after login
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value)
        EXPECTED: - Once time is up, the bet is successfully processed
        """
        pass

    def test_019_repeat_all_steps_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat all steps for logged in user
        EXPECTED: Results are the same
        """
        pass
