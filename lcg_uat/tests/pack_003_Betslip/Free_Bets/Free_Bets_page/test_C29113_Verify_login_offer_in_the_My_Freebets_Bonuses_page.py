from datetime import datetime

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
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.login
@pytest.mark.desktop
@vtest
class Test_C29113_Verify_login_offer_in_the_My_Freebets_Bonuses_page(BaseUserAccountTest):
    """
    TR_ID: C29113
    TR_ID: C16706455
    NAME: Verify login offer in the My Freebets/Bonuses page
    """
    keep_browser_open = True

    def test_000_login(self):
        """
        DESCRIPTION: Login as user with freebets available
        EXPECTED: User is logged in as user with freebets available
        """
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)

    def test_001_navigate_to_freebets_page(self):
        """
        DESCRIPTION: My Freebets Page is opened
        EXPECTED: Free bets page is opened
        """
        self.navigate_to_page(name='freebets')

    def test_002_verify_user_balance(self):
        """
        DESCRIPTION: Display customer cash balance
        EXPECTED: Total balance (sum of all freebet amounts+cash balance)
        EXPECTED: Displayed cash balance
        EXPECTED: Total balance is displayed
        """
        if self.brand == 'bma':
            cash_balance = self.site.freebets.balance.cash_balance
            self.assertTrue(cash_balance, msg='User\'s cash balance is not shown')

            self.assertEqual(cash_balance, self.site.header.user_balance,
                             msg=f'User\'s balance "{cash_balance}" shown on Freebets page is not equal to '
                             f'balance shown on balance btn "{self.site.header.user_balance}"')

        total_balance = self.site.freebets.balance.total_balance
        self.assertTrue(total_balance, msg='User\'s total balance is not shown')

    def test_003_verify_each_of_offer(self):
        """
        DESCRIPTION: Freebet description
        EXPECTED: Freebet value in pounds and pence, including 2 decimal places at all times
        EXPECTED: Use by date in format of DD/MM/YYYY
        EXPECTED: Link to the Freebet Details
        EXPECTED: Freebet details is displayed
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

    def test_004_check_accordance_of_amounts(self):
        """
        DESCRIPTION: Verify if sum of all offers equal to sum in header
        EXPECTED: Cash balance and total balance are equal
        """
        expected_freebet_total_sum = 0
        freebets = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebets, msg='No freebets found')
        for freebet_name, freebet in freebets.items():
            expected_freebet_total_sum += freebet.freebet_value
        if self.brand == 'bma':
            actual_total_freebets_sum = self.site.freebets.freebets_content.section_header.total_balance
        else:
            actual_total_freebets_sum = self.site.freebets.balance.total_balance
        expected_freebet_total_sum = round(float(expected_freebet_total_sum), 2)
        self.assertAlmostEqual(expected_freebet_total_sum, actual_total_freebets_sum, delta=0.01,
                               msg=f'Total sum of all offers "{expected_freebet_total_sum}" '
                                   f'is not equal to value in header "{actual_total_freebets_sum}"')
        if self.brand == 'bma':
            cash_balance = self.site.freebets.balance.cash_balance
            total_balance = self.site.freebets.balance.total_balance
            actual = round(float(expected_freebet_total_sum + cash_balance), 2)
            self.assertEqual(actual, total_balance,
                             msg=f'FreeBets amount "{expected_freebet_total_sum}" + cash amount "{cash_balance}" = '
                                 f'"{actual}" '
                                 f'does not equal to total amount "{total_balance}"')
