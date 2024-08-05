import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Overask cannot be triggered in prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C29125_Reject_One_Bet_Out_of_Several_Selections(BaseBetSlipTest):
    """
    TR_ID: C29125
    NAME: Reject One Bet Out of Several Selections
    DESCRIPTION: This test case verifies rejecting of one bet out of several selections by a trader triggered by overask functionality
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    PRECONDITIONS: 4. Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
    PRECONDITIONS: 5. Initial Data' checkbox is present within 'Overask' config and unchecked by default
    PRECONDITIONS: 6. The Initial response of the config contains 'The initialDataConfig: false'
    PRECONDITIONS: 7. The Initial Data response on homepage is absent
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Overask:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: ![](index.php?/attachments/get/109045765)
    """
    keep_browser_open = True
    selection_ids = []
    event_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Create events
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        self.__class__.max_mult_bet = self.max_bet + 0.1
        for i in range(0, 3):
            event_params = self.ob_config.add_UK_racing_event(
                max_bet=self.max_bet,
                max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.__class__.expected_user_balance = self.site.header.user_balance

    def test_002_add_a_few_selections_and_go_betslip(self):
        """
        DESCRIPTION: Add a few selections and go Betslip
        EXPECTED: The selections are added to betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_ids[0], self.selection_ids[1], self.selection_ids[2]])

    def test_003_enter_value_in_stake_fields_that_does_not_exceed_max_allowed_bet_limitfor_one_of_added_selections(self, bet_type='Single'):
        """
        DESCRIPTION: Enter value in 'Stake' fields that does not exceed max allowed bet limit for one of added selections
        EXPECTED: 'Stake' field is populated with value
        """
        if bet_type == 'Single':
            self.__class__.section = self.get_betslip_sections().Singles
        else:
            self.__class__.section = self.get_betslip_sections(multiples=True).Multiples

        self.assertTrue(self.section.items(), msg='*** No stakes found')

        stake_name1, stake1 = list(self.section.items())[0]
        if bet_type == 'Single':
            stake_bet_amounts1 = {stake_name1: self.max_bet - 0.01}
        else:
            stake_bet_amounts1 = {stake_name1: self.max_mult_bet - 0.01}
        self.enter_stake_amount(stake=(stake_name1, stake1), stake_bet_amounts=stake_bet_amounts1)

    def test_004_leave_at_least_one_stake_field_empty(self):
        """
        DESCRIPTION: Leave at least one 'Stake' field empty
        EXPECTED: 'Stake' field is empty
        """
        # covered in step 3

    def test_005_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button_place_bet_from_ox_99_button(self, bet_type='Single'):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for one of added selections and click / tap 'Bet Now' button/ 'Place bet' (From OX 99) button
        EXPECTED: The bet is sent to Openbet system for review
        """
        stake_name3, stake3 = list(self.section.items())[2]
        if bet_type == 'Single':
            stake_bet_amounts3 = {stake_name3: self.max_bet + 0.01}
        else:
            stake_bet_amounts3 = {stake_name3: self.max_mult_bet + 0.01}
        self.enter_stake_amount(stake=(stake_name3, stake3), stake_bet_amounts=stake_bet_amounts3)
        sleep(3)
        self.get_betslip_content().bet_now_button.click()

    def test_006_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask excedds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed()
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

        has_overask_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(has_overask_message, msg='Overask message closed after click on background')

    def test_007_trigger_rejecting_the_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger rejecting the bet by a trader in OpenBet system
        EXPECTED: *   The bet is rejected in OpenBet
        EXPECTED: *   Confirmation is sent and received in Oxygen app
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.event_ids[2])
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.decline_bet(event_id=self.event_ids[2], bet_id=bet_id, betslip_id=betslip_id)

    def test_008_verify_betslip(self, bet_type='Single'):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * Auto-accepted bet is placed and Bet Receipt is displayed
        EXPECTED: * Rejected bet is not placed and a 'This bet has not been accepted by traders!' message is shown
        EXPECTED: * Bet with empty 'Stake' field is ignored and not placed
        EXPECTED: * 'Go betting' button is present ('Reuse Selections' button is absent)
        EXPECTED: * Balance is reduced accordingly
        EXPECTED: * Auto-accepted bet is listed in 'Bet History' and 'My Account' pages
        EXPECTED: ![](index.php?/attachments/get/33996) ![](index.php?/attachments/get/33997)
        """
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(),
                        msg='"Go betting" button isn\'t present')

        self.assertFalse(self.site.bet_receipt.footer.has_reuse_selections_button(expected_result=False),
                         msg='"Re-use selection" button isn\'t disabled')
        if bet_type == 'Single':
            self.__class__.expected_user_balance = self.expected_user_balance - (self.max_bet - 0.01)
        else:
            self.__class__.expected_user_balance = self.expected_user_balance - (self.max_mult_bet - 0.01)
        self.verify_user_balance(expected_user_balance=self.expected_user_balance)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        if bet_type == 'Single':
            _, section = list(betreceipt_sections.items())[0]
            overask_warning_message = section.declined_bet.stake_content.stake_message
        else:
            _, section = list(betreceipt_sections.items())[1]
            overask_warning_message = section.multiple_declined_bet.stake_message

        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

    def test_009_click__tap_continue_go_betting_from_ox_99_button(self):
        """
        DESCRIPTION: Click / tap 'Continue'/ 'Go betting' (From OX 99) button
        EXPECTED: * Betslip is cleared automatically
        EXPECTED: * 'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: * Betslip is closed automatically (mobile)
        """
        self.site.bet_receipt.footer.done_button.click()
        if self.device_type == 'desktop':
            self.device.refresh_page()
            betslip = self.get_betslip_content()
            no_selections_title = betslip.no_selections_title
            self.assertTrue(no_selections_title, msg=f'"{vec.betslip.NO_SELECTIONS_TITLE}" title is not shown')
            self.assertEqual(no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Title "{no_selections_title}" is not as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
        else:
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Bet Slip is not closed')

        self.__class__.expected_user_balance = self.site.header.user_balance

    def test_010_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        """
        self.test_002_add_a_few_selections_and_go_betslip()

    def test_011_repeat_steps_2_9_but_on_step_5_enter_max_value_in_stake_field_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #2-9 but on step #5 enter max value in 'Stake' field for Multiple bet
        """
        self.test_003_enter_value_in_stake_fields_that_does_not_exceed_max_allowed_bet_limitfor_one_of_added_selections(
            bet_type='Double')
        self.test_005_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button_place_bet_from_ox_99_button(
            bet_type='Double')
        self.test_006_verify_betslip()
        self.test_007_trigger_rejecting_the_bet_by_a_trader_in_openbet_system()
        self.test_008_verify_betslip(bet_type='Double')
        self.test_009_click__tap_continue_go_betting_from_ox_99_button()

    def test_012_add_a_few_selections_from_the_same_race_event_and_go_betslip_forecaststricasts_section(self):
        """
        DESCRIPTION: Add a few selections from the same <Race> event and go Betslip, 'Forecasts/Tricasts' section
        """
        self.selection_ids.clear()
        self.event_ids.clear()
        for i in range(3):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=4, forecast=True,
                                                              max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

    def test_013_repeat_steps_2_9_but_on_step_5_enter_max_value_in_stake_field_for_forecaststricasts_bet(self):
        """
        DESCRIPTION: Repeat steps #2-9 but on step #5 enter max value in 'Stake' field for Forecasts/Tricasts bet
        """
        self.test_002_add_a_few_selections_and_go_betslip()
        self.test_003_enter_value_in_stake_fields_that_does_not_exceed_max_allowed_bet_limitfor_one_of_added_selections()
        self.test_005_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_one_of_added_selections_and_click__tap_bet_now_button_place_bet_from_ox_99_button()
        self.test_006_verify_betslip()
        self.test_007_trigger_rejecting_the_bet_by_a_trader_in_openbet_system()
        self.test_008_verify_betslip()
        self.test_009_click__tap_continue_go_betting_from_ox_99_button()
