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
class Test_C62912817_Verify_user_is_able_to_perform_Cashout_Watch_live_Stream_and_games_during_Play_break_session(Common):
    """
    TR_ID: C62912817
    NAME: Verify user is able to perform Cashout, Watch live Stream and games during Play break session
    DESCRIPTION: The test case verifies user is able to perform Cashout, Watch live Stream and games during Play break session
    PRECONDITIONS: User selected play breka time
    PRECONDITIONS: Gambling Controls-> Time Management
    PRECONDITIONS: --> User placed Cashout Bet before set break time
    """
    keep_browser_open = True

    def test_001_user_log_into_oxygen_application(self):
        """
        DESCRIPTION: User log into Oxygen Application
        EXPECTED: User logged in successfully and landed on Homepage of the application
        """
        pass

    def test_002_go_to_my_bets___verify_user_is_able_to_make_cash_out_from_my_bets_open_bets__cashout_tabs(self):
        """
        DESCRIPTION: Go to My Bets -> Verify user is able to make CASH OUT from My Bets (OPEN BETS / CASHOUT tabs)
        EXPECTED: Cashout should be performed
        """
        pass

    def test_003_verify_user_is_able_to_watch_live_streamings_and_play_free_games(self):
        """
        DESCRIPTION: Verify User is able to watch live Streamings and Play free games
        EXPECTED: User should be able to watch live Streaming & play free games
        """
        pass
