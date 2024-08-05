import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.virtual_sports
@vtest
class Test_C874393_Virtual_Sport_Page(Common):
    """
    TR_ID: C874393
    NAME: Virtual Sport Page
    DESCRIPTION: This test case verifies the Virtual Sport page, list and order of Virtual Sports types
    DESCRIPTION: NOTE:
    DESCRIPTION: On step #3 - Darts and Boxing are absent (prod)
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=750377&group_order=asc
    DESCRIPTION: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_go_to_virtual_sports(self):
        """
        DESCRIPTION: Go to 'Virtual Sports'
        EXPECTED: - 'Virtual Sports' page displayed with header contains all icons for the virtual, sorted as configured on CMS
        EXPECTED: - First configured on CMS sport displayed on the page load
        """
        pass

    def test_002_verify_the_page(self):
        """
        DESCRIPTION: Verify the page
        EXPECTED: The page contains the following elements:
        EXPECTED: * Header with a back button and "Virtual" label
        EXPECTED: * Sport carousel
        EXPECTED: * Video stream window
        EXPECTED: * Event selector ribbon
        EXPECTED: * Circle Countdown timer
        EXPECTED: * Markets with price odds buttons
        EXPECTED: **For Desktop:**
        EXPECTED: * Breadcrumbs are displayed below 'Virtual' header
        EXPECTED: * Breadcrumbs are displayed in the following format : 'Home' > 'Virtuals'
        """
        pass

    def test_003_navigate_to_a_different_event_of_the_same_virtual_sport_using_event_selector_ribbon(self):
        """
        DESCRIPTION: Navigate to a different event of the same virtual sport using event selector ribbon
        EXPECTED: User is able to navigate to a different event of the same virtual sport
        """
        pass

    def test_004_navigate_to_a_different_virtual_sport_using_sport_carousel(self):
        """
        DESCRIPTION: Navigate to a different virtual sport using Sport carousel
        EXPECTED: User is navigated to the event of the selected virtual sport
        """
        pass
