import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C2594264_Verify_Next_Races_Module_when_theres_no_events_to_show(Common):
    """
    TR_ID: C2594264
    NAME: Verify 'Next Races' Module when there's no events to show
    DESCRIPTION: This test case verifies 'Next Races' module when there's no events to show
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Make sure race events are NOT available for current day.
    PRECONDITIONS: In order to control Events displaying in the Next Races Widget on the Horse Racing page, go to CMS -> Tap 'System-configuration' -> NEXTRACES
    PRECONDITIONS: To load CMS use the next link: CMS_ENDPOINT/keystone/structure,
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog function.
    PRECONDITIONS: Desktop screen resolution > 970 px, 1025px
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Oxygen application is loaded
        """
        pass

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: 
        """
        pass

    def test_003_check_next_races_module(self):
        """
        DESCRIPTION: Check 'Next Races' module
        EXPECTED: 'Next Races' module is absent
        """
        pass
