import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29109_Estimated_Returns_Calculation_For_Singles_with_Free_Bet(Common):
    """
    TR_ID: C29109
    NAME: 'Estimated Returns' Calculation For Singles with Free Bet
    DESCRIPTION: This test case verifies calculation of Estimated Returns value for a Single Bet when free bet is selected
    DESCRIPTION: AUTOTEST: 2553426
    PRECONDITIONS: Make sure user has free bets available.
    """
    keep_browser_open = True

    def test_001_add_single_bet_to_the_bet_slip(self):
        """
        DESCRIPTION: Add Single Bet to the Bet Slip
        EXPECTED: Selection is added
        """
        pass

    def test_002_go_to_betslip_singles_section(self):
        """
        DESCRIPTION: Go to 'BetSlip', 'Singles' section
        EXPECTED: 'Singles' section is shown
        """
        pass

    def test_003_select_free_bet_from_the_dropdown(self):
        """
        DESCRIPTION: Select free bet from the dropdown
        EXPECTED: *   Free bet is chosen
        EXPECTED: *   'Stake' field is empty
        """
        pass

    def test_004_verify_total_est_returnsvalue(self):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: **Free Bet Value * (priceNum/priceDen)** - if odds have a fractional format
        EXPECTED: **Free Bet Value * Odds - Free Bet Value** - if odds have a decimal format
        """
        pass

    def test_005_select_free_bet_option_and_enter_stake_amount_manually(self):
        """
        DESCRIPTION: Select free bet option and enter stake amount manually
        EXPECTED: *   Free bet is selected
        EXPECTED: *   Entered stake is displayed in the 'Stake' field
        """
        pass

    def test_006_verify_total_est_returnsvalue(self):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: **(free_bet + stake) * ((priceNum/priceDen)+1)-free_bet** - if Odds in a fractional format
        EXPECTED: **(free_bet + stake) * Odds - free_bet** - if Odds in a decimal format
        """
        pass
