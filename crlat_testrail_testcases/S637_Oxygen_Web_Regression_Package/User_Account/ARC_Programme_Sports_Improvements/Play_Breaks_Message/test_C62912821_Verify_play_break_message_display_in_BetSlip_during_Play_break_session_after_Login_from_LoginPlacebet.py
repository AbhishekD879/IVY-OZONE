import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C62912821_Verify_play_break_message_display_in_BetSlip_during_Play_break_session_after_Login_from_LoginPlacebet(Common):
    """
    TR_ID: C62912821
    NAME: Verify play break message display in BetSlip during Play break session after Login from Login&Placebet
    DESCRIPTION: The test case verifies user gets play break message in BetSlip during playbreak session after login
    PRECONDITIONS: User selected play breka time
    PRECONDITIONS: Gambling Controls-&gt; Time Management
    PRECONDITIONS: User is on Play break Session[Triggered PB session for the user]
    """
    keep_browser_open = True

    def test_001_user_access_the_oxygen_application(self):
        """
        DESCRIPTION: User access the Oxygen Application
        EXPECTED: User is navigated to Oxygen homepage
        """
        pass

    def test_002_add_one_selection_to_betslip_and_tap_on_login_place_bet_to_login_as_play_break_user(self):
        """
        DESCRIPTION: Add one selection to BetSlip and TAP on Login &place bet to login as play break user
        EXPECTED: User gets play break message in BetSlip After login
        """
        pass

    def test_003_verify_placebet_and_stake_fields_are_in_disable_state(self):
        """
        DESCRIPTION: Verify PlaceBet and Stake Fields are in disable state
        EXPECTED: Place Bet and Stake fields should be disabled
        """
        pass

    def test_004_parallelly_open_native_app_and_login_with_same_user_and_check_user_is_on_play_break_session_in_native_app_too(self):
        """
        DESCRIPTION: Parallelly, Open native app and login with same user and check user is on play break session in native app too
        EXPECTED: User should be on Play break session
        EXPECTED: Stake and place bet option should be in disabled state
        """
        pass

    def test_005_wait_till_pb_session_over_and_enter_stake_and_place_bet(self):
        """
        DESCRIPTION: Wait till PB session over and enter stake and place bet
        EXPECTED: User should be able to place bet after PB session over
        """
        pass
