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
class Test_C57732042_Verify_the_restriction_of_a_game_from_the_Splash_page_for_a_User_with_KYC_Account_in_review_status(Common):
    """
    TR_ID: C57732042
    NAME: Verify the restriction of a game from the Splash page for a User with KYC 'Account in  review' status
    DESCRIPTION: This test case verifies the restriction of game from the Splash page for a User with KYC 'Account in review' status.
    PRECONDITIONS: 1. The CMS has been configured as 'Log in to view' (the 'START' option is selected in the 'Login rule' field).
    PRECONDITIONS: 2. The User is logged out.
    PRECONDITIONS: 3. The User has a KYC 'Account in  review' status.
    """
    keep_browser_open = True

    def test_001_tap_on_the_cta_to_start_the_quiz_log_in_to_play_for_free(self):
        """
        DESCRIPTION: Tap on the CTA to start the quiz (Log in to Play for free).
        EXPECTED: The Login pop-up is opened.
        """
        pass

    def test_002_enter_valid_credentials(self):
        """
        DESCRIPTION: Enter valid credentials.
        EXPECTED: The 'Account in review' pop-up is displayed.
        """
        pass
