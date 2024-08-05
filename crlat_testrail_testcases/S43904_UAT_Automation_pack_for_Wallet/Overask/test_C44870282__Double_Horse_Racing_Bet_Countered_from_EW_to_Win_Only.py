import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870282__Double_Horse_Racing_Bet_Countered_from_EW_to_Win_Only(Common):
    """
    TR_ID: C44870282
    NAME: - Double Horse Racing Bet Countered from EW to Win Only
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_an_oa_double_ew_bet(self):
        """
        DESCRIPTION: Place an OA double EW bet
        EXPECTED: The bet should have gone through to the OA flow
        """
        pass

    def test_002_in_the_ti_change_the_bet_from_ew_to_win_only_and_click_submit(self):
        """
        DESCRIPTION: In the TI, change the bet from EW to Win Only and click Submit
        EXPECTED: On the Front End, you should see a counter offer which is half of the original stake and you should see the text Win Only under the text
        """
        pass

    def test_003_check_that_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the Potential Returns are correct
        EXPECTED: The Potential Returns should be correct
        """
        pass

    def test_004_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: The bet should have been placed and the bet receipt should be seen
        """
        pass

    def test_005_check_that_the_bet_receipt_shows_the_correct_potential_returns(self):
        """
        DESCRIPTION: Check that the bet receipt shows the correct Potential Returns
        EXPECTED: The bet receipt should show the correct Potential Returns
        """
        pass
