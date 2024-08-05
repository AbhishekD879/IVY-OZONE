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
class Test_C18574309_Verify_number_of_legs_in_placeBet_response_for_Multiple_bet_placement(Common):
    """
    TR_ID: C18574309
    NAME: Verify number of legs  in 'placeBet' response for Multiple bet placement
    DESCRIPTION: This test case verify number of legs  in 'placeBet' response for Multiple bet placement
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Log in app with the user that has a positive balance
    PRECONDITIONS: 3. Add at least 2 selections from different evennt to the Betslip
    PRECONDITIONS: 4. Make Bet Placement
    PRECONDITIONS: 5. Check data in 'placeBet' response
    PRECONDITIONS: **Note:**
    PRECONDITIONS: For checking the data find the 'placeBet' response in Dev Tools -> Network -> Preview
    PRECONDITIONS: ![](index.php?/attachments/get/35972)
    """
    keep_browser_open = True

    def test_001_open_placebet_response_and_check_the_number_of_received_legs_for_multiple_betsplacebet___bet___bettyperef_id_eg_dbl___leg(self):
        """
        DESCRIPTION: Open 'placeBet' response and check the number of received legs for Multiple bets
        DESCRIPTION: placeBet -> bet -> betTypeRef: {id: "e.g. DBL"} -> leg
        EXPECTED: 'leg' section contains ids of all selections from particular Multiple bets
        EXPECTED: (e.g.
        EXPECTED: 2 selections ids for Double
        EXPECTED: 3 selections ids for Treble
        EXPECTED: etc.)
        """
        pass
