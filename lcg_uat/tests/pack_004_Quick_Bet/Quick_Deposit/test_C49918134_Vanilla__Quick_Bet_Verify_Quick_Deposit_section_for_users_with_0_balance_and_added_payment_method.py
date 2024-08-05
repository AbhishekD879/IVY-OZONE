import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.portal_dependant
@vtest
class Test_C49918134_Vanilla__Quick_Bet_Verify_Quick_Deposit_section_for_users_with_0_balance_and_added_payment_method(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C49918134
    NAME: [Vanilla] - [Quick Bet]  Verify Quick Deposit section for users with 0 balance and added payment method
    DESCRIPTION: This test case verifies Quick Deposit section within Quick Bet for users with 0 balance and added payment method
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS and user`s settings
        PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            market_name, outcomes = next(((market['market']['name'], market['market']['children']) for market in event['event']['children']
                                         if market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.event_name = normalize_name(event['event']['name'])
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(selection_ids.values())[1]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event.event_id
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.selection_id = list(event.selection_ids.values())[1]
            market_name = normalize_name(
                self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_load_the_application(self):
        """
        DESCRIPTION: Load the application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_log_in_with_user_that_has_0_on_his_balance_and_added_payment_method_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has 0 on his balance and added payment method to his account
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.user_0_balance_with_card)
        user_balance = self.site.header.user_balance
        if user_balance:
            self.open_betslip_with_selections(selection_ids=self.selection_id)
            self.bet_amount = user_balance
            self.site.wait_content_state_changed(timeout=5)
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.navigate_to_page("Homepage")

    def test_003_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * Added selection and all data are displayed in Quick Bet
        EXPECTED: * 'Make a Deposit' button is displayed and disabled
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')

        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        self.assertEqual(self.quick_bet.content.event_name, self.event_name,
                         msg=f'Actual event name "{self.quick_bet.content.event_name}" '
                             f'does not match expected "{self.event_name}"')

    def test_004_enter_some_value_in_stake_field_manually_or_use_quick_stake__buttons(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field manually or use 'Quick Stake ' buttons
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Make a Deposit' becomes enabled
        """
        self.quick_bet.content.amount_form.input.value = 5
        actual_enter_value = self.quick_bet.content.amount_form.input.value
        self.assertEqual(actual_enter_value, '5.00',
                         msg=f'Actaul entered value: "{actual_enter_value}" is not same a Expected value: "5.00"')
        self.__class__.make_deposit_button = self.site.quick_bet_panel.make_quick_deposit_button
        self.assertTrue(self.make_deposit_button.is_enabled(), msg='Make Deposit button was not enabled')

    def test_005_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'Make a Deposit' button
        EXPECTED: Quick Deposit iFrame opens
        """
        self.make_deposit_button.click()
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_deposit_panel(),
                        msg='Quick Deposit section is not shown')

    def test_006_enter_cvvtap_deposit_and_place_bet_button(self):
        """
        DESCRIPTION: Enter CVV
        DESCRIPTION: Tap 'Deposit and Place Bet' button
        EXPECTED: Quick Bet is opened
        EXPECTED: Bet is successfully placed
        """
        quick_deposit = self.site.quick_bet_panel.quick_deposit_panel.stick_to_iframe()
        quick_deposit.cvv_2.click()
        keyboard = quick_deposit.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv)
        keyboard.enter_amount_using_keyboard(value='enter')
        deposit_button = quick_deposit.deposit_and_place_bet_button
        self.assertTrue(deposit_button.is_enabled(expected_result=True),
                        msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        deposit_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet panel is not opened')
        self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(), msg='Bet placement was not successful')
