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
class Test_C9726401_Event_Hub_Verify_navigation_through_Quick_Links_on_Event_Hub(Common):
    """
    TR_ID: C9726401
    NAME: Event Hub: Verify navigation through Quick Links on Event Hub
    DESCRIPTION: This test case verifies navigation through Quick Links on Event hub
    PRECONDITIONS: 1. Go to CMS -> Sport Pages->Event Hub and configure 5 active Quick links for current Time period on Event hub in order to have more Quick links than the screen can feet.
    PRECONDITIONS: 2. Load oxygen application and navigate to Event hub tab
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True

    def test_001_coral_verify_navigation_to_other_links_by_swiping_through(self):
        """
        DESCRIPTION: **[CORAL]** Verify navigation to other links by swiping through.
        EXPECTED: * Quick links are displayed in a Carousel as separate blocks.
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: * Quick links that don't fit the width of the screen are cut off
        EXPECTED: * User is able to navigate to the other quick links by swiping through
        """
        pass

    def test_002_ladbrokes_verify_navigation_to_other_links_by_swiping_updown(self):
        """
        DESCRIPTION: **[LADBROKES]** Verify navigation to other links by swiping up/down.
        EXPECTED: * Quick links are displayed as fixed vertical list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        EXPECTED: * User is able to navigate to the other quick links by swiping up/down.
        """
        pass
