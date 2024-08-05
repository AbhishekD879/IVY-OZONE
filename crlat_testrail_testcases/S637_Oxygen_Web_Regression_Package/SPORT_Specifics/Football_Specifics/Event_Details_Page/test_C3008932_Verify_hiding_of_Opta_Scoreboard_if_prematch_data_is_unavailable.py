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
class Test_C3008932_Verify_hiding_of_Opta_Scoreboard_if_prematch_data_is_unavailable(Common):
    """
    TR_ID: C3008932
    NAME: Verify hiding of Opta Scoreboard if prematch data is unavailable
    DESCRIPTION: This test case verifies cases when Opta Scoreboard is shown or not, depending on prematch data availability
    PRECONDITIONS: Several Football events should be configured in the following way:
    PRECONDITIONS: 1) pre-match event with Opta Scoreboard NOT mapped
    PRECONDITIONS: 2) pre-match event with Opta Scoreboard mapped; event start time should be **within** 5 days in future
    PRECONDITIONS: 3) pre-match event with Opta Scoreboard mapped; event start time should be **more than** 5 days in future
    PRECONDITIONS: 4) pre-match event with Opta Scoreboard and pre-match statistic mapped; event start time should be **more than** 5 days in future
    PRECONDITIONS: How to map pre-match statistics:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Football+Pre-match+Statistics
    PRECONDITIONS: To map Opta Scoreboard:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Opta+Scoreboard+mapping+to+an+OB+event
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Open browser console > network > all
    PRECONDITIONS: 4. **bymapping** request verifies if Opta Scoreboard is mapped to OB event:
    PRECONDITIONS: e.g. on stg env: https://com-stage.api.datafabric.nonprod.aws.ladbrokescoral.com/sdm/events/bymapping/CORAL/5172936?&api-key=COMc368624411e44b6e80e83c5a7f7c03c7
    PRECONDITIONS: 5. **prematch** request verifies if pre-match data from Opta Scoreboard is available:
    PRECONDITIONS: e.g. on stg env:  https://com-stage.api.datafabric.nonprod.aws.ladbrokescoral.com/sdm/stats/prematch/CORAL/5172936/?api-key=COMc368624411e44b6e80e83c5a7f7c03c7)
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_event_1_from_preconditions(self):
        """
        DESCRIPTION: Navigate to event details page of event #1 from preconditions
        EXPECTED: - **bymapping** request returns 404
        EXPECTED: - Opta Scoreboard is NOT shown
        """
        pass

    def test_002_navigate_to_event_details_page_of_event_2_from_preconditions(self):
        """
        DESCRIPTION: Navigate to event details page of event #2 from preconditions
        EXPECTED: - **bymapping** request returns 200
        EXPECTED: - **prematch** request returns 200
        EXPECTED: - Opta Scoreboard is shown
        """
        pass

    def test_003_navigate_to_event_details_page_of_event_3_from_preconditions(self):
        """
        DESCRIPTION: Navigate to event details page of event #3 from preconditions
        EXPECTED: - **bymapping** request returns 200
        EXPECTED: - **prematch** request returns 404
        EXPECTED: - Opta Scoreboard is NOT shown
        """
        pass

    def test_004_navigate_to_event_details_page_of_event_4_from_preconditions(self):
        """
        DESCRIPTION: Navigate to event details page of event #4 from preconditions
        EXPECTED: - **bymapping** request returns 200
        EXPECTED: - **prematch** request returns 404
        EXPECTED: - Opta Scoreboard is NOT shown
        EXPECTED: - Pre-match statistics is shown instead
        """
        pass
