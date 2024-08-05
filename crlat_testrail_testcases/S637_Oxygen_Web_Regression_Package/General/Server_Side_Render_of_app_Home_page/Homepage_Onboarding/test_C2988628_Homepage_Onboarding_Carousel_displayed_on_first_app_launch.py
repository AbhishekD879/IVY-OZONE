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
class Test_C2988628_Homepage_Onboarding_Carousel_displayed_on_first_app_launch(Common):
    """
    TR_ID: C2988628
    NAME: Homepage Onboarding Carousel displayed on first app launch
    DESCRIPTION: This test case verifies that Onboarding carousel overlay is displayed for new users
    PRECONDITIONS: Multiple (3) onboarding overlays configured in CMS
    PRECONDITIONS: User is new (Or has no cache/cookies)
    """
    keep_browser_open = True

    def test_001_navigate_to_oxygen_fe(self):
        """
        DESCRIPTION: Navigate to Oxygen FE
        EXPECTED: Onboarding carousel overlay is displayed
        """
        pass

    def test_002_observe_onboarding_carousel_overlay(self):
        """
        DESCRIPTION: Observe Onboarding carousel overlay
        EXPECTED: Onboarding overlay contains:
        EXPECTED: * First overlay image set in CMS
        EXPECTED: * Images indicator (dots)
        EXPECTED: * Close button
        """
        pass

    def test_003_slide_carousel_left(self):
        """
        DESCRIPTION: Slide Carousel left
        EXPECTED: Next slide is displayed
        """
        pass

    def test_004_slide_carousel_right(self):
        """
        DESCRIPTION: Slide Carousel right
        EXPECTED: Previous slide is displayed
        """
        pass

    def test_005_tap_on_close_button(self):
        """
        DESCRIPTION: Tap on Close button
        EXPECTED: Onboarding overlay is closed
        """
        pass

    def test_006_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: Onboarding overlay is not displayed
        """
        pass

    def test_007_change_ordernumber_of_images_in_cms_and_call_the_onboarding_overlay_again(self):
        """
        DESCRIPTION: Change order/number of images in CMS and call the onboarding overlay again
        EXPECTED: All changes are displayed on app load
        """
        pass
