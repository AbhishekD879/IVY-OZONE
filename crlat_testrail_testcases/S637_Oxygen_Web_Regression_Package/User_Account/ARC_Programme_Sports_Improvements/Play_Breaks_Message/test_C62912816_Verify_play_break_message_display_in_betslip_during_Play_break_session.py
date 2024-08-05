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
class Test_C62912816_Verify_play_break_message_display_in_betslip_during_Play_break_session(Common):
    """
    TR_ID: C62912816
    NAME: Verify play break message display in betslip during Play break session
    DESCRIPTION: The test case verifies user gets play break message in betslip during playbreak session
    PRECONDITIONS: User selected play breka time
    PRECONDITIONS: Gambling Controls-> Time Management
    """
    keep_browser_open = True

    def test_001_user_log_into_oxygen_application(self):
        """
        DESCRIPTION: User log into Oxygen Application
        EXPECTED: User logged in successfully and landed on Homepage of the application
        """
        pass

    def test_002_add_one_selection_to_betslip_and_try_to_place_bet(self):
        """
        DESCRIPTION: Add one selection to betslip and try to place bet
        EXPECTED: User gets play break message in betslip
        """
        pass

    def test_003_verify_placebet_and_stake_fields_are_in_disable_state(self):
        """
        DESCRIPTION: Verify PlaceBet and Stake Fields are in disable state
        EXPECTED: PlaceBet and Stake fields shuoul be disabled
        """
        pass
