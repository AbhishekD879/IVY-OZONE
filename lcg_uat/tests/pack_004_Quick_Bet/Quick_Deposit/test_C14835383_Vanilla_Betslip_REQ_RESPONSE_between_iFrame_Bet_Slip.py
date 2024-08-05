import pytest
import tests
import datetime
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import switch_to_main_page, hide_number


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.quick_deposit
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1730')
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1783')
@pytest.mark.login
@vtest
class Test_C14835383_Vanilla_Betslip_REQ_RESPONSE_between_iFrame__Bet_Slip(BaseSportTest, BaseBetSlipTest,
                                                                           BaseUserAccountTest):
    """
    TR_ID: C14835383
    NAME: [Vanilla] - Betslip - REQ/RESPONSE between iFrame & Bet Slip
    DESCRIPTION: OXYGEN Bet Slip Component & the iFrame to handle various events during the QD process.
    PRECONDITIONS: 1. User Logged into app with a positive balance;
    """
    keep_browser_open = True
    deposit_amount = 5.00
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'
    over_balance = 1
    card_number = tests.settings.quick_deposit_card

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Login into the app with User that has a positive balance
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        gvc_settings = self.gvc_wallet_user_client.gvc_settings
        self.__class__._prefix, self.__class__._brand = gvc_settings.auth_username_prefix, gvc_settings.brand_id
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=self.username,
                                                                     amount=self.deposit_amount,
                                                                     card_number=self.card_number,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            market = next((market for market in event['event']['children']
                           if market.get('market').get('templateMarketName') == 'Match Betting' and
                           market['market'].get('children')), None)
            outcomes_resp = market['market']['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                 for i in outcomes_resp}
            self.__class__.team1 = list(all_selection_ids.keys())[0]
            self.__class__.selection_id = all_selection_ids.get(self.team1)
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, selection_ids = event_params.team1, event_params.selection_ids
            self.__class__.selection_id = selection_ids[self.team1]
        self.site.wait_content_state(state_name='HomePage')
        self.site.login(username=self.username)
        self.__class__.session_token = self.get_local_storage_cookie_value_as_dict('OX.USER').get('sessionToken')

        self.__class__.channelID = 'MW' if self.device_type == "mobile" else 'WC'

    def test_001_add_one_selection_to_the_betslip(self):
        """
        DESCRIPTION: * Add one selection to the Betslip (Click on 'Add to Betslip' button on "Quick Bet" pop up if accessing from mobile)
        DESCRIPTION: Open  Betslip view;
        EXPECTED: Betslip is opened;
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_enter_stake_that_exceeds_over_the_balance(self):
        """
        DESCRIPTION: * Enter Stake that exceeds over the balance;
        EXPECTED: * 'Place bet' button is changed to "Make a Deposit";
        EXPECTED: * A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'Stake of "{self.team1}" was not found')
        self.__class__.user_balance = self.site.header.user_balance
        self.bet_amount = self.user_balance + self.over_balance
        self.enter_stake_amount(stake=(stake.name, stake))
        self.__class__.estimated_returns = '{0:g}'.format(float(self.get_betslip_content().total_estimate_returns))
        self.__class__.total_stake = self.get_betslip_content().total_stake
        info_panel_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(info_panel_text, expected_message_text,
                         msg=f'Error message "{info_panel_text}" is not the same as expected "{expected_message_text}"')
        bet_button_name = self.get_betslip_content().make_quick_deposit_button.name
        self.assertEqual(bet_button_name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Button name "{bet_button_name}" is not '
                             f'the same as expected "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_003_click_on_make_a_deposit(self):
        """
        DESCRIPTION: * Click on 'Make a Deposit";
        EXPECTED: * QD GVC Overlay is displayed with all available payment methods for User;
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.betslip.quick_deposit.is_displayed(timeout=30),
                        msg='"Quick Deposit" section is not shown')

    def test_004_select_any_desired_payment_method(self):
        """
        DESCRIPTION: * Select any desired payment method;
        EXPECTED: * Payment method is selected;
        """
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        self.quick_deposit.accounts.click()
        self.quick_deposit.accounts.has_select_menu(timeout=2)
        visa_name = hide_number(self.card_number)
        self.assertTrue(self.quick_deposit.accounts.select_menu.is_payment_option_present(visa_name),
                        msg=f'{visa_name} was not found among available payment options')
        self.quick_deposit.accounts.select_menu.click_item(visa_name)
        switch_to_main_page()

    def test_005_check_the_url_which_is_sent_as_initial_url_params_to_the_iframe(self):
        """
        DESCRIPTION: * Check the URL which is sent as initial url params to the iframe
        EXPECTED: URL is:
        EXPECTED: https://re-coralcashier.ivycomptech.co.in/cashierapp/cashier.html?userId=cl_testuser&brandId=CORAL&productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=fdsadsffdsafds&stake=xxxx&estimatedReturn=xxx
        EXPECTED: * Contains Stake;
        EXPECTED: * Contains Estimated returns;
        """
        url = self.quick_deposit.get_iframe_url()

        expected_url = f'{tests.settings.cashier_url}cashierapp/cashier.html?' \
                       f'userId={self._prefix}{self.username}' \
                       f'&brandId={self._brand}&productId=SPORTSBOOK' \
                       f'&channelId={self.channelID}&langId=en' \
                       f'&sessionKey={self.session_token}' \
                       f'&stake={int(float(self.total_stake) * 100)}' \
                       f'&estimatedReturn={self.estimated_returns}#/'
        self.assertEqual(url, expected_url, msg=f'"{url}" does not match "{expected_url}"')

    def test_006_observe_amount_field_in_the_qd_iframe(self):
        """
        DESCRIPTION: * Observe "Amount" field in the QD iFrame;
        EXPECTED: The difference between the amount of stake and balance should be prepopulated; (if difference between amount of stake and balance is less than 10, prepopulated amount is 10)
        """
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        self.__class__.amount = self.quick_deposit.amount.input.value
        float_amount = float(self.amount)
        float_total_stake = float(self.total_stake)
        if self.over_balance < 10:
            self.assertEqual(self.amount, '5.00',
                             msg='The difference between the amount of stake and balance is incorrect')
        else:
            self.assertEqual(float_amount, float_total_stake - self.user_balance,
                             msg=f'The difference between the amount of stake "{float_amount}" '
                                 f'and balance "{self.user_balance}" is incorrect')

    def test_007_observe_the_qd_iframe_for_the_total_stake_potential_return_values_presence(self):
        """
        DESCRIPTION: * Observe the QD iFrame for The Total Stake & Potential Return values presence;
        EXPECTED: The Total Stake & Potential Return values are displayed on the GVC QD.
        """
        self.__class__.potential_returns = self.quick_deposit.potential_returns_value
        self.assertTrue(self.potential_returns, msg='Potential return is not present!')
        self.__class__.total_stake = self.quick_deposit.total_stake_value
        self.assertTrue(self.total_stake, msg='Total stake is not present!')

    def test_008_change_the_stake_decrease_or_increase_for_chosen_selection_notice_hide_qd_overlay_via_inspect_elements(self):
        """
        DESCRIPTION: * Change the stake (decrease or increase) for chosen selection;
        DESCRIPTION: Notice: (Hide QD overlay via Inspect elements);
        EXPECTED: Estimated Returns are recalculated and redisplayed on QD iFrame:
        EXPECTED: * Initial URL with parameters was resent;
        EXPECTED: * Values recalculated;
        """
        switch_to_main_page()
        self.get_betslip_content().quick_deposit.close_button.click()
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'Stake of "{self.team1}" was not found')
        self.bet_amount = self.user_balance + self.over_balance + 1
        self.enter_stake_amount(stake=(stake.name, stake))
        estimated_returns_recalculated = '{0:g}'.format(float(self.get_betslip_content().total_estimate_returns))
        self.__class__.total_stake_recalculated = self.get_betslip_content().total_stake
        self.assertNotEqual(estimated_returns_recalculated, self.estimated_returns,
                            msg=f'Estimated returns "{self.estimated_returns}" have not been '
                                f'recalculated to "{estimated_returns_recalculated}"!')
        self.get_betslip_content().make_quick_deposit_button.click()
        self.assertTrue(self.get_betslip_content().quick_deposit.is_displayed(timeout=15),
                        msg='"Quick Deposit" section is not shown')
        url = self.quick_deposit.get_iframe_url()
        expected_url = f'{tests.settings.cashier_url}cashierapp/cashier.html?' \
                       f'userId={self._prefix}{self.username}' \
                       f'&brandId={self._brand}&productId=SPORTSBOOK' \
                       f'&channelId={self.channelID}&langId=en' \
                       f'&sessionKey={self.session_token}' \
                       f'&stake={int(float(self.total_stake_recalculated) * 100)}' \
                       f'&estimatedReturn={estimated_returns_recalculated}#/'
        self.assertEqual(url, expected_url, msg=f'"{url}" does not match "{expected_url}"')

    def test_009_check_that_iframe_can_be_resizable_enable_disable_embedded_keyboard(self):
        """
        DESCRIPTION: Check that iFrame can be resizable:
        DESCRIPTION: * Enable/Disable embedded keyboard
        EXPECTED: QD iFrame height is changed for every resize event;
        """
        self._logger.warning('*** Not verified by autotest')

    def test_010_click_on_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: * Click on 'Deposit and Place Bet' button
        EXPECTED: Quick Deposit iFrame is closed
        """
        quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        self.__class__.actual_deposit_amount = self.quick_deposit.amount.input.value
        quick_deposit.cvv_2.click()

        if self.device_type == 'desktop':
            quick_deposit.cvv_2.input.value = tests.settings.quick_deposit_card_cvv
        else:
            keyboard = quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv)

        deposit_button = quick_deposit.deposit_and_place_bet_button

        self.assertTrue(deposit_button.is_displayed(expected_result=True),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not displayed')
        self.assertTrue(deposit_button.is_enabled(expected_result=True),
                        msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        name = deposit_button.name
        self.assertEqual(name, vec.gvc.DEPOSIT_AND_PLACE_BTN,
                         msg=f'Actual button name: "{name}"'
                             f'is not equal to expected: "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')
        deposit_button.click()

    def test_011_observe_the_place_bet_button_on_betslip(self):
        """
        DESCRIPTION: * Observe the 'Place Bet' button on Betslip
        EXPECTED: Spinner is displayed on the 'Place Bet' button without text
        EXPECTED: * User balance is refilled with a diff (balance stake);
        EXPECTED: * Bet is placed automatically;
        EXPECTED: * Betslip receipt is displayed;
        """
        switch_to_main_page()
        updated_balance = self.user_balance + float(self.actual_deposit_amount)
        self.assertTrue(self.site.is_bet_receipt_displayed(timeout=20), msg='Bet Receipt is not displayed')
        self.assertEqual(self.site.bet_receipt.receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.site.bet_receipt.receipt_header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        expected_user_balance = updated_balance - float(self.total_stake_recalculated)
        self.verify_user_balance(expected_user_balance)
