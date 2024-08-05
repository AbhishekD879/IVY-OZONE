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
class Test_C57732147_Verify_BE_APIs_for_manually_set_scores_for_non_current_game(Common):
    """
    TR_ID: C57732147
    NAME: Verify BE APIs for manually set scores for non-current game
    DESCRIPTION: This test case verifies BE APIs for manually set scores for the non-current  event in Postman
    PRECONDITIONS: - CSM https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints
    PRECONDITIONS: /one-two-free/
    PRECONDITIONS: - Kibana Logs https://search-ladbrokescoral-logs-dev-qwxuyxesgs3eucjfy33g534srq.eu-west-2.es.amazonaws.com/_plugin/kibana/app/kibana#/discover?_g=()&_a=(columns:!(log),filters:!(),index: otf-stats-dev0
    PRECONDITIONS: - Postman should be installed (file "postman_collection1" is attached)
    PRECONDITIONS: - env [domenname]/1-2-free
    PRECONDITIONS: - BigQuery user is logged in to Google Cloud Platform ( https://console.cloud.google.com/bigquery )
    PRECONDITIONS: - User is logged
    PRECONDITIONS: - In the CMS select non-current game
    """
    keep_browser_open = True

    def test_001_go_to_the_postman_and_sett_the_scores_for_non_current__game(self):
        """
        DESCRIPTION: Go to the Postman and sett the scores for non-current  game
        EXPECTED: Scores are setted
        EXPECTED: response Status: 200
        """
        pass

    def test_002_go_bigquery_and_verify_that_scores_are_set_in_the_tableselect_from_ladbrokes_big_query_12free_pl_resultsorder_by_resulteddate_desc(self):
        """
        DESCRIPTION: Go BigQuery and verify that scores are set in the table
        DESCRIPTION: SELECT* FROM 'ladbrokes-big-query_12Free_PL_Results'
        DESCRIPTION: ORDER BY ResultedDate DESC
        EXPECTED: scores are setted
        """
        pass

    def test_003_go_to_kibana_and_check_logs(self):
        """
        DESCRIPTION: Go to Kibana and check logs
        EXPECTED: Scores are present in the logs
        EXPECTED: Successfully added Game Results to BigQuery for Game ххх
        """
        pass
