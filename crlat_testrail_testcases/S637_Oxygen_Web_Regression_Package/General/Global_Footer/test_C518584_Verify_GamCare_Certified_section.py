import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C518584_Verify_GamCare_Certified_section(Common):
    """
    TR_ID: C518584
    NAME: Verify GamCare Certified section
    DESCRIPTION: This test case verifies GamCare Certified page displaying after  'GamCare Certified' logo tapping
    PRECONDITIONS: 1. GamCare Certified page is configured in CMS - Static Block
    PRECONDITIONS: 2. Functionality is applicabled for both logged in and logged out users
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_scroll_application_to_the_bottom___global_footer_section(self):
        """
        DESCRIPTION: Scroll application to the bottom -> Global Footer section
        EXPECTED: 'GamCare Certified' icon is displayed in Global Footer
        """
        pass

    def test_003_tap_gamcare_certified_icon(self):
        """
        DESCRIPTION: Tap 'GamCare Certified' icon
        EXPECTED: 'GamCare Certified' page is opened in the same tab
        """
        pass

    def test_004_verify_gamcare_certified_page_content(self):
        """
        DESCRIPTION: Verify 'GamCare Certified' page content
        EXPECTED: Content is appropriate to CMS configuration for the page
        """
        pass

    def test_005_tap__gamecare_certified_button_on_the_page(self):
        """
        DESCRIPTION: Tap  'Gamecare Certified' button on the page
        EXPECTED: 'http://www.gamcare.org.uk/training-and-certification/gamcare-certification/who-gamcare-certified' link is opened
        """
        pass
