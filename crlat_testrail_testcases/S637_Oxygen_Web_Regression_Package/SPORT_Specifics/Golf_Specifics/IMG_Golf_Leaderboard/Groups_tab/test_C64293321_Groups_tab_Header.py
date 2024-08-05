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
class Test_C64293321_Groups_tab_Header(Common):
    """
    TR_ID: C64293321
    NAME: Groups tab Header
    DESCRIPTION: This tc verifies if fav icon, search option and round dropdown is displayed on the header
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_login_into_application(self):
        """
        DESCRIPTION: Login into application.
        EXPECTED: User is logged in
        """
        pass

    def test_002_navigate_to_leaderboard_when_the_event_is_inplay(self):
        """
        DESCRIPTION: Navigate to Leaderboard when the event is inplay.
        EXPECTED: LB should load
        """
        pass

    def test_003_navigate_to_groups_tab(self):
        """
        DESCRIPTION: Navigate to Groups tab.
        EXPECTED: Groups tab is opened
        """
        pass

    def test_004_verify_below_headers_are_present_in_groups_tab_(self):
        """
        DESCRIPTION: Verify below headers are present in Groups tab :
        EXPECTED: Mentioned headers should be present in the Groups tab.
        """
        pass

    def test_005____favorites(self):
        """
        DESCRIPTION: --> Favorites
        EXPECTED: 
        """
        pass

    def test_006____search_option(self):
        """
        DESCRIPTION: --> Search option
        EXPECTED: 
        """
        pass

    def test_007____rounds_dropdown(self):
        """
        DESCRIPTION: --> Rounds dropdown"
        EXPECTED: 
        """
        pass