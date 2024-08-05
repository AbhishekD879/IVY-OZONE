import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.cash_out
@pytest.mark.currency
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@pytest.mark.timeout(750)
@vtest
class Test_C29219_Verify_Currency_Symbol_on_the_Open_Bets_tab(BaseBetSlipTest):
    """
    TR_ID: C29219
    NAME: Verify Currency Symbol on the 'Open Bets' tab
    DESCRIPTION: This test case verifies  Currency Symbol on the 'My Bets' tab.
    """
    keep_browser_open = True
    bet_amount = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        EXPECTED: Created football test event
        """
        if tests.settings.backend_env == 'prod':
            selections = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self.__class__.selection_ids = list(selections.values())
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
            self.__class__.selection_ids = [event.selection_ids[event.team1], event.selection_ids[event.team2]]

    def test_001_login_and_place_bet(self, username=None):
        """
        DESCRIPTION: Log in user with **GBP** currency
        DESCRIPTION: Place a bet
        """
        username = username if username else tests.settings.betplacement_user

        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet()
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0

    def test_002_navigate_to_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        """
        self.site.open_my_bets_cashout()

    def test_003_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: 'Regular' sort filter is selected by default
        """
        self.site.open_my_bets_open_bets()
        result = wait_for_result(lambda: self.site.open_bets.tab_content.grouping_buttons.current == vec.bma.SPORTS,
                                 name=f'"{vec.bma.SPORTS}" to became active',
                                 timeout=2)
        self.assertTrue(result, msg=f'{vec.bma.SPORTS} sorting type is not selected by default')

    def test_004_verify_currency_symbol_in_bet_details(self, currency='£'):
        """
        DESCRIPTION: Verify currency symbol in Bet Details
        EXPECTED: Currency symbol matches with the currency symbol:
        EXPECTED: - as per user's settings set during registration
        EXPECTED: - next to the user balance
        """
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in list(sections.items())[:1]:
            section.scroll_to()
            self.softAssert(self.assertEqual, section.stake.currency, currency,
                            msg=f'Bet section: "{section_name}" Stake currency: "{section.stake.currency}" not '
                            f'the same as expected: "{currency}"')
            self.softAssert(self.assertEqual, section.est_returns.currency, currency,
                            msg=f'Bet section: "{section_name}" Estimated Returns currency: '
                            f'"{section.est_returns.currency}" not the same as expected: "{currency}"')

    def test_005_tap_on_pools_sort_filter_and_verify_currency_symbol_in_bet_details(self, currency='£'):
        """
        DESCRIPTION: Verify 'Open Bets' tab content when 'Pools' sort filter is selected
        DESCRIPTION: Verify currency symbol in bet details
        EXPECTED: 'Pending' bets are displayed
        EXPECTED: All currency symbols at any time are:
        EXPECTED: - for GBP: symbol = '**£**';
        EXPECTED: - for 'USD': symbol = '**$**';
        EXPECTED: - for 'EUR': symbol = '**€'**'
        """
        result = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        self.assertTrue(result, msg=f'{vec.bet_history.POOLS_TAB_NAME} tab is not opened')

        bets = self.site.open_bets.my_bets_sections_list.items_as_ordered_dict if \
            self.site.open_bets.has_my_bets_sections_list() else {}
        if bets:
            for bet_name, bet in list(bets.items())[0]:
                bet.scroll_to()
                self.assertEqual(bet.bet_status, 'open',
                                 msg=f'"{bet.bet_status}" bet displayed on Open Bets pools sort filter')
                self.assertEqual(bet.unit_stake.currency, currency,
                                 msg=f'Unit stake currency is: "{bet.unit_stake.currency}", expected: "{currency}"')
                self.assertEqual(bet.total_stake.currency, currency,
                                 msg=f'Total stake currency is: "{bet.total_stake.currency}", expected: "{currency}"')

    def test_006_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        self.site.logout()

    def test_007_log_in_user_with_eur_currency_repeat_steps_1_6(self):
        """
        DESCRIPTION: Log in user with **EUR** currency
        EXPECTED: The same as on the steps №1-6
        """
        self.test_001_login_and_place_bet(username=tests.settings.user_with_euro_currency_and_card)
        self.test_002_navigate_to_my_bets_page()
        self.test_003_tap_open_bets_tab()
        self.test_004_verify_currency_symbol_in_bet_details(currency='€')
        self.test_005_tap_on_pools_sort_filter_and_verify_currency_symbol_in_bet_details(currency='€')
        self.test_006_tap_logout_menu_item()

    def test_008_log_in_user_with_usd_currency_repeat_steps_1_6(self):
        """
        DESCRIPTION: Log in user with **USD** currency
        EXPECTED: The same as on the steps №1-6
        """
        self.test_001_login_and_place_bet(username=tests.settings.user_with_usd_currency_and_card)
        self.test_002_navigate_to_my_bets_page()
        self.test_003_tap_open_bets_tab()
        self.test_004_verify_currency_symbol_in_bet_details(currency='$')
        self.test_005_tap_on_pools_sort_filter_and_verify_currency_symbol_in_bet_details(currency='$')
        self.test_006_tap_logout_menu_item()
