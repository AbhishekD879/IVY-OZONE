import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create event on Market level with MoneyBack promo icon
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.login
@vtest
class Test_C2807911_Verify_MoneyBack_icon_for_Multiple_Bet_on_Bet_Receipt(BaseBetSlipTest):
    """
    TR_ID: C2807911
    NAME: Verify MoneyBack icon for Multiple Bet on Bet Receipt
    DESCRIPTION: This test case verifies that the MoneyBack icon is displayed for Multiple Bet on the Bet Receipt within BetSlip
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * MoneyBack promo is available for <Sport> events on Market level
    PRECONDITIONS: * Selection should be added to the BetSlip from events **WITH** MoneyBack promo available and **WITHOUT** as well
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events and login
        """
        self.__class__.selection_ids = []
        for index in range(4):
            if index < 2:
                event = self.ob_config.add_autotest_premier_league_football_event(market_money_back=True)
            else:
                event = self.ob_config.add_autotest_premier_league_football_event()
            self.selection_ids.append(list(event.selection_ids.values())[0])

        self.site.login()

    def test_001_add_a_couple_of_sport_selection_from_the_preconditions_to_the_betslip(self):
        """
        DESCRIPTION: Add a couple of <Sport> selection from the preconditions to the BetSlip
        EXPECTED: * <Sport> selections are added to the BetSlip
        EXPECTED: * Multiple bets are shown on the BetSlip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_enter_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for one of **Multiple** bet and place a bet
        EXPECTED: * Multiple Bet is placed successfully
        EXPECTED: * Bet Receipt for Multiple is displayed
        """
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_verify_moneyback_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'MoneyBack' icon on the Bet Receipt
        EXPECTED: * 'MoneyBack' icon is displayed under each selection (under market name/event name section) which has 'MoneyBack' available
        """
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        first_section = list(bet_receipt_sections.values())[0]
        bet = list(first_section.items_as_ordered_dict.values())
        for i in range(len(bet)):
            if i < 2:
                self.assertTrue(bet[i].has_promo_icon(expected_result=True),
                                msg='MoneyBack icon is not present on bet receipt')
                self.assertEqual(bet[i].promo_label_text, vec.bma.MONEY_BACK.upper(),
                                 msg=f'Actual text:"{bet[i].promo_label_text}" is not changed to Expected text:"{vec.bma.MONEY_BACK.upper()}".')
            else:
                self.assertFalse(bet[i].has_promo_icon(expected_result=False),
                                 msg='MoneyBack icon is present on bet receipt')

    def test_004_repeat_steps_1_3_for_available_moneyback_promo_on_market_level(self):
        """
        DESCRIPTION: Repeat steps 1-3 for available MoneyBack promo on Market level
        EXPECTED:
        """
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=[self.selection_ids[0], self.selection_ids[1]])
        self.test_002_enter_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet()
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        first_section = list(bet_receipt_sections.values())[0]
        bet = list(first_section.items_as_ordered_dict.values())
        for i in range(len(bet)):
            self.assertTrue(bet[i].has_promo_icon(expected_result=True),
                            msg='MoneyBack icon is not present on bet receipt')
            self.assertEqual(bet[i].promo_label_text, vec.bma.MONEY_BACK.upper(),
                             msg=f'Actual text:"{bet[i].promo_label_text}" is not changed to Expected text:"{vec.bma.MONEY_BACK.upper()}".')
