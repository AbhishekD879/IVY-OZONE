import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C44870128_Customer_logs_in_to_the_application__either_GBP_USD_or_EUR_symbol_is_shown_in_all_areas(Common):
    """
    TR_ID: C44870128
    NAME: Customer logs in to the application - either GBP, USD, or EUR  symbol is shown in all areas
    DESCRIPTION: Customer logs in to the application - either GBP, USD, EUR or SEK symbol is shown in all areas, based on the Currency selected in Registration (Supported currencies: GBP, USD, EUR, SEK)
    PRECONDITIONS: Make sure you have 4 registered users with different currency settings: GBP, EUR, USD, SEK
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: 'GBP': symbol = '**£**';
    PRECONDITIONS: 'USD': symbol = '**$**';
    PRECONDITIONS: 'EUR': symbol = '**€'**;
    """
    keep_browser_open = True

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_verify_currency_symbol_next_to_the_user_balanceverify_currency_on_the_my_balance_pageverify_currency_on_the_global_header_for_desktopverify_currency_symbol_on_the_open_betssettled_bets_and_cashout_tab_for_a_user_who_has_placed_some_bets(self):
        """
        DESCRIPTION: Verify currency symbol next to the user balance
        DESCRIPTION: Verify Currency on the My Balance page
        DESCRIPTION: Verify Currency on the Global Header for Desktop
        DESCRIPTION: Verify Currency Symbol on the Open Bets,Settled Bets and Cashout tab (for a user who has placed some bets)
        EXPECTED: Currency symbol matches  as per user's settings set during registration
        """
        pass

    def test_003_log_in_with_user_that_has_usd_currency_and_repeat_step_2(self):
        """
        DESCRIPTION: Log in with user that has 'USD' currency and repeat step #2
        EXPECTED: 
        """
        pass

    def test_004_log_in_with_user_that_has_eur_currency_and_repeat_step_2(self):
        """
        DESCRIPTION: Log in with user that has 'EUR' currency and repeat step #2
        EXPECTED: 
        """
        pass
