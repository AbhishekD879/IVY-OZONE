import pytest
import tests
import re
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from datetime import datetime
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot grant free bets and cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C51702947_Vanilla_Ladbrokes_Verify_FreeBets_displaying_in_my_Account(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C51702947
    NAME: [Vanilla Ladbrokes] Verify FreeBets displaying in my Account.
    DESCRIPTION: This test case verifies that users are able to see what FreeBets they have available.
    """
    keep_browser_open = True
    amount = r'(-?[0-9]+(\.[0-9]+)?)'
    currency = '£'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: - User is logged in with only 1 FreeBet available
        PRECONDITIONS: - Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account (Select Reward Token = 2428)
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.home_team_selection_id = list(self.event.selection_ids.values())[0]
        self.ob_config.grant_freebet(username=self.username, level='selection', id=self.home_team_selection_id)

    def test_001_navigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets(self):
        """
        DESCRIPTION: Navigate to My Account > 'Promotions' > Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        EXPECTED: Sports Free Bets page is displayed
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
            actual_menu_items = list(self.site.right_menu.items_as_ordered_dict)
            self.assertTrue((item in vec.bma.OFFERS_FREE_BETS_MENU_ITEMS for item in actual_menu_items),
                            msg=f'Actual offers & free bets items: "{actual_menu_items}"'
                                f' are not same as Expected offers & free bets items: '
                                f'"{vec.bma.OFFERS_FREE_BETS_MENU_ITEMS}"')
            self.site.right_menu.click_item(vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[1])
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3])

    def test_002_validate_sports_free_bets_page(self):
        """
        DESCRIPTION: Validate Sports Free Bets page
        EXPECTED: - "FREE BET" title (with the back button on the desktop)
        EXPECTED: - Total amount of Free Bets is displayed next to "Free Bet Available" text and total balance of Free Bets (sum of the existing ones) displayed as "Total: 'amount: currency sum'"
        EXPECTED: - List of available free bets.
        EXPECTED: ![](index.php?/attachments/get/73054822)
        """
        self.assertTrue(wait_for_result(lambda: self.site.freebets.header_line, timeout=20),
                        msg='User is not navigated to "Free Bets" page')
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebet_items, msg='No Free Bets found on page')
        date_now = datetime.utcnow()
        for freebet_item_name, freebet_item in list(freebet_items.items())[:10]:
            self.assertTrue(freebet_item_name, msg='Freebet title is not present')
            if freebet_item.has_expires():
                expiration_date = freebet_item.expires
                self.assertIn(' day', expiration_date)
            else:
                expiration_date = freebet_item.used_by
                self.assertTrue(expiration_date, msg=f'Freebet: "{freebet_item_name}" expiration date is not present')
                self.assertTrue(date_now <= expiration_date,
                                msg=f'Freebet: "{freebet_item_name}" offer is expired')
            self.assertTrue(freebet_item.freebet_value,
                            msg=f'Freebet: "{freebet_item_name}" value is not present')

        if self.brand == 'ladbrokes':
            auto_freebet = list(freebet_items.values())[-1]
            match = re.search(self.amount, auto_freebet.name)
            free_bet_value = f'{vec.bma.FREE_BET.upper()}: {self.currency}{match.group()}'
            self.assertEqual(auto_freebet.name, free_bet_value,
                             msg=f'Freebet name "{auto_freebet.name}" is not the same as expected "{free_bet_value}"')
            self.assertTrue(auto_freebet.freebet_text,
                            msg=f'Freebet text "{auto_freebet.freebet_text}" is not displayed')
            self.assertEqual(auto_freebet.freebet_title, free_bet_value,
                             msg=f'Freebet name "{auto_freebet}" is not the same as expected "{free_bet_value}"')
        else:
            free_bet = self.site.freebets.freebets_content.section_header
            auto_freebet = f'{free_bet.total_balance_with_currency} {free_bet.header_title}'
            match = re.search(self.amount, auto_freebet)
            free_bet_value = f'{self.currency}{match.group()} {vec.bma.FREE_BETS.upper()}'
            self.assertTrue(free_bet.has_fb_icon(), msg=f'"Free Bet Icon" is not displayed')
            self.assertTrue(self.site.freebets.header_line.back_button, msg=f'"Back button" is not displayed')
            self.assertEqual(auto_freebet, free_bet_value,
                             msg=f'Freebet name "{auto_freebet}" is not the same as expected "{free_bet_value}"')

    def test_003_check_elements_of_available_free_bet(self):
        """
        DESCRIPTION: Check elements of available free bet
        EXPECTED: - FreeBet amount
        EXPECTED: - Use by date (e.g. DD/MM/YYYY - HH:MM)
        EXPECTED: - Text taken from ‘freebetOfferName’ (e.g. “Acca Insurance”, “Money back”)
        EXPECTED: - Go Betting link
        EXPECTED: - "i" information icon
        """
        # Covered in step 3

    def test_004_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')

    def test_005_login_to_the_account_with_multiple_freebets_available_and_validate__list_using_the_next_steps_1_3(self):
        """
        DESCRIPTION: Login to the account with multiple FreeBets available and validate  list using the next steps (1-3)
        EXPECTED: - All available FreeBets are displayed sorted by expiration date (Use By)
        """
        self.site.login(username=self.username)
        expires_date = []
        self.ob_config.grant_freebet(username=self.username, level='selection', id=self.home_team_selection_id)
        self.ob_config.grant_freebet(username=self.username, level='selection', id=self.home_team_selection_id)
        self.test_001_navigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets()
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebet_items, msg='No Free Bets found on page')
        for freebet_item_name, freebet_item in list(freebet_items.items())[:10]:
            self.assertTrue(freebet_item_name, msg='Freebet title is not present')
            if freebet_item.has_expires():
                expiration_date = freebet_item.used_by
                expires_date = expires_date.append(expiration_date)
        self.assertEqual(expires_date, sorted(expires_date),
                         msg='Free bets are not in expired date order')
