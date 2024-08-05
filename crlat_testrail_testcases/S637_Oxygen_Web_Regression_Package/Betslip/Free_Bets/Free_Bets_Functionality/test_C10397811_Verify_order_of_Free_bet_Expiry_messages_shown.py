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
class Test_C10397811_Verify_order_of_Free_bet_Expiry_messages_shown(Common):
    """
    TR_ID: C10397811
    NAME: Verify order of Free bet Expiry messages shown
    DESCRIPTION: This test case verifies, that if User has few Free Bets expiring within 24 hours, when they logs into the app Free Bet Expiry Message with the closest expiry date is shown.
    DESCRIPTION: Note: Per comment in https://jira.egalacoral.com/browse/BMA-50888, Free Bet Expiry message (dialog window) should NOT be shown on Ladbrokes brand at all on all platforms from OX 102 (vanilla).
    PRECONDITIONS: 1. User has few Free Bets expiring within 24 hours available on their account (time of expiry differs for all bets)
    """
    keep_browser_open = True

    def test_001_log_in_to_app(self):
        """
        DESCRIPTION: Log in to App.
        EXPECTED: Free Bet Expiry message is shown for the Free Bet with the closest expiry date (e.g. "You have a free bet which is due to expire in 25 mins")
        EXPECTED: Note: Free Bet expiry message (dialog window) should NOT be shown on Ladbrokes brand on all platforms.
        """
        pass

    def test_002_close_message(self):
        """
        DESCRIPTION: Close message.
        EXPECTED: Message is closed.
        """
        pass

    def test_003_log_out_and_log_in_to_app_again(self):
        """
        DESCRIPTION: Log out and log in to App again.
        EXPECTED: Free Bet Expiry message is shown for the next Free Bet with the closest expiry date (e.g. "You have a free bet which is due to expire in 5 hours")
        EXPECTED: Note: Free Bet expiry message (dialog window) should NOT be shown on Ladbrokes brand on all platforms.
        """
        pass

    def test_004_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3.
        EXPECTED: Free Bet Expiry message is shown for the next Free Bet with the closest expiry date (e.g. "You have a free bet which is due to expire in 12 hours")
        """
        pass

    def test_005_repeat_steps_2_3_until_messages_for_all_free_bets_expiring_within_24_hours_are_shown(self):
        """
        DESCRIPTION: Repeat steps 2-3 until messages for ALL Free Bets expiring within 24 hours are shown.
        EXPECTED: After log in NO messages about Free Bets expiring are shown
        EXPECTED: Note: Free Bet expiry message (dialog window) should NOT be shown on Ladbrokes brand on all platforms.
        """
        pass
