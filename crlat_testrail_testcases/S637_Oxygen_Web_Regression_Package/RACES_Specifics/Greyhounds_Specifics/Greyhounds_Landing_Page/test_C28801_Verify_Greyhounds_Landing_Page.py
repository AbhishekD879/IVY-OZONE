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
class Test_C28801_Verify_Greyhounds_Landing_Page(Common):
    """
    TR_ID: C28801
    NAME: Verify Greyhounds Landing Page
    DESCRIPTION: This test case verifies Greyhounds landing page
    PRECONDITIONS: Make sure that events for all tabs are available on the Site Server for <Race> sports
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
        DESCRIPTION: Tap Greyhounds icon from the Sports Menu Ribbon
        EXPECTED: 1.  Greyhounds landing page is opened
        EXPECTED: 2.  'Today' tab is opened by default
        EXPECTED: 3.  Banner carousel if it is configured on the CMS is displayed above the all tabs
        """
        pass

    def test_003_check_4_tabs_displaying(self):
        """
        DESCRIPTION: Check 4 tabs displaying
        EXPECTED: 'Today', 'Tomorrow', 'Future' and 'Results' tabs are displayed in one row
        EXPECTED: Results tab was removed in OX98
        """
        pass
