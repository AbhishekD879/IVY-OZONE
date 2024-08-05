import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.user_account
@pytest.mark.freebets
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.desktop
@vtest
class Test_AT_005_Verify_Freebet_Icon(BaseUserAccountTest):
    """
    VOL_ID: C9698289
    NAME: Verify Freebet icon
    """
    keep_browser_open = True

    def test_000_login(self):
        """
        DESCRIPTION: Log in with user that have Freebets
        EXPECTED: Logged in as user with freebets available
        """
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username, async_close_dialogs=False)

    def test_001_verify_freebet_icon(self):
        """
        DESCRIPTION: Verify presence of Freebet Icon for user with freebets available
        EXPECTED: Freebet icon appears
        """
        self.assertTrue(self.site.header.user_panel.my_account_button.has_freebet_icon(),
                        msg='Freebet icon is not displayed')

    def test_002_verify_absence_of_freebet_icon_for_logged_user(self):
        """
        DESCRIPTION: Log out and verify that Freebet icon is not shown
        EXPECTED: Logged out and freebet icon is gone
        """
        self.site.logout()
        self.assertFalse(self.site.header.has_freebets(expected_result=False, timeout=2),
                         msg='Freebet icon is displayed for logged out user')

    def test_003_verify_absence_of_freebet_icon_for_user_without_freebets(self):
        """
        DESCRIPTION: Log in with user that do not have Freebets and verify absence of Freebet icon
        EXPECTED: Freebet icon appears
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, close_all_banners=False, timeout_close_dialogs=1)
        self.site.wait_content_state('Homepage', timeout=30)
        self.assertFalse(self.site.header.has_freebets(expected_result=False, timeout=2), msg='Freebet icon is displayed for user without Freebets')
