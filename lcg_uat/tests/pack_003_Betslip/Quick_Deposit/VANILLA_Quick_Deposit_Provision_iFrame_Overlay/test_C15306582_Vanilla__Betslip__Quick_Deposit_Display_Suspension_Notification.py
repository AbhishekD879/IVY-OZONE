import pytest
import tests
import voltron.environments.constants as vec

from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can not create event in Prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.mobile_only
@pytest.mark.quick_deposit
@vtest
class Test_C15306582_Vanilla__Betslip__Quick_Deposit_Display_Suspension_Notification(BaseBetSlipTest):
    """
    TR_ID: C15306582
    NAME: [Vanilla] - Betslip - Quick Deposit: Display Suspension Notification
    DESCRIPTION: This test case verifies suspension notification above the Quick Deposit iframe on Betslip
    PRECONDITIONS: Link to backoffice tool for event suspension: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True
    addition = 5.00
    selection_name = ''

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()

        self.__class__.selection_id = self.event.selection_ids[self.event.team1]
        self.__class__.eventID = self.event.event_id
        self.__class__.selection_name = self.event.team1
        self.__class__.event_name = f'{self.event.team1} v {self.event.team2}'
        self.navigate_to_page("Homepage")
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.refresh_page()

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.login()
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_add_1_selection_to_the_betslip_click_on_add_to_the_betslip_button_on_quick_bet_pop_up_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Add 1 selection to the betslip (click on 'Add to the Betslip' button on "Quick Bet" pop up if accessing from mobile)
        EXPECTED: Selection is added
        """
        self.navigate_to_edp(event_id=self.event.event_id)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg=f'No one market section found on event: "{self.event_name}" EDP')
        market = markets.get(self.expected_market_sections.match_result)
        self.assertTrue(market,
                        msg=f'Market: "{self.expected_market_sections.match_result}" '
                            f'section not found in: {list(markets.keys())}')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes,
                        msg=f'No one outcome found in market: "{self.expected_market_sections.match_result}" section')
        team1 = self.event.team1.upper() if self.brand == 'ladbrokes' else self.event.team1
        self.assertIn(team1, outcomes, msg=f'"{team1}" is not displayed in markets')
        outcomes[team1].bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()

    def test_003_navigate_to_betslip_view_click_on_betslip_button_in_the_header_if_accessing_from_mobile(self):
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

    def test_004_enter_value_higher_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit' after increasing stake to higher than User balance
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of x.xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        self.__class__.bet_amount = self.user_balance + self.addition
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        actual_stake_amount = self.stake.amount_form.input.value
        actual_message = self.get_betslip_content().bet_amount_warning_message
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.addition)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" is not the same as expected "{expected_message}"')
        expected_stake_amount = '{0:.2f}'.format(self.bet_amount)
        self.assertEqual(actual_stake_amount, expected_stake_amount,
                         msg=f'Actual stake input amount: "{actual_stake_amount}", expected: "{expected_stake_amount}"')

        self.assertEqual(self.get_betslip_content().make_quick_deposit_button.name,
                         vec.Quickdeposit.MAKE_DEPOSIT_BUTTON_CAPTION,
                         msg=f'"{self.get_betslip_content().make_quick_deposit_button.name}" is no the same as '
                             f'expected "{vec.Quickdeposit.MAKE_DEPOSIT_BUTTON_CAPTION}"')

    def test_005_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed with available payment method set for User
        EXPECTED: 'Deposit&Place Bet' button is enabled
        """

        self.get_betslip_content().make_quick_deposit_button.click()
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

    def test_006_fill_in_cvv2_fieldtrigger_the_following_situation_in_backoffice_tool_for_this_eventeventstatuscodesand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Fill in CVV2 field
        DESCRIPTION: Trigger the following situation in Backoffice tool for this event:
        DESCRIPTION: eventStatusCode="S"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: For Coral - The event suspension message 'Please beware one of your selections have been suspended' is displayed above the Quick Deposit overlay header
        EXPECTED: For Ladbrokes - The event suspension message 'One of your selections has been suspended' is displayed in the top and disappears after few minutes
        EXPECTED: 'Deposit&Place Bet' button becomes disabled
        """
        self.quick_deposit.cvv_2.click()
        keyboard = self.quick_deposit.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv, delay=0.7)
        keyboard.enter_amount_using_keyboard(value='enter')
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_enabled(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
        self.quick_deposit.switch_to_main_page()
        self.site.betslip.quick_deposit.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        self.device.refresh_page()
        self.site.open_betslip()
        number_of_selections = 1
        expected_message = vec.betslip.SINGLE_DISABLED
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(len(singles_section) == number_of_selections, msg=f'Should be "{number_of_selections}" stakes '
                                                                          f'found but present "{len(singles_section)}"')
        for stake_name, stake in singles_section.items():
            self.assertTrue(stake.is_suspended(timeout=30), msg=f'Stake "{stake_name}" is not suspended')
            result = stake.amount_form.input.is_enabled(timeout=10, expected_result=False)
            self.assertFalse(result, msg=f'Amount field is not disabled for "{stake_name}"')

        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                         msg='Bet Now button is not disabled')
        betnow_error = self.get_betslip_content().wait_for_error()
        result = wait_for_result(
            lambda: betnow_error == expected_message,
            name='Betslip error to change',
            timeout=5)
        self.assertTrue(result, msg=f'Bet Now section warning "{betnow_error}"'
                                    f'is not the same as expected: "{expected_message}"')

    def test_007_make_the_event_active_againeventstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Make the event active again:
        DESCRIPTION: eventStatusCode="A"
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: For Coral - The event suspension message 'Please beware one of your selections have been suspended' disappears
        EXPECTED: 'Deposit&Place Bet' button becomes enabled
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.device.refresh_page()
        self.site.open_betslip()
        timeout: int = 40
        singles_section = self.get_betslip_sections().Singles
        for stake in list(singles_section.values()):
            self.assertFalse(stake.is_suspended(expected_result=False, timeout=timeout), msg=f'Stake is not active')
            self.assertTrue(stake.amount_form.input.is_enabled(expected_result=True, timeout=5),
                            msg=f'Stake amount input field for suspended event "{stake.event_name}" is not enabled')

        self.get_betslip_content().make_quick_deposit_button.click()
        self.assertTrue(self.get_betslip_content().has_deposit_form(),
                        msg='"Quick Deposit" section is not displayed')
        self.__class__.quick_deposit = self.site.betslip.quick_deposit.stick_to_iframe()
        self.quick_deposit.cvv_2.click()
        keyboard = self.quick_deposit.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv, delay=0.7)
        keyboard.enter_amount_using_keyboard(value='enter')
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_enabled(),
                        msg=f'"{vec.gvc.DEPOSIT_AND_PLACE_BTN}" button is not enabled')
