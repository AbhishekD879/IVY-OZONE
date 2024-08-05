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
class Test_C57732062_Verify_Turning_On_Off_of_End_Page_blocks(Common):
    """
    TR_ID: C57732062
    NAME: Verify Turning On/Off of  'End Page' blocks
    DESCRIPTION: This test case verifies 'Answers Summary' with results
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user has completed a quiz and results are set in CMS
    PRECONDITIONS: 4. All End page toggles Turned ON
    PRECONDITIONS: 5. Upsell configured
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

    def test_002_turn_upsell_toggle_off__save_changes__open_end_page(self):
        """
        DESCRIPTION: Turn Upsell toggle: OFF
        DESCRIPTION: - Save Changes
        DESCRIPTION: - Open End page
        EXPECTED: Upsell block NOT displayed on End Page
        """
        pass

    def test_003_turn_results_toggle_off__save_changes__open_end_page(self):
        """
        DESCRIPTION: Turn Results toggle: OFF
        DESCRIPTION: - Save Changes
        DESCRIPTION: - Open End page
        EXPECTED: Results block NOT displayed on End Page
        EXPECTED: (Answer Summary toggle should be ON to show results)
        """
        pass

    def test_004_turn_answer_summary_toggle_off__save_changes__open_end_page(self):
        """
        DESCRIPTION: Turn Answer Summary toggle: OFF
        DESCRIPTION: - Save Changes
        DESCRIPTION: - Open End page
        EXPECTED: Answer Summary block NOT displayed on End Page
        """
        pass

    def test_005_turn_prizes_toggle_off__save_changes__open_end_page(self):
        """
        DESCRIPTION: Turn Prizes toggle: OFF
        DESCRIPTION: - Save Changes
        DESCRIPTION: - Open End page
        EXPECTED: Prizes block NOT displayed on End Page
        """
        pass
