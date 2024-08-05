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
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.mobile_only
@vtest
class Test_C16677803_Vanilla_Verify_Stake_field_when_QD_iFrame_is_opened(BaseBetSlipTest):
    """
    TR_ID: C16677803
    NAME: [Vanilla] Verify 'Stake' field when QD iFrame is opened.
    DESCRIPTION: This test case verifies that Quick Deposit iFrame closes when tapping on Stake field
    PRECONDITIONS: Login into Application
    """
    keep_browser_open = True
    stake_amount = 1
    events = {}
    number_of_events = 4
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def click_on_deposit(self):
        deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(deposit_button.is_enabled(), msg=f'"{deposit_button.name}" button is not enabled')
        self.assertEqual(deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')
        self.get_betslip_content().make_quick_deposit_button.click()
        self.site.wait_content_state_changed(timeout=30)
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='"Quick Deposit" section is not displayed')

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

    def test_000_preconditions(self):
        """
        DESCRIPTION: create events
        DESCRIPTION: Login into Application
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            self.events[self.eventID] = f'{event_params.team1} v {event_params.team2}'

            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_1 = event_params1.event_id
            self.events[self.eventID_1] = f'{event_params1.team1} v {event_params1.team2}'

            event_params2 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_2 = event_params2.event_id
            self.events[self.eventID_2] = f'{event_params2.team1} v {event_params2.team2}'

            event_params3 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_3 = event_params3.event_id
            self.events[self.eventID_3] = f'{event_params3.team1} v {event_params3.team2}'
            self.__class__.expected_betslip_counter_value += 4
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
            self.__class__.eventID = event1['event']['id']
            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=event1)
            self.__class__.expected_betslip_counter_value += 1

            # event 2
            self.__class__.eventID_1 = events[1]['event']['id']
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=events[1])
            self.__class__.expected_betslip_counter_value += 1

            self.__class__.eventID_2 = events[2]['event']['id']
            self.__class__.league3 = self.get_accordion_name_for_event_from_ss(event=events[2])
            self.__class__.expected_betslip_counter_value += 1

            self.__class__.eventID_3 = events[3]['event']['id']
            self.__class__.league4 = self.get_accordion_name_for_event_from_ss(event=events[3])
            self.__class__.expected_betslip_counter_value += 1

        self.__class__.username = tests.settings.quick_deposit_user
        self.site.login(username=self.username)

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Home')

    def test_002_add_1_sportraces_selection_to_the_betslip_click_on_add_to_the_betslip_button_on_quick_bet_pop_up_if_accessing_from_mobile(
            self):
        """
        DESCRIPTION: Add 1 <Sport>/<Races> selection to the betslip (click on 'Add to the Betslip' button on "Quick Bet" pop up if accessing from mobile)
        EXPECTED: Selection is added
        """
        self.site.open_sport(name='FOOTBALL')
        event = self.get_event_from_league(event_id=self.eventID,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event')
        self.__class__.selection_name, selection_price = list(output_prices.items())[0]
        selection_price.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(selection_price.is_selected(timeout=2),
                        msg=f'Bet button "{self.selection_name}" is not active after selection')

    def test_003_navigate_to_betslip_view_click_on_betslip_button_in_the_header_if_accessing_from_mobile(self):
        """
        DESCRIPTION: Navigate to Betslip view (click on 'Betslip' button in the header if accessing from mobile)
        EXPECTED: Betslip is opened, selection is displayed
        """

        self.site.open_betslip()
        section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(section.items())[0]
        self.assertTrue(section.items(), msg='*** No stakes found')
        self.assertTrue(self.stake, msg=f'"{self.selection_name}" stake was not found on the Betslip')

    def test_004_enter_value_higher_than_user_balance_in_stake_field(self):
        """
        DESCRIPTION: Enter value higher than user balance in 'Stake' field
        EXPECTED: 'Place Bet' button is changed to 'Make a Deposit'
        """
        try:
            user_balance = self.get_betslip_content().header.user_balance if self.site.wait_logged_in(
                login_criteria='betslip_balance', timeout=3) else 0
        except NotImplementedError as e:
            self._logger.warning(e)
            user_balance = self.get_balance_by_page('all')
        self.__class__.stake_value = user_balance + self.stake_amount
        self.stake.amount_form.input.click()
        self.__class__.keyboard = self.get_betslip_content().keyboard
        self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        self.keyboard.enter_amount_using_keyboard(value=self.stake_value)
        self.click_on_deposit()

    def test_005_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        # covered in step 4

    def test_006_tap_on_stake_textbox(self):
        """
        DESCRIPTION: Tap on 'Stake' textbox
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: 'Stake' textbox is editable
        """
        self.stake.amount_form.input.click()
        self.assertFalse(self.get_betslip_content().has_deposit_form(), msg='"Quick Deposit" section is displayed')
        self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        self.keyboard.enter_amount_using_keyboard(value=self.bet_amount)
        default_stake_value = self.stake.amount_form.input.value
        self.assertEqual(self.bet_amount, float(default_stake_value), msg='stake value is not editable')

    def test_007_close_betslip_viewadd_at_least_3_selections_from_different_event_to_the_bet_slip(self):
        """
        DESCRIPTION: Close Betslip view
        DESCRIPTION: Add at least 3 selections from different event to the Bet Slip
        EXPECTED: Selections are added
        """

        self.site.close_betslip()
        self.add_selection_betslip(event_id=self.eventID_1, section_name=self.league2)
        self.add_selection_betslip(event_id=self.eventID_2, section_name=self.league3)
        self.add_selection_betslip(event_id=self.eventID_3, section_name=self.league4)

    def test_008_navigate_to_betslip_viewenter_value_higher_than_user_balance_to_all_stake_textboxes_all_single_stakes_multiples_stakes_4_fold_acca_double_treble_yankee_lucky_flagtap_on_make_a_deposit_button(
            self):
        """
        DESCRIPTION: Navigate to Betslip view
        DESCRIPTION: Enter value higher than user balance to all 'Stake' textboxes (All Single Stakes; Multiples stakes: 4 Fold Acca, Double, Treble, Yankee, Lucky, Flag)
        DESCRIPTION: Tap on 'Make a Deposit' button
        EXPECTED: Betslip view is opened
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed
        """
        self.site.open_betslip()
        section = self.get_betslip_sections().Singles
        for stake in list(section.values()):
            stake.amount_form.input.click()
            self.__class__.keyboard = self.get_betslip_content().keyboard
            self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                            msg='Numeric keyboard is not shown')
            self.keyboard.enter_amount_using_keyboard(value=self.stake_value)
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        for stake in list(multiples_section.values()):
            stake.amount_form.input.click()
            self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                            msg='Numeric keyboard is not shown')
            self.keyboard.enter_amount_using_keyboard(value=self.stake_value)
        self.click_on_deposit()

    def test_009_tap_on_any_stake_textbox_in_multiple_sectionobserve_all_stake_textboxes(self):
        """
        DESCRIPTION: Tap on any 'Stake' textbox in Multiple section
        DESCRIPTION: Observe all 'Stake' textboxes
        EXPECTED: 'Quick Deposit' iFrame is closed
        EXPECTED: All 'Stake' textboxes are editable
        """
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        stake_name, stake = list(multiples_section.items())[0]
        stake.amount_form.input.click()
        self.assertTrue(self.keyboard.is_displayed(name='Numeric keyboard shown', timeout=5),
                        msg='Numeric keyboard is not shown')
        self.assertFalse(self.get_betslip_content().has_deposit_form(), msg='"Quick Deposit" section is displayed')
        for stake in list(multiples_section.values()):
            stake.amount_form.input.click()
            self.keyboard.enter_amount_using_keyboard(value=self.bet_amount)
            default_stake_value = stake.amount_form.input.value
            self.assertEqual(self.bet_amount, float(default_stake_value), msg='stake value is not editable')
        section = self.get_betslip_sections().Singles
        for stake in list(section.values()):
            stake.amount_form.input.click()
            self.keyboard.enter_amount_using_keyboard(value=self.bet_amount)
            default_stake_value = stake.amount_form.input.value
            self.assertEqual(self.bet_amount, float(default_stake_value), msg='stake value is not editable')
