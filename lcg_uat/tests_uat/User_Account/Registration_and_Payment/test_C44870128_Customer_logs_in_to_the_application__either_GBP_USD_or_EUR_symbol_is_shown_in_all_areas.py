import pytest
import tests
import voltron.environments.constants as vec
import datetime

from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from random import choice


@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.right_hand_menu
@pytest.mark.currency
@pytest.mark.my_bets
@pytest.mark.desktop
@pytest.mark.uat
@vtest
class Test_C44870128_Customer_logs_in_to_the_application__either_GBP_USD_or_EUR_symbol_is_shown_in_all_areas(BaseBetSlipTest):
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

    def create_user_with_different_currency(self, currencycode):
        deposit_amount = 20.00
        now = datetime.datetime.now()
        expiry_year = str(now.year)
        expiry_month = f'{now.month:02d}'
        username = self.gvc_wallet_user_client.register_new_user(currencycode=currencycode).username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount=str(deposit_amount),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard', expiry_month=expiry_month,
                                                                     expiry_year=expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        return username

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP **currency
        EXPECTED: User is logged in successfully
        """
        self.site.login()

    def test_002_verify_currency_symbol_next_to_the_user_balance(self, currency='£', expected_betslip_counter_value=0):
        """
        DESCRIPTION: Verify currency symbol next to the user balance
        DESCRIPTION: Verify Currency on the My Balance page
        DESCRIPTION: Verify Currency on the Global Header for Desktop
        DESCRIPTION: Verify Currency Symbol on the Open Bets,Settled Bets and Cashout tab(for a user who has placed some bets)
        NOTE: Not able to settled bets on prod
        EXPECTED: Currency symbol matches  as per user's settings set during registration
        """
        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        user_balance = self.site.header.user_balance_section.name
        self.assertIn(currency, user_balance,
                      msg=f'"{currency}" symbol is not present on user balance "{user_balance}"')
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     all_available_events=True,
                                                     additional_filters=cashout_filter,
                                                     in_play_event=False)
        event1 = choice(events)
        match_result_market = next((market['market'] for market in event1['event']['children'] if
                                    market.get('market').get('templateMarketName') == 'Match Betting'), None)
        outcomes = match_result_market['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        selection_id = list(all_selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

        self.site.open_my_bets_cashout()
        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                       number_of_bets=1)
        cashout_amount = str(bet.buttons_panel.full_cashout_button.amount)
        self.assertIn(currency, cashout_amount, msg=f'"{currency}" symbol is not present on "{vec.bet_history.CASH_OUT_TAB_NAME}"')

        self.site.open_my_bets_open_bets()
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                         number_of_bets=1)
        stake_value = bet.stake.value
        self.assertIn(currency, stake_value, msg=f'"{currency}" symbol is not present on "{vec.bet_history.OPEN_BETS_TAB_NAME}"')

        self.site.open_my_bets_settled_bets()
        settled_bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        if len(settled_bets) is 0:
            actual_message = self.site.bet_history.tab_content.accordions_list.no_bets_message
            self.assertEqual(actual_message, vec.bet_history.NO_HISTORY_INFO,
                             msg=f'Actual "{actual_message}" is not the same as expected "{vec.bet_history.NO_HISTORY_INFO}"')

        self.site.header.right_menu_button.avatar_icon.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        my_balance = self.site.right_menu.balance_amount
        self.assertIn(currency, my_balance, msg=f'"{currency}" symbol is not present in "{my_balance}"')
        self.site.right_menu.logout()

    def test_003_log_in_with_user_that_has_usd_currency_and_repeat_step_2(self):
        """
        DESCRIPTION: Log in with user that has 'USD' currency and repeat step #2
        """
        if self.brand == 'bma':
            username = tests.settings.user_with_usd_currency_and_card
        else:
            username = self.create_user_with_different_currency("USD")
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        self.site.login(username=username)
        self.test_002_verify_currency_symbol_next_to_the_user_balance(currency='$')

    def test_004_log_in_with_user_that_has_eur_currency_and_repeat_step_2(self):
        """
        DESCRIPTION: Log in with user that has 'EUR' currency and repeat step #2
        """
        if self.brand == 'bma':
            username = tests.settings.user_with_euro_currency_and_card
        else:
            username = self.create_user_with_different_currency("EUR")
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')
        self.site.login(username=username)
        self.test_002_verify_currency_symbol_next_to_the_user_balance(currency='€')
