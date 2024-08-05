import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732120_Verify_submit_of_User_predictions(Common):
    """
    TR_ID: C57732120
    NAME: Verify submit of User predictions
    DESCRIPTION: This test case verifies submit of User predictions
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
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

    def test_002_choose_scores_and_tap_on_submit_button(self):
        """
        DESCRIPTION: Choose scores and Tap on 'Submit' button
        EXPECTED: - FE send POST /api/v1/prediction with Game Id and User ID and body (see Swagger for actual request example)
        EXPECTED: - user should be navigated to 'You are in'
        """
        pass
