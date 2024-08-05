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
class Test_C57732065_Verify_prize_indication_for_Answers_Summary(Common):
    """
    TR_ID: C57732065
    NAME: Verify prize indication for 'Answers Summary'
    DESCRIPTION: This test case verifies 'Answers Summary' on 'Latest' Tab
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user has completed a quiz and results are available in CMS
    """
    keep_browser_open = True

    def test_001___tap_on_correct_4_link__tap_on_see_previous_results_button(self):
        """
        DESCRIPTION: - Tap on Correct 4 link
        DESCRIPTION: - Tap on 'See previous results' button
        EXPECTED: - User navigated to the end page (Results page) and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d962a2ffb679bba35fce2
        EXPECTED: - All data retrieved from CMS and correctly displayed
        EXPECTED: - Footer text displayed retrieved from 'End Page > Game Description' field
        """
        pass

    def test_002___change_correct_answers_on_cms_selectcms__question_enginee__activequiz__question_tab__save_changes(self):
        """
        DESCRIPTION: - Change correct answers on CMS, select
        DESCRIPTION: CMS > Question Enginee > [activequiz] > Question tab
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        pass

    def test_003___open_correct_4_again(self):
        """
        DESCRIPTION: - Open Correct 4 again
        EXPECTED: Prize indicator in the corner of answer card displayed according to changes:
        EXPECTED: - If user WON 1st prize: Show amount £ in green
        EXPECTED: - If user WON 2nd prize: Show amount £ in amber
        EXPECTED: - If user LOST: Show red corner with lost icon Leave Blank
        """
        pass

    def test_004___change_event_scores_on_cms_selectcms__question_enginee__activequiz__event_details_tab__save_changes(self):
        """
        DESCRIPTION: - Change Event Scores on CMS, select
        DESCRIPTION: CMS > Question Enginee > [activequiz] > Event details tab
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        pass

    def test_005___open_correct_4_again(self):
        """
        DESCRIPTION: - Open Correct 4 again
        EXPECTED: Game Header with results displayed according to changes:
        EXPECTED: - **Arsenal 2** (Win team displayed bold)
        EXPECTED: - Watford 0
        """
        pass
