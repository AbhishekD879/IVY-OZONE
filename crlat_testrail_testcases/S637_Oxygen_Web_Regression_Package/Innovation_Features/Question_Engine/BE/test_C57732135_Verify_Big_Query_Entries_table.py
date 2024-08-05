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
class Test_C57732135_Verify_Big_Query_Entries_table(Common):
    """
    TR_ID: C57732135
    NAME: Verify Big Query 'Entries' table
    DESCRIPTION: This test case verifies Big Query 'Entries' table
    PRECONDITIONS: Please look for some insights on pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to Coral/Ladbrokes
    PRECONDITIONS: 2. The user is logged in to Google Cloud Platform ( https://console.cloud.google.com/bigquery )
    PRECONDITIONS: 3. Active quiz already exist
    """
    keep_browser_open = True

    def test_001___open_correct_4__submit_answers(self):
        """
        DESCRIPTION: - Open Correct 4
        DESCRIPTION: - Submit answers
        EXPECTED: Answers successfully submitted
        """
        pass

    def test_002___open_big_query_service_httpsconsolecloudgooglecombigquery__find_table_in_left_sidebar_by_path_ladbrokes_big_query__question_engine__entries_valuesql_requestselect__from_ladbrokes_big_queryquestion_engineentries_devorder_by_createddatedesc(self):
        """
        DESCRIPTION: - Open Big Query service: https://console.cloud.google.com/bigquery
        DESCRIPTION: - Find Table in left sidebar by path 'ladbrokes-big-query > Question_Engine > Entries_[value]'
        DESCRIPTION: **SQL request:**
        DESCRIPTION: ```SELECT * FROM `ladbrokes-big-query.Question_Engine.Entries_DEV`
        DESCRIPTION: ORDER BY CreatedDate
        DESCRIPTION: DESC```
        EXPECTED: Table successfully opened and has the following columns
        EXPECTED: (Represent user submission (specific answers to the Quiz questions)):
        EXPECTED: - Brand
        EXPECTED: - Game
        EXPECTED: - GameID
        EXPECTED: - CustomerID
        EXPECTED: - Username
        EXPECTED: - CreatedDate
        EXPECTED: - EventID
        EXPECTED: - Predictions
        EXPECTED: - GameStartDate
        EXPECTED: - GameEndDate
        """
        pass

    def test_003___open_correct_4_using_different_login_credentials__submit_answers(self):
        """
        DESCRIPTION: - Open Correct 4 using different login credentials
        DESCRIPTION: - Submit answers
        EXPECTED: Answers successfully submitted
        """
        pass

    def test_004___open_big_query_service_httpsconsolecloudgooglecombigquery__find_table_in_left_sidebar_by_path_ladbrokes_big_query__question_engine__entries_valuesql_requestselect__from_ladbrokes_big_queryquestion_engineentries_devorder_by_createddatedesc(self):
        """
        DESCRIPTION: - Open Big Query service: https://console.cloud.google.com/bigquery
        DESCRIPTION: - Find Table in left sidebar by path 'ladbrokes-big-query > Question_Engine > Entries_[value]'
        DESCRIPTION: **SQL request:**
        DESCRIPTION: ```SELECT * FROM `ladbrokes-big-query.Question_Engine.Entries_DEV`
        DESCRIPTION: ORDER BY CreatedDate
        DESCRIPTION: DESC```
        EXPECTED: Table successfully opened and has the following columns
        EXPECTED: (Represent user submission (specific answers to the Quiz questions):
        EXPECTED: - Brand
        EXPECTED: - Game
        EXPECTED: - GameID
        EXPECTED: - CustomerID
        EXPECTED: - Username
        EXPECTED: - CreatedDate
        EXPECTED: - EventID
        EXPECTED: - Predictions
        EXPECTED: - GameStartDate
        EXPECTED: - GameEndDate
        """
        pass
