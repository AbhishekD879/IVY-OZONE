import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot grant freebet on PROD/HL
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.freebets
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C14714885_Vanilla_Verify_if_FB_badge_is_shown_on_avatar_in_the_header(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C14714885
    NAME: [Vanilla] Verify if 'FB'-badge is shown on avatar in the header
    DESCRIPTION: This test case verifies that users are able to see on the avatar in the header if there are any FreeBets available
    PRECONDITIONS: - User is logged in with only 1 FreeBet available
    PRECONDITIONS: - Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account (Select Reward Token = 3088)
    PRECONDITIONS: - FreeBets menu item exists if available in CMS (Right Menu) no matter if FreeBets are available to user or not
    """
    keep_browser_open = True
    proxy = None
    freebet_value = 1.03

    def test_000_preconditions(self):
        """
        DESCRIPTION: Pre-conditions
        EXPECTED: User with 1 freebet is available
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.team1 = event_params.team1
        self.__class__.team2 = event_params.team2

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount)

        self.site.login(username=self.username, async_close_dialogs=False)
        avatar = self.site.header.user_panel.my_account_button
        if not avatar.has_freebet_icon():
            self.site.logout()
            self.ob_config.grant_freebet(username=self.username, freebet_value=self.freebet_value)
            self.site.login(username=self.username)

    def test_001_open_main_page_and_verify_the_header(self):
        """
        DESCRIPTION: Open main page and verify the header
        EXPECTED: 'FB'-badge is shown on avatar in the header
        """
        self.__class__.avatar = self.site.header.user_panel.my_account_button
        self.site.wait_content_state('Home Page')
        self.assertTrue(self.avatar.has_freebet_icon(),
                        msg='Freebet icon is not present')

    def test_002_use_free_bet_available_for_the_user_and_verify_the_header(self):
        """
        DESCRIPTION: Use free bet available for the user and verify the header
        EXPECTED: 'FB'-badge is not shown anymore on avatar in the header
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])
        self.place_single_bet(freebet=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

        self.assertFalse(self.avatar.has_freebet_icon(expected_result=False),
                         msg='Freebet icon is present')

    def test_003_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')

    def test_004_login_to_the_account_with_multiple_more_than_two_freebets_available_and_verify_the_header(self):
        """
        DESCRIPTION: Login to the account with multiple (more than two) FreeBets available and verify the header
        EXPECTED: 'FB'-badge is shown on avatar in the header
        """
        for _ in range(3):
            self.ob_config.grant_freebet(username=self.username, freebet_value=self.freebet_value)
        self.site.login(username=self.username)
        avatar = self.site.header.user_panel.my_account_button

        self.assertTrue(avatar.has_freebet_icon(), msg='Freebet icon is not present')

    def test_005_use_one_of_the_free_bet_and_verify_the_header(self):
        """
        DESCRIPTION: Use one of the free bet and verify the header
        EXPECTED: 'FB'-badge is shown on avatar in the header
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team2])
        self.place_single_bet(freebet=True)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

        avatar = self.site.header.user_panel.my_account_button
        self.assertTrue(avatar.has_freebet_icon(), msg='Freebet icon is not present')
