import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   # Overask cannot be triggered in prod.
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C16413755_Accepting_split_double_bets_linked_parts__only_one_bet_placed(BaseBetSlipTest):
    """
    TR_ID: C16413755
    NAME: Accepting split double bets & linked parts - only one bet placed
    DESCRIPTION: This test case verifies Accepting split double bets & linked parts - only one bet placed
    DESCRIPTION: Instruction how to split & link Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True
    max_bet = 0.5
    stake_part1 = 0.5
    price_part1 = 1.50
    stake_part2 = 0.5
    price_part2 = 1.50
    eventIDs = []
    selectionIDs = []
    number_of_stakes = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        for i in range(0, 2):
            event = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
            self.eventIDs.append(event.event_id)
            self.selectionIDs.append(event.selection_ids[event.team1])
        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol

    def test_001_add_2_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 2 selections from different events to the Betslip
        EXPECTED: Double Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.__class__.bet_amount = self.max_bet + 0.5
        self.open_betslip_with_selections(selection_ids=self.selectionIDs)

    def test_002__enter_stake_into_a_double_field_value_which_is_higher_than_the_maximum_limit_for_added_selection_tap_button_place_bet(
            self):
        """
        DESCRIPTION: * Enter stake into a 'Double' field value which is higher than the maximum limit for added selection
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        """
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title: Bet review notification is not shown to the user')

    def test_003_in_ti_trigger__bet_split__link_parts_of_split_bet__stakeoddsprice_type_modification_submit_changes(
            self):
        """
        DESCRIPTION: In TI trigger:
        DESCRIPTION: - Bet split
        DESCRIPTION: - Link parts of split bet
        DESCRIPTION: - Stake/Odds/Price Type modification
        DESCRIPTION: > Submit changes
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
                                     stake_part2=self.stake_part2, price_part2=self.price_part2,
                                     linked=True)

    def test_004_in_app_verify_bet_parts_with_modified_values_displaying_in_betslip(self):
        """
        DESCRIPTION: In app: Verify bet parts with modified values displaying in Betslip
        EXPECTED: * The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: * The bet parts are stacked:
        EXPECTED: * Parent selection doesn't have a Remove button
        EXPECTED: * Remove button displays only on the child selection
        EXPECTED: * Buttons 'Cancel' and 'Place Bet' are displayed
        EXPECTED: ![](index.php?/attachments/get/34128) ![](index.php?/attachments/get/34129)
        """
        self.site.wait_splash_to_hide()
        self.__class__.sections = self.get_betslip_content().overask_trader_section.items
        is_selection_splitted = wait_for_result(lambda: len(self.sections) == 6,
                                                timeout=10,
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
            if section in [2]:
                self.assertFalse(self.sections[section].has_remove_button(),
                                 msg=f'Remove button is present for "{self.sections[section].name}"')
            if section in [5]:
                self.assertTrue(self.sections[section].has_remove_button(),
                                msg=f'Remove button is not present for "{self.sections[section].name}"')

        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='Place bet button is not displayed')
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg='Cancel button is disabled')

    def test_005_remove_one_of_the_double_selections(self):
        """
        DESCRIPTION: Remove one of the Double selections
        EXPECTED: One Double selection is removed
        """
        self.sections[5].remove_btn.click()
        result = wait_for_result(lambda: self.sections[5].undo_icon.is_displayed(),
                                 name='"UNDO button" to be displayed', timeout=60)
        self.assertTrue(result,
                        msg='"UNDO button" is not displayed when the user clicks on the "Selection removal icon(X)"')
        self.assertTrue(self.sections[5].leg_remove_marker.is_displayed(), msg='"REMOVED" icon is not displayed')

    def test_006_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap button 'Place Bet'
        EXPECTED: Bet is successfully placed without removed selection
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        your_bets = f'{vec.betslip.YOUR_BETS}: ({self.number_of_stakes})'
        self.assertEqual(self.site.bet_receipt.receipt_sub_header.bet_counter_text, your_bets,
                         msg=f'Actual bet count: {self.site.bet_receipt.receipt_sub_header.bet_counter_text} is '
                             f'not the same as expected: "{your_bets}"')
