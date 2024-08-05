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
class Test_C57732145_Verify_BE_APIs_for_OTF_Predictions(Common):
    """
    TR_ID: C57732145
    NAME: Verify BE APIs for OTF-Predictions
    DESCRIPTION: This test case verifies BE APIs for OTF-Predictions using Postman collection
    PRECONDITIONS: CMS API specification (coral/admin):
    PRECONDITIONS: https://cms-dev0.coralsports.dev.cloud.ladbrokescoral.com
    PRECONDITIONS: 1. Actual version of Collection and Environment imported to Postman: https://confluence.egalacoral.com/display/SPI/OTF+API+Test+Cases+-+Postman
    PRECONDITIONS: 2. Select actual testing Environment by changing {{env}} variable to: dev0, dev1, dev2 and {{brand}} variable to: ladbrokes, bma
    PRECONDITIONS: 3. Login using 'CMS Login' POST method from 1-2-Free collection
    PRECONDITIONS: 4. Valid 'gameId' and unique 'userId', 'customerId' set in POST Prediction body
    """
    keep_browser_open = True

    def test_001___open_postman_collection_runner_and_choose_folder_1_2_free__otf_predictions__select_imported_environment_1_2_free__run_testing_by_clicking_or_run_game_button(self):
        """
        DESCRIPTION: - Open Postman Collection Runner and choose folder: '1-2-Free > OTF-Predictions'
        DESCRIPTION: - Select imported Environment: '1-2-Free'
        DESCRIPTION: - Run testing by clicking or 'Run Game' button
        EXPECTED: All described tests should return **PASSED** status:
        EXPECTED: - Status code is 200
        EXPECTED: - Status code is 201
        EXPECTED: - Status code is 204
        EXPECTED: - Status code is 404
        EXPECTED: - Response is valid and have a body
        EXPECTED: - Body matches string
        EXPECTED: - Response value equal request value
        EXPECTED: - Response ID different from request ID
        """
        pass

    def test_002___run_prediction_post_method_with_same_values__verify_body_response(self):
        """
        DESCRIPTION: - Run 'Prediction' POST method with same values
        DESCRIPTION: - Verify body response
        EXPECTED: - All tests for current method should return **FAIL** status
        EXPECTED: - Body consist:
        EXPECTED: {
        EXPECTED: "httpStatus": "BAD_REQUEST",
        EXPECTED: "reason": "GamePredictions with id 'UserID.GameID' already exists"
        EXPECTED: }
        """
        pass

    def test_003___open_add_actual_scores_put_method__set_valid_eventids_and_actualscores_for_current_active_game__run_method__verify_actualscores_for_events(self):
        """
        DESCRIPTION: - Open 'Add actual scores' PUT method
        DESCRIPTION: - Set valid eventIds and actualScores for Current active game
        DESCRIPTION: - Run method
        DESCRIPTION: - Verify actualScores for events
        EXPECTED: - actualScores for particular events successfully updated
        EXPECTED: - changes reflected to OTF
        """
        pass
