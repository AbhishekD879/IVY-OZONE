import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C15478414_Ladbrokes_Verify_HR_EDP_is_properly_displayed_when_Silks_info_is_missing_in_Racing_Post_API(Common):
    """
    TR_ID: C15478414
    NAME: [Ladbrokes] Verify HR EDP is properly displayed when Silks info is missing in Racing Post API
    DESCRIPTION: This test case verifies that EDP is properly displayed when data from Racing Post API is unavailable or partially missing
    PRECONDITIONS: - Horse Racing Event is mapped with DF API data
    PRECONDITIONS: - List of Aggregation MS {envs.}: https://confluence.egalacoral.com/display/SPI/Aggregation+Java
    PRECONDITIONS: https://{env.}/silks/racingpost/17058,243739,266307,61763,...
    PRECONDITIONS: - Silk ID is received in response from https://ld-{env.}.api.datafabric.{env.}.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/{event id}/content?locale=en-GB&api-key={api key}
    PRECONDITIONS: in horses.silk: "{silk id}.png" attribute
    """
    keep_browser_open = True

    def test_001_navigate_to_hr_event_details_page_which_is_not_mapped_with_racing_post_dataor_in_browser_devtools_block_request_to_racing_post_data_from_which_silk_id_is_receivedand_verify_silk_icons(self):
        """
        DESCRIPTION: Navigate to HR event details page which is not mapped with Racing Post data
        DESCRIPTION: (OR in browser devtools block request to Racing Post data from which Silk ID is received)
        DESCRIPTION: and verify silk icons
        EXPECTED: - Silk icons are not displayed
        EXPECTED: - Generic silk images are not displayed
        EXPECTED: - Only runner numbers are displayed and selection (horse) names
        """
        pass

    def test_002_navigate_to_hr_edp_which_is_mapped_with_racing_post_data_andin_browser_devtools_block_request_to_aggregation_ms_and_verify_silk_icons(self):
        """
        DESCRIPTION: Navigate to HR EDP which is mapped with Racing Post data and
        DESCRIPTION: in browser devtools block request to Aggregation MS and verify silk icons
        EXPECTED: - Generic silk images displayed for all horses along with Runner details received from Racing Post data DF API (e.g. trainer, form, weight, age, etc.)
        """
        pass

    def test_003_navigate_to_hr_edp_page_which_is_mapped_with_racing_post_data_where_1_or_more_horses_are_missing_silk_info_in_racing_post_data_df_api(self):
        """
        DESCRIPTION: Navigate to HR EDP page which is mapped with Racing Post data where 1 or more horses are missing silk info in Racing Post data (DF API)
        EXPECTED: - Generic silk images displayed for horse(s) with missing silk info along with Runner details received from Racing Post data DF API (e.g. trainer, form, weight, age, etc.)
        """
        pass
