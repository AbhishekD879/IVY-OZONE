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
class Test_C57731991_Verify_getting_predictions_for_user_with_current_username(Common):
    """
    TR_ID: C57731991
    NAME: Verify getting predictions for user with current 'username'
    DESCRIPTION: This test case verifies getting predictions for user with current 'username'
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    PRECONDITIONS: 3. User made prediction previously for this Active Game
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link
        EXPECTED: User successfully navigated to 1-2-Free
        """
        pass

    def test_002_open_browser_network__xhr_requests_eg_httpsotf_hlv0coralsportsnonprodcloudladbrokescoralcomapiv1initial_datausername(self):
        """
        DESCRIPTION: Open browser Network > XHR requests (e.g. https://otf-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/initial-data/'username')
        EXPECTED: GET request for predictions exits with valid keys:
        EXPECTED: - userId
        EXPECTED: - game Id
        EXPECTED: - eventPredictions
        EXPECTED: - customerId
        EXPECTED: - resulted
        """
        pass
