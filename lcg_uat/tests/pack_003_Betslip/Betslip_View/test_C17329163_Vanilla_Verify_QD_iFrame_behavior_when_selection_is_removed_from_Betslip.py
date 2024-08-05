import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from random import choice
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C17329163_Vanilla_Verify_QD_iFrame_behavior_when_selection_is_removed_from_Betslip(BaseBetSlipTest):
    """
    TR_ID: C17329163
    NAME: [Vanilla] Verify QD iFrame behavior when selection is removed from Betslip
    DESCRIPTION: This test case verifies the QD iFrame behavior when selection is removed from Betslip
    PRECONDITIONS: Login into Application (user should have positive balance)
    """
    keep_browser_open = True
    additional_amount = 5.0
    events = {}
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def add_selection_betslip(self, event_id, section_name):
        event = self.get_event_from_league(event_id=event_id,
                                           section_name=section_name)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event ')
        selection_name, selection_price = list(output_prices.items())[0]
        selection_price.click()
        self.assertTrue(selection_price.is_selected(timeout=2),
                        msg=f'Bet button "{selection_name}" is not active after selection')

    def click_on_deposit(self):
        deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(deposit_button.is_enabled(), msg=f'"{deposit_button.name}" button is not enabled')
        self.assertEqual(deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')
        self.get_betslip_content().make_quick_deposit_button.click()
        self.site.wait_content_state_changed(timeout=30)
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='"Quick Deposit" section is not displayed')

    def test_000_preconditions(self):
        """
        DESCRIPTION: create events
        DESCRIPTION: Login into Application
        """
        if tests.settings.backend_env != 'prod':
            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_1 = event_params1.event_id
            self.events[self.eventID_1] = f'{event_params1.team1} v {event_params1.team2}'

            event_params2 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_2 = event_params2.event_id
            self.events[self.eventID_2] = f'{event_params2.team1} v {event_params2.team2}'

            event_params3 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_3 = event_params3.event_id
            self.events[self.eventID_3] = f'{event_params3.team1} v {event_params3.team2}'
            self.__class__.expected_betslip_counter_value += 3
            actual_value = len(self.events.items())
            self.assertTrue(actual_value == self.expected_betslip_counter_value,
                            msg=f'Actual number of created events "{actual_value}" '
                                f'is not the same as expected "{self.expected_betslip_counter_value}"')
            self.__class__.league1 = self.__class__.league2 = self.__class__.league3 = self.__class__.league4 = tests.settings.football_autotest_league

        else:
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)
            if len(events) < 4:
                SiteServeException('Not enough event found')
            event1 = choice(events)
            events.remove(event1)
            self.__class__.eventID_1 = events[1]['event']['id']
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=events[1])
            self.__class__.expected_betslip_counter_value += 1

            self.__class__.eventID_2 = events[2]['event']['id']
            self.__class__.league3 = self.get_accordion_name_for_event_from_ss(event=events[2])
            self.__class__.expected_betslip_counter_value += 1

            self.__class__.eventID_3 = events[3]['event']['id']
            self.__class__.league4 = self.get_accordion_name_for_event_from_ss(event=events[3])
            self.__class__.expected_betslip_counter_value += 1
        self.site.login(username=tests.settings.quick_deposit_user)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_at_least_3_sportraces_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add at least 3 <Sport>/<Races> selection to the betslip
        EXPECTED: Selections are added
        """
        self.site.open_sport(name='FOOTBALL')
        self.add_selection_betslip(event_id=self.eventID_1, section_name=self.league2)
        if self.site.quick_bet_panel:
            self.site.quick_bet_panel.close()
        self.add_selection_betslip(event_id=self.eventID_2, section_name=self.league3)
        self.add_selection_betslip(event_id=self.eventID_3, section_name=self.league4)

    def test_002_navigate_to_betslip_view_click_on_betslip_button_in_the_header_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Navigate to Betslip view (click on 'Betslip' button in the header if accessing from mobile)
        EXPECTED: Betslip is opened, selections are displayed
        """
        self.site.open_betslip()
        section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(section.items())[0]
        stake_name2, self.__class__.stake2 = list(section.items())[1]
        stake_name3, self.__class__.stake3 = list(section.items())[2]
        self.assertTrue(section, msg='No selections found')

    def test_003_enter_value_higher_than_user_balance_in_stake_field_for_first_selection(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field for first selection
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit'
        """
        self.__class__.stake_value = self.user_balance + self.additional_amount
        self.stake.amount_form.input.click()
        keyboard = self.get_betslip_content().keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=self.stake_value)
        self.click_on_deposit()

    def test_004_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        # Covered in step 3

    def test_005_tap_on_close_button_for_first_selection_in_the_betslip(self):
        """
        DESCRIPTION: Tap on Close button for first selection in the Betslip
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: All 'Stake' textboxes are editable
        EXPECTED: Betslip view with disabled Place Bet button is displayed
        """
        self.stake.remove_button.click()
        self.assertFalse(self.get_betslip_content().has_deposit_form(timeout=10),
                         msg='"Quick Deposit" section is displayed')
        section = self.get_betslip_sections().Singles
        stake_name1, self.__class__.stake1 = list(section.items())[0]
        stake_name2, self.__class__.stake2 = list(section.items())[1]
        self.assertTrue(section, msg='No selections found')
        self.stake1.amount_form.input.click()
        self.__class__.keyboard = self.get_betslip_content().keyboard
        self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        self.keyboard.enter_amount_using_keyboard(value=self.bet_amount)
        default_stake_value = self.stake1.amount_form.input.value
        self.assertEqual(self.bet_amount, float(default_stake_value), msg='stake value is not editable')

    def test_006_enter_value_higher_than_user_balance_in_stake_field_for_first_selection_and_value_less_than_user_balance_in_stake_field_for_second_selection_in_the_betslip(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field for first selection and value less than user balance in 'Stake' field for second selection in the Betslip
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit'
        """
        self.clear_input_using_keyboard()
        self.keyboard.enter_amount_using_keyboard(value=self.stake_value)
        stake_value = self.user_balance - self.additional_amount
        self.stake2.amount_form.input.click()
        self.keyboard.enter_amount_using_keyboard(value=stake_value)
        self.click_on_deposit()

    def test_007_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        # Covered in step 6

    def test_008_tap_on_close_button_for_second_selection(self):
        """
        DESCRIPTION: Tap on Close button for second selection
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: All 'Stake' textboxes are editable
        EXPECTED: Betslip view with enabled Make a Deposit button is displayed
        """
        self.stake1.remove_button.click()
        self.assertFalse(self.get_betslip_content().has_deposit_form(timeout=10),
                         msg='"Quick Deposit" section is displayed')
        section = self.get_betslip_sections().Singles
        stake_name, stake = list(section.items())[0]
        self.assertTrue(section, msg='No selections found')
        stake.amount_form.input.click()
        keyboard = self.get_betslip_content().keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        self.clear_input_using_keyboard()
        keyboard.enter_amount_using_keyboard(value=self.bet_amount)
        default_stake_value = stake.amount_form.input.value
        self.assertEqual(self.bet_amount, float(default_stake_value), msg='stake value is not editable')
