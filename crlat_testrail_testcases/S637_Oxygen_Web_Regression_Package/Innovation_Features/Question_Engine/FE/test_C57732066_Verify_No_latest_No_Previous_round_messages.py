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
class Test_C57732066_Verify_No_latest_No_Previous_round_messages(Common):
    """
    TR_ID: C57732066
    NAME: Verify 'No latest/No Previous round' messages
    DESCRIPTION: This test case verifies 'No latest/No Previous round' messages
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Coral/Ladbrokes test environment
    PRECONDITIONS: 3. There are not active quizzes
    PRECONDITIONS: 3. The user is not played previous quizzes
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
        EXPECTED: - Latest Tab succssefuly opened and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d9629fcbfc79bf47f04d5
        EXPECTED: - 'No Latest rounds' message displayed underneath the tab headers
        """
        pass

    def test_003_user_tap_on_previous_tab(self):
        """
        DESCRIPTION: User tap on Previous Tab
        EXPECTED: - Previous Tab succssefuly opened and it designed accordingly:
        EXPECTED: https://app.zeplin.io/project/5d4b121f8d5c26520b23a39a/screen/5d4d96290d6e049b180969b8
        EXPECTED: - 'No Previous rounds' message displayed underneath the tab headers
        """
        pass
