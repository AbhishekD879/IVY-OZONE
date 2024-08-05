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
class Test_C57732157_Verify_view_of_a_Question_page_and_transition(Common):
    """
    TR_ID: C57732157
    NAME: Verify view of a Question page and transition
    DESCRIPTION: This test case verifies view of a Question page and transition
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user is on the Splash page
    """
    keep_browser_open = True

    def test_001_tap_on_play_now_for_free(self):
        """
        DESCRIPTION: Tap on 'Play now for free'
        EXPECTED: - Question page displayed and designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002_select_answer(self):
        """
        DESCRIPTION: Select answer
        EXPECTED: - The Selected answer is highlighted
        EXPECTED: - The user is navigated to the next question after 2 seconds delay
        """
        pass
