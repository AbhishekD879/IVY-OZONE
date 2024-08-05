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
class Test_C62851777_Verify_GA_tracking_capturing_when_placing_bet_through_betslip(Common):
    """
    TR_ID: C62851777
    NAME: Verify  GA tracking capturing when placing bet through betslip
    DESCRIPTION: This test case verifies the GA tracking for messaging link through betslip
    PRECONDITIONS: User is logged FE
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_go_to_any_sports_and_add_selection_to_betslip(self):
        """
        DESCRIPTION: Go to any sports and add selection to betslip
        EXPECTED: Selection is added to betslip
        """
        pass

    def test_003_check_the_messaging_in_betslip(self):
        """
        DESCRIPTION: Check the Messaging in Betslip
        EXPECTED: Messaging component is displayed prior to bet placement as per CMS config
        """
        pass

    def test_004_validate_the_ga_tracking_after_after_messaging_in_betslip(self):
        """
        DESCRIPTION: Validate the GA tracking after after messaging in betslip
        EXPECTED: 
        """
        pass
