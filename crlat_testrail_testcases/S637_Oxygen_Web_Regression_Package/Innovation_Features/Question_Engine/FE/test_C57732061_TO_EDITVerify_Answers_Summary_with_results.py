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
class Test_C57732061_TO_EDITVerify_Answers_Summary_with_results(Common):
    """
    TR_ID: C57732061
    NAME: [TO-EDIT]Verify 'Answers Summary' with results
    DESCRIPTION: [TO-EDIT] step 2 needs editing
    DESCRIPTION: This test case verifies 'Answers Summary' with results
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user has completed a quiz and results are set in CMS
    """
    keep_browser_open = True

    def test_001___tap_on_correct_4_link__tap_on_see_your_results_button(self):
        """
        DESCRIPTION: - Tap on Correct 4 link
        DESCRIPTION: - Tap on 'See your results' button
        EXPECTED: - User navigated to the Latest tab on End page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a2ffb679bba35fce2
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002___change_entry_deadline_to_past__tap_on_correct_4_link__tap_on_see_previous_results_button(self):
        """
        DESCRIPTION: - Change Entry deadline to past
        DESCRIPTION: - Tap on Correct 4 link
        DESCRIPTION: - Tap on 'See previous results' button
        EXPECTED: - User navigated to the Previous tab on End page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a8847a29b543109bd
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass
