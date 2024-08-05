import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2513213_Verify_Toggling_of_Connect_tutorial_overlay(Common):
    """
    TR_ID: C2513213
    NAME: Verify Toggling of 'Connect tutorial overlay'
    DESCRIPTION: This test case verify that 'Connect tutorial overlay' can be switched on/off in CMS:
    DESCRIPTION: CMS -> System configuration -> Connect -> overlay
    PRECONDITIONS: 1. Load CMS and make sure 'Connect tutorial overlay' is turned off: System configuration -> Connect -> overlay = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Overlay will be displayed when following is present in browser Local Storage: find 'OX.retailOverlayRemain' (if not exist add it manually); set value with '4'
    PRECONDITIONS: 2. Load SportBook App
    """
    keep_browser_open = True

    def test_001_reload_home_page(self):
        """
        DESCRIPTION: Reload Home Page
        EXPECTED: * No Tutorial Overlay is displayed
        EXPECTED: * In Local Storage: 'OX.retailOverlayRemain' still contains value '4'
        """
        pass

    def test_002__load_cms_turn_overlay_feature_on(self):
        """
        DESCRIPTION: * Load CMS
        DESCRIPTION: * Turn 'overlay' feature on
        EXPECTED: 
        """
        pass

    def test_003_reload_home_page(self):
        """
        DESCRIPTION: Reload Home Page
        EXPECTED: * Tutorial Overlay is displayed
        EXPECTED: * In Local Storage: 'OX.retailOverlayRemain' contains value '3'
        """
        pass

    def test_004_reload_home_page_one_more_time(self):
        """
        DESCRIPTION: Reload Home Page one more time
        EXPECTED: * Tutorial Overlay is displayed
        EXPECTED: * In Local Storage: 'OX.retailOverlayRemain' contains value '2'
        """
        pass
