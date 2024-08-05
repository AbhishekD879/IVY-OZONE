import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C22887901_Vanilla_Verify_Time_Managment_option(Common):
    """
    TR_ID: C22887901
    NAME: [Vanilla] Verify Time Managment option
    DESCRIPTION: This test case verifies redirection to a page where user can control time spending on gaming after certain steps being done on 'Gambling Controls' page.
    PRECONDITIONS: Load app
    PRECONDITIONS: Prepare users:
    PRECONDITIONS: (Users should be real-money players - at least one deposit is done in the past)
    PRECONDITIONS: 1) UK user
    PRECONDITIONS: 2) non UK user
    PRECONDITIONS: Steps:
    PRECONDITIONS: Navigate to My Account -> Gambling Controls
    PRECONDITIONS: Select 'Time Management' option and tap/click 'CHOOSE'
    """
    keep_browser_open = True

    def test_001_log_in_as_a_user_1uk_and_do_steps_from_preconditions(self):
        """
        DESCRIPTION: Log in as a user #1(UK) and do steps from preconditions
        EXPECTED: User is redirected to **Time management** page.
        """
        pass

    def test_002_log_out_from_the_app(self):
        """
        DESCRIPTION: Log out from the App
        EXPECTED: 
        """
        pass

    def test_003_log_in_as_a_user_2non_uk_and_try_to_repeat_steps_from_preconditions(self):
        """
        DESCRIPTION: Log in as a user #2(non UK) and try to repeat steps from preconditions
        EXPECTED: 'Time Management' option is not available for non UK players
        """
        pass
