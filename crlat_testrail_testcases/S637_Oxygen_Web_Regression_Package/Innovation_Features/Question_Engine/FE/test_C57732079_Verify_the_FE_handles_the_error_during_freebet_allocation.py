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
class Test_C57732079_Verify_the_FE_handles_the_error_during_freebet_allocation(Common):
    """
    TR_ID: C57732079
    NAME: Verify the FE handles the error during freebet allocation
    DESCRIPTION: This test case verifies that the FE handles the error during freebet allocation.
    PRECONDITIONS: 1. The CMS User is logged in.
    PRECONDITIONS: 2. Navigate to the 'Prizes' tab of an active Quiz.
    PRECONDITIONS: 3. Select the "Token" value in the 'Submit' row.
    PRECONDITIONS: 4. Set an invalid promotion id in the 'Promotion Id' field.
    PRECONDITIONS: 5. Click the 'Save Changes' button.
    PRECONDITIONS: 6. Click the 'Yes' button.
    PRECONDITIONS: For more information please consider heh provided instructions:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+instantly+assign+free+bets+for+a+user+from+BE
    """
    keep_browser_open = True

    def test_001_open_a_quiz(self):
        """
        DESCRIPTION: Open a Quiz.
        EXPECTED: The Quiz is displayed.
        """
        pass

    def test_002_select_any_option(self):
        """
        DESCRIPTION: Select any option.
        EXPECTED: 1. The User is redirected to the Home page.
        EXPECTED: 2. The freebet amount is not increased.
        """
        pass
