import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.user_account
@pytest.mark.freebets
@pytest.mark.static_block
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9771136_No_FreeBets_available(BaseUserAccountTest):
    """
    TR_ID: C9771136
    NAME: No FreeBets available
    DESCRIPTION: This test case verifies FreeBets menu item behaviour when there are no FreeBets available to the user
    PRECONDITIONS: - User has no FreeBets available
    PRECONDITIONS: - FreeBets menu item exists if available in CMS (Right Menu) no matter if FreeBets are available to user or not
    """
    keep_browser_open = True
    is_enabled = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if not cls.is_enabled and tests.settings.cms_env != 'prd0':
            cms = cls.get_cms_config()
            cms.enable_static_block(uri=cms.constants.NO_FREEBET_STATIC_BLOCK_URI, enable=False)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify CMS settings and set cookies
        """
        self.__class__.is_enabled = self.cms_config.is_static_block_enabled(uri=self.cms_config.constants.NO_FREEBET_STATIC_BLOCK_URI)
        if not self.is_enabled:
            if tests.settings.cms_env != 'prd0':
                self.cms_config.enable_static_block(uri=self.cms_config.constants.NO_FREEBET_STATIC_BLOCK_URI)
            else:
                raise CmsClientException(f'Static block with uri "{self.cms_config.constants.NO_FREEBET_STATIC_BLOCK_URI}" is disabled, '
                                         f'cannot execute the test on prod endpoints')

    def test_001_login_to_the_account_with_no_freebets_available(self):
        """
        DESCRIPTION: Login to the account with no FreeBets available
        EXPECTED: User is logged in
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, close_all_banners=False, timeout_close_dialogs=1)
        self.site.wait_content_state('Homepage', timeout=30)

    def test_002_navigate_to_freebets_bonuses(self):
        """
        DESCRIPTION: Navigate to My Freebets/Bonuses
        EXPECTED: 'No Freebets available' message appears
        """
        self.navigate_to_page(name='freebets')
        self.site.wait_content_state('Freebets')
        wait_for_result(lambda: self.site.freebets.freebets_content.no_freebets_message != '',
                        name='no free bets message to be displayed',
                        timeout=5)
        actual_message = self.site.freebets.freebets_content.no_freebets_message
        self.assertEqual(actual_message, vec.bma.NO_FREE_BETS_FOUND,
                         msg=f'Actual message: "{actual_message}" does not match expected: '
                             f'"{vec.bma.NO_FREE_BETS_FOUND}"')
