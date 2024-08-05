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
class Test_C57732063_Verify_Answers_Summary_without_results(Common):
    """
    TR_ID: C57732063
    NAME: Verify 'Answers Summary' without results
    DESCRIPTION: This test case verifies 'Answers Summary' on 'Latest' Tab
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user has completed a quiz and results are not yet available in CMS
    """
    keep_browser_open = True

    def test_001___tap_on_correct_4_link__tap_on_see_previous_results_button(self):
        """
        DESCRIPTION: - Tap on Correct 4 link
        DESCRIPTION: - Tap on 'See previous results' button
        EXPECTED: - User navigated to the end page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962ac05f3d5241970342
        EXPECTED: - All data retrieved from CMS and correctly displayed
        EXPECTED: I will see a summary of the questions and my answers as per the attached design as follows:
        EXPECTED: - Header (Your Answers)
        EXPECTED: - Question Numbers
        EXPECTED: - Question
        EXPECTED: - User's answer (formatted bold)
        """
        pass
