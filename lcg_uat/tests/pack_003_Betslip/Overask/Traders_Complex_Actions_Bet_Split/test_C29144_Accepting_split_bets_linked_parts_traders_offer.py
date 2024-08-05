import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C29144_Accepting_split_bets_linked_parts_traders_offer(BaseBetSlipTest):
    """
    TR_ID: C29144
    NAME: Accepting split bets & linked parts trader's offer
    DESCRIPTION: This test case verifies bet split and linking within Overask functionality
    DESCRIPTION: Instruction how to split & link Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True
    username = None
    bet_amount = 3
    stake_part1 = 1.00
    price_part1 = 1.50
    stake_part2 = 0.09
    price_part2 = 1.50

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with bet limit 2
        DESCRIPTION: Login as a user that has sufficient funds to place a bet
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=2)
        self.__class__.eventID, self.__class__.team1, self.__class__.selection_ids = \
            event_params.event_id, event_params.team1, event_params.selection_ids

        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)

    def test_001_add_selection_to_the_betslip_open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip > Open Betslip
        EXPECTED: Selection is successfully added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection > Tap 'Bet Now' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        self.place_single_bet()
        overask = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask to appear', timeout=10)
        self.assertTrue(overask, msg='Overask is not shown')

    def test_003_in_ti_trigger_bet_split_link_parts_of_split_bet_stake_odds_price_type_modification_submit_changes(self):
        """
        DESCRIPTION: In TI trigger:
        DESCRIPTION: - Bet split
        DESCRIPTION: - Link parts of split bet
        DESCRIPTION: - Stake/Odds/Price Type modification
        DESCRIPTION: > Submit changes
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id,
                                     stake_part1=self.stake_part1, price_part1=self.price_part1,
                                     stake_part2=self.stake_part2, price_part2=self.price_part2,
                                     linked=True)

    def test_004_verify_bet_parts_with_modified_values_displaying_in_betslip(self):
        """
        DESCRIPTION: The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: The bet parts are stacked:
        EXPECTED: Parent selection doesn't have a Remove button
        EXPECTED: Remove button displays only on the child selection
        EXPECTED: Buttons 'Cancel' and 'Place Bet' are displayed
        """
        is_selection_splitted = wait_for_result(lambda: len(self.get_betslip_sections().Singles) == 2,
                                                timeout=5,
                                                name='Selections to become splitted into 2 parts')
        self.assertTrue(is_selection_splitted, msg='Selection is not splitted into 2 parts')
        singles_section = self.get_betslip_sections().Singles

        for stake_name, stake in singles_section.items():
            self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Modified price for "{stake_name}" is not highlighted in yellow')

        stake_name1, stake1 = list(singles_section.items())[0]
        expected_stake_value1 = float(stake1.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value1, self.stake_part1,
                         msg=f'Changed amount should be present, get "{expected_stake_value1}" instead')
        self.assertFalse(stake1.has_remove_button(expected_result=False),
                         msg=f'Remove button is present for "{stake_name1}"')

        stake_name2, self.__class__.stake2 = list(singles_section.items())[1]
        expected_stake_value2 = float(self.stake2.offered_stake.name.strip('£'))
        self.assertEqual(expected_stake_value2, self.stake_part2,
                         msg=f'Changed amount should be present, get "{expected_stake_value2}" instead')
        self.assertTrue(self.stake2.has_remove_button(), msg=f'Remove button is not present for "{stake_name2}"')

        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='Confirm button is disabled')
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg='Cancel button is disabled')

    def test_005_unselect_one_of_bet_parts(self):
        """
        DESCRIPTION: REMOVE one of the Bet parts (Child part)
        EXPECTED: Only child part of bet can be removed
        EXPECTED: Button 'Place Bet' enabled
        """
        self.stake2.scroll_to()
        self.stake2.select()
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[1]
        self.__class__.undo_button = stake.undo_button
        self.assertTrue(self.undo_button.is_displayed(), msg='UNDO button is not displayed')

        self.__class__.place_bet_button = self.get_betslip_content().confirm_overask_offer_button
        self.assertTrue(self.place_bet_button.is_enabled(), msg=f'"{self.place_bet_button.name}" button is disabled')

    def test_006_select_one_of_bet_parts(self):
        """
        DESCRIPTION: UNDO one of the child Bet parts
        EXPECTED: 'Place Bet' button remains enabled
        EXPECTED: Child selection is restored
        """
        self.undo_button.click()
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[1]
        self.assertTrue(stake.is_displayed(), msg='Child selection is not restored')
        self.assertTrue(stake.has_remove_button(), msg=f'Remove button is not present for "{stake_name}"')
        self.assertTrue(self.place_bet_button.is_enabled(), msg=f'"{self.place_bet_button.name}" button is disabled')

    def test_007_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap button 'Place Bet'
        EXPECTED: Linked bets are placed successfully
        EXPECTED: Bet receipt page is displayed and placed bets are displayed as separate singles
        """
        self.place_bet_button.click()
        self.check_bet_receipt_is_displayed()

        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        singles_name = vec.betslip.BETSLIP_SINGLES_NAME.title()
        singles = betreceipt_sections.get(singles_name, None)
        self.assertTrue(singles, msg='Singles section was not found')
        self.assertEqual(len(singles.items), 2,
                         msg=f'Bet receipt section should have 2 placed bets found: "{len(singles.items)}"')
