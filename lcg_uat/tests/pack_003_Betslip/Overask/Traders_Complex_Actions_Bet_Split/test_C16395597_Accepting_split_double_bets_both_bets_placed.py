import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Overask cannot be triggered in prod.
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.overask
@vtest
class Test_C16395597_Accepting_split_double_bets_both_bets_placed(BaseBetSlipTest):
    """
    TR_ID: C16395597
    NAME: Accepting split double bets- both bets placed
    DESCRIPTION: This test case verifies accepting split double bets without linked parts - both bets placed
    DESCRIPTION: Instruction how to split Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    PRECONDITIONS: * For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: * User is logged in to the application
    """
    keep_browser_open = True
    max_bet = None
    stake_part1 = 0.5
    price_part1 = 1.50
    stake_part2 = 0.5
    price_part2 = 1.50
    eventIDs = []
    selectionIDs = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        for i in range(0, 2):
            event = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
            self.eventIDs.append(event.event_id)
            self.selectionIDs.append(event.selection_ids[event.team1])
        self.site.login()
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol

    def test_001_add_2_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 2 selections from different events to the Betslip
        EXPECTED: Selections are successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.__class__.bet_amount = self.max_bet + 0.5
        self.open_betslip_with_selections(selection_ids=self.selectionIDs)

    def test_002__enter_stake_into_a_double_field_value_which_is_higher_than_the_maximum_limit_for_added_selection_tap_button_place_bet(self):
        """
        DESCRIPTION: * Enter stake into a 'Double' field value which is higher than the maximum limit for added selection
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title: Bet review notification is not shown to the user')

    def test_003_trigger_bet_split_and_stakeoddsprice_type_modification_by_trader(self):
        """
        DESCRIPTION: Trigger Bet Split and Stake/Odds/Price Type modification by Trader.
        EXPECTED:
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.eventIDs)
        account_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        bet_id = list(bets_details.keys())[0]
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventIDs, bet_id=[bet_id],
                                     betslip_id=betslip_id,
                                     stake_part1=self.stake_part1, price_part1=self.price_part1,
                                     stake_part2=self.stake_part2, price_part2=self.price_part2)

    def test_004_verify_bet_parts_with_modified_values_displaying_in_betslip(self):
        """
        DESCRIPTION: Verify Bet parts with modified values displaying in Betslip
        EXPECTED: *  'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Splitted parts of the selection are displayed
        EXPECTED: * Only parent part has Remove button (Double(x1), Treble, etc.)
        EXPECTED: * The new values are shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons are enabled
        EXPECTED: ![](index.php?/attachments/get/33889) ![](index.php?/attachments/get/33888)
        """
        self.site.wait_splash_to_hide()
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" '
                             f'is not as expected: "{cms_overask_trader_message}" from CMS')

        self.__class__.sections = self.get_betslip_content().overask_trader_section.items
        is_selection_splitted = wait_for_result(lambda: len(self.sections) == 6,
                                                timeout=30,
                                                name='Selections to become splitted into 2 parts')
        self.assertTrue(is_selection_splitted, msg='Selection is not splitted into 2 parts')
        for section in range(len(self.sections)):
            if section in [2, 5]:
                odds = float(self.sections[section].stake_value.text.replace(self.user_currency, ""))
                self.assertEqual(odds, self.stake_part1,
                                 msg=f'Actuals odds:"{odds}" is not same as Expected odds: "{self.stake_part1}"')
                price_color = self.sections[section].stake_value.background_color_value
                self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                 msg=f'"Modified price" is not highlighted in yellow')

                self.assertTrue(self.sections[section].has_remove_button(),
                                msg=f'Remove button is not present for "{self.sections[section].name}"')

        betslip_section = self.get_betslip_content()
        total_stake = betslip_section.total_stake
        est_returns = betslip_section.total_estimate_returns
        self.verify_estimated_returns(est_returns=float(est_returns), bet_amount=total_stake,
                                      is_double=True, odds=[self.price_part1, self.price_part2])

        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='Place bet button is not displayed')
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg='Cancel button is disabled')

    def test_005_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap button 'Place Bet'
        EXPECTED: Bet is successfully placed with all selections from the trader's offer
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()

        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        doubles_name = vec.bet_history.BET_TYPES.DBL
        self.assertEqual(len(bet_receipt_sections), 1,
                         msg=f'Length of Actual betreceipt sections" "{len(bet_receipt_sections)}" '
                             f'is not same as length of Expected betreceipt sections: "1" ')
        self.assertEqual(list(bet_receipt_sections.keys())[0], doubles_name,
                         msg=f'Found section "{list(bet_receipt_sections.keys())[0]}" '
                             f'is not same as expected section "{doubles_name}"')
