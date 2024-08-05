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
class Test_C2538043_Estimated_Returns_Calculation_For_Multiple_with_Free_Bet(Common):
    """
    TR_ID: C2538043
    NAME: 'Estimated Returns' Calculation For Multiple with Free Bet
    DESCRIPTION: This test case verifies calculation of Estimated Returns value when free bet is selected
    DESCRIPTION: AUTOTEST: 2554724
    PRECONDITIONS: Make sure user has free bets available.
    """
    keep_browser_open = True

    def test_001_add_several_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add several selections from different events to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_002_go_to_multiples_section(self):
        """
        DESCRIPTION: Go to 'Multiples' section
        EXPECTED: 
        """
        pass

    def test_003_select_free_bet_from_the_dropdown(self):
        """
        DESCRIPTION: Select free bet from the dropdown
        EXPECTED: *  Free bet is chosen
        EXPECTED: *  'Stake' field is empty
        """
        pass

    def test_004_verify_est_returnsvalue(self):
        """
        DESCRIPTION: Verify **'Est. Returns'** value
        EXPECTED: **'Est. Returns'** value is calculated based on formula:
        EXPECTED: **(free_bet/lines_number)*potential_payout-free_bet**
        EXPECTED: * payout.potential and lines_number attributes are taken from 'builtBet' response;
        """
        pass

    def test_005_select_free_bet_option_and_enter_stake_amount_manually(self):
        """
        DESCRIPTION: Select free bet option and enter stake amount manually
        EXPECTED: *  Free bet is selected
        EXPECTED: *  Entered stake is displayed in the 'Stake' field
        """
        pass

    def test_006_verify_est_returnsvalue(self):
        """
        DESCRIPTION: Verify **'Est. Returns'** value
        EXPECTED: **'Est. Returns'** value is calculated based on formula:
        EXPECTED: **((free_bet/lines_number)+stake)*potential_payout-free_bet**
        EXPECTED: * payout.potential and lines_number attributes are taken from 'builtBet' response;
        """
        pass
