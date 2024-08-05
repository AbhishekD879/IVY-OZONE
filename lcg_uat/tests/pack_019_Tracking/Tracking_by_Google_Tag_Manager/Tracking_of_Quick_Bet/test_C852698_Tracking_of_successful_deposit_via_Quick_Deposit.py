import datetime
import pytest
import re

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import normalize_name
from voltron.utils.helpers import switch_to_main_page


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.quick_deposit
@pytest.mark.quick_bet
@pytest.mark.google_analytics
@pytest.mark.low
@pytest.mark.mobile_only
@pytest.mark.other
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C852698_Tracking_of_successful_deposit_via_Quick_Deposit(BaseSportTest, BaseBetSlipTest, BaseDataLayerTest, BaseUserAccountTest):
    """
    TR_ID: C852698
    VOL_ID: C9698158
    NAME: Tracking of successful deposit via Quick Deposit
    DESCRIPTION: This test case verifies tracking of successful deposit via Quick Deposit within Quick Bet
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. User is logged in
    PRECONDITIONS: 4. User has the following cards added to his account: Visa, Visa Electron, Master Card and Maestro
    """
    keep_browser_open = True
    users_data = None
    over_balance = 5.0
    username = None
    card_type = None
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def verify_tracking(self):
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='quickbet',
                                                              eventAction='place bet')
        self.assertTrue(actual_response, msg='GA Tracking info not present')
        action_fiend_id = actual_response[u'ecommerce'][u'purchase'][u'actionField']['id']
        product_name = actual_response[u'ecommerce'][u'purchase'][u'products'][0]['name']
        product_id = actual_response[u'ecommerce'][u'purchase'][u'products'][0]['id']

        self.assertTrue(re.match(r'[a-z]+', product_name),
                        msg='products.name "%s" has incorrect format.Expected format: "deposit XX' % product_name)

        self.assertTrue(re.match(r'[O]\/[0-9]+\/[0-9]+', action_fiend_id),
                        msg='actionField.id "%s" is not a number"' % action_fiend_id)
        self.assertTrue(re.match(r'[O]\/[0-9]+\/[0-9]+', product_id), msg='products.id "%s" is not a number"' % product_id)
        self.site.close_all_dialogs(async_close=False, timeout=15)
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide(timeout=15)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as user with balance at least 100 pounds. Tap Right menu icon
        EXPECTED: User is logged in with 100 pounds
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        username_master_card = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username_master_card, amount=str(20),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        first_user_card_type = 'Master Card'
        # TODO commented as there's no valid visa card that supports quick deposit
        # username_visa = self.gvc_wallet_user_client.register_new_user().username
        # self.add_card_and_deposit(username=username_visa, amount=tests.settings.min_deposit_amount)

        self.__class__.users_data = {
            username_master_card: first_user_card_type,
            # username_visa: 'Visa'
        }

    def test_001_create_events(self):
        """
        DESCRIPTION: Create/find event
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=1)
            self.__class__.eventID = events[0]['event']['id']
            market_name = next(
                (normalize_name(market.get('market', {}).get('name', '')) for market in events[0]['event']['children']
                 if market.get('market').get('templateMarketName') == 'Match Betting'),
                None)
            if not market_name:
                raise SiteServeException(f'Match Betting market not found for event {self.eventID}')

        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')

        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        self._logger.info(f'*** Using event {self.eventID} with market "{self.expected_market}"')

    def test_002_verifying_quick_stakes(self):
        """
        DESCRIPTION: Run test steps multiple times for different users
        """
        for self.__class__.username, self.__class__.card_type in self.users_data.items():
            self._logger.info('*** Verifications for user "%s" with "%s" card' % (self.username, self.card_type))

            self.step_001_login()
            self.step_002_navigate_to_football_event_page()
            self.step_003_click_on_football_event_bet_button()
            self.step_004_enter_numeric_value_to_stake()
            self.step_005_tap_on_make_a_quick_deposit_button()
            self.step_006_enter_cvv()
            self.step_007_type_in_console_datalayer_tap_enter_and_check_the_response()
            self.step_008_check_balance()
            self.step_009_logout()

    def step_001_login(self):
        """
        DESCRIPTION: Login as a user that has sufficient funds to place a bet
        """
        self.site.login(username=self.username)
        self.__class__.user_balance = self.site.header.user_balance

    def step_002_navigate_to_football_event_page(self):
        """
        DESCRIPTION: Navigate to Event Details page
        """
        self.navigate_to_edp(event_id=self.eventID)

    def step_003_click_on_football_event_bet_button(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick Bet is displayed
        EXPECTED: Added selection and all data are displayed in Quick Bet
        """
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)

    def step_004_enter_numeric_value_to_stake(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: 'Stake' field is pre-populated with value
        EXPECTED: 'Funds needed for bet "<currency symbol>XX.XX' error message is displayed immediately
        EXPECTED: 'PLACE BET' button becomes 'MAKE A QUICK DEPOSIT' immediately and is enabled by default
        """
        self.device.driver.implicitly_wait(0.7)
        self.site.quick_bet_panel.selection.quick_stakes.wait_until_refreshed(timeout=1)
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.user_balance + self.over_balance
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.over_balance)

        if self.brand == 'ladbrokes':
            result = self.site.quick_bet_panel.wait_for_deposit_info_panel()
            self.assertTrue(result, msg=f'"Min Deposit" message is not shown')
            message = self.site.quick_bet_panel.deposit_info_message.text
        else:
            self.assertTrue(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(expected_result=True),
                            msg='Quick Bet Info Panel is not present')
            message = self.site.quick_bet_panel.info_panels_text[0]
        self.assertEqual(message, expected_message,
                         msg='Actual message "%s" does not match expected "%s"' %
                             (message, expected_message))
        self.device.driver.implicitly_wait(0)

    def step_005_tap_on_make_a_quick_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A QUICK DEPOSIT' button
        EXPECTED: Quick Deposit section is displayed over of Quick Bet
        """
        self.site.quick_bet_panel.make_quick_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(), msg='Quick Deposit is not shown')

    def step_006_enter_cvv(self):
        """
        DESCRIPTION: Enter valid CVV, amount and tap 'MAKE A QUICK DEPOSIT' button
        EXPECTED: Success message is displayed
        """
        self.__class__.quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        self.quick_deposit.cvv_2.click()
        keyboard = self.quick_deposit.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=tests.settings.master_card_cvv)
        keyboard.enter_amount_using_keyboard(value='enter')
        deposit_button = self.quick_deposit.deposit_and_place_bet_button
        self.assertTrue(deposit_button.is_enabled(expected_result=True),
                        msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        deposit_button.click()

        switch_to_main_page()

        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

    def step_007_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField': {
        EXPECTED: 'id': <<id number>>,
        EXPECTED: 'revenue': '1'
        EXPECTED: },
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<< DEPOSIT NAME >>',
        EXPECTED: 'id': '<< DEPOSIT NUMBER >>',
        EXPECTED: 'price': '1',
        EXPECTED: 'category': 'credit card',
        EXPECTED: 'quantity': 1
        EXPECTED: }]
        EXPECTED: }
        EXPECTED: },
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/deposit/success',
        EXPECTED: 'location' : 'quickbet'
        EXPECTED: });
        """
        self.verify_tracking()

    def step_008_check_balance(self):
        """
        DESCRIPTION: Check balance
        """
        user_balance_after = str(self.site.header.user_balance)
        expected_balance = '0.0' if self.brand == 'ladbrokes' or tests.settings.backend_env == 'prod' else '5.0'
        self.assertEqual(user_balance_after, expected_balance, msg='Actual amount "%s" does not match expected "%s"'
                                                                   % (user_balance_after, expected_balance))

    def step_009_logout(self):
        """
        DESCRIPTION: Logout
        """
        self.site.logout()
