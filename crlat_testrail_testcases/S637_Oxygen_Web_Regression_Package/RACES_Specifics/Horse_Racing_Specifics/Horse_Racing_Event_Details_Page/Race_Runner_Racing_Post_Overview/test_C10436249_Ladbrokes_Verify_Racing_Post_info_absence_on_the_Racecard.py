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
class Test_C10436249_Ladbrokes_Verify_Racing_Post_info_absence_on_the_Racecard(Common):
    """
    TR_ID: C10436249
    NAME: [Ladbrokes] Verify Racing Post info absence on the Racecard
    DESCRIPTION: This test case verifies whether Racing Post pieces of info (including stars) don't display if it is absent in a response from DF API
    PRECONDITIONS: *  Racing Post information is absent (or mocked as absent) in a response from Racing Post API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    """
    keep_browser_open = True

    def test_001__block_response_from_racing_post_api_for_one_event_open_horse_racing__event_verify_absence_of_racing_post_information(self):
        """
        DESCRIPTION: * Block response from Racing Post API for one event
        DESCRIPTION: * Open Horse racing > Event
        DESCRIPTION: * Verify absence of Racing Post information
        EXPECTED: Racing Post information is absent on the page
        EXPECTED: - 'Race Title' info
        EXPECTED: - 'Race Type' info
        EXPECTED: - 'Going (Soft / Heavy /Good / Standard etc)' info
        EXPECTED: - 'Distance' info is absent
        EXPECTED: - 'SHOW MORE ⋁' button' is absent
        EXPECTED: - No following items are present:
        EXPECTED: - Runner Age
        EXPECTED: - Runner Weight
        EXPECTED: - RPR
        EXPECTED: - Runner Comment
        EXPECTED: - CD/C/BF (if a course winner and/or if a beaten favorite)
        EXPECTED: - Star Rating
        """
        pass
