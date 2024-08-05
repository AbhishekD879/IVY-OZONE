import datetime

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.deposit
@pytest.mark.quick_bet
@pytest.mark.quick_deposit
@pytest.mark.payments
@pytest.mark.login
@pytest.mark.mobile_only
@vtest
class Test_C23229012_Vanilla__Quick_Bet_Verify_Quick_Deposit_section_for_users_without_payment_methods(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C23229012
    VOL_ID: C49357308
    NAME: [Vanilla] - [Quick Bet] Verify Quick Deposit section for users without credit card
    DESCRIPTION: This test case verifies Quick Deposit section within Quick Bet for users without credit card
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Application is loaded
        DESCRIPTION: 2. Log in under user account with positive balance
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']
            self.__class__.market_name = next(
                (market.get('market').get('name') for market in event['event']['children']
                 if market.get('market').get('templateMarketName') == 'Match Betting'),
                None)
        else:
            event_params = self.ob_config.add_football_event_to_autotest_league2()
            self.__class__.eventID = event_params.event_id
            team1, team2 = event_params.team1, event_params.team2
            self.__class__.event_name = f'{team1} v {team2}'
            self.__class__.market_name = self.ob_config.football_config. \
                autotest_class.autotest_league2.market_name.replace('|', '')
        self.__class__.user_card = tests.settings.visa_card
        self.__class__.cvv = tests.settings.visa_card_cvv

        self._logger.info(f'*** Football event "{self.event_name}" with eventID "{self.eventID}"')

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_log_in_with_user_that_has_0_on_his_balance_and_no_credit_card_added_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has 0 on his balance and no credit card added to his account
        EXPECTED: User is logged in
        """
        self.site.login(username=self.username)

    def test_003_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * Added selection and all data are displayed in Quick Bet
        """
        self.navigate_to_edp(event_id=self.eventID)
        market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=self.market_name)
        self.add_selection_from_event_details_to_quick_bet(market_name=market_name)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
        event_name = self.site.quick_bet_panel.selection.content.event_name
        self.assertEqual(event_name, self.event_name,
                         msg=f'Actual event name "{event_name}" is not the same as expected "{self.event_name}"')

    def test_004_enter_some_value_in_stake_field_manually_or_use_quick_stake__buttons(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field manually or use 'Quick Stake ' buttons
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Make a Deposit' is enabled
        """
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.quick_bet.selection.content.amount_form.input.value = self.bet_amount

        stake = self.quick_bet.selection.content.amount_form.input.value
        self.assertEqual(stake, f'{self.bet_amount:.2f}',
                         msg=f'Actual stake value: "{stake}" '
                         f'is not as expected: "{self.bet_amount:.2f}"')
        self.assertTrue(self.quick_bet.make_quick_deposit_button.is_displayed(),
                        msg=f'Button "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}" is not displayed')

        self.assertTrue(self.quick_bet.make_quick_deposit_button.is_enabled(),
                        msg=f'Button "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}" is not enabled')

        actual_name = self.quick_bet.make_quick_deposit_button.name
        self.assertEqual(actual_name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name "{actual_name}" != Expected "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_005_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'Make a Deposit' button
        EXPECTED: User is redirected to 'Deposit' page
        """
        self.quick_bet.make_quick_deposit_button.click()
        wait_for_result(lambda: self.site.deposit.is_displayed(),
                        name='Deposit page is not loaded',
                        timeout=20)
        self.assertTrue(self.site.select_deposit_method.is_displayed(),
                        msg='User is not redirected to "Deposit" page')
        available_deposit_options = self.site.select_deposit_method.items_as_ordered_dict
        self.assertTrue(available_deposit_options, msg='No deposit options available')

        self.site.select_deposit_method.visa_button.click()
        self.assertTrue(self.site.deposit.is_displayed(),
                        msg='"Deposit page" is not displayed')

    def test_006_add_any_card_as_payment_method_fill_in_all_required_fieldstap_deposit_button(self):
        """
        DESCRIPTION: Add any card as payment method, fill in all required fields
        DESCRIPTION: Tap Deposit button
        EXPECTED: 'Your deposit has been successful' message appears
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        card_date = f'{now.month:02d}/{shifted_year[-2:]}'
        deposit_amount = 20

        self.site.deposit.add_new_card_and_deposit(amount=deposit_amount,
                                                   expiry_date=card_date,
                                                   card_number=self.user_card,
                                                   cvv_2=self.cvv)

        expected = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(deposit_amount)
        actual = self.site.deposit_transaction_details.successful_message
        self.assertEqual(actual, expected,
                         msg=f'Actual message "{actual}" != Expected "{expected}"')

    def test_007_tap_ok_button(self):
        """
        DESCRIPTION: Tap 'OK' button
        EXPECTED: User is redirected to Quick Bet
        EXPECTED: Place Bet button is available and active
        """
        self.site.deposit_transaction_details.ok_button.click()
        if 'beta' in tests.HOSTNAME and (not 'beta' and 'sports.coral.co.uk' or 'sports.ladbrokes.com') in self.device.get_current_url():
            self.navigate_to_page('/')
            '''
            if this TC is running for beta/lower environments, and when close the deposit method page
            it will redirects us to production environment. which is expected.
            So in the above step we are navigating back to the environment this TC was running on.
            '''
            self.site.wait_content_state(state_name="Homepage")
        else:
            self.site.wait_content_state('EventDetails')
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
            self.assertTrue(self.site.quick_bet_panel.place_bet.is_displayed(),
                            msg='Place Bet button is not shown')
            self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                            msg='Place Bet button is not active')
