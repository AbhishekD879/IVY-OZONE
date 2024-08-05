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
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.login
@vtest
class Test_C29127_Offer_the_Max_Bet_User_Accepts(BaseBetSlipTest):
    """
    TR_ID: C29127
    NAME: Offer the Max Bet
    DESCRIPTION: This test case verifies offering the maximum bet by a trader triggered by overask functionality
    """
    keep_browser_open = True
    username = None
    max_bet = 0.03
    max_mult_bet = 0.05

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in
        """
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False
        event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=1, max_bet=self.max_bet,
                                                           max_mult_bet=self.max_mult_bet)
        self.__class__.eventID, self.__class__.selection_ids = event_params1.event_id, event_params1.selection_ids

        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '1/12'},
                                                           max_bet=self.max_bet,
                                                           max_mult_bet=self.max_mult_bet, sp=True)
        self.__class__.selection_ids_2 = event_params2.selection_ids

        event_params3 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '1/19'},
                                                           max_bet=self.max_bet,
                                                           max_mult_bet=self.max_mult_bet)
        self.__class__.eventID3, self.__class__.selection_ids_3 = event_params3.event_id, event_params3.selection_ids

        self.__class__.selection_name, self.__class__.selection_id = list(self.selection_ids.items())[0]
        self.__class__.selection2_name, self.__class__.selection2_id = list(self.selection_ids_2.items())[0]
        self.__class__.selection3_name, self.__class__.selection3_id = list(self.selection_ids_3.items())[0]

        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)

    def test_001_add_selection_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add selection and go Betslip, 'Singles' section
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button(
            self, single=True):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button
        EXPECTED: The bet is sent to Openbet system for review
        """
        if single:
            self.__class__.bet_amount = self.max_bet + 1
            self.place_single_bet()
        else:
            self.__class__.bet_amount = self.max_mult_bet + 1
            self.place_multiple_bet(number_of_stakes=1)
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

        has_overask_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(has_overask_message, msg='Overask message closed after click on background')

    def test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.max_bet,
                                       price_type='S')

    def test_005_verify_betslip(self, single=True):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: The Estimate returns are updated according to new Stake value
        EXPECTED: 'Cancel' and 'Place a bet' buttons enabled
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

        betslip_section = self.get_betslip_content()
        est_returns = betslip_section.total_estimate_returns
        self.assertEqual(est_returns, 'N/A', msg='Est returns is not equal "N/A"')

        if single:
            section = self.get_betslip_sections().Singles
        else:
            section = self.get_betslip_sections(multiples=True).Multiples
        stake_name, stake = list(section.items())[0]
        self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for "{stake_name}" is not highlighted in yellow')

        self.assertTrue(betslip_section.has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(betslip_section.confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

    def test_006_uncheck_checkbox_with_max_bet_offer(self):
        """
        DESCRIPTION: Uncheck checkbox with max bet offer
        EXPECTED: *   'Accept & Bet' button becomes disabled
        EXPECTED: *   Message: "You're not accepting this Trade Offer" is displayed on the grey background below the unchecked selection
        """
        pass  # not valid step from OX 99

    def test_007_check_checkbox_with_max_bet_offer__click__tap_accept__bet_number_of_accepted_bets_button(self):
        """
        DESCRIPTION: Check checkbox with max bet offer > Click / tap 'Accept & Bet ([number of accepted bets])' button
        EXPECTED: *   Bet is placed and balance is reduced accordingly
        EXPECTED: *   Bet is listed in 'Bet History' and 'My Account' pages
        """
        pass  # not valid step from OX 99

    def test_008_repeat_steps__2_7(self):
        """
        DESCRIPTION: Repeat steps # 2-7
        """
        pass  # not valid step from OX 99

    def test_009_click__tap_cancel_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button
        EXPECTED: * Bet is not placed
        EXPECTED: * Selections are present in betslip without offer and without entered stake
        """
        cancel_btn = self.get_betslip_content().cancel_button
        cancel_btn.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        self.assertTrue(dialog, msg='"CANCEL OFFER?" dialog is not shown')
        dialog.cancel_offer_button.click()
        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=3),
                             msg='Betslip widget was not closed')
        else:
            result = wait_for_result(lambda: self.get_betslip_content().no_selections_title,
                                     name='Betslip to be cleared',
                                     timeout=3)
            self.assertTrue(result, msg='BetSlip was not cleared')

    def test_010_add_a_few_selections_and_go_betslip_multiples_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Multiples' section
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection2_id, self.selection3_id))

    def test_011_repeat_steps_2_9_but_on_step_3_enter_max_value_in_stake_field_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #2-9 but on step #3 enter max value in 'Stake' field for Multiple bet
        """
        self.test_002_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button(single=False)
        self.test_003_verify_betslip()

        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID3)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.max_mult_bet,
                                       price_type='S')

        self.test_005_verify_betslip(single=False)
        self.test_009_click__tap_cancel_button()
