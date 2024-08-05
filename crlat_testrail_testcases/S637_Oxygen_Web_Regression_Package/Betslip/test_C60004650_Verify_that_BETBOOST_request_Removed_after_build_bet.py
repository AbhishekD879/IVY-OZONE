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
class Test_C60004650_Verify_that_BETBOOST_request_Removed_after_build_bet(Common):
    """
    TR_ID: C60004650
    NAME: Verify that BETBOOST request Removed after build bet
    DESCRIPTION: This Test Сase verifies that there is no BETBOOST request after 'build bet' request.
    PRECONDITIONS: 1. Should be created a user with available odds boost.
    PRECONDITIONS: 2. How to add odds boost token https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+add+Odds+boost+token
    """
    keep_browser_open = True

    def test_001_open_app_and_login_with_user_from_preconditionsadd_selection_to_betslip(self):
        """
        DESCRIPTION: Open App and login with user from preconditions.
        DESCRIPTION: Add selection to betslip.
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        pass

    def test_002_add_a_couple_of_additional_selections_to_betslip(self):
        """
        DESCRIPTION: Add a couple of additional selections to betslip.
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        pass

    def test_003_remove_one_of_the_selections_from_the_betslip(self):
        """
        DESCRIPTION: Remove one of the selections from the betslip
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        pass

    def test_004_remove_all_selections_from_the_betslip(self):
        """
        DESCRIPTION: Remove all selections from the betslip.
        EXPECTED: 
        """
        pass

    def test_005_for_mobileadd_selection_to_quick_bet(self):
        """
        DESCRIPTION: **For Mobile**
        DESCRIPTION: Add selection to 'Quick Bet'
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        pass

    def test_006_for_mobilepress_x_and_remove_selection_to_quick_betopen_betslip(self):
        """
        DESCRIPTION: **For Mobile**
        DESCRIPTION: Press 'X' and remove selection to 'Quick Bet'.
        DESCRIPTION: Open Betslip.
        EXPECTED: - Selection from the 'Quick Bet' added to the betslip.
        EXPECTED: - Open devtool. There is NO **/Proxy/accountFreebets?freebetTokenType=BETBOOST** request to BBP after successful /buildBet response.
        EXPECTED: - All valid freebets and odds boost should be available for user.
        EXPECTED: - Oxygen-UI should use missing freeBetOfferType from /Proxy/v1/buildBet response for filtering and sorting logic of odds boosts in betslip.
        """
        pass
