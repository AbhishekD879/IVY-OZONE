import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # no freebets with value 0.00.  todo: it will work for prod if we have freebets users with value
# @pytest.mark.hl
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C51875588_Vanilla_No_FreeBets_available(Common):
    """
    TR_ID: C51875588
    NAME: [Vanilla] No FreeBets available
    DESCRIPTION: This test case verifies FreeBets menu item behaviour when there are no FreeBets available to the user
    PRECONDITIONS: - User has no FreeBets available
    """
    keep_browser_open = True

    def test_001_login_to_the_account_with_no_freebets_available(self):
        """
        DESCRIPTION: Login to the account with no FreeBets available
        EXPECTED: User is logged in
        """
        self.site.login(tests.settings.freebet_user_with_value_0, timeout_close_dialogs=5)
        self.site.wait_content_state('Homepage', timeout=40)

    def test_002_coralnavigate_to_my_account__offers__free_bets__sports_free_betsladbrokesnavigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets(
            self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Navigate to My Account > 'Offers & Free Bets' > Sports Free Bets
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Navigate to My Account > 'Promotions' > Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        EXPECTED: **Coral:**
        EXPECTED: * "MY FREE BETS/BONUSES" title (with the back button on the desktop)
        EXPECTED: * Total amount of Free Bets is displayed as "'free bets icon'<currency>0.00 Free Bets" text and the total balance of Free Bets displayed as "Total Balance: <currency>0.00"
        EXPECTED: **Ladbrokes:**
        EXPECTED: * "FREE BET" title (with the back button on the desktop)
        EXPECTED: * Total amount of Free Bets is displayed as "Free Bet Available (0)" text and the total balance of Free Bets displayed as "Total: <currency>0.00"
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='Right menu is not displayed')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_RIGHT_MENU.sports_free_bets)
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_RIGHT_MENU.free_bets)

        avatar = self.site.header.user_panel.my_account_button
        self.assertFalse(avatar.has_freebet_icon(), msg='Freebet icon is not present')

        page_title = self.site.freebets.header_line.page_title.text
        if self.brand == 'bma':
            self.assertEqual(page_title, vec.bma.FREEBETS.upper(), msg=f'MY FREE BETS/BONUSES "{page_title}" title is not '
                                                                       f'equal to the "{vec.bma.FREEBETS.upper()}"')
        else:
            self.assertEqual(page_title, vec.bma.FREE_BET.upper(), msg=f'FREE BET "{page_title}" title is not equal '
                                                                       f'to the "{vec.bma.FREE_BET.upper()}"')
        if self.brand == 'bma':
            self.assertTrue(self.site.freebets.header_line.has_back_button, msg='back button is not displayed')
            self.assertTrue(self.site.freebets.freebets_content.section_header.has_fb_icon(), msg='Free Bet icon is not '
                                                                                                  'displayed')
            balance_with_currency = self.site.freebets.freebets_content.section_header.total_balance_with_currency
            self.assertEqual('£0.00', balance_with_currency, msg=f'£0.00 is not equal to "{balance_with_currency}"')
            user_balance = self.site.header.user_balance
            total_freebet_balance = self.site.freebets.balance.total_balance
            total_balance = total_freebet_balance - user_balance
            self.assertEqual(total_balance, 0.0, msg=f'0.0 is not equal to the "{total_balance}"')
        else:
            self.assertTrue(self.site.has_back_button, msg='back button is not displayed')
            no_freebets_msg = self.site.freebets.balance.no_freebets_message
            self.assertEqual(no_freebets_msg, vec.bma.NO_FREE_BETS_FOUND, msg='not equal')
            total_freebet_balance = self.site.freebets.balance.total_balance
            self.assertEqual(0.0, total_freebet_balance, msg=f'0.0 is not equal to the "{total_freebet_balance}"')
