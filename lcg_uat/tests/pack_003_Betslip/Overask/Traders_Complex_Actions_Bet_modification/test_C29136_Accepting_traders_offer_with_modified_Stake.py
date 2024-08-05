import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C29136_Accepting_traders_offer_with_modified_Stake(BaseBetSlipTest):
    """
    TR_ID: C29136
    NAME: Accepting trader's offer with modified Stake
    DESCRIPTION: This test case verifies accepting trader's offer with modified Stake
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True
    eventID, eventID2, eventID3 = None, None, None
    selection_ids_2, selection_ids_3 = None, None
    max_bet = 0.03
    max_mult_bet = 0.06
    username = None
    selection_name, selection2_name, selection3_name = None, None, None
    selection_id, selection2_id, selection3_id = None, None, None
    suggested_max_bet = None
    stake_bet_amounts = {}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: User is logged in to application
        """
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

        self.__class__.stake_bet_amounts = {
            self.selection2_name: self.bet_amount,
            self.selection3_name: self.max_bet + 1
        }

        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        """
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet()

    def test_003_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: Overask is triggered for the User
        EXPECTED: The bet review notification is shown to the User
        """
        overask = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask excedds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

    def test_004_trigger_stake_modification_by_trader_and_verify_new_stake_value_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Stake modification by Trader and verify new Stake value displaying in Betslip
        EXPECTED: 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: The Estimate returns are updated according to new Stake value
        EXPECTED: 'Cancel' and 'Place a bet' buttons enabled
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.__class__.suggested_max_bet = 3.5
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet,
                                       price_type='S')

        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

        est_returns = self.get_betslip_content().total_estimate_returns
        self.assertEqual(est_returns, 'N/A', msg='Est returns is not equal "N/A"')
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for "{stake_name}" is not highlighted in yellow {stake.offered_stake.background_color_value}')

        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

    def test_005_tap_accept_bet_number_of_accepted_bets_button(self, counter=1):
        """
        DESCRIPTION: Tap 'Accept & Bet ([number of accepted bets])' button
        EXPECTED: The bet is placed as per normal process
        """
        confirm_btn = self.get_betslip_content().confirm_overask_offer_button
        confirm_btn.click()
        self.check_bet_receipt_is_displayed()

        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        singles_name = vec.betslip.BETSLIP_SINGLES_NAME.title()

        singles = betreceipt_sections.get(singles_name, None)
        self.assertTrue(singles, msg='Singles section was not found')
        receipts = singles.items
        self.assertEqual(counter, len(receipts),
                         msg=f'Bet receipt section should have "{counter}" placed bet found: "{len(receipts)}"')
        self.site.bet_receipt.footer.click_done()

    def test_006_add_few_selections_to_the_betslipand_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them enter stake value which will trigger Overask for the selection
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection2_id, self.selection3_id))
        self.place_single_bet(stake_bet_amounts=self.stake_bet_amounts)
        self.test_003_tap_bet_now_button()

    def test_007_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps 4-6
        EXPECTED: All added selections are placed after Trader Offer confirmation
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID3)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.__class__.suggested_max_bet = 2.00
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id, betslip_id=betslip_id,
                                       max_bet=self.suggested_max_bet)
        overask_trader_offer = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section, name='Overask trader offer to appear', timeout=10)
        self.assertTrue(overask_trader_offer, msg='Overask trader offer is not triggered for the User')

        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

        est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(est_returns, 'N/A', msg='Est returns is equal "N/A"')

        singles_section = self.get_betslip_sections().Singles
        stake = singles_section[self.selection3_name] if self.selection3_name in singles_section.keys() else None
        self.assertTrue(stake, msg=f'Stake {self.selection3_name} was not found')
        self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price {self.selection3_name} is not highlighted in yellow')

        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')
        self.__class__.expected_betslip_counter_value = 0
        self.test_005_tap_accept_bet_number_of_accepted_bets_button(counter=2)
