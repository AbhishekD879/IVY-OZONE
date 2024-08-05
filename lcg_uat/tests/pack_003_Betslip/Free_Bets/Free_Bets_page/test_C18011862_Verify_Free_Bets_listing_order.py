import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from datetime import datetime
from datetime import timedelta
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not grant freebet token in prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C18011862_Verify_Free_Bets_listing_order(BaseSportTest, BaseUserAccountTest):
    """
    TR_ID: C18011862
    NAME: Verify Free Bets listing order
    DESCRIPTION: This test case verifies order in which Free Bets are listed
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User has more that 1 Free Bets with different expiration date available on his account
    """
    keep_browser_open = True

    def test_001_open_my_account_ladbrokes__right_menu_coral(self):
        """
        DESCRIPTION: Open My Account (Ladbrokes) / Right menu (Coral)
        EXPECTED: My Account / Right menu displayed
        """
        username = tests.settings.freebet_user
        exp_date = datetime.now() + timedelta(hours=24)
        self.ob_config.grant_freebet(username=username,
                                     expiration_date=exp_date)
        self.site.login(username=username)
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='Right menu is not displayed')

    def test_002_coralclick_on_my_free_bets__bonuses_menu_itemladbrokesclick_on_free_bets_menu_item(self):
        """
        DESCRIPTION: *Coral*
        DESCRIPTION: Click on 'My Free Bets / Bonuses' menu item
        DESCRIPTION: *Ladbrokes*
        DESCRIPTION: Click on 'Free Bets' menu item
        EXPECTED: *Coral*
        EXPECTED: Free Bets page opened
        EXPECTED: *Ladbrokes*
        EXPECTED: Free Bets menu expanded
        """
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_RIGHT_MENU.sports_free_bets)
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_RIGHT_MENU.free_bets)
        page_title = self.site.freebets.header_line.page_title.text
        if self.brand == 'bma':
            self.assertEqual(page_title, vec.bma.FREEBETS.upper(),
                             msg=f'MY FREE BETS/BONUSES "{page_title}" title is not '
                                 f'equal to the "{vec.bma.FREEBETS.upper()}"')
        else:
            self.assertEqual(page_title, vec.bma.FREE_BET.upper(), msg=f'FREE BET "{page_title}" title is not equal '
                                                                       f'to the "{vec.bma.FREE_BET.upper()}"')

    def test_003_verify_order_in_which_available_free_best_are_displayed(self):
        """
        DESCRIPTION: Verify order in which available Free Best are displayed
        EXPECTED: Free bets are listed in expiry date order
        EXPECTED: (if expiry date is the same, higher value bets are prioritized)
        """
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
