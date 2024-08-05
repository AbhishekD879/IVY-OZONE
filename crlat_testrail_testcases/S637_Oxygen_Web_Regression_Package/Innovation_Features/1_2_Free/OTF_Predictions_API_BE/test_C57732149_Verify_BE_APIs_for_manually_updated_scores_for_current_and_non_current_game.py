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
class Test_C57732149_Verify_BE_APIs_for_manually_updated_scores_for_current_and_non_current_game(Common):
    """
    TR_ID: C57732149
    NAME: Verify BE APIs for manually updated scores for current and non-current game
    DESCRIPTION: This test case verifies BE APIs for manually updated scores for the current and non-current game
    PRECONDITIONS: - CSM link https://cms-api-ui-dev0.coralsports.dev.cloud.ladbrokescoral.com/one-two-free/
    PRECONDITIONS: - Kibana Logs https://search-ladbrokescoral-logs-dev-qwxuyxesgs3eucjfy33g534srq.eu-west-2.es.amazonaws.com/_plugin/kibana/app/kibana#/discover?_g=()&_a=(columns:!(log),filters:!(),index: otf-stats-dev0
    PRECONDITIONS: - In the CMS fined current active game and non-current game
    PRECONDITIONS: - Postman should be installed (file "postman_collection1" is attached)
    PRECONDITIONS: - env https://rooney-excalibur.ladbrokes.com/1-2-free
    PRECONDITIONS: - BigQuery user is logged in to Google Cloud Platform ( https://console.cloud.google.com/bigquery )
    PRECONDITIONS: - User is logged
    """
    keep_browser_open = True

    def test_001_go_to_the_postman_and_updated_the_scores_for_the_current_game(self):
        """
        DESCRIPTION: Go to the Postman and updated the scores for the current game
        EXPECTED: Scores are updated
        EXPECTED: response Status: 200
        """
        pass

    def test_002_go_bigquery_and_verify_that_scores_are_updatedselect_from_ladbrokes_big_query_12free_pl_resultsorder_by_resulteddate_des(self):
        """
        DESCRIPTION: Go BigQuery and verify that scores are updated
        DESCRIPTION: SELECT* FROM 'ladbrokes-big-query_12Free_PL_Results'
        DESCRIPTION: ORDER BY ResultedDate DES
        EXPECTED: scores are updated
        """
        pass

    def test_003_go_to_kibana_and_check_logs(self):
        """
        DESCRIPTION: Go to Kibana and check logs
        EXPECTED: Scores are present in the logs
        EXPECTED: Successfully added Game Results to BigQuery for Game
        """
        pass

    def test_004_reapit_1_3_steps_for_the_non_current_game(self):
        """
        DESCRIPTION: Reapit 1-3 steps for the non-current game
        EXPECTED: 
        """
        pass
