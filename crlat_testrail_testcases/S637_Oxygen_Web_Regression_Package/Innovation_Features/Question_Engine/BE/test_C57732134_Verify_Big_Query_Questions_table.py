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
class Test_C57732134_Verify_Big_Query_Questions_table(Common):
    """
    TR_ID: C57732134
    NAME: Verify Big Query 'Questions' table
    DESCRIPTION: This test case verifies Big Query 'Questions' table
    PRECONDITIONS: Please look for some insights on pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged in to CMS
    PRECONDITIONS: 2. The user is logged in to Google Cloud Platform ( https://console.cloud.google.com/bigquery )
    PRECONDITIONS: 3. Active quiz already exist
    """
    keep_browser_open = True

    def test_001___open_cms__change_entry_deadline_to_past_for_active_quiz__save_changes(self):
        """
        DESCRIPTION: - Open CMS
        DESCRIPTION: - Change Entry Deadline to past for active Quiz
        DESCRIPTION: - Save changes
        EXPECTED: Changes successfully saved
        """
        pass

    def test_002___open_big_query_service_httpsconsolecloudgooglecombigquery__find_table_in_left_sidebar_by_path_ladbrokes_big_query__question_engine__questions_valuesql_requestselect__from_ladbrokes_big_queryquestion_enginequestions_devorder_by_uploadeddatedesc(self):
        """
        DESCRIPTION: - Open Big Query service: https://console.cloud.google.com/bigquery
        DESCRIPTION: - Find Table in left sidebar by path 'ladbrokes-big-query > Question_Engine > Questions_[value]'
        DESCRIPTION: **SQL request:**
        DESCRIPTION: ```SELECT * FROM `ladbrokes-big-query.Question_Engine.Questions_DEV`
        DESCRIPTION: ORDER BY UploadedDate
        DESCRIPTION: DESC```
        EXPECTED: Table successfully opened and has the following columns:
        EXPECTED: - Brand
        EXPECTED: - Game
        EXPECTED: - GameID
        EXPECTED: - GameStartDate
        EXPECTED: - GameEndDate
        EXPECTED: - Event
        EXPECTED: - Question_Number
        EXPECTED: - Question_Text
        EXPECTED: - Answer_Option
        EXPECTED: - Answer_Text
        """
        pass
