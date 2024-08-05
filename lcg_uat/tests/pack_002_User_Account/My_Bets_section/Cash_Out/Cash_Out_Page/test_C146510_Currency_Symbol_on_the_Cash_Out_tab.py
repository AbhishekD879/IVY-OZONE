import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.user_account
@pytest.mark.currency
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.cash_out
@pytest.mark.low
@pytest.mark.login
@vtest
class Test_C146510_Currency_Symbol_On_The_Cash_Out_Tab(BaseCashOutTest):
    """
    TR_ID: C146510
    NAME: Currency Symbol on the 'Cash Out' tab
    DESCRIPTION: This test case verifies Verify Currency Symbol on the 'Cash Out' tab
    """
    keep_browser_open = True
    bet_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Created football test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
        self.__class__.selection_ids = [event.selection_ids[event.team1], event.selection_ids[event.team2]]
        start_time_local = self.convert_time_to_local(date_time_str=event.event_date_time)
        self.__class__.bet_name = f'SINGLE - [{event.team1} v {event.team2} {start_time_local}]'

    def test_001_login_as_user_with_gbp_currency_and_place_bet(self, username=None):
        """
        DESCRIPTION: Log in user with **GBP** currency
        DESCRIPTION: Place a bet
        """
        username = username if username else tests.settings.betplacement_user

        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_002_navigate_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        """
        self.site.open_my_bets_cashout()

    def test_003_verify_currency_symbol(self, currency='£'):
        """
        DESCRIPTION: Verify currency symbol next to the **Stake** value in bet line details
        DESCRIPTION: Verify currency symbol next to the **Est. Returns** value in bet line details
        DESCRIPTION: Verify currency symbol on the '**CASH OUT**' button
        DESCRIPTION: Tap 'CASH OUT' button and verify currency symbol on the '**CONFIRM**' button
        DESCRIPTION: Tap 'CASH OUT' button and verify currency symbol on the '**SUCCESSFULLY CASHED OUT**' button - cannot verify as it displays ~ 5 sec
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        self.verify_cashout_currency_symbol(currency=currency)

    def test_004_login_as_user_with_eur_currency_and_repeat_steps_1_3(self):
        """
        DESCRIPTION: Log in user with **EUR** currency
        DESCRIPTION: Place a bet
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify currency symbol next to the **Stake** value in bet line details
        DESCRIPTION: Verify currency symbol next to the **Est. Returns** value in bet line details
        DESCRIPTION: Verify currency symbol on the '**CASH OUT**' button
        DESCRIPTION: Tap 'CASH OUT' button and verify currency symbol on the '**CONFIRM**' button
        DESCRIPTION: Tap 'CASH OUT' button and verify currency symbol on the '**SUCCESSFULLY CASHED OUT**' button - cannot verify as it displays ~ 5 sec
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        self.site.logout()
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_login_as_user_with_gbp_currency_and_place_bet(
            username=tests.settings.user_with_euro_currency_and_card)
        self.test_002_navigate_to_my_bets_page()
        self.test_003_verify_currency_symbol(currency='€')

    def test_005_login_as_user_with_usd_currency_and_repeat_steps_1_3(self):
        """
        DESCRIPTION: Log in user with **USD** currency
        DESCRIPTION: Place a bet
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        DESCRIPTION: Verify currency symbol next to the **Stake** value in bet line details
        DESCRIPTION: Verify currency symbol next to the **Est. Returns** value in bet line details
        DESCRIPTION: Verify currency symbol on the '**CASH OUT**' button
        DESCRIPTION: Tap 'CASH OUT' button and verify currency symbol on the '**CONFIRM**' button
        DESCRIPTION: Tap 'CASH OUT' button and verify currency symbol on the '**SUCCESSFULLY CASHED OUT**' button - cannot verify as it displays ~ 5 sec
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        self.site.logout()
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_login_as_user_with_gbp_currency_and_place_bet(
            username=tests.settings.user_with_usd_currency_and_card)
        self.test_002_navigate_to_my_bets_page()
        self.test_003_verify_currency_symbol(currency='$')
