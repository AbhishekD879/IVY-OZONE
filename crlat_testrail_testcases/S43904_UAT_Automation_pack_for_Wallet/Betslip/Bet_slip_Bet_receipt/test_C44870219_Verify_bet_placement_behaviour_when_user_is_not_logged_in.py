import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870219_Verify_bet_placement_behaviour_when_user_is_not_logged_in(Common):
    """
    TR_ID: C44870219
    NAME: Verify bet placement behaviour when user is not logged in.
    DESCRIPTION: Check  this journey for both Quick bet and bet slip
    PRECONDITIONS: - Quick bet applicable for mobiles only
    """
    keep_browser_open = True

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: User can able to launch the app
        """
        pass

    def test_002_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: User must be displayed Quick bet Pop up
        EXPECTED: -User sees Add to bet slip and Login and place a bet buttons
        """
        pass

    def test_003_enter_stake_and_click_on_login_and_place_a_bet_button(self):
        """
        DESCRIPTION: Enter stake and click on login And place a bet button
        EXPECTED: User should see "Login/register" overlay displayed
        EXPECTED: Close the overlay
        """
        pass

    def test_004_check_the_same_behaviour_for_bet_slip_journey(self):
        """
        DESCRIPTION: Check the same behaviour for bet slip journey
        EXPECTED: 
        """
        pass

    def test_005_add_two_or_three_selections_to_bet_slip(self):
        """
        DESCRIPTION: Add two or three selections to bet slip
        EXPECTED: User sees "Login and place a bet" button on bet slip.
        """
        pass

    def test_006_click_on_login_and_place_a_bet_button(self):
        """
        DESCRIPTION: Click on "Login and place a bet" button
        EXPECTED: User should see "Login/register" overlay displayed
        """
        pass
