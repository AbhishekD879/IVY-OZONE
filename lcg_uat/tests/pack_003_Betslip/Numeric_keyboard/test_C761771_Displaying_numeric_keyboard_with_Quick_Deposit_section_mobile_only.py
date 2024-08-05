import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


# @pytest.mark.lad_prod  # test case not up to date
# @pytest.mark.lad_hl  TODO adapt once story related to BMA-44329 will be completed
# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException


@pytest.mark.betslip
@pytest.mark.iphone
@pytest.mark.numeric_keyboard
@pytest.mark.quick_deposit
@pytest.mark.mobile_only
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C761771_Displaying_numeric_keyboard_with_Quick_Deposit_section_mobile_only(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C761771
    VOL_ID: C9697748
    NAME: Displaying numeric keyboard with Quick Deposit section mobile only
    DESCRIPTION: This test case verifies numeric keyboard displaying with Quick Deposit section
    PRECONDITIONS: Oxygen application is loaded
    PRECONDITIONS: User account with Zero balance and supported card types added
    PRECONDITIONS: User account with positive balance and supported card types added
    """
    # TODO adapt once story related to BMA-44329 will be completed
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
            outcomes = market['market']['children']
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids

    def test_001_log_in_with_account_with_zero_balance(self):
        """
        DESCRIPTION: Log in with **account with Zero balance**
        EXPECTED: User is logged in
        """
        # todo: adapt     VOL-4387  [Vanilla] Adapt Quick Deposit tests
        user = self.gvc_wallet_user_client.register_new_user()
        self.add_card_and_deposit(username=self.username,
                                  amount=tests.settings.min_deposit_amount,
                                  card_number=tests.settings.quick_deposit_card)

        self.site.login(username=user)

    def test_002_add_one_selection_to_the_betslip_open_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip > Open Betslip
        EXPECTED: Selection is available within Betslip
        EXPECTED: 'Quick Deposit' section is shown
        EXPECTED: Numeric keyboard is not shown withing 'Quick Deposit' section
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        self.__class__.betslip_content = self.get_betslip_content()
        self.assertTrue(self.get_betslip_content().quick_deposit.is_expanded(),
                        msg='"Quick Deposit" section is not expanded')
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(expected_result=False,
                                                                          name='Betslip keyboard shown'),
                         msg='Betslip keyboard is not shown')

    def test_003_tap_on_quick_deposit_section_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header
        EXPECTED: Keyboard disappears
        EXPECTED: 'Quick Stake' buttons are shown below 'Deposit Amount' and 'CVV' fields
        """
        self.get_betslip_content().quick_deposit.form_header.click()
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard is not hidden',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')

        quick_stake_panel = self.get_betslip_content().quick_stake_panel
        self.assertTrue(quick_stake_panel.is_displayed(), msg='Numeric keyboard for "Quick Stake" is not opened')
        quick_stake_buttons = quick_stake_panel.items_as_ordered_dict
        self.assertTrue(quick_stake_buttons, msg='"Quick Stake" buttons are not displayed')

    def test_004_set_focus_over_stake_field_amount_or_cvv_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Stake' field/ 'Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: Keyboard is shown below 'Quick Deposit' section
        """
        self.get_betslip_content().quick_deposit.amount_form.input.click()
        self.assertTrue(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown'),
                        msg='Betslip keyboard is not shown')

    def test_005_tap_on_quick_deposit_section_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header
        EXPECTED: Keyboard disappears
        EXPECTED: 'Quick Stake' buttons are shown below 'Deposit Amount' and 'CVV' fields
        """
        self.get_betslip_content().quick_deposit.form_header.click()
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard is not hidden',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')

        quick_stake_panel = self.get_betslip_content().quick_stake_panel
        self.assertTrue(quick_stake_panel.is_displayed(), msg='Numeric keyboard for "Quick Stake" is not opened')
        quick_stake_buttons = quick_stake_panel.items_as_ordered_dict
        self.assertTrue(quick_stake_buttons, msg='"Quick Stake" buttons are not displayed')

    def test_006_enter_value_into_stake_field(self, bet_amount=None):
        """
        DESCRIPTION: Enter value into 'Stake' field
        EXPECTED: - Message 'Please deposit a min of #CURRENCY_VALUE.VALUE' to continue placing your bet' is shown above 'MAKE A DEPOSIT' button, where
        """
        bet_amount = bet_amount if bet_amount else self.bet_amount
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        stake.amount_form.input.click()
        self.enter_value_using_keyboard(value=bet_amount)

        message_text = self.get_betslip_content().quick_deposit.warning_panel.text
        expected_message_text = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(message_text, expected_message_text,
                         msg=f'Message text is incorrect, expected "{expected_message_text}", found "{message_text}"')

    def test_007_tap_on_quick_deposit_section_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header
        EXPECTED: Keyboard disappears
        EXPECTED: 'Quick Deposit' section is expanded
        """
        self.get_betslip_content().quick_deposit.form_header.click()
        self.assertTrue(self.get_betslip_content().quick_deposit.is_expanded(),
                        msg='"Quick Deposit" section is collapsed')
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard is not hidden',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')

    def test_008_set_focus_over_stake_fields_amount_or_cvv_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Stake' fields/ 'Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: Keyboard is shown below 'Quick Deposit' section
        """
        self.get_betslip_content().quick_deposit.amount_form.input.click()
        self.assertTrue(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown'),
                        msg='Betslip keyboard is not shown')

    def test_009_tap_on_x_button_in_quick_deposit_section(self):
        """
        DESCRIPTION: Tap on 'X' button in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard disappears
        EXPECTED: - 'Quick Deposit' section is collapsed
        """
        self.get_betslip_content().quick_deposit.close_button.click()
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard is not hidden',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')
        self.assertFalse(self.get_betslip_content().quick_deposit.is_expanded(expected_result=False),
                         msg='"Quick Deposit" section is expanded')

    def test_010_add_several_selections_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Close Betslip -> Add several selections to the Betslip -> Open Betslip
        EXPECTED: Selections are available within Betslip
        EXPECTED: No keyboard is displayed
        """
        self.site.close_betslip()
        self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])
        self.__class__.betslip_content = self.get_betslip_content()

        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard is not hidden',
                                                                          timeout=3,
                                                                          expected_result=False),
                         msg='Betslip keyboard is not hidden')

    def test_011_set_focus_over_any_stake_field(self):
        """
        DESCRIPTION: Set focus over any 'Stake' field
        EXPECTED: - Numeric keyboard is shown above 'MAKE A DEPOSIT' button
        """
        stakes = self.get_betslip_sections().Singles
        self.assertTrue('Draw' in stakes, msg=f'"Draw" stake is not found in [{stakes.keys()}]')
        stakes['Draw'].amount_form.input.click()
        self.assertTrue(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown'),
                        msg='Betslip keyboard is not shown')

    def test_012_repeat_steps_3_9(self):
        """
        DESCRIPTION: Repeat steps 3-9
        EXPECTED: Results are the same
        """
        self.test_003_tap_on_quick_deposit_section_header()
        self.test_004_set_focus_over_stake_field_amount_or_cvv_in_quick_deposit_section()
        self.test_005_tap_on_quick_deposit_section_header()
        self.test_006_enter_value_into_stake_field()
        self.test_007_tap_on_quick_deposit_section_header()
        self.test_008_set_focus_over_stake_fields_amount_or_cvv_in_quick_deposit_section()
        self.test_009_tap_on_x_button_in_quick_deposit_section()

    def test_013_clear_betslip_and_log_out(self):
        """
        DESCRIPTION: Clear Betslip and Log out
        EXPECTED: Betslip is cleared
        EXPECTED: User is logged out
        """
        self.clear_betslip()
        self.site.logout()

    def test_014_log_in_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Log in with **user account with positive balance**
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_015_add_one_selection_to_the_betslip_open_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip > Open Betslip
        EXPECTED: Selection is available within Betslip
        EXPECTED: No 'Quick Deposit' section is shown
        EXPECTED: Numeric keyboard is not available
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        self.__class__.betslip_content = self.get_betslip_content()
        self.assertFalse(self.betslip_content.has_deposit_form(expected_result=False),
                         msg='There\'s Quick deposit form!')
        self.assertFalse(self.betslip_content.keyboard.is_displayed(expected_result=False,
                                                                    name='Betslip keyboard is not shown'),
                         msg='Betslip keyboard is not shown')

    def test_016_tap_on_balance_deposit_button_in_the_betslip_header(self):
        """
        DESCRIPTION: Tap on Balance -> 'Deposit' button in the Betslip header
        EXPECTED: - 'Quick Deposit' section is shown
        EXPECTED: - Numeric keyboard is not shown
        """
        self.get_betslip_content().quick_deposit_link.click()
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard is not hidden',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')
        self.assertTrue(self.betslip_content.has_deposit_form(), msg='There\'s no Quick deposit form!')

    def test_017_set_focus_over_stake_fields_amount_or_cvv_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Stake' fields/ 'Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: Keyboard is shown below 'Quick Deposit' section
        """
        self.test_004_set_focus_over_stake_field_amount_or_cvv_in_quick_deposit_section()

    def test_018_tap_on_quick_deposit_section_headerx_button_in_quick_deposit_section_quick_deposit_link_in_the_betslip_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header/'X' button in 'Quick Deposit' section/'Quick Deposit' link in the Betslip header
        EXPECTED: 'Quick Deposit' section disappears
        EXPECTED: Keyboard is no longer available
        """
        self.test_005_tap_on_quick_deposit_section_header()

    def test_019_enter_value_into_stake_field_that_exceeds_users_balance_without_losing_focus_from_stake_field(self):
        """
        DESCRIPTION: Enter value into 'Stake' field that exceeds user's balance (without losing focus from 'Stake' field)
        EXPECTED: 'Funds needed' message appears
        EXPECTED: Keyboard is displayed below collapsed 'Quick Deposit' section
        """
        balance = self.get_betslip_content().header.user_balance
        bet_amount = float(balance) + self.bet_amount
        self.test_006_enter_value_into_stake_field(bet_amount=bet_amount)

    def test_020_remove_entered_value_from_stake_field_without_losing_focus_from_stake_field(self):
        """
        DESCRIPTION: Remove entered value from 'Stake' field (without losing focus from 'Stake' field)
        EXPECTED: - Message 'Please deposit a min of #CURRENCY_VALUE.VALUE' disappears
        EXPECTED: Keyboard remains displayed
        """
        self.clear_input_using_keyboard()
        self.assertTrue(self.betslip_content.keyboard.is_displayed(name='Betslip keyboard shown'),
                        msg='Betslip keyboard is not shown')

        message_text = self.get_betslip_content().quick_deposit.warning_panel.text
        expected_message_text = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(message_text, expected_message_text,
                         msg=f'Message text is incorrect, expected "{expected_message_text}", found "{message_text}"')

    def test_021_add_several_selections_to_the_betslip_open_betslip(self):
        """
        DESCRIPTION: Add several selections to the Betslip > Open Betslip
        EXPECTED: Selections are available within Betslip
        EXPECTED: No 'Quick Deposit' section is available
        EXPECTED: No keyboard is displayed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])
        self.__class__.betslip_content = self.get_betslip_content()
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard is not hidden',
                                                                          timeout=3,
                                                                          expected_result=False),
                         msg='Betslip keyboard is not hidden')
        self.assertFalse(self.betslip_content.has_deposit_form(expected_result=False),
                         msg='There\'s Quick deposit form!')
        self.get_betslip_sections()
