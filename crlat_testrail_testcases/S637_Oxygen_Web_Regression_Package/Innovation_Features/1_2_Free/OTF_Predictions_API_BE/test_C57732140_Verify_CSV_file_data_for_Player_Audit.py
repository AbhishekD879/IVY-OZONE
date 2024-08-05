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
class Test_C57732140_Verify_CSV_file_data_for_Player_Audit(Common):
    """
    TR_ID: C57732140
    NAME: Verify CSV file data for Player Audit
    DESCRIPTION: This test case verifies generating CSV for Player Audit
    PRECONDITIONS: 1. Permission to CSV file on S3 provided (e.g. https://s3.eu-west-2.amazonaws.com/otf-dev0/Germany League 9-17 Feb-2019-02-18_11-21-59.csv)
    """
    keep_browser_open = True

    def test_001_open_httpss3eu_west_2amazonawscomotf_dev0(self):
        """
        DESCRIPTION: Open https://s3.eu-west-2.amazonaws.com/otf-dev0
        EXPECTED: - XML page successfully opened
        EXPECTED: - XML structure displayed:
        EXPECTED: <Contents>
        EXPECTED: <Key>Germany League 9-17 Feb-2019-02-19_11-25-00.csv</Key>
        EXPECTED: <LastModified>2019-02-19T11:25:01.000Z</LastModified>
        EXPECTED: <ETag>"8be748f1056d187aa8e925d2741ca6d2"</ETag>
        EXPECTED: <Size>320949</Size>
        EXPECTED: <StorageClass>STANDARD</StorageClass>
        EXPECTED: </Contents>
        """
        pass

    def test_002_add_tag_key_to_url_from_step_1_to_make_path_to_csveg_httpss3eu_west_2amazonawscomotf_dev0germany_league_9_17_feb_2019_02_19_11_25_00csvopen_output_url(self):
        """
        DESCRIPTION: Add tag <Key> to URL from Step 1 to make path to CSV
        DESCRIPTION: (e.g. https://s3.eu-west-2.amazonaws.com/otf-dev0/Germany League 9-17 Feb-2019-02-19_11-25-00.csv)
        DESCRIPTION: Open output URL
        EXPECTED: CSV File successfully downloaded
        """
        pass

    def test_003_open_downloaded_csv(self):
        """
        DESCRIPTION: Open downloaded CSV
        EXPECTED: CSV has data from previous user predictions
        EXPECTED: CSV structure:
        EXPECTED: - Customer_ID
        EXPECTED: - Username
        EXPECTED: - GameID
        EXPECTED: - CreatedDate
        EXPECTED: - Correct
        EXPECTED: - EventId1
        EXPECTED: - Prediction1
        EXPECTED: - Result1
        EXPECTED: - EventId2
        EXPECTED: - Prediction2
        EXPECTED: - Result2
        EXPECTED: - EventId3
        EXPECTED: - Prediction3
        EXPECTED: - Result3
        """
        pass
