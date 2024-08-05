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
class Test_C62912820_Verify_play_break_message_display_in_quick_bet_during_Play_break_session_after_Login_from_LoginQuickbet_Screen(Common):
    """
    TR_ID: C62912820
    NAME: Verify play break message display in quick bet during Play break session after Login from Login&Quickbet Screen
    DESCRIPTION: The test case verifies user gets play break message in QuickBet during playbreak session after login
    PRECONDITIONS: User selected play breka time
    PRECONDITIONS: Gambling Controls-> Time Management
    """
    keep_browser_open = True

    def test_001_user_access_the_oxygen_application(self):
        """
        DESCRIPTION: User access the Oxygen Application
        EXPECTED: User is navigated to Oxygen homepage
        """
        pass

    def test_002_add_one_selection_to_quickbet_and_tap_on_login_place_bet_to_login_as_play_break_user(self):
        """
        DESCRIPTION: Add one selection to QuickBet and TAP on Login &place bet to login as play break user
        EXPECTED: User gets play break message in QuickBet after login
        """
        pass

    def test_003_verify_placebet_and_stake_fields_are_in_disable_state(self):
        """
        DESCRIPTION: Verify PlaceBet and Stake Fields are in disable state
        EXPECTED: PlaceBet and Stake fields shuoul be disabled
        """
        pass
