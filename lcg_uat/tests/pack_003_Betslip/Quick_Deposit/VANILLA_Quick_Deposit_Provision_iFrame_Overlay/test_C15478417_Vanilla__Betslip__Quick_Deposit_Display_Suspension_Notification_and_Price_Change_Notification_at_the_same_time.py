import pytest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import switch_to_main_page


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can not create event in Prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.quick_deposit
@pytest.mark.mobile_only
@vtest
class Test_C15478417_Vanilla__Betslip__Quick_Deposit_Display_Suspension_Notification_and_Price_Change_Notification_at_the_same_time(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C15478417
    NAME: [Vanilla] - Betslip - Quick Deposit: Display Suspension Notification and Price Change Notification at the same time
    DESCRIPTION: This test case verifies Suspension Notification and Price Change Notification triggered at the same time on Betslip
    PRECONDITIONS: Link to backoffice tool for price change/event suspension: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User balance is more than 0
    """
    keep_browser_open = True
    addition = 5.00
    selection_name = ''
    old_price = '1/2'
    new_price_increased = '999/7'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        event = self.ob_config.add_autotest_premier_league_football_event(price=self.old_price)
        self.__class__.selection_id = event.selection_ids[event.team1]
        self.__class__.selection_name = self.event.team1
        self.__class__.event_name = f'{self.event.team1} v {self.event.team2}'
        self.navigate_to_page("Homepage")
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.refresh_page()
        self.site.login()
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_1_selection_to_the_betslip_click_on_add_to_the_betslip_button_on_quick_bet_pop_up_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Add 1 selection to the betslip (click on 'Add to the Betslip' button on "Quick Bet" pop up if accessing from mobile)
        EXPECTED: Selection is added
        """
        self.navigate_to_edp(event_id=self.event.event_id)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg=f'No one market section found on event: "{self.event_name}" EDP')
        if self.brand == 'bma':
            expected_section = self.expected_market_sections.match_result
        else:
            expected_section = "Match Result"

        market = markets.get(expected_section)
        self.assertTrue(market,
                        msg=f'Market: "{expected_section}" '
                            f'section not found in: {list(markets.keys())}')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes,
                        msg=f'No one outcome found in market: "{expected_section}" section')
        team1 = self.event.team1.upper() if self.brand == 'ladbrokes' else self.event.team1
        self.assertIn(team1, outcomes, msg=f'"{team1}" is not displayed in markets')
        outcomes[team1].bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()

    def test_002_navigate_to_betslip_view_click_on_betslip_button_in_the_header_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Navigate to Betslip view (click on 'Betslip' button in the header if accessing from mobile)
        EXPECTED: Betslip is opened, selection is displayed
        """
        self.site.header.bet_slip_counter.click()
        self.assertTrue(self.get_betslip_content(),
                        msg='Betslip widget was not opened')
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No one added selection found on Betslip')
        self.__class__.stake = singles_section.get(self.selection_name)
        self.assertTrue(self.stake, msg=f'"{self.selection_name}" stake was not found on the Betslip')

    def test_003_enter_value_higher_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit' after increasing stake to higher than User balance
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        bet_amount = self.user_balance + self.addition
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        actual_stake_amount = self.stake.amount_form.input.value
        actual_message = self.get_betslip_content().bet_amount_warning_message
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.addition)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" is not the same as expected "{expected_message}"')
        expected_stake_amount = '{0:.2f}'.format(bet_amount)
        self.assertEqual(actual_stake_amount, expected_stake_amount,
                         msg=f'Actual stake input amount: "{actual_stake_amount}", expected: "{expected_stake_amount}"')
        self.assertEqual(self.get_betslip_content().make_quick_deposit_button.name,
                         vec.Quickdeposit.MAKE_DEPOSIT_BUTTON_CAPTION,
                         msg=f'"{self.get_betslip_content().make_quick_deposit_button.name}" is no the same as '
                             f'expected "{vec.Quickdeposit.MAKE_DEPOSIT_BUTTON_CAPTION}"')

    def test_004_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed with available payment method set for User
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        self.assertTrue(self.get_betslip_content().quick_deposit.is_displayed(timeout=30),
                        msg='"Quick Deposit" section is not shown')
        self.assertTrue(self.get_betslip_content().has_deposit_form(),
                        msg='"Quick Deposit" section is not displayed')
        self.__class__.quick_deposit = self.site.betslip.quick_deposit.stick_to_iframe()
        actual_name = self.quick_deposit.deposit_and_place_bet_button
        self.assertEqual(actual_name.name, vec.gvc.DEPOSIT_AND_PLACE_BTN,
                         msg=f'Actual button name "{actual_name}" != Expected "{vec.gvc.DEPOSIT_AND_PLACE_BTN}"')
        warning_message = self.quick_deposit.warning_panel
        expected_warning_message = \
            vec.gvc.FUNDS_NEEDED_FOR_BET.format(self.addition)
        self.assertEqual(warning_message, expected_warning_message,
                         msg=f'Incorrect warning message. \nActual:\n[{warning_message}]\nExpected:\n[{expected_warning_message}]')
        self.assertFalse(self.quick_deposit.is_enabled(expected_result=False),
                         msg=f'{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is enabled')

    def test_005_change_price_for_the_selection_and_suspend_eventstatuscodes_it_in_backoffice_tool(self):
        """
        DESCRIPTION: Change price for the selection and suspend (eventStatusCode="S") it in Backoffice tool
        EXPECTED: Changes are saved
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price_increased)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_id,
                                                                 price=self.new_price_increased)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{self.selection_id}" is not received')
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)

    def test_006_observe_the_quick_deposit_iframe(self):
        """
        DESCRIPTION: Observe the Quick Deposit iFrame
        EXPECTED: For Coral - The event suspension message 'Please beware one of your selections have been suspended' is displayed above the Quick Deposit overlay header
        EXPECTED: For Ladbrokes - The event suspension message 'One of your selections has been suspended' is displayed in the top and disappears after few minutes
        """
        switch_to_main_page()
        self.assertTrue(self.get_betslip_content().quick_deposit.close_button.is_enabled(),
                        msg='Quick deposit panel close button is not enabled.')
        self.get_betslip_content().quick_deposit.close_button.click()
        betnow_error = self.get_betslip_content().wait_for_error()
        result = wait_for_result(
            lambda: betnow_error == vec.betslip.SINGLE_DISABLED,
            name='Betslip error to change',
            timeout=5)
        self.assertTrue(result, msg=f'Bet Now section warning "{betnow_error}"'
                                    f'is not the same as expected: "{vec.betslip.SINGLE_DISABLED}"')

    def test_007_make_the_event_active_againeventstatuscodea_in_backoffice_tool_and_observe_the_quick_deposit_iframe(self):
        """
        DESCRIPTION: Make the event active again
        DESCRIPTION: (eventStatusCode="A") in Backoffice tool and observe the Quick Deposit iFrame
        EXPECTED: The event suspension message disappears
        EXPECTED: For Coral - 'Some of your prices have changed!' message is displayed above the selection
        EXPECTED: For Ladbrokes - 'Price Changed from * to *' message is displayed above the selection
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)
        general_error_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(general_error_msg, vec.betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Actual error message: "{general_error_msg}" '
                             f'is not equal to expected: "{vec.betslip.PRICE_CHANGE_BANNER_MSG}"')
        expected_message = vec.quickbet.PRICE_IS_CHANGED.format(old=self.old_price, new=self.new_price_increased)
        singles_sections = self.get_betslip_sections().Singles
        actual_message = list(singles_sections.values())[0].error_message
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual messasge "{actual_message}" != expected "{expected_message}"')
