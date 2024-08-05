import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.high
@vtest
class Test_C2553176_Accepting_split_bet_without_linked_parts__both_bets_placed(BaseBetSlipTest):
    """
    TR_ID: C2553176
    NAME: Accepting split bet without linked parts - both bets placed
    DESCRIPTION: This test case verifies splitting Overask bets without linking its parts
    DESCRIPTION: Instruction how to split Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True
    bet_amount = 3.00
    stake_part1 = 1.50
    price_part1 = 1.50
    stake_part2 = 0.50
    price_part2 = 0.50

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=2)

        self.__class__.eventID, self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params.event_id, event_params.team1, event_params.team2, event_params.selection_ids

        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection
        """
        self.place_single_bet()

    def test_003_tap_bet_now_buttonfrom_ox_99_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        DESCRIPTION: **From OX 99**
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        EXPECTED: **From OX 99**
        EXPECTED: ![](index.php?/attachments/get/33504) ![](index.php?/attachments/get/33505)
        """
        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title: Bet review notification is not shown to the user')

    def test_004_triggerbet_split_and_stakeoddsprice_type_modificationby_trader(self):
        """
        DESCRIPTION: Trigger Bet Split and Stake/Odds/Price Type modification by Trader.
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventID,
                                     bet_id=[bet_id], betslip_id=betslip_id,
                                     stake_part1=self.stake_part1, price_part1=self.price_part1,
                                     stake_part2=self.stake_part2, price_part2=self.price_part2)

    def test_005_verify_bet_parts_with_modified_values_displaying_in_betslip(self):
        """
        DESCRIPTION: Verify Bet parts with modified values displaying in Betslip
        EXPECTED: * The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: * Splitted parts of the selection are expanded
        EXPECTED: * Enabled pre-ticked check boxes are shown next to each selection instead of '-'(expand)/'+'(collapse) icon
        EXPECTED: * "You're accepting this Trade Offer" message is shown under each part of the selecion on the gray background
        EXPECTED: * 'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons are displayed enabled
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Splitted parts of the selection are displayed
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: NEW design:
        EXPECTED: ![](index.php?/attachments/get/33507) ![](index.php?/attachments/get/33508)
        """
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" '
                             f'is not as expected: "{cms_overask_trader_message}" from CMS')

        singles_section = self.get_betslip_sections().Singles

        stake_name1, self.__class__.stake1 = list(singles_section.items())[0]
        expected_stake_value1 = float(self.stake1.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value1, self.stake_part1,
                         msg=f'New stake value: "{expected_stake_value1}" '
                             f'is not as expected: "{self.stake_part1}"')

        stake_name2, self.__class__.stake2 = list(singles_section.items())[1]
        expected_stake_value2 = float(self.stake2.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value2, self.stake_part2,
                         msg=f'New stake value: "{expected_stake_value2}" '
                             f'is not as expected: "{self.stake_part2}"')

        betslip_section = self.get_betslip_content()
        total_stake = betslip_section.total_stake
        est_returns = betslip_section.total_estimate_returns
        expected_est_returns = float(total_stake) * 1.5
        self.assertEqual(float(est_returns), expected_est_returns,
                         msg=f'Actual Est. Returns: {float(est_returns)} '
                             f'is not as expected: "{expected_est_returns}')

        place_bet_button = betslip_section.confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')

        cancel_button = betslip_section.cancel_button
        self.assertTrue(cancel_button.is_enabled(), msg=f'"{cancel_button.name}" button is disabled')

    def test_006_tap_accept__bet_2_buttonfrom_ox_99_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap 'Accept & Bet (2)' button
        DESCRIPTION: **From OX 99**
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: Bets are placed as per normal process
        """
        place_bet_button = self.get_betslip_content().confirm_overask_offer_button
        place_bet_button.click()
        self.check_bet_receipt_is_displayed()

        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        if self.device_type == 'mobile':
            self.site.bet_receipt.close_button.click()

    def test_007_add_few_selections_to_the_betslipand_for_one_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them enter stake value which will trigger Overask for the selection
        EXPECTED: Selections are successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1], self.selection_ids[self.team2]))

    def test_008_repeat_steps_3_6(self):
        """
        DESCRIPTION: Repeat steps 3-6
        EXPECTED: All added selections are placed after Trader Offer confirmation
        """
        self.place_single_bet()
        self.test_003_tap_bet_now_buttonfrom_ox_99_tap_button_place_bet()
        self.test_004_triggerbet_split_and_stakeoddsprice_type_modificationby_trader()
        self.test_005_verify_bet_parts_with_modified_values_displaying_in_betslip()
        self.test_006_tap_accept__bet_2_buttonfrom_ox_99_tap_button_place_bet()
