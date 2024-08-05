import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C10436244_Ladbrokes_Verify_info_about_race_on_the_Race_Card_EDP(Common):
    """
    TR_ID: C10436244
    NAME: [Ladbrokes] Verify info about race on the Race Card (EDP)
    DESCRIPTION: This test case verifies information from Racing Post about the race on the Racing Card (EDP)
    DESCRIPTION: AUTOTEST:
    DESCRIPTION: Mobile [C21761438]
    DESCRIPTION: Desktop [C21839629]
    PRECONDITIONS: * Event(s) with Racing Post data are available
    PRECONDITIONS: * A user is on a Race Card (Event Details page) of an event with available Racing Post
    PRECONDITIONS: NOTE
    PRECONDITIONS: * Racing Post information is present in a response from DF API https://raceinfo-api.ladbrokes.com/race_info/ladbrokes/[eventID]
    PRECONDITIONS: * Racing Post information or it’s parts for the specific event can be absent so it will be absent in the UI as well
    """
    keep_browser_open = True

    def test_001_verify_the_information_about_the_race_on_the_racing_carddesign_mobilehttpsappzeplinioproject5ba39ed8bae1840f5adf5467screen5bb5fb254f797f1a1be2c8a7design_desktophttpsappzeplinioproject5c6d3e910cb0f599dfd2145bscreen5c6d6283959ef19a213306d1(self):
        """
        DESCRIPTION: Verify the information about the race on the Racing Card
        DESCRIPTION: [Design Mobile](https://app.zeplin.io/project/5ba39ed8bae1840f5adf5467/screen/5bb5fb254f797f1a1be2c8a7)
        DESCRIPTION: [Design Desktop](https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5c6d6283959ef19a213306d1)
        EXPECTED: Further information from Racing Post is displayed:
        EXPECTED: - Race Title
        EXPECTED: - Race Type
        EXPECTED: - Going (Soft / Heavy /Good / Standard etc)
        EXPECTED: - Distance
        """
        pass

    def test_002_verify_race_title(self):
        """
        DESCRIPTION: Verify Race Title
        EXPECTED: - Race Title  is displayed below event time & name (e.g., 'Watch Irish Racing on Racing TV')
        EXPECTED: - Race Title = 'raceName' attribute from Racing Post response
        """
        pass

    def test_003_verify_race_type(self):
        """
        DESCRIPTION: Verify Race Type
        EXPECTED: - Race Type is displayed below Race Title (e.g., 'Chase Turf')
        EXPECTED: - Race Type = 'RaceType'attribute from Racing Post response. Description is displayed (not code)
        EXPECTED: ![](index.php?/attachments/get/36064)
        """
        pass

    def test_004_verify_going_soft__heavy_good__standard_etc(self):
        """
        DESCRIPTION: Verify Going (Soft / Heavy /Good / Standard etc)
        EXPECTED: - Going is displayed below Race Title, after Race Type (e.g., 'Good to Soft')
        EXPECTED: - Going = 'goingCode' attribute from Racing Post response  (e.g.,"GS")
        """
        pass

    def test_005_verify_distance(self):
        """
        DESCRIPTION: Verify Distance
        EXPECTED: - Distance is displayed below Race Title, after 'Going' (e.g., 2m 4f)
        EXPECTED: - Distance = 'distance' attribute from Racing Post response
        """
        pass
