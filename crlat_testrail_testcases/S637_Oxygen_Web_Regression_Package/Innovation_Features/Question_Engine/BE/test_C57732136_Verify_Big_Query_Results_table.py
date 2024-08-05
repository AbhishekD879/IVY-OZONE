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
class Test_C57732136_Verify_Big_Query_Results_table(Common):
    """
    TR_ID: C57732136
    NAME: Verify Big Query 'Results' table
    DESCRIPTION: This test case verifies Big Query 'Results' table
    PRECONDITIONS: Please look for some insights on pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Google Cloud Platform ( https://console.cloud.google.com/bigquery )
    PRECONDITIONS: 3. Active quiz already exist
    PRECONDITIONS: 4. Entry deadline in past
    """
    keep_browser_open = True

    def test_001___open_cms__put_correct_answer_mark_for_a_few_questions__save_changes(self):
        """
        DESCRIPTION: - Open CMS
        DESCRIPTION: - Put 'Correct' answer mark for a few Questions
        DESCRIPTION: - Save changes
        EXPECTED: Changes successfully saved
        """
        pass

    def test_002___open_big_query_service_httpsconsolecloudgooglecombigquery__find_table_in_left_sidebar_by_path_ladbrokes_big_query__question_engine__results_valuesql_requestselect__from_ladbrokes_big_queryquestion_engineresults_devorder_by_resulteddatedesc(self):
        """
        DESCRIPTION: - Open Big Query service: https://console.cloud.google.com/bigquery
        DESCRIPTION: - Find Table in left sidebar by path 'ladbrokes-big-query > Question_Engine > Results_[value]'
        DESCRIPTION: **SQL request:**
        DESCRIPTION: ```SELECT * FROM `ladbrokes-big-query.Question_Engine.Results_DEV`
        DESCRIPTION: ORDER BY ResultedDate
        DESCRIPTION: DESC```
        EXPECTED: Table successfully opened and has the following columns
        EXPECTED: (Represents correct answers to a specific Quiz):
        EXPECTED: - Brand
        EXPECTED: - Game
        EXPECTED: - GameID
        EXPECTED: - Resulted
        EXPECTED: - Question_Number
        EXPECTED: - Answer_option
        EXPECTED: **NOTE:**
        EXPECTED: Will be populated as soon as Quiz is regarded as resulted (each Question has 'Correct Answer' mark)
        EXPECTED: A new record is added each time CMS user makes changes to the resulted Quiz
        """
        pass

    def test_003___open_cms_again__put_correct_answer_mark_for_different_to_previous_set_questions__save_changes(self):
        """
        DESCRIPTION: - Open CMS again
        DESCRIPTION: - Put 'Correct' answer mark for different to previous set Questions
        DESCRIPTION: - Save changes
        EXPECTED: Changes successfully saved
        """
        pass

    def test_004___open_big_query_service_httpsconsolecloudgooglecombigquery__find_table_in_left_sidebar_by_path_ladbrokes_big_query__question_engine__results_valuesql_requestselect__from_ladbrokes_big_queryquestion_engineresults_devorder_by_resulteddatedesc(self):
        """
        DESCRIPTION: - Open Big Query service: https://console.cloud.google.com/bigquery
        DESCRIPTION: - Find Table in left sidebar by path 'ladbrokes-big-query > Question_Engine > Results_[value]'
        DESCRIPTION: **SQL request:**
        DESCRIPTION: ```SELECT * FROM `ladbrokes-big-query.Question_Engine.Results_DEV`
        DESCRIPTION: ORDER BY ResultedDate
        DESCRIPTION: DESC```
        EXPECTED: Table successfully opened and has the following columns
        EXPECTED: (Represents correct answers to a specific Quiz):
        EXPECTED: - Brand
        EXPECTED: - Game
        EXPECTED: - GameID
        EXPECTED: - Resulted
        EXPECTED: - Question_Number
        EXPECTED: - Answer_option
        EXPECTED: **NOTE:**
        EXPECTED: Will be populated as soon as Quiz is regarded as resulted (each Question has 'Correct Answer' mark)
        EXPECTED: A new record is added each time CMS user makes changes to the resulted Quiz
        """
        pass
