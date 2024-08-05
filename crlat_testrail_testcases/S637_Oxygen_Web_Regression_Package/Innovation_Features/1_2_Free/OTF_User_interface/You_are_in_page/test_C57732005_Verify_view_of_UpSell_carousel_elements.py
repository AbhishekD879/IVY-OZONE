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
class Test_C57732005_Verify_view_of_UpSell_carousel_elements(Common):
    """
    TR_ID: C57732005
    NAME: Verify view of UpSell carousel elements
    DESCRIPTION: This test case verifies UpSell carousel elements
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    """
    keep_browser_open = True

    def test_001_user_submit_predictions(self):
        """
        DESCRIPTION: User 'Submit' predictions
        EXPECTED: 'You are in' page opened successfully
        EXPECTED: **Ordering:**
        EXPECTED: Match betting - BTTS - O/U 2.5
        EXPECTED: **OpenBet markets names:**
        EXPECTED: |Match Result| for Match betting
        EXPECTED: |Both Teams to Score| for BTTS
        EXPECTED: |Over/Under Total Goals| |2.5| for Over/Under 2.5 goal
        EXPECTED: All data retrieved from CMS and correctly designed according to: https://app.zeplin.io/project/5c471d82d6094838624e7232/dashboard
        EXPECTED: First carousel block 'Match Results' with:
        EXPECTED: - Title
        EXPECTED: - Matches with Match Results information
        EXPECTED: - Odds information
        EXPECTED: - Green button with 'ADD TO BETSLIP' text
        """
        pass

    def test_002_user_swipes_left_of_carousel_block(self):
        """
        DESCRIPTION: User swipes left of carousel block
        EXPECTED: Second carousel block 'BTTS' with:
        EXPECTED: - Title
        EXPECTED: - Matches with BTTS Yes/No information
        EXPECTED: - Odds information
        EXPECTED: - 'Add To Slip' button
        """
        pass

    def test_003_user_swipes_left_of_carousel_block_again(self):
        """
        DESCRIPTION: User swipes left of carousel block again
        EXPECTED: Third carousel block 'Over/Under 2.5 goal' with:
        EXPECTED: - Title
        EXPECTED: - Matches with Over/Under 2.5 information
        EXPECTED: - Odds information
        EXPECTED: - 'Add To Slip' button
        """
        pass
