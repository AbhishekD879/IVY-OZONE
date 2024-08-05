import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not create event on Market level with Extra place promo icon
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2637330_Verify_Extra_Place_icon_for_Multiple_Bet_on_BetSlip_and_Bet_Receipt(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C2637330
    NAME: Verify Extra Place icon for Multiple Bet on BetSlip and Bet Receipt
    DESCRIPTION: This test case verifies that the Extra Place icon is displayed for Multiple Bet on the Bet Receipt within BetSlip
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-33486 Promo / Signposting : Extra Place : Icons for Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33486
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Extra Place promo is available for <Race> events on Market level
    PRECONDITIONS: * Selection should be added to the BetSlip from events **WITH** Extra Place promo available and **WITHOUT** as well
    """
    keep_browser_open = True
    price1 = {0: '1/4'}
    price2 = {0: '1/2'}

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
        PRECONDITIONS: * User is logged in and has positive balance
        PRECONDITIONS: * Extra Place promo is available for <Race> event on Market level.
        PRECONDITIONS: * Selection should be added to the BetSlip from events **WITH** Extra Place promo available and **WITHOUT** as well
        """
        event1 = self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=True,
                                                    lp_prices=self.price1)
        event2 = self.ob_config.add_UK_racing_event(number_of_runners=1, market_extra_place_race=False,
                                                    lp_prices=self.price2)
        self.__class__.selection_id1 = list(event1.selection_ids.values())[0]
        self.__class__.selection_id2 = list(event2.selection_ids.values())[0]
        self.site.login()

    def test_001_add_a_couple_of_race_selection_from_the_preconditions_to_the_betslip(self):
        """
        DESCRIPTION: Add a couple of <Race> selection from the preconditions to the BetSlip
        EXPECTED: * <Race> selections are added to the BetSlip
        EXPECTED: * Multiple bets are shown on the BetSlip
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id1, self.selection_id2])
        section = self.get_betslip_sections(multiples=True)
        multiple_section = section.Singles, section.Multiples
        self.assertTrue(multiple_section, msg='*** No Multiple stakes found')

    def test_002_enter_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for one of **Multiple** bet and place a bet
        EXPECTED: * Multiple Bet is placed successfully
        EXPECTED: * Bet Receipt for Multiple is displayed
        """
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_003_verify_extra_place_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Bet Receipt
        EXPECTED: * 'Extra Place' icon is displayed under each selection (under market name/event name section) which has 'Extra Place' available
        EXPECTED: * 'Extra Place' icon is separated by a dashed line from the bottom
        """
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='Bet receipt sections not found')
        receipts = receipt_sections['Double'].items_as_ordered_dict
        self.assertTrue(receipts, msg='Receipts not found in bet receipt section')
        first_section = list(receipts.values())[0]
        self.assertTrue(first_section.has_promo_icon, msg='Failed to display "Extra Place" icon')
        second_section = list(receipts.values())[1]
        self.assertFalse(second_section.has_promo_icon(expected_result=False),
                         msg='"Extra Place" icon is displayed which is unexpected')
