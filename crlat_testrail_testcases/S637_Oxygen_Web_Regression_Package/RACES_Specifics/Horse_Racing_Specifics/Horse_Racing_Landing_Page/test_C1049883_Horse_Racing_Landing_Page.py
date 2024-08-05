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
class Test_C1049883_Horse_Racing_Landing_Page(Common):
    """
    TR_ID: C1049883
    NAME: Horse Racing Landing Page
    DESCRIPTION: This test case verifies Horse Racing landing page
    DESCRIPTION: AUTOTEST: [C527897]
    PRECONDITIONS: Make sure that events for all tabs are available on the Site Server for Horse Racing
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Oxygen application is loaded
        """
        pass

    def test_002_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap Horse Racing icon from the Sports Menu Ribbon
        EXPECTED: 1.  Horse Racing landing page is opened
        EXPECTED: 2.  'Featured' (Ladbrokes - 'Meetings') tab is opened by default
        """
        pass

    def test_003_check_4_tabs_displaying(self):
        """
        DESCRIPTION: Check 4 tabs displaying.
        EXPECTED: - For Coral brand: The 'Featured', 'Future', 'Specials' and 'YourCall' tabs are displayed in one row.
        EXPECTED: - For Ladbrokes brand: The 'Meetings', 'Next races', 'Future' and 'Specials' tabs are displayed in one row.
        """
        pass
