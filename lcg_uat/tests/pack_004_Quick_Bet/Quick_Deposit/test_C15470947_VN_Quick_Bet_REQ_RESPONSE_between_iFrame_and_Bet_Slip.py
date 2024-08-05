import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import switch_to_main_page, hide_number


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.quick_deposit
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1730')
@pytest.mark.portal_dependant
@vtest
class Test_C15470947_Vanilla___Quick_Bet___REQ_RESPONSE_between_iFrame__Bet_Slip(BaseSportTest, BaseUserAccountTest):
    """
    TR_ID: C15470947
    VOL_ID: C24281912
    NAME: [Vanilla] - Quick Bet - REQ/RESPONSE between iFrame & Bet Slip
    DESCRIPTION: OXYGEN Quick Bet Component & the iFrame to handle various events during the QD process.
    PRECONDITIONS: * Login into the app with User that has a positive balance;
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        Login into the app with User that has a positive balance
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        self.__class__.card = tests.settings.quick_deposit_card

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.event_id = event['event']['id']
            market = next((market for market in event['event']['children']
                           if market.get('market').get('templateMarketName') == 'Match Betting' and
                           market['market'].get('children')), None)
            market_name = market['market']['name']
            outcomes_resp = market['market']['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                 for i in outcomes_resp}
            if self.brand == 'ladbrokes':
                self.__class__.team1 = (list(all_selection_ids.keys())[0]).upper()
            else:
                self.__class__.team1 = list(all_selection_ids.keys())[0]
            self.__class__.selection_id = all_selection_ids.get(self.team1)
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_id = event_params.event_id
            self.__class__.team1, selection_ids = event_params.team1, event_params.selection_ids
            self.__class__.selection_id = selection_ids[self.team1]
            market_name = self.ob_config.football_config. \
                autotest_class.autotest_premier_league.market_name.replace('|', '')

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        gvc_settings = self.gvc_wallet_user_client.gvc_settings
        self.__class__._prefix, self.__class__._brand = gvc_settings.auth_username_prefix, gvc_settings.brand_id
        self.__class__.username = tests.settings.quick_deposit_user
        self.site.login(username=self.username)
        self.__class__.session_token = self.get_local_storage_cookie_value_as_dict('OX.USER').get('sessionToken')

    def test_001_select_any_desired_event_and_tap_on_any_selection(self):
        """
        DESCRIPTION: * Select any desired event and tap on any selection;
        EXPECTED: * Quick Bet pop up is displayed;
        """
        self.navigate_to_edp(self.event_id)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

    def test_002_enter_stake_that_exceeds_over_the_balance(self):
        """
        DESCRIPTION: Enter Stake that exceeds over the balance;
        EXPECTED: 'Place bet' button is changed to "Make a Deposit";
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of £x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        self.__class__.over_balance = 4.95
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_displayed(timeout=2),
                        msg='Amount input field is not displayed')
        self.__class__.user_balance = self.site.header.user_balance
        self.quick_bet.content.amount_form.input.value = self.user_balance + self.over_balance
        self.__class__.estimated_returns = f'{float(self.quick_bet.bet_summary.total_estimate_returns):g}'
        self.__class__.total_stake = self.quick_bet.bet_summary.total_stake
        if self.over_balance < 5:
            expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(5)
        else:
            expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.over_balance)

        if self.brand == 'ladbrokes':
            self.assertTrue(self.site.quick_bet_panel.wait_for_deposit_info_panel(),
                            msg='Deposit Info Panel is not present')
            message = self.site.quick_bet_panel.deposit_info_message.text
        else:
            self.assertTrue(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(),
                            msg='Quick Bet Info Panel is not present')
            message = self.site.quick_bet_panel.info_panels_text[0]
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_message}"')

    def test_003_click_on_make_a_deposit(self):
        """
        DESCRIPTION: * Click on 'Make a Deposit";
        EXPECTED: * QD GVC Overlay is displayed with all available payment methods for User;
        """
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.site.wait_content_state_changed(timeout=2)
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(timeout=10),
                        msg='"Quick Deposit" section is not shown')

    def test_004_select_any_desired_payment_method(self):
        """
        DESCRIPTION: * Select any desired payment method;
        EXPECTED: * Payment method is selected;
        """
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.quick_deposit.accounts.click()
        self.quick_deposit.accounts.has_select_menu(timeout=5)
        visa_name = hide_number(self.card)
        self.assertTrue(
            self.quick_deposit.accounts.select_menu.is_payment_option_present(option_name=visa_name, timeout=5),
            msg=f'{visa_name} was not found among available payment options')
        self.quick_deposit.accounts.select_menu.click_item(item_name=visa_name)
        switch_to_main_page()

    def test_005_check_the_url_which_is_sent_as_initial_url_params_to_the_iframe(self):
        """
        DESCRIPTION: * Check the URL which is sent as initial url params to the iframe
        EXPECTED: URL is:
        EXPECTED: https://cashier.coral.co.uk/cashierapp/cashier.html?userId=[username]&brandId=CORAL&productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=[session_key]]&stake=[stake_amount]&estimatedReturn=[estimated_returns_amount]
        EXPECTED: (e.g. - https://cashier.coral.co.uk/cashierapp/cashier.html?userId=cl_testgvccl-API4&brandId=CORAL&productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=0600d4bcc1bd40dc875734924d94fb0e&stake=3000&estimatedReturn=75#/)
        EXPECTED: * Contains Stake;
        EXPECTED: * Contains Estimated returns;
        """
        url = self.site.quick_bet_panel.quick_deposit_panel.get_iframe_url()
        expected_url = f"{tests.settings.cashier_url}cashierapp/cashier.html?" \
                       f"userId={self._prefix}{self.username}" \
                       f"&brandId={self._brand}&productId=SPORTSBOOK" \
                       f"&channelId=MW&langId=en" \
                       f"&sessionKey={self.session_token}" \
                       f"&stake={int(float(self.total_stake) * 100)}" \
                       f"&estimatedReturn={self.estimated_returns}#/"
        self.assertEqual(url, expected_url, msg=f'"{url}" does not match "{expected_url}"')

    def test_006_observe_amount_field_in_the_qd_iframe(self):
        """
        DESCRIPTION: Observe "Amount" field in the QD iFrame;
        EXPECTED: The difference between the amount of stake and balance should be prepopulated; (if difference between amount of stake and balance is less than 5, prepopulated amount is 5)
        """
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.__class__.amount = self.quick_deposit.amount.input.value
        sleep(2)
        float_amount = float(self.amount)
        prepopulated_value = 5.0 if self.over_balance < 5 else float(self.total_stake) - self.user_balance
        self.assertEqual(float_amount, prepopulated_value,
                         msg=f'Deposit amount prepopulated incorrectly. '
                             f'Actual "{float_amount}". Expected "{prepopulated_value}"')

    def test_007_observe_the_qd_iframe_for_the_total_stake_potential_return_values_presence(self):
        """
        DESCRIPTION: Observe the QD iFrame for The Total Stake & Potential Return values presence;
        EXPECTED: The Total Stake & Potential Return values are displayed on the GVC QD.
        """
        potential_returns = self.quick_deposit.potential_returns_value
        self.assertTrue(potential_returns, msg='Potential return is not present!')
        self.total_stake = self.quick_deposit.total_stake_value
        self.assertTrue(self.total_stake, msg='Total stake is not present!')

    def test_008_close_qd_overlay_and_change_the_stake_decrease_or_increase_for_chosen_selection(self):
        """
        DESCRIPTION: Close QD overlay and change the stake (decrease or increase) for chosen selection;
        EXPECTED: Estimated Returns are recalculated and redisplayed on QD iFrame:
        EXPECTED: * Initial URL with parameters was resent;
        EXPECTED: * Values recalculated;
        """
        switch_to_main_page()
        self.site.quick_bet_panel.quick_deposit_panel.close_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='"Quick Bet" section is not shown')

        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        self.quick_bet.content.amount_form.input.value = self.user_balance + self.over_balance + 1
        estimated_returns_recalculated = '{0:g}'.format(float(self.quick_bet.bet_summary.total_estimate_returns))
        self.__class__.total_stake_recalculated = self.quick_bet.bet_summary.total_stake
        self.assertNotEqual(estimated_returns_recalculated, self.estimated_returns,
                            msg=f'Estimated returns "{self.estimated_returns}" have not been '
                                f'recalculated to "{estimated_returns_recalculated}"!')

        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='"Quick Deposit" section is not shown')

        url = self.site.quick_bet_panel.quick_deposit_panel.get_iframe_url()
        expected_url = f"{tests.settings.cashier_url}cashierapp/cashier.html?" \
                       f"userId={self._prefix}{self.username}" \
                       f"&brandId={self._brand}&productId=SPORTSBOOK" \
                       f"&channelId=MW&langId=en" \
                       f"&sessionKey={self.session_token}" \
                       f"&stake={int(float(self.total_stake_recalculated) * 100)}" \
                       f"&estimatedReturn={estimated_returns_recalculated}#/"
        self.assertEqual(url, expected_url, msg=f'{url} does not match {expected_url}')

    def test_009_check_that_iframe_can_be_resizable_enable_disable_embedded_keyboard(self):
        """
        DESCRIPTION: Check that iFrame can be resizable:
        DESCRIPTION: * Enable/Disable embedded keyboard
        EXPECTED: QD iFrame height is changed for every resize event;
        """
        # Only for manual testing

    def test_010_enter_secure_id_and_click_on_deposit_and_place_bet(self):
        """
        DESCRIPTION: Enter Secure Id and click on 'Deposit and Place Bet'
        EXPECTED: Quick Deposit iFrame is closed
        """
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.quick_deposit.cvv_2.click()

        keyboard = self.quick_deposit.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=tests.settings.visa_card_cvv, delay=0.7)
        keyboard.enter_amount_using_keyboard(value='enter')

        deposit_button = self.quick_deposit.deposit_and_place_bet_button
        self.assertTrue(deposit_button.is_displayed(expected_result=True),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not displayed')
        self.assertTrue(deposit_button.is_enabled(expected_result=True),
                        msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        self.assertEqual(deposit_button.name, vec.gvc.DEPOSIT_AND_PLACE_BTN,
                         msg=f'Actual button name: "{deposit_button.name}" '
                             f'is not equal to expected: "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')
        deposit_button.click()
        sleep(2)

    def test_011_observe_the_place_bet_button_on_quick_bet(self):
        """
        DESCRIPTION: Observe the 'Place Bet' button on Quick Bet
        EXPECTED: Spinner is displayed on the 'Place Bet' button without text
        EXPECTED: * User balance is refilled with a diff (balance stake);
        EXPECTED: * Bet is placed automatically;
        EXPECTED: * Betslip receipt is displayed;
        """
        updated_balance = self.user_balance + float(self.amount) + 1
        sleep(3)
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        bet_receipt = self.site.quick_bet_panel.bet_receipt
        bet_receipt.header.has_bet_placed_text()
        self.assertEqual(bet_receipt.header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{bet_receipt.header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        self.__class__.user_balance = self.site.header.user_balance
        expected_user_balance = updated_balance - float(self.total_stake_recalculated)
        self.verify_user_balance(expected_user_balance=expected_user_balance, delta=0.06)  # because of VANO-1730
