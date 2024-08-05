import pytest
import tests
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #overask cannot be triggered for prod
# @pytest.mark.hl
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C16413758_Accepting_split_multiple_bets_linked_parts_traders_offer(BaseBetSlipTest):
    """
    TR_ID: C16413758
    NAME: Accepting split multiple bets & linked parts trader's offer
    DESCRIPTION: This test case verifies accepting split multiple bets & linked parts trader's offer
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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        for i in range(0, 3):
            event = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
            self.eventIDs.append(event.event_id)
            self.selectionIDs.append(event.selection_ids[event.team1])
        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol

    def test_001_add_3_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add 3 selections from different events to the Betslip
        EXPECTED: Selections are successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.__class__.bet_amount = self.max_bet + 0.5
        self.open_betslip_with_selections(selection_ids=self.selectionIDs)

    def test_002__enter_stake_value_into_treble_field_which_is_higher_than_the_maximum_limit_for_added_selections_tap_button_place_bet(self):
        """
        DESCRIPTION: * Enter stake value into 'Treble' field which is higher than the maximum limit for added selections
        DESCRIPTION: * Tap button 'Place Bet'
        EXPECTED: * Overask is triggered for the User
        EXPECTED: * The bet review notification is shown to the User
        """
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title: Bet review notification is not shown to the user')

    def test_003_in_ti_trigger__bet_split__link_parts_of_split_bet__stakeoddsprice_type_modification_submit_changes(self):
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
        EXPECTED: *   Buttons 'Cancel' and 'Place Bet' are displayed
        EXPECTED: ![](index.php?/attachments/get/34134) ![](index.php?/attachments/get/34135)
        """
        self.site.wait_splash_to_hide()
        self.__class__.sections = self.get_betslip_content().overask_trader_section.items
        is_selection_splitted = wait_for_result(lambda: len(self.sections) == 8,
                                                timeout=10,
                                                name='Selections to become splitted into 2 parts')
        self.assertTrue(is_selection_splitted, msg='Selection is not splitted into 2 parts')
        for section in range(len(self.sections)):
            if section in [3, 7]:
                odds = float(self.sections[section].stake_value.text.replace(self.user_currency, ""))
                self.assertEqual(odds, self.stake_part1,
                                 msg=f'Actuals odds:"{odds}" is not same as Expected odds: "{ self.stake_part1}"')
                price_color = self.sections[section].stake_value.background_color_value
                self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                 msg=f'"Modified price" is not highlighted in yellow')
            if section in [3]:
                self.assertFalse(self.sections[section].has_remove_button(),
                                 msg=f'Remove button is present for "{self.sections[section].name}"')
            if section in [7]:
                self.assertTrue(self.sections[section].has_remove_button(),
                                msg=f'Remove button is not present for "{self.sections[section].name}"')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='Place bet button is not displayed')
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg='Cancel button is disabled')

    def test_005_tap_button_place_bet(self):
        """
        DESCRIPTION: Tap button 'Place Bet'
        EXPECTED: * Linked bets are placed successfully
        EXPECTED: * Bet receipt page is displayed and placed bets are displayed as multiples
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        treble_name = vec.bet_history.BET_TYPES.TBL
        self.assertEqual(len(betreceipt_sections), 2,
                         msg=f'Bet receipt section should have 2 placed bets found: "{treble_name}"')
        for section in range(len(betreceipt_sections)):
            self.assertEqual(betreceipt_sections[section].name, treble_name,
                             msg=f'Found section "{betreceipt_sections[section]}" is not same as expected section "{treble_name}"')
