import pytest
import tests
from datetime import datetime
from datetime import timedelta
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.prod : cannot grant free bets in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.freebets
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C10397813_Verify_Free_Bet_Expiry_message_isnt_shown_on_the_Home_Page_for_Free_Bets_expiring_after_24_hours(Common):
    """
    TR_ID: C10397813
    NAME: Verify Free Bet Expiry message isn't shown on the Home Page for Free Bets expiring after 24 hours
    DESCRIPTION: This test case verifies, that if User has Free Bet expiring after 24 hours, when they logs into the app - Free Bet Expiry message isn't shown.
    DESCRIPTION: Note: Per comment in https://jira.egalacoral.com/browse/BMA-50888, Free Bet Expiry message (dialog window) should NOT be shown on Ladbrokes brand at all on all platforms from OX 102 (vanilla).
    PRECONDITIONS: 1. User has Free Bet expiring after 24 hours available on their account
    """
    keep_browser_open = True

    def test_000_log_in_to_app(self):
        """
        DESCRIPTION: Log in to App.
        EXPECTED: Free Bet Expiry message isn't shown.
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state(state_name='homepage')
        exp_date = datetime.now() + timedelta(hours=48)
        self.ob_config.grant_freebet(username=username, expiration_date=exp_date)
        self.site.login(username=username, async_close_dialogs=True)
        self.assertFalse(self.site.contents.has_free_bets_notification(), msg='The freebet expiry message is displayed')
