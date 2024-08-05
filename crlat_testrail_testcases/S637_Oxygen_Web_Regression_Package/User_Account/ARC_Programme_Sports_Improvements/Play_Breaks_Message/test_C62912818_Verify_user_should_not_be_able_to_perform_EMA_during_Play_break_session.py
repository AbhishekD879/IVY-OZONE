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
class Test_C62912818_Verify_user_should_not_be_able_to_perform_EMA_during_Play_break_session(Common):
    """
    TR_ID: C62912818
    NAME: Verify user should not be able to perform EMA during Play break session
    DESCRIPTION: The test case verifies user is able to perform EMA during Play break session
    PRECONDITIONS: User selected play breka time
    PRECONDITIONS: Gambling Controls-> Time Management
    PRECONDITIONS: --> User placed mutilple Bet before set break time
    """
    keep_browser_open = True

    def test_001_user_log_into_oxygen_application(self):
        """
        DESCRIPTION: User log into Oxygen Application
        EXPECTED: User logged in successfully and landed on Homepage of the application
        """
        pass

    def test_002_go_to_my_bets___verify_user_is_able_to_edit_ema_from_my_bets_open_bet_tab(self):
        """
        DESCRIPTION: Go to My Bets -> Verify user is able to edit EMA from My Bets (OPEN BET TAB)
        EXPECTED: EMA button should be deactivated
        """
        pass
