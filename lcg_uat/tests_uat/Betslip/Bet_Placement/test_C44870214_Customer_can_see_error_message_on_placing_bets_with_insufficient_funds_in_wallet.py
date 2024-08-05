import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import switch_to_main_page
import datetime


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870214_Customer_can_see_error_message_on_placing_bets_with_insufficient_funds_in_wallet(BaseBetSlipTest):
    """
    TR_ID: C44870214
    NAME: Customer can see error message on placing bets with insufficient funds in wallet
    DESCRIPTION: This test case verify insufficient balance
    """
    keep_browser_open = True
    deposit_amount = 5.00
    additional_amount = 5.0
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: HomePage opened
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            market = next((market for market in event['event']['children']
                           if 'Match Betting' in market['market']['templateMarketName']), None)
            if not market:
                raise SiteServeException('No "Match Betting" market has been found')
            outcomes = market['market'].get('children')
            if not outcomes:
                raise SiteServeException('No outcomes has been found')

            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('"Home" has not been found in outcomes')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids
        self._logger.info(f'*** Football event with selection ids "{self.selection_ids}" and team "{self.team1}"')

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: user logged in
        """
        user = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=user,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        self.site.login(user)

    def test_003_go_to_any_sport_and_add_selection_to_bqbetslip(self):
        """
        DESCRIPTION: Go to any sport and add selection to bQ/Betslip
        EXPECTED: Selection added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_004_verify__message_display_when_user_enter_stake_more_than_the_account_balance_to(self):
        """
        DESCRIPTION: Verify  message display when user Enter stake more than the account balance to
        EXPECTED: 'Please deposit a min £XX.XX to continue placing your bet' message displayed in betslip.
        """
        user_balance = self.site.header.user_balance
        stake_value = user_balance + self.additional_amount
        section = self.get_betslip_sections().Singles
        self.assertTrue(section, msg='"sections" not displayed')
        stake_name, self.__class__.stake = list(section.items())[0]
        self.stake.amount_form.input.value = stake_value
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        actual_message = self.get_betslip_content().bet_amount_warning_message
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message: "{actual_message}" does not match expected: "{expected_message}"')
        self.__class__.make_deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(self.make_deposit_button.is_enabled(),
                        msg=f'"{self.make_deposit_button.name}" button is not enabled')
        self.assertEqual(self.make_deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{self.make_deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_005_verify_qd_pop_opens_when_user_click_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Verify QD pop opens when user click on Make a deposit button
        EXPECTED: QD pop displayed
        EXPECTED: -Visa card - registered
        EXPECTED: -Deposit Amount
        EXPECTED: -CVV
        EXPECTED: -Total stake
        EXPECTED: Potential Returns
        """
        self.make_deposit_button.click()
        self.assertTrue(self.get_betslip_content().has_deposit_form(),
                        msg='"Quick Deposit" section is not displayed')
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        deposit_amount = self.quick_deposit.amount.input.value
        self.assertTrue(deposit_amount, msg=f'"{deposit_amount}" is not displayed')
        self.assertTrue(self.quick_deposit.cvv_2, msg='"CVV" is not displayed')
        total_stake = self.quick_deposit.total_stake_value
        self.assertTrue(total_stake, msg='"Total stake" is not present!')
        potential_returns = self.quick_deposit.potential_returns_value
        self.assertTrue(potential_returns, msg='"Potential return" is not present!')

    def test_006_verify_acceptdeposit__place_bet_button_gets_enabled_once_user_enter_the_amount_and_cvv(self):
        """
        DESCRIPTION: Verify Accept(DEPOSIT & PLACE BET) button gets enabled once user enter the amount and CVV
        EXPECTED: Accept(DEPOSIT & PLACE BET) button is  enabled
        """
        if self.device_type == 'mobile':
            self.quick_deposit.cvv_2.click()
            keyboard = self.quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='"Numeric keyboard" shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value=tests.settings.visa_card_cvv)
            keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = tests.settings.visa_card_cvv

        deposit_button = self.quick_deposit.deposit_and_place_bet_button
        self.assertTrue(deposit_button.is_enabled(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        deposit_button.click()
        switch_to_main_page()

    def test_007_verify_bet_is_placed_when_user_tapsclick_on_acceptdeposit__place_bet_button(self):
        """
        DESCRIPTION: Verify bet is placed when user taps/click on Accept(DEPOSIT & PLACE BET) button
        EXPECTED: Bet placed successfully
        """
        self.check_bet_receipt_is_displayed()
