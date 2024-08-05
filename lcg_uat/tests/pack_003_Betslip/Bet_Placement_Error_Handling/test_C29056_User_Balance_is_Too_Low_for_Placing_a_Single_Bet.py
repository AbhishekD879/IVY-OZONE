import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C29056_User_Balance_is_Too_Low_for_Placing_a_Single_Bet(BaseBetSlipTest):
    """
    TR_ID: C29056
    NAME: User Balance is Too Low for Placing a Single Bet
    DESCRIPTION: This test case verifies bet slip error handling in case when user balance is too low.
    DESCRIPTION: Autotest Mobile: [C16074331]
    DESCRIPTION: Autotest Desktop: [C16268913]
    PRECONDITIONS: 1.  Application is loaded
    PRECONDITIONS: 2.  User is logged in
    PRECONDITIONS: 3.  The user account is NOT sufficient to cover any stake
    PRECONDITIONS: 4.  User doesn't have added debit/credit cards
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> sport it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event landing page
    PRECONDITIONS: NOTE: in order to check Max Allowed Bet enter extremely large stake value in 'Stake' field and tap 'Bet Now' button to see what is Max allowed bet for selection.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find a few selections to the Bet Slip
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_id = (event_params.selection_ids[event_params.team1])
        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        number_of_events=1)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(selection_ids.values())[0]
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.wait_content_state("Home")
        balance = self.site.header.user_balance
        self.assertEqual(balance, 0.00,
                         msg=f'{balance} not equal to {0.00}')

    def test_001_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_enter_a_stake_which_will_exceed_users_balance_but_wont_exceed_a_max_bet_allowed(self):
        """
        DESCRIPTION: Enter a stake which will exceed user's balance but won't exceed a max bet allowed
        EXPECTED: 'Bet Now' (from OX 99 'Place Bet') button is enabled
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake.name, stake))
        deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(deposit_button.is_enabled(), msg=f'"{deposit_button.name}" button is not enabled')
        self.assertEqual(deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'\nActual button name: "{deposit_button.name}"'
                             f'\nis not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_003_tap_bet_now_from_ox_99_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' (from OX 99 'Place Bet') button
        EXPECTED: User is navigated to 'Deposit' page
        EXPECTED: * User is navigated to 'Add Credit Card' tab for **Coral** brand
        EXPECTED: * User is navigated to 'Account One' system for **Ladbrokes** brand
        EXPECTED: * Betslip is closed
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        wait_for_result(lambda: self.site.deposit.is_displayed(),
                        name='User is not navigated to the deposit page',
                        timeout=20)
        self.assertTrue(self.site.select_deposit_method.is_displayed(), msg='User is not navigated to the deposit page')
        if self.brand == 'ladbrokes' and tests.settings.backend_env == 'tst2':
            self.assertTrue(self.site.select_deposit_method.debit_card_button.is_displayed(),
                            msg='"Master Card" button is not displayed"')
        else:
            self.assertTrue(self.site.select_deposit_method.master_card_button.is_displayed(),
                            msg='"Master Card" button is not displayed"')
            self.assertTrue(self.site.select_deposit_method.visa_button.is_displayed(),
                            msg='"Visa Card" button is not displayed')
            self.assertTrue(self.site.select_deposit_method.maestro_button.is_displayed(),
                            msg='"Maestro Card" button is not displayed')
