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
class Test_C57732059_Verify_view_and_data_on_End_page(Common):
    """
    TR_ID: C57732059
    NAME: Verify view and data on 'End' page
    DESCRIPTION: This test case verifies view and data on 'End' page
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. The user has completed a quiz and submit my final answers
    """
    keep_browser_open = True

    def test_001_tap_on_correct_4_link(self):
        """
        DESCRIPTION: Tap on Correct 4 link
        EXPECTED: - User navigated to the end page (Results page) and it designed accordingly:
        EXPECTED: Latest tab (no results):
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887b0ee7db716c262a26f
        EXPECTED: Latest tab (with results):
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887afc14b1a61fd80d1d0
        EXPECTED: Previous tab:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d8887ae6f32f30287e19caa
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002___make_changes_to_each_field_on_cms__question_enginee__end_page__endpage__save_changes(self):
        """
        DESCRIPTION: - Make changes to each field on CMS > Question Enginee > End Page > [endpage]
        DESCRIPTION: - Save changes
        EXPECTED: Changes saved on CMS
        """
        pass

    def test_003_open_end_page_again(self):
        """
        DESCRIPTION: Open 'End' page again
        EXPECTED: - All data retrieved from CMS and correctly displayed
        EXPECTED: - All successfully styled
        """
        pass
