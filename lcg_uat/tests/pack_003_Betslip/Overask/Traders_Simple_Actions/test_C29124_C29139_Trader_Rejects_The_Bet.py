import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import perform_offset_mouse_click


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.login
@vtest
class Test_C29124_C29139_Trader_rejects_the_Bet(BaseBetSlipTest):
    """
    TR_ID: C29124
    TR_ID: C29139
    NAME: Reject a Bet
    DESCRIPTION: This test case verifies rejecting of a bet by a trader triggered by overask functionality
    """
    keep_browser_open = True
    max_bet = 3
    max_mult_bet = 6

    def test_000_preconditions(self):
        """
        DESCRIPTION: - User is logged in to application
        """
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=1, max_bet=self.max_bet,
                                                           max_mult_bet=self.max_mult_bet)
        self.__class__.eventID, self.__class__.selection_ids = event_params1.event_id, event_params1.selection_ids
        prices = {0: '1/12'}

        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=prices, max_bet=self.max_bet,
                                                           max_mult_bet=self.max_mult_bet)
        self.__class__.eventID2, self.__class__.selection_ids_2 = event_params2.event_id, event_params2.selection_ids
        prices2 = {0: '1/19'}

        event_params3 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=prices2, max_bet=self.max_bet,
                                                           max_mult_bet=self.max_mult_bet)
        self.__class__.eventID3, self.__class__.selection_ids_3 = event_params3.event_id, event_params3.selection_ids

        self.__class__.selection_name, self.__class__.selection_id = list(self.selection_ids.items())[0]
        self.__class__.selection2_name, self.__class__.selection2_id = list(self.selection_ids_2.items())[0]
        self.__class__.selection3_name, self.__class__.selection3_id = list(self.selection_ids_3.items())[0]

        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_selection_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add selection and go Betslip, 'Singles' section
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection(self, single=True):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button/ 'Place bet' (From OX 99) button
        EXPECTED: The bet is sent to Openbet system for review
        """
        if single:
            self.__class__.bet_amount = self.max_bet + 1
            self.place_single_bet()
        else:
            self.__class__.bet_amount = self.max_mult_bet + 1
            self.place_multiple_bet(number_of_stakes=2)
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask excedds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed()
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

        self.get_betslip_content().overask.overask_title.click()
        perform_offset_mouse_click()
        has_overask_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(has_overask_message, msg='Overask message closed after click on background')

    def test_004_trigger_rejecting_the_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger rejecting the bet by a trader in OpenBet system
        EXPECTED: *   The bet is rejected in OpenBet
        EXPECTED: *   Confirmation and the reason of rejecting are sent and received in Oxygen app
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.decline_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)

    def test_005_verify_betslip(self, single=True):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Bet is not placed and a 'This bet has not been accepted by traders!' message is shown
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Go betting' button is present
        EXPECTED: * Balance is not reduced
        EXPECTED: ![](index.php?/attachments/get/33805) ![](index.php?/attachments/get/33804)
        """
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        _, section = list(betreceipt_sections.items())[0]
        if single:
            overask_warning_message = section.declined_bet.stake_content.stake_message
        else:
            overask_warning_message = section.multiple_declined_bet.stake_message

        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

        self.verify_user_balance(expected_user_balance=self.user_balance)
        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(),
                        msg='"Go betting" button isn\'t present')

    def test_006_click__tap_continue_go_betting_from_ox_99_button(self):
        """
        DESCRIPTION: Click / tap 'Continue'/ 'Go betting' (From OX 99) button
        EXPECTED: *   Betslip is cleared automatically
        EXPECTED: *   'You have no selections in the slip' message is shown (tablet, desktop)
        EXPECTED: *   Betslip is closed automatically (mobile)
        """
        self.site.bet_receipt.footer.done_button.click()

        if self.is_mobile:
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Bet Slip is not closed')
        else:
            actual_message = self.get_betslip_content().no_selections_title
            self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Actual title message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

            if self.brand != 'ladbrokes':
                no_selections = self.get_betslip_content().no_selections_message
                self.assertEqual(no_selections, vec.betslip.NO_SELECTIONS_MSG,
                                 msg=f'Actual body message "{no_selections}" != Expected {vec.betslip.NO_SELECTIONS_MSG}')

    def test_007_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection2_id, self.selection3_id))

    def test_008_repeat_steps__2_6_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps № 2-6 for Multiple bet
        """
        self.test_002_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection(single=False)
        self.test_003_verify_betslip()
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID3)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.decline_bet(event_id=self.eventID3, bet_id=bet_id, betslip_id=betslip_id)

        self.test_005_verify_betslip(single=False)
        self.test_006_click__tap_continue_go_betting_from_ox_99_button()
