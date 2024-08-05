import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C9647797_Verify_blocking_of_access_to_GH_HR_for_Featured_page_widget(Common):
    """
    TR_ID: C9647797
    NAME: Verify blocking of access to GH & HR for Featured page/widget
    DESCRIPTION: This test case verifies that German user doesn't have access to Greyhound (GH) and Horse Racing (HR) in Featured page/widget
    PRECONDITIONS: 1. Ensure that there are GH, International Totes, and HR Featured with different 'Select Events by' drop-down items is configured in CMS:
    PRECONDITIONS: * EventsModule  (CMS > Featured Tab Modules > Active Featured Modules)
    PRECONDITIONS: * SurfaceBetModule (CMS > Main Navigation > Homepage > Surface Bet Module > Active Surface Bets)
    PRECONDITIONS: 2. Featured with categoryId in (19, 21, 161) are not displayed for german users  (Console > Network > WS > find '?EIO=3&transport=websoket' > Frames > 42/0,["FEATURED_STRUCTURE_CHANGED",…]
    PRECONDITIONS: 3. German user is logged in
    """
    keep_browser_open = True

    def test_001_open_featured_section_for_mobiletabletthe_featured_tab_is_opened_by_default_on_the_homepagefor_desktopscroll_down_the_homepage_to_find_featured(self):
        """
        DESCRIPTION: Open 'Featured' section :
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: The 'Featured' tab is opened by default on the Homepage
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Scroll down the homepage to find Featured
        EXPECTED: * The section is displayed
        EXPECTED: * GH and HR are not available in any of Featured Modules
        """
        pass
