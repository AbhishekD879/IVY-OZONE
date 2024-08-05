import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C2637330_Verify_Extra_Place_icon_for_Multiple_Bet_on_BetSlip_and_Bet_Receipt(Common):
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

    def test_001_add_a_couple_of_race_selection_from_the_preconditions_to_the_betslip(self):
        """
        DESCRIPTION: Add a couple of <Race> selection from the preconditions to the BetSlip
        EXPECTED: * <Race> selections are added to the BetSlip
        EXPECTED: * Multiple bets are shown on the BetSlip
        """
        pass

    def test_002_enter_value_in_stake_field_for_one_of_multiple_bet_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field for one of **Multiple** bet and place a bet
        EXPECTED: * Multiple Bet is placed successfully
        EXPECTED: * Bet Receipt for Multiple is displayed
        """
        pass

    def test_003_verify_extra_place_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Bet Receipt
        EXPECTED: * 'Extra Place' icon is displayed under each selection (under market name/event name section) which has 'Extra Place' available
        EXPECTED: * 'Extra Place' icon is separated by a dashed line from the bottom
        """
        pass
