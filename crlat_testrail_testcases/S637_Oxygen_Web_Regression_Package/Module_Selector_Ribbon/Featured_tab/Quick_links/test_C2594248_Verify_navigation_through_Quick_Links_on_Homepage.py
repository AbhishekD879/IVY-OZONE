import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C2594248_Verify_navigation_through_Quick_Links_on_Homepage(Common):
    """
    TR_ID: C2594248
    NAME: Verify navigation through Quick Links on Homepage
    DESCRIPTION: This test case verifies navigation through Quick Links on Homepage
    PRECONDITIONS: 1. Go to CMS -> Sport Pages->Homepage and configure active Quick link for current Time period on Homepage
    PRECONDITIONS: 2. Load oxygen application and navigate to Featured tab
    PRECONDITIONS: Design for Coral (now its matching Ladbrokes, i.e. quick links are stacked in a vertical list): https://jira.egalacoral.com/browse/BMA-52016
    PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
    PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
    PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
    """
    keep_browser_open = True

    def test_001_verify_navigation_to_other_links_by_swiping_updown(self):
        """
        DESCRIPTION: Verify navigation to other links by swiping up/down.
        EXPECTED: * Quick links are displayed as fixed vertical list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        EXPECTED: * User is able to navigate to the other quick links by swiping up/down.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        pass
