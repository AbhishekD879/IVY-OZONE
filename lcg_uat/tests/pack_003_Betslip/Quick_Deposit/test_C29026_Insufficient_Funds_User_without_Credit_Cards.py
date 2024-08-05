import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29026_Insufficient_Funds_User_without_Credit_Cards(BaseSportTest, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C29026
    NAME: Insufficient Funds User without Credit Cards
    DESCRIPTION: This test case verifies the absence of Quick Deposit section and presence of Insufficient Funds Error message for the User with no registered Credit Cards

    """
    keep_browser_open = True
    addition = 5

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User account with **0 balance and NO registered Credit Cards** (additional pop-up Quick Deposit)
        PRECONDITIONS: 2. User account with **positive balance but NO registered Credit Cards**
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children']
                             if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name, self.__class__.selection_id = list(self.selection_ids.items())[1]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_name, self.__class__.selection_id = list(event.selection_ids.items())[0]

    def test_001_log_in_with_user_account_from_preconditions___1(self):
        """
        DESCRIPTION: Log in with user account (from preconditions - #1)
        EXPECTED: - User is logged in
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_002_add_any_selection_to_the_bet_slip_and_open_the_bet_slippagewidget(self):
        """
        DESCRIPTION: Add any selection to the Bet Slip and open the Bet Slip page/widget
        EXPECTED: - Made selection is displayed correctly within Bet Slip content area
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertTrue(self.singles_section.items(), msg='No stakes found')
        self.assertIn(self.selection_name, self.singles_section.keys(),
                      msg=f'Actual list "{self.singles_section.items()}" does not contain Added selection "{self.selection_name}"')

    def test_003_enter_stake___anyand_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter 'Stake' :
        DESCRIPTION: - any
        DESCRIPTION: and tap 'PLACE BET' button
        EXPECTED: - 'QUICK DEPOSIT' section is not displayed
        EXPECTED: - Betslip is closed
        EXPECTED: - User is navigated to 'Deposit' page, 'Add Credit/Debit Cards' tab for **Coral** brand
        EXPECTED: * User is navigated to Account One system for **Ladbrokes** brand
        """
        self.__class__.stake_name, stake = list(self.singles_section.items())[0]
        self.enter_stake_amount(stake=(self.stake_name, stake))
        self.get_betslip_content().make_quick_deposit_button.click()
        self.site.wait_content_state_changed(timeout=60)
        select_deposit_method = self.site.select_deposit_method
        available_deposit_options = select_deposit_method.items_as_ordered_dict
        self.assertTrue(available_deposit_options, msg='No deposit options available')

    def test_004_log_out_of_the_app_and_log_in_with_user_account_from_preconditions___2(self):
        """
        DESCRIPTION: Log out of the app and Log in with user account (from preconditions - #2)
        """
        self.navigate_to_page('Homepage')
        self.site.logout()
        self.site.login(username=tests.settings.user_positive_balance_without_card)

    def test_005_clear_betslip_and_then_add_any_selection_to_the_bet_slip_and_open_the_bet_slippagewidget(self):
        """
        DESCRIPTION: Clear Betslip and then add any selection to the Bet Slip and open the Bet Slip page/widget
        EXPECTED: - Made selection is displayed correctly within Bet Slip content area
        """
        self.__class__.user_balance = self.site.header.user_balance
        counter_value = int(self.site.header.bet_slip_counter.counter_value)
        if counter_value > 0:
            self.site.header.bet_slip_counter.click()
            self.clear_betslip()
            self.device.go_back()
        self.test_002_add_any_selection_to_the_bet_slip_and_open_the_bet_slippagewidget()

    def test_006_enter_stake___greater_than_user_balanceand_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter 'Stake' :
        DESCRIPTION: - greater than user balance
        DESCRIPTION: and tap 'PLACE BET' button
        EXPECTED: Expected Result should match ER from step 3
        """
        self.__class__.bet_amount = self.user_balance + self.addition
        self.test_003_enter_stake___anyand_tap_place_bet_button()
