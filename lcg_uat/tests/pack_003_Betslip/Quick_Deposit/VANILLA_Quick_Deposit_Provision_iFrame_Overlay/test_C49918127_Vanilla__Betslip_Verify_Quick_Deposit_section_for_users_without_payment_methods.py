import datetime
import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C49918127_Vanilla__Betslip_Verify_Quick_Deposit_section_for_users_without_payment_methods(BaseSportTest, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C49918127
    NAME: [Vanilla] - [Betslip] Verify Quick Deposit section for users without payment methods
    DESCRIPTION: This test case verifies Quick Deposit section within Betslip for users without payment methods
    """
    keep_browser_open = True
    bet_amount = 5
    deposit_amount = 5
    now = datetime.datetime.now()
    shifted_year = str(now.year + 5)
    card_date = f'{now.month:02d}/{shifted_year[-2:]}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User account with **0 balance without payment methods
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            market_name, outcomes = next(
                ((market['market']['name'], market['market']['children']) for market in event['event']['children']
                 if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name, self.__class__.selection_id = list(selection_ids.items())[1]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event.event_id
            self.__class__.selection_name, self.__class__.selection_id = list(event.selection_ids.items())[1]

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_log_in_with_user_that_has_0_on_his_balance_and_no_payment_methods_added_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has 0 on his balance and no payment methods added to his account
        EXPECTED: User is logged in
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_003_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        if self.device_type == 'mobile':
            if self.site.betslip.has_bet_now_button():
                self.site.close_betslip()
                self.site.wait_content_state_changed(10)
                self.site.open_betslip()

    def test_004_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: * Betslip is opened with added selection
        EXPECTED: * 'Make a Deposit' button is displayed and disabled
        """
        self.__class__.make_deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(self.make_deposit_button.is_displayed(),
                        msg=f'"{self.make_deposit_button.name}" button is not displayed')
        self.assertFalse(self.make_deposit_button.is_enabled(expected_result=False),
                         msg=f'"{self.make_deposit_button.name}" button is enabled')

    def test_005_enter_some_value_in_stake_field(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Make a Deposit' button becomes enabled
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        self.assertIn(self.selection_name, singles_section.keys(),
                      msg=f'Actual list "{singles_section.items()}" does not contain Added selection "{self.selection_name}"')
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.assertTrue(self.make_deposit_button.is_enabled(),
                        msg=f'"{self.make_deposit_button.name}" button is not enabled')

    def test_006_clicktap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Click/tap on 'Make a Deposit' button
        EXPECTED: Deposit page is opened
        """
        self.make_deposit_button.click()
        self.site.wait_content_state_changed(timeout=60)
        select_deposit_method = wait_for_result(lambda: self.site.select_deposit_method, timeout=20,
                        name='deposit method not displayed displayed.')
        self.assertTrue(select_deposit_method,msg="select_deposit_method not displayed")
        available_deposit_options = select_deposit_method.items_as_ordered_dict
        self.assertTrue(available_deposit_options, msg='No deposit options available')

    def test_007_add_any_card_as_payment_method_fill_in_all_required_fieldstap_deposit_button(self):
        """
        DESCRIPTION: Add any card as payment method, fill in all required fields.
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: 'Your deposit has been successful' message appears
        """
        self.site.select_deposit_method.master_card_button.click()
        self.site.deposit.card_number.input.send_keys(keys=tests.settings.quick_deposit_card)
        self.site.deposit.expiry_date.input.send_keys(keys=self.card_date)
        if self.device_type == 'mobile':
            self.site.deposit.next_button.click()
        self.site.deposit.amount.input.value = self.deposit_amount
        self.site.deposit.cvv_2.input.send_keys(keys=tests.settings.visa_card_cvv)
        self.site.deposit.deposit_button.click()
        expected = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.deposit_amount)
        actual = self.site.deposit_transaction_details.successful_message
        self.assertEqual(actual, expected,
                         msg=f'Actual message "{actual}" != Expected "{expected}"')
        ok_button = self.site.deposit_transaction_details.ok_button.is_displayed()
        self.assertTrue(ok_button, msg='"OK" button is not present')

    def test_008_tap_ok_buttonopen_betslip(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Open Betslip
        EXPECTED: 'Place Bet' button is available and active
        """
        self.site.deposit_transaction_details.ok_button.click()
        self.navigate_to_page(name='?automationtest=true&q=1')
        self.site.open_betslip()
        self.assertTrue(self.site.betslip.has_bet_now_button(), msg='Place Bet button is not present.')
        place_bet_button = self.site.betslip.bet_now_button
        self.assertTrue(place_bet_button.is_displayed(), msg='Place Bet button is not displayed.')
        self.assertTrue(place_bet_button.is_enabled(), msg='Place Bet button is not enabled.')
        place_bet_button.click()
