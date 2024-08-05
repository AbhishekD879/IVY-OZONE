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
class Test_C9272845_Verify_Quick_Deposit_stand_alone_section_after_logout(Common):
    """
    TR_ID: C9272845
    NAME: Verify 'Quick Deposit' stand alone section after logout
    DESCRIPTION: This test case verifies 'Quick Deposit' stand alone section after logout
    DESCRIPTION: AUTOTEST
    DESCRIPTION: MOBILE: [C24102243]
    PRECONDITIONS: 1. App is loaded;
    PRECONDITIONS: 2. User has credit cards added to his account;
    PRECONDITIONS: 3. User is logged in;
    PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    PRECONDITIONS: 5. In order to trigger case when the session is over, perform the next steps:
    PRECONDITIONS: - Log in to one browser tab;
    PRECONDITIONS: - Duplicate tab;
    PRECONDITIONS: - Log out from the second tab -> session is over in both tabs.
    """
    keep_browser_open = True

    def test_001_follow_step_4_from_preconditions(self):
        """
        DESCRIPTION: Follow step 4 from Preconditions
        EXPECTED: User session is over
        """
        pass

    def test_002_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify 'Quick Deposit' section
        EXPECTED: - Quick Deposit section is NOT displayed anymore
        EXPECTED: - 'Log out' pop up is displayed
        """
        pass
