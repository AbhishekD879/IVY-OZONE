import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@vtest
class Test_C14876363_Vanilla__Quick_Bet__GVC_iFrame_appearance(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C14876363
    NAME: [Vanilla] - Quick Bet - GVC iFrame appearance
    DESCRIPTION: This test case verifies the appearance of GVC iFrame
    PRECONDITIONS: User balance is more than 0
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True
    additional_amount = 5.0

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create test event, PROD: Find active events
        DESCRIPTION: Log in with a user that has a positive balance
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        self.__class__.event_id = event['event']['id']
        self.__class__.event_name = normalize_name(event['event']['name'])
        self.__class__.league = self.get_accordion_name_for_event_from_ss(event=event)
        outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                        market['market'].get('children')), None)
        self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') and
                                     outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
        if not self.team1:
            raise SiteServeException('No Home team found')

        self._logger.info(f'*** Found Football event with name: "{self.event_name}" and id: "{self.event_id}"')
        self.site.login(username=tests.settings.quick_deposit_user)
        self.site.wait_content_state('homepage')
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: Selected price/odds are highlighted in green
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        sport_name = vec.sb.FOOTBALL.title()
        self.site.open_sport(name=sport_name)
        self.site.wait_content_state(state_name=sport_name)

        event = self.get_event_from_league(event_id=self.event_id,
                                           section_name=self.league)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices, msg=f'Could not find output prices for event "{self.event_name}"')

        bet_button = output_prices.get(self.team1)
        self.assertTrue(bet_button, msg=f'Bet button for "{self.team1}" was not found')
        bet_button.click()
        self.assertTrue(bet_button.is_selected(), msg='Outcome button is not highlighted in green')
        self.assertEqual(bet_button.background_color_value, vec.colors.SELECTED_BET_BUTTON_COLOR,
                         msg=f'Selected price/odds for "{bet_button}" is not highlighted in green {vec.colors.SELECTED_BET_BUTTON_COLOR}')
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.assertEqual(self.quick_bet.header.title, vec.quickbet.QUICKBET_TITLE,
                         msg=f'Actual title "{self.quick_bet.header.title}" does not match expected "{vec.quickbet.QUICKBET_TITLE}"')

    def test_002_enter_value_less_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Enter value less than user balance in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        EXPECTED: 'Place Bet' button becomes enabled
        """
        self.quick_bet.selection.content.amount_form.input.click()
        self.quick_bet.selection.content.amount_form.enter_amount(value=self.bet_amount)
        actual_stake = self.quick_bet.selection.bet_summary.total_stake
        self.assertEqual(actual_stake, f'{self.bet_amount:.2f}',
                         msg=f'Actual "Total Stake" value "{actual_stake}" != Expected "{self.bet_amount:.2f}"')
        self.assertTrue(self.quick_bet.place_bet.is_enabled(), msg='The button "Place bet" is not active')

    def test_003_change_value_in_stake_field_for_value_higher_than_user_balance(self):
        """
        DESCRIPTION: Change value in 'Stake' field for value higher than user balance
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit' after increasing stake to higher than User balance
        EXPECTED: A warning message is displayed above 'Total Stake':
        EXPECTED: "Please deposit a min of .xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        stake_value = self.user_balance + self.additional_amount
        self.quick_bet.selection.content.amount_form.input.clear()
        self.quick_bet.selection.content.amount_form.input.click()
        self.quick_bet.selection.content.amount_form.enter_amount(value=stake_value)

        self.__class__.expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        if self.brand == 'ladbrokes':
            actual_message = self.quick_bet.bet_amount_warning_message
            self.assertEqual(actual_message, self.expected_message,
                             msg=f'Actual message: "{actual_message}" does not match expected: "{self.expected_message}"')
        else:
            actual_message = self.quick_bet.info_panels_text
            self.assertTrue(actual_message, msg='Quick Bet deposit notification is not found')
            self.assertIn(self.expected_message, actual_message,
                          msg=f'Actual message: "{self.expected_message}" is not in expected: "{actual_message}"')

        self.__class__.make_deposit_button = self.quick_bet.make_quick_deposit_button
        self.assertTrue(self.make_deposit_button.is_enabled(),
                        msg=f'"{self.make_deposit_button.name}" button is not enabled')
        self.assertEqual(self.make_deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{self.make_deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_004_tap_on_make_a_deposit_buttonobserve_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        DESCRIPTION: Observe 'Make a Deposit' button
        EXPECTED: Spinner and 'Make a Deposit' text is displayed on the 'Make a Quick Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay appears with available payment method set for User
        """
        self.make_deposit_button.click()
        self.assertTrue(self.quick_bet.wait_for_quick_deposit_panel(timeout=20),
                        msg=f'"Quick Deposit" panel is not displayed')

    def test_005_observe_the_header_of_iframe_overlay(self):
        """
        DESCRIPTION: Observe the header of iFrame overlay
        EXPECTED: The label 'Quick Deposit' is displayed on the iFrame header
        EXPECTED: Close (X) button is displayed on the right top corner on the iFrame header
        """
        # used sleep due to Quick deposit panel is taking time to load properly
        sleep(10)
        self.__class__.quick_deposit = self.quick_bet.quick_deposit_panel
        text = self.quick_deposit.header.title
        self.assertTrue(text,
                        msg=f'Quick deposit panel label Quick Deposit is not displayed')
        self.assertEqual(text, vec.bma.DEPOSIT_NOTIFICATION_TITLE,
                         msg=f'Actual button name: "{text}" '
                             f'is not as expected: "{vec.bma.DEPOSIT_NOTIFICATION_TITLE}"')
        self.assertTrue(self.quick_deposit.close_button,
                        msg=f'Quick deposit panel close button is not enabled.')

    def test_006_tap_close_x_button(self):
        """
        DESCRIPTION: Tap close (X) button
        EXPECTED: The Quick Deposit overlay is closed
        EXPECTED: User returns to the Quick Bet overlay
        """
        self.quick_deposit.close_button.click()
        self.site.wait_content_state_changed(timeout=15)
        self.assertFalse(self.quick_bet.wait_for_quick_deposit_panel(),
                         msg=f'"Quick Deposit" panel is displayed')
        self.assertTrue(self.quick_bet.header.close_button,
                        msg=f'Quick bet panel close button is not enabled.')
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')

    def test_007_observe_the_warning_message(self):
        """
        DESCRIPTION: Observe the warning message
        EXPECTED: The warning message "Please deposit a min of .xx to continue placing your bet", where x.xx is the difference between Stake and actual Balance Account
        """
        if self.brand == 'ladbrokes':
            actual_message = self.quick_bet.bet_amount_warning_message
            self.assertEqual(actual_message, self.expected_message,
                             msg=f'Actual message: "{actual_message}" does not match expected: "{self.expected_message}"')
        else:
            actual_message = self.quick_bet.info_panels_text
            self.assertTrue(actual_message, msg='Quick Bet deposit notification is not found')
            self.assertIn(self.expected_message, actual_message,
                          msg=f'Actual message: "{self.expected_message}" is not in expected: "{actual_message}"')
