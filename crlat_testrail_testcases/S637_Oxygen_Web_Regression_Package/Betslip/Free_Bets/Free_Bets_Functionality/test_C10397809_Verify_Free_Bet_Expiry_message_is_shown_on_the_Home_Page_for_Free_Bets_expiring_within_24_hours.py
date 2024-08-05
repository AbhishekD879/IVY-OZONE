import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C10397809_Verify_Free_Bet_Expiry_message_is_shown_on_the_Home_Page_for_Free_Bets_expiring_within_24_hours(Common):
    """
    TR_ID: C10397809
    NAME: Verify Free Bet Expiry message is shown on the Home Page for Free Bets expiring within 24 hours
    DESCRIPTION: This test case verifies, that if User has Free Bet expiring within 24 hours, when they logs into the app - Free Bet Expiry message is shown.
    DESCRIPTION: Note: Per comment in https://jira.egalacoral.com/browse/BMA-50888, Free Bet Expiry message should NOT be shown on Ladbrokes brand at all on all platforms from OX 102 (vanilla).
    PRECONDITIONS: 1. User has Free Bet expiring within 24 hours available on their account
    """
    keep_browser_open = True

    def test_001_log_in_to_app(self):
        """
        DESCRIPTION: Log in to App.
        EXPECTED: Free Bet Expiry message is shown:
        EXPECTED: "You have a free bet which is due to expire in X hours/X mins"
        EXPECTED: (X mins when it's due to expire within an hour).
        EXPECTED: Note: Calculation of X = Free Bet Expiry Time - Current Time, rounded to the nearest hour.
        EXPECTED: i.e. When remaining time is 10 Hours 31 mins, X = 11 hrs.
        EXPECTED: When remaining time is 10 hrs 29 mins, X = 10 hrs.
        EXPECTED: When remaining time is 40 mins, X = 40 mins.
        EXPECTED: Note 2: Free Bet expiry message should not be shown on Ladbrokes brand on all platforms.
        """
        pass

    def test_002_press_close_button_on_free_bet_expiry_message(self):
        """
        DESCRIPTION: Press close button on Free Bet Expiry message.
        EXPECTED: Free Bet Expiry message is closed.
        """
        pass
