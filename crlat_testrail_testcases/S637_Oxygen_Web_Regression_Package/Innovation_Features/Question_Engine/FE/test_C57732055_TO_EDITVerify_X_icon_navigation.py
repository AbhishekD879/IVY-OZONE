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
class Test_C57732055_TO_EDITVerify_X_icon_navigation(Common):
    """
    TR_ID: C57732055
    NAME: [TO-EDIT]Verify 'X' icon navigation
    DESCRIPTION: [THE CASE IS OUTDATED]:
    DESCRIPTION: -The toggle is called "Use back button to exit and hide X button" in CMS
    DESCRIPTION: -Mobile has the back button and 'X' button
    DESCRIPTION: -Desktop has one 'Exit'button
    DESCRIPTION: - The pop-up is an expected behavior
    DESCRIPTION: This test case verifies 'Back', 'X' navigation
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. Quiz which does not have a splash page (e.g Survey) configured
    PRECONDITIONS: 4. Toggle to use 'X' button turned ON on CMS
    """
    keep_browser_open = True

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - Quiz page successfully displayed
        EXPECTED: - 'X' icon displayed instead of the 'Back' button
        """
        pass

    def test_002___select_the_x_button_on_different_quiz_pages(self):
        """
        DESCRIPTION: - Select the 'X' button on different Quiz pages
        EXPECTED: - User will return to the URL page where they launched the quiz from
        EXPECTED: - User will not see the pop-up again after abandoning the quiz
        """
        pass

    def test_003___turn_off_toggle_to_use_x_on_cms__check_quiz_fe(self):
        """
        DESCRIPTION: - Turn OFF Toggle to use 'X' on CMS
        DESCRIPTION: - Check Quiz FE
        EXPECTED: - 'Back' icon displayed instead of the 'X' and return the user to the previous page
        """
        pass
