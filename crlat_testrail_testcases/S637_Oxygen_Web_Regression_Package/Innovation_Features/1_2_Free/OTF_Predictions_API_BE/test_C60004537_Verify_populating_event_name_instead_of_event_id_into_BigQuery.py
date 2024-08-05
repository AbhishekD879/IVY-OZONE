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
class Test_C60004537_Verify_populating_event_name_instead_of_event_id_into_BigQuery(Common):
    """
    TR_ID: C60004537
    NAME: Verify populating event name instead of event id into BigQuery
    DESCRIPTION: This test case verifies populating event name instead of event id into BigQuery
    PRECONDITIONS: - CSM https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=CMS-API+Endpoints /one-two-free/
    PRECONDITIONS: - BigQuery user is logged in to Google Cloud Platform ( https://console.cloud.google.com/bigquery )
    PRECONDITIONS: - User is logged
    PRECONDITIONS: - In the CMS create one current active game and add 3 event ids (active can be just one game)
    """
    keep_browser_open = True

    def test_001_open_app_and_set_predictions(self):
        """
        DESCRIPTION: Open app and set predictions
        EXPECTED: Predictions are setted
        """
        pass

    def test_002___go_bigquery_and_run_the_queryselect__from_ladbrokes_big_queryrooney_12free1_2_free_pl_raw_entries_order_by_createddate_desc__verify_the_table_column_event1_event2_event3(self):
        """
        DESCRIPTION: - Go BigQuery and Run the query:
        DESCRIPTION: SELECT * FROM `ladbrokes-big-query.Rooney_12Free.1_2_Free_PL_RAW_Entries` order by CreatedDate desc
        DESCRIPTION: - Verify the Table column 'Event1', 'Event2', 'Event3'
        EXPECTED: In the Table column 'Event1', 'Event2', 'Event3'	event name is instead of event id
        """
        pass
