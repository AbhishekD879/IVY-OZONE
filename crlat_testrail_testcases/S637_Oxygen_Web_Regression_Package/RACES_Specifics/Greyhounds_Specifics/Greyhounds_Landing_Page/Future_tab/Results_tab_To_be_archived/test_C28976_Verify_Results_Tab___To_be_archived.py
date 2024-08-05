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
class Test_C28976_Verify_Results_Tab___To_be_archived(Common):
    """
    TR_ID: C28976
    NAME: Verify 'Results' Tab  -  To be archived
    DESCRIPTION: This test case verifies 'Results' tab.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the Sports Menu Ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_tap_results_tab(self):
        """
        DESCRIPTION: Tap 'Results' tab
        EXPECTED: 'Results' tab is opened
        """
        pass

    def test_004_verify_results_tab(self):
        """
        DESCRIPTION: Verify 'Results' tab
        EXPECTED: *   Two sorting types are present:
        EXPECTED: **'By Latest Results'** and** 'By Meetings'**
        EXPECTED: *   'By Latest Results' sorting type is selected by default
        """
        pass

    def test_005_check_portrait_and_landscape_modes_for_devices(self):
        """
        DESCRIPTION: Check portrait and landscape modes for devices
        EXPECTED: Whole page is displayed correctly
        """
        pass
