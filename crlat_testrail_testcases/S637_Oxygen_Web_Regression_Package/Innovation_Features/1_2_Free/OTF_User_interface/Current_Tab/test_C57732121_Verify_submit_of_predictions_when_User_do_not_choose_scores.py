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
class Test_C57732121_Verify_submit_of_predictions_when_User_do_not_choose_scores(Common):
    """
    TR_ID: C57732121
    NAME: Verify submit of predictions when User do not choose scores
    DESCRIPTION: This test case verifies submit of predictions when User do not chose scores
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: 'Current Tab' is successfully opened
        """
        pass

    def test_002_do_not_choose_scores_and_tap_on_submit_button(self):
        """
        DESCRIPTION: Do NOT choose scores and Tap on 'Submit' button
        EXPECTED: FE should send POST /api/v1/prediction with Game ID and User ID and body (see Swagger for actual request example)
        EXPECTED: **where scores is 0-0**
        """
        pass
