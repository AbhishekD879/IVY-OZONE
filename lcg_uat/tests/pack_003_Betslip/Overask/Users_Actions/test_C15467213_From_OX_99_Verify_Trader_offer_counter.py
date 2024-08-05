import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.trader_timeout
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C15467213_From_OX_99_Verify_Trader_offer_counter(BaseBetSlipTest):
    """
    TR_ID: C15467213
    NAME: [From OX 99] Verify Trader offer counter
    DESCRIPTION: This test case verifies Offer expires counter
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is more that allowed Max stake value
    PRECONDITIONS: ![](index.php?/attachments/get/31369)
    PRECONDITIONS: ![](index.php?/attachments/get/31370)
    """
    keep_browser_open = True
    selection_ids = []
    event_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'

    def test_001_add_selection_and_go_to_betslip(self, sel_id=None):
        """
        DESCRIPTION: Add selection and go to Betslip
        """
        if not sel_id:
            sel_id = self.selection_ids[0]
        self.open_betslip_with_selections(selection_ids=sel_id)

    def test_002_enter_a_value_in_stake_field_that_exceeds_max_allowed_bet_limit_for_particular_selection_and_clicktap_place_bet_button(
            self):
        """
        DESCRIPTION: Enter a value in 'Stake' field that exceeds max allowed bet limit for particular selection and click/tap 'Place bet' button
        EXPECTED: * The bet is sent to Openbet system for review
        """
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet(number_of_stakes=1)

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * Overask overlay appears
        """
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self, event_id=None):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: * Confirmation is sent and received in Oxygen app
        """
        if not event_id:
            event_id = self.event_ids[0]
        try:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, offer_timeout=30)
            account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(
                username=self.username,
                event_id=event_id)
            self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                           betslip_id=betslip_id, max_bet=self.max_bet,
                                           price_type='S')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_005_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Selection with the maximum bet offer is expanded
        EXPECTED: *   The maximum bet offer for selected on step #2 bet and [X] remove button is shown to the user
        EXPECTED: *   Message 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' appears on the grey background above the selection
        EXPECTED: *   **Expire counter appears**
        EXPECTED: * **readBet** response **offerExpiresAt: “timestamp”** **where timestamp** is **“2019-07-08T13:16:55.000+01:00” e.g** date when the offer is expired
        EXPECTED: *   'Place Bet  and 'Cancel' buttons are present
        EXPECTED: *   'Place Bet  and 'Cancel' buttons are enabled
        EXPECTED: ![](index.php?/attachments/get/31372)
        """
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

        sections = self.get_betslip_sections().Singles
        stake_name, stake = list(sections.items())[0]
        self.assertTrue(stake.remove_button.is_displayed(),
                        msg=f'Remove button was not found for stake "{stake_name}"')
        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

        betslip_section = self.get_betslip_content()
        est_returns = betslip_section.total_estimate_returns
        self.assertEqual(est_returns, 'N/A', msg='Est returns is not equal "N/A"')

    def test_006_close_betslip_by_close_button_x(self):
        """
        DESCRIPTION: Close betslip by close button [X]
        EXPECTED: Betslip is closed
        """
        self.site.close_betslip()
        self.site.wait_content_state('Homepage')

    def test_007_open_betslip_again(self):
        """
        DESCRIPTION: Open betslip again
        EXPECTED: * Betslip is opened
        EXPECTED: * Selection is displayed
        EXPECTED: * Counter displayed correctly
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.assertEqual(len(singles_section.items()), self.expected_betslip_counter_value,
                         msg='Both selections should be present in betslip')

    def test_008_wait_for_the_counter_is_ended_000(self):
        """
        DESCRIPTION: Wait for the counter is ended (0:00)
        EXPECTED: The trader offer is expired, betslip is changed to (look at the design for Coral and Ladbrokes):
        EXPECTED: *   'Place Bet' button is present
        EXPECTED: *   'Place Bet' button is disabled
        EXPECTED: *  For Ladbrokes  **Your offer has expired** text appears on the top and on the bottom.
        EXPECTED: *  For Coral - **Your offer has expired** text appears only on the bottom.
        EXPECTED: ![](index.php?/attachments/get/31381)
        EXPECTED: ![](index.php?/attachments/get/31383)
        """
        self.site.wait_content_state_changed(timeout=32)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')
        overask_message = self.get_betslip_content().wait_for_overask_message_to_change(timeout=15)
        self.assertTrue(overask_message, msg='Overask Offer timeout message is not triggered for the User')
        overask_offer_timeout_message = self.get_betslip_content().overask_warning
        self.assertEqual(overask_offer_timeout_message, vec.betslip.OVERASK_MESSAGES.customer_action_time_expired,
                         msg=f'Actual message "{overask_offer_timeout_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.customer_action_time_expired}"')
        self.assertTrue(self.get_betslip_content().has_bet_now_button(),
                        msg='"Place Bet" button is not present"')
        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(),
                         msg='"Place Bet" button is enabled')
        self.clear_betslip()

    def test_009_repeat_steps_1_7(self):
        """
        DESCRIPTION: Repeat steps 1-7
        """
        self.test_001_add_selection_and_go_to_betslip(sel_id=self.selection_ids[1])
        self.test_002_enter_a_value_in_stake_field_that_exceeds_max_allowed_bet_limit_for_particular_selection_and_clicktap_place_bet_button()
        self.test_003_verify_betslip()
        self.test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(event_id=self.event_ids[1])
        self.test_005_verify_betslip()
        self.test_006_close_betslip_by_close_button_x()
        self.test_007_open_betslip_again()

    def test_010_tap_place_bet_button_to_accept_traders_offer(self):
        """
        DESCRIPTION: Tap "Place bet" button to accept Trader's offer
        EXPECTED: * Accepted bet is successfully placed
        EXPECTED: * Bet receipt is displayed
        """
        confirm_btn = self.get_betslip_content().confirm_overask_offer_button
        confirm_btn.click()
        self.check_bet_receipt_is_displayed()
