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
class Test_C57732069_Verify_Submit_message(Common):
    """
    TR_ID: C57732069
    NAME: Verify 'Submit' message
    DESCRIPTION: This test case verifies 'Submit' message
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    """
    keep_browser_open = True

    def test_001___open_correct_4__submit_final_answers(self):
        """
        DESCRIPTION: - Open Correct 4
        DESCRIPTION: - Submit final answers
        EXPECTED: - User navigated to the Latest Tab (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ac05f3d5241970342
        EXPECTED: - Green stripe with Submit message text displayed (message will fade away after 3sec)
        """
        pass

    def test_002_user_tap_on_previous_tab_and_open_again_latest_tab(self):
        """
        DESCRIPTION: User tap on Previous Tab and open again Latest Tab
        EXPECTED: - Latest Tab succssefuly opened
        EXPECTED: - Submit message text should not be displayed
        EXPECTED: - Information about Latest game is correctly displayed
        """
        pass
