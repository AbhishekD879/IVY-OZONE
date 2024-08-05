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
class Test_C64293294_Verify_the_default_tab_selection_of_main_header_in_EDP(Common):
    """
    TR_ID: C64293294
    NAME: Verify the default tab selection of main header in EDP
    DESCRIPTION: This tc verifies the default tab selection of main header in EDP page
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_in_play_event_edp_page(self):
        """
        DESCRIPTION: Navigate to golf in-play event EDP page
        EXPECTED: User should be navigated to Leaderboard when the event is in-play
        """
        pass

    def test_002_leaderboard_tab_in_main_header_is_selected_by_default_when_there_are_no_groups_for_the_selected_inplay_event(self):
        """
        DESCRIPTION: Leaderboard tab in main header is selected by default when there are no groups for the selected inplay event
        EXPECTED: Leaderboard tab in main header should be selected by default
        """
        pass

    def test_003_groups_tab_in_main_header_is_selected_by_default_if_there_are_any_active_groups_fo_the_selected_event(self):
        """
        DESCRIPTION: Groups tab in main header is selected by default if there are any active groups fo the selected event
        EXPECTED: Groups tab in main header should be displayed by default if there are any active groups for that event
        """
        pass
