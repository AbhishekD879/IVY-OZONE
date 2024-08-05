import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C62851779_Verify_GA_tracking_capturing_for_mybets(Common):
    """
    TR_ID: C62851779
    NAME: Verify GA tracking capturing for mybets
    DESCRIPTION: This test case verifies the GA tracking for messaging link through my bets
    PRECONDITIONS: User is logged FE
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_go_to_any_sport_and_add_single_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any sport and add single selection to betslip
        EXPECTED: Selection is displayed and  added to betslip
        """
        pass

    def test_003_verify_bet_receipt_displaying__after_clickingtapping_the_place_bet_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying  after clicking/tapping the 'Place Bet' button
        EXPECTED: .Bet is placed successfully
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: .Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_005_navigate_to_my_bets__open_bets_tab(self):
        """
        DESCRIPTION: Navigate to My bets- Open Bets tab
        EXPECTED: Placed bets is displayed ,Messaging component is displayed after bet placement as per CMS
        """
        pass

    def test_006_when_user_click_on_message_link(self):
        """
        DESCRIPTION: When user click on message link
        EXPECTED: Application will re-direct user to RG screen
        """
        pass

    def test_007_validate_the_ga_tracking_after_after_messaging_in_mybets(self):
        """
        DESCRIPTION: Validate the GA tracking after after messaging in mybets
        EXPECTED: 
        """
        pass
