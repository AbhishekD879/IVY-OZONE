import pytest
import datetime
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import switch_to_main_page, hide_number


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.quick_bet
@pytest.mark.desktop
@pytest.mark.build_your_bet
@pytest.mark.quick_deposit
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1532')
@vtest
class Test_C15392950_Vanilla_Build_Your_Bet_REQ_RESPONSE_between_iFrame_Bet_Slip(BaseBanachTest, BaseUserAccountTest):
    """
    TR_ID: C15392950
    NAME: [Vanilla] - Build Your Bet - REQ/RESPONSE between iFrame & Bet Slip
    DESCRIPTION: OXYGEN Bet Slip Component & the iFrame to handle various events during the QD process - Build Your Bet area.
    DESCRIPTION: Acceptance criteria:
    DESCRIPTION: * The difference amount i.e. stake - balance shall be sent via the iframe so that the GVC QD can pre-populate this amount.
    DESCRIPTION: * The Total Stake & Potential Return values shall be sent via the iframe so that these values are displayed on the GVC QD.
    DESCRIPTION: * Price Change & Event suspension notifications shall be sent via the iframe so that the GVC QD can display appropriate messages on the confirmation button.
    DESCRIPTION: * iFrame - height to be sent on every resize event, so that the content within the iframe is displayed proportionally.
    DESCRIPTION: Note:
    DESCRIPTION: * Please refer to the story - VANO-138 for QD functional requirements.
    """
    keep_browser_open = True
    card_number = tests.settings.quick_deposit_card
    proxy = None
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Login into the app with User that has a positive balance;
        PRECONDITIONS: 2. The test event was created in Openbet and opened in a separate browser tab;
        PRECONDITIONS: 3. The test event details were opened in the Oxygen application so User can see test markets for price change and suspension;
        PRECONDITIONS: 4. Navigate to event details page > Build your bet tab
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        gvc_settings = self.gvc_wallet_user_client.gvc_settings
        self.__class__._prefix, self.__class__._brand = gvc_settings.auth_username_prefix, gvc_settings.brand_id

        self.__class__.channelID = None
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=self.username,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=tests.settings.quick_deposit_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        self.__class__.eventID = self.get_ob_event_with_byb_market()

        self.site.login(username=self.username)
        self.__class__.session_token = self.get_local_storage_cookie_value_as_dict('OX.USER').get('sessionToken')
        self.assertTrue(self.session_token,
                        msg='Session token is absent!')
        self.navigate_to_edp(self.eventID)
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.__class__.channelID = 'MW' if self.device_type == "mobile" else 'WC'

    def test_001_add_2_selection_to_the_betslip_from_below_build_your_bet_tab(self):
        """
        DESCRIPTION: * Add 2 selection to the betslip from below Build your bet tab
        EXPECTED: * Selection are added;
        EXPECTED: A tab with selections appears with a "Place Bet" button
        """
        # self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.match_betting,
        #                                     selection_index=1)
        # self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.both_teams_to_score_in_both_halves,
        #                                     selection_index=1)

        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')

        match_betting_selection_names = match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)

        self.__class__.initial_counter += 1

        # Double Chance selection
        double_chance_market = self.get_market(market_name=self.expected_market_sections.double_chance)
        double_chance_market.scroll_to()
        double_chance_market_names = double_chance_market.set_market_selection(selection_index=1)[0]
        self.assertTrue(double_chance_market_names, msg='No one selection added to Dashboard')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(timeout=13)
        self.assertTrue(is_expanded, msg='Dashboard is not expanded by default')

    def test_002_tap_on_place_bet_button(self):
        """
        DESCRIPTION: * Tap on "Place Bet" button
        EXPECTED: *Betslip is opened at the bottom of page (UI is similar to quick bet);
        """
        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip has not appeared')

    def test_003_enter_stake_that_exceeds_over_the_balance(self):
        """
        DESCRIPTION: * Enter Stake that exceeds over the balance  (e.g. - 155 USD/EU/GBP);
        EXPECTED: * 'Place bet' button is changed to "Make a Deposit";
        """
        self.__class__.over_balance = 10.0
        self.__class__.user_balance = self.site.header.user_balance
        stake = self.user_balance + self.over_balance
        self.__class__.panel = self.site.byb_betslip_panel
        self.panel.selection.content.amount_form.input.value = stake
        self.__class__.quick_deposit_button = self.panel.make_quick_deposit_button
        self.assertTrue(self.quick_deposit_button.is_displayed(),
                        msg=f'"MAKE A QUICK DEPOSIT" button is not displayed below BetSlip')
        self.__class__.estimated_returns = '{0:g}'.format(
            float(self.panel.selection.bet_summary.total_estimate_returns))
        self.__class__.total_stake = self.panel.selection.bet_summary.total_stake

    def test_004_click_on_make_a_deposit(self):
        """
        DESCRIPTION: * Click on 'Make a Deposit";
        EXPECTED: * QD GVC Overlay is displayed with all available payment methods for User;
        """
        self.quick_deposit_button.click()
        self.assertTrue(self.panel.wait_for_quick_deposit_panel(),
                        msg='Quick deposit menu is not opened')
        self.__class__.quick_deposit = self.panel.quick_deposit_panel.stick_to_iframe(timeout=15)
        self.assertFalse(self.quick_deposit.deposit_and_place_bet_button.is_enabled(
            expected_result=False), msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not disabled')
        self.quick_deposit.accounts.click()
        self.quick_deposit.accounts.has_select_menu(timeout=10)
        self.__class__.visa_name = hide_number(self.card_number)
        self.assertTrue(self.quick_deposit.accounts.select_menu.is_payment_option_present(self.visa_name, timeout=5),
                        msg=f'{self.visa_name} was not found among available payment options')

    def test_005_select_any_desired_payment_method(self):
        """
        DESCRIPTION: * Select any desired payment method;
        EXPECTED: * Payment method is selected;
        """
        self.quick_deposit.accounts.select_menu.click_item(self.visa_name)
        self.assertEqual(self.quick_deposit.accounts.selected_account(), hide_number(self.card_number),
                         msg=f'Expected "{hide_number(self.card_number)}" '
                             f'!= Actual "{self.quick_deposit.accounts.selected_account()}"')
        switch_to_main_page()

    def test_006_check_the_url_which_is_sent_as_initial_url_params_to_the_iframe(self):
        """
        DESCRIPTION: Check the URL which is sent as initial url params to the iframe
        EXPECTED: URL is:
        EXPECTED: https://cashier.coral.co.uk/cashierapp/cashier.html?userId=[username]&brandId=CORAL&productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=[session_key]]&stake=[stake_amount]&estimatedReturn=[estimated_returns_amount]
        EXPECTED: (e.g. - https://cashier.coral.co.uk/cashierapp/cashier.html?userId=cl_testgvccl-API4&brandId=CORAL&productId=SPORTSBOOK&channelId=MW&langId=en&sessionKey=0600d4bcc1bd40dc875734924d94fb0e&stake=3000&estimatedReturn=75#/)
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

    def test_007_observe_amount_field_in_the_qd_iframe(self):
        """
        DESCRIPTION: Observe "Amount" field in the QD iFrame;
        EXPECTED: The difference between the amount of stake and balance should be prepopulated on the Payment page;
        """
        self.__class__.quick_deposit = self.panel.quick_deposit_panel.stick_to_iframe()
        self.__class__.amount = self.quick_deposit.amount.input.value
        float_amount = float(self.amount)
        float_total_stake = float(self.total_stake)
        self.assertEqual(float_amount, float_total_stake - self.user_balance,
                         msg=f'The difference between the amount of stake "{float_amount}" '
                             f'and balance "{self.user_balance}" is incorrect')

    def test_008_observe_the_qd_iframe_for_the_total_stake_and_potential_return_values_presence(self):
        """
        DESCRIPTION: Observe the QD iFrame for The Total Stake & Potential Return values presence;
        EXPECTED: The Total Stake & Potential Return values are displayed on the GVC QD.
        """
        potential_returns = self.quick_deposit.potential_returns_value
        self.assertTrue(potential_returns, msg='Potential return is not present!')
        self.total_stake = self.quick_deposit.total_stake_value
        self.assertTrue(self.total_stake, msg='Total stake is not present!')

    def test_009_change_the_stake_decrease_or_increase_for_chosen_selection(self):
        """
        DESCRIPTION: Change the stake (decrease or increase) for chosen selection;
        EXPECTED: Estimated Returns are recalculated and redisplayed on QD iFrame:
        EXPECTED: * Initial URL with parameters was resent;
        EXPECTED: * Values recalculated;
        """
        switch_to_main_page()
        self.quick_deposit.close_button.click()
        self.assertTrue(self.panel.selection.content.amount_form.input.is_enabled(),
                        msg='Amount form is not enabled!')
        self.panel.selection.content.amount_form.input.value = self.user_balance + self.over_balance + 1
        estimated_returns_recalculated = '{0:g}'.format(float(self.panel.selection.bet_summary.total_estimate_returns))
        self.__class__.total_stake_recalculated = self.panel.selection.bet_summary.total_stake
        self.assertNotEqual(estimated_returns_recalculated, self.estimated_returns,
                            msg=f'Estimated returns "{self.estimated_returns}" have not been '
                                f'recalculated to "{estimated_returns_recalculated}"!')

        self.panel.make_quick_deposit_button.click()
        self.assertTrue(self.panel.wait_for_quick_deposit_panel(),
                        msg='"Quick Deposit" section is not shown')

        url = self.panel.quick_deposit_panel.get_iframe_url()
        expected_url = f'{tests.settings.cashier_url}cashierapp/cashier.html?' \
                       f'userId={self._prefix}{self.username}' \
                       f'&brandId={self._brand}&productId=SPORTSBOOK' \
                       f'&channelId={self.channelID}&langId=en' \
                       f'&sessionKey={self.session_token}' \
                       f'&stake={int(float(self.total_stake_recalculated) * 100)}' \
                       f'&estimatedReturn={estimated_returns_recalculated}#/'
        self.assertEqual(url, expected_url, msg=f'{url} does not match {expected_url}')

    def test_010_check_that_iframe_can_be_resizable_enable_disable_embedded_keyboard(self):
        """
        DESCRIPTION: Check that iFrame can be resizable:
        DESCRIPTION: * Enable/Disable embedded keyboard
        EXPECTED: QD iFrame height is changed for every resize event;

        Not verified in scope of automation testing
        """
        pass

    def test_011_click_on_deposit_and_place_bet(self):
        """
        DESCRIPTION: Click on 'Deposit and Place Bet'
        EXPECTED: * Quick Deposit iFrame is closed
        EXPECTED: * User balance is refilled with a diff (balance stake);
        EXPECTED: * Bet is placed automatically;
        EXPECTED: * Betslip receipt is displayed;
        """
        self.__class__.quick_deposit = self.panel.quick_deposit_panel.stick_to_iframe()
        self.quick_deposit.cvv_2.click()

        if self.device_type == 'desktop':
            self.quick_deposit.cvv_2.input.value = tests.settings.visa_card_cvv
        else:
            keyboard = self.quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value=tests.settings.visa_card_cvv)
            keyboard.enter_amount_using_keyboard(value='enter')

        deposit_button = self.quick_deposit.deposit_and_place_bet_button

        self.assertTrue(deposit_button.is_displayed(expected_result=True),
                        msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not displayed')
        self.assertTrue(deposit_button.is_enabled(expected_result=True),
                        msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        self.assertEqual(deposit_button.name, vec.gvc.DEPOSIT_AND_PLACE_BTN,
                         msg=f'Actual button name: "{deposit_button.name}"'
                             f'is not equal to expected: "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')
        deposit_button.click()

        switch_to_main_page()

        self.assertTrue(self.panel.bet_receipt.is_displayed(), msg='Bet Receipt is not displayed')
        self.assertEqual(self.panel.bet_receipt.header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.panel.bet_receipt.header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
