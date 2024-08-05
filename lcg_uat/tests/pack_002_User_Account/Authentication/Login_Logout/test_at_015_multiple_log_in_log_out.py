import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.user_account
@pytest.mark.multisession
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_AT_015_multiple_login_logout(Common):
    """
    NAME: Verify successful multiple login/logout for users with freebets available
    """
    keep_browser_open = True

    def test_001_validate_logged_in_logged_out(self):
        """
        DESCRIPTION: Validate Logged in / Logged out states
        EXPECTED: Users with freebets available are able to login
        """
        for attempt in range(1, 11):
            self._logger.debug(f'*** Attempt to login #{attempt}')
            self.site.login(username=tests.settings.freebet_user, async_close_dialogs=False, timeout_close_dialogs=10)
            self.site.logout()
