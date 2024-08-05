import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C667800_Verify_Body_View_970px_or_less_than_970px_for_Desktop(Common):
    """
    TR_ID: C667800
    NAME: Verify Body View (970px or less than 970px) for Desktop
    DESCRIPTION: This test case verifies Desktop Body View (970px or less than 970px).
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_verify_desktop_body_view_for_device_screen_with_width_less_than_970px_when_actual_size_of_page_is_970px(self):
        """
        DESCRIPTION: Verify Desktop Body View for device screen with width less than 970px when actual size of page is 970px
        EXPECTED: Desktop View is displayed with Left menu navigation and 2 columns
        EXPECTED: Desktop Body View consists of:
        EXPECTED: * Header
        EXPECTED: * Left Navigation view - fixed width 160px
        EXPECTED: * Main view - fixed width 500 px
        EXPECTED: * Right Column View - fixed 290px
        EXPECTED: * Global footer
        EXPECTED: * Horizontal slider at the bottom of page
        """
        pass

    def test_002_verify_desktop_body_view_for_device_screen_with_width_970px_when_actual_size_of_page_more_than_970px_or_equal_to_970px(self):
        """
        DESCRIPTION: Verify Desktop Body View for device screen with width 970px when actual size of page more than 970px or equal to 970px
        EXPECTED: Desktop View is displayed with Left menu navigation and 2 columns
        EXPECTED: Desktop Body View consists of:
        EXPECTED: * Header
        EXPECTED: * Left Navigation view - fixed width 160px
        EXPECTED: * Main view - fixed width 500 px
        EXPECTED: * Right Column View - fixed 290px
        EXPECTED: * Global footer
        """
        pass

    def test_003_navigate_to_different_pages_across_the_application_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Navigate to different pages across the application and repeat steps 2-3
        EXPECTED: 
        """
        pass

    def test_004_load_oxygen_app_on_the_tablet(self):
        """
        DESCRIPTION: Load Oxygen app on the Tablet
        EXPECTED: * Homepage is loaded
        EXPECTED: * Tablet view is displayed on device without Left navigation menu
        EXPECTED: * Sports Menu Ribbon is displayed below Main Header
        EXPECTED: * Right Column is displayed
        EXPECTED: * Mobile footer is displayed at the bottom of the page
        """
        pass

    def test_005_navigate_to_different_pages_across_the_application_on_the_tablet(self):
        """
        DESCRIPTION: Navigate to different pages across the application on the Tablet
        EXPECTED: * Tablet view is displayed on device without Left navigation menu
        EXPECTED: * Right Column is displayed
        EXPECTED: * Mobile footer is displayed at the bottom of the page
        """
        pass
