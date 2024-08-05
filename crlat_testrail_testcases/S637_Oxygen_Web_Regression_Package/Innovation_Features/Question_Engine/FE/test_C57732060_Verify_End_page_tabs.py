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
class Test_C57732060_Verify_End_page_tabs(Common):
    """
    TR_ID: C57732060
    NAME: Verify 'End' page tabs
    DESCRIPTION: This test case verifies 'End' page tabs
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
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a
        EXPECTED: - All data retrieved from CMS and correctly displayed
        """
        pass

    def test_002_user_tap_on_latest_tab(self):
        """
        DESCRIPTION: User tap on Latest Tab
        EXPECTED: - Latest Tab successfully opened
        EXPECTED: - Submit message text displayed according to configuration on CMS
        EXPECTED: - Information about Latest game is correctly displayed
        """
        pass

    def test_003_user_tap_on_previous_tab(self):
        """
        DESCRIPTION: User tap on Previous Tab
        EXPECTED: - Previous Tab successfully opened
        EXPECTED: - Information about Previous game is correctly displayed
        """
        pass
