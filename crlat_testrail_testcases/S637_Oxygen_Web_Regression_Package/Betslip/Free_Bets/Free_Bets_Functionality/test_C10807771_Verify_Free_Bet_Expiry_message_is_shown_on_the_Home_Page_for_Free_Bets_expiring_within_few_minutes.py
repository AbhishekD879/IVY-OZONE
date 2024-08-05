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
class Test_C10807771_Verify_Free_Bet_Expiry_message_is_shown_on_the_Home_Page_for_Free_Bets_expiring_within_few_minutes(Common):
    """
    TR_ID: C10807771
    NAME: Verify Free Bet Expiry message is shown on the Home Page for Free Bets expiring within few minutes
    DESCRIPTION: This test case verifies, that if User has Free Bet expiring within next few minutes, when they logs into the app - Free Bet Expiry message is shown.
    DESCRIPTION: When User closes message, it isn't shown again (neither in current login session, nor after re-login).
    DESCRIPTION: Note: Per comment in https://jira.egalacoral.com/browse/BMA-50888, Free Bet Expiry message should NOT be shown on Ladbrokes brand at all on all platforms from OX 102 (vanilla).
    PRECONDITIONS: 1. User has Free Bet expiring within next few minutes (1-3 mins) available on their account
    """
    keep_browser_open = True

    def test_001_log_in_to_app(self):
        """
        DESCRIPTION: Log in to App.
        EXPECTED: Free Bet Expiry message is shown:
        EXPECTED: "You have a free bet which is due to expire in X mins"
        EXPECTED: Note: Free Bet expiry message should NOT be shown on Ladbrokes brand on all platforms.
        """
        pass

    def test_002_press_close_button_on_free_bet_expiry_message(self):
        """
        DESCRIPTION: Press close button on Free Bet Expiry message.
        EXPECTED: Free Bet Expiry message is closed.
        """
        pass

    def test_003_log_out_and_log_in_again(self):
        """
        DESCRIPTION: Log out and log in again.
        EXPECTED: Verify, that Free Bet Expiry message isn't shown again.
        """
        pass
