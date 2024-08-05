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
class Test_C2635879_Verify_Extra_Place_icon_for_Single_Bet_on_BetSlip_and_Bet_Receipt(Common):
    """
    TR_ID: C2635879
    NAME: Verify Extra Place icon for Single Bet on BetSlip and Bet Receipt
    DESCRIPTION: This test case verifies that the Extra Place icon is displayed on the Bet Receipt within BetSlip
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [BMA-33486 Promo / Signposting : Extra Place : Icons for Bet Receipt] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-33486
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Extra Place promo is available for <Race> event on Market level
    PRECONDITIONS: NOTE: Extra place icon should NOT be displayed on Quick betslip and Main Bet Slip - but should be displayed on Bet Receipt and Quick Bet Receipt - https://jira.egalacoral.com/browse/BMA-51626?focusedCommentId=2656965&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-2656965
    """
    keep_browser_open = True

    def test_001_add_race_selection_with_available_extra_place_promo_on_market_level_to_the_betslipquickbet_for_mobile(self):
        """
        DESCRIPTION: Add <Race> selection with available Extra Place promo on Market level to the BetSlip/Quickbet (for mobile)
        EXPECTED: <Race> selection is added to the BetSlip/Quickbet (for mobile)
        """
        pass

    def test_002_enter_value_in_stake_field_and_place_a_bet(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and place a bet
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_003_verify_extra_place_icon_on_the_bet_receipt(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Bet Receipt
        EXPECTED: * 'Extra Place' icon is displayed below market name/event name section
        """
        pass
