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
class Test_C57732043_Verify_the_restriction_of_a_game_from_the_Submit_pop_up_for_a_User_with_KYC_Account_in_review_status(Common):
    """
    TR_ID: C57732043
    NAME: Verify the restriction of a game from the 'Submit' pop-up for a User with KYC 'Account in review' status
    DESCRIPTION: This test case verifies the restriction of game from the 'Submit' pop-up for a User with KYC 'Account in review' status.
    PRECONDITIONS: 1. The CMS has been configured as 'Log in to submit' (the 'SUBMIT' option is selected in the 'Login rule' field).
    PRECONDITIONS: 2. The User is logged out.
    PRECONDITIONS: 3. The User has a KYC 'Account in review' status.
    """
    keep_browser_open = True

    def test_001_tap_on_the_submit_cta_log_in_to_submit(self):
        """
        DESCRIPTION: Tap on the submit CTA (Log in to submit).
        EXPECTED: The Login pop-up is opened.
        """
        pass

    def test_002_enter_valid_credentials(self):
        """
        DESCRIPTION: Enter valid credentials.
        EXPECTED: The 'Account in review' pop-up is displayed.
        """
        pass
