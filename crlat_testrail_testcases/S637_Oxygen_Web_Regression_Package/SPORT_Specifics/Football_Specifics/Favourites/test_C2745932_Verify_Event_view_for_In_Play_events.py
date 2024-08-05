import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2745932_Verify_Event_view_for_In_Play_events(Common):
    """
    TR_ID: C2745932
    NAME: Verify Event view for In-Play events
    DESCRIPTION: This Test Case verified Event view for In-Play events on Favourites page/widget
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_add_football_in_play_event_to_favourites(self):
        """
        DESCRIPTION: Add Football In-Play event to Favourites
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_favourite_matches_matcheswidget(self):
        """
        DESCRIPTION: Navigate to 'Favourite Matches' matches/widget
        EXPECTED: 
        """
        pass

    def test_003_verify_event_view_for_in_play_event(self):
        """
        DESCRIPTION: Verify Event view for In-Play event
        EXPECTED: In-Play event contains:
        EXPECTED: - Fixture header (Home, Draw, Away)
        EXPECTED: - Primary Market Price/Odds buttons
        EXPECTED: - Event name
        EXPECTED: - "+x Markets" link
        EXPECTED: - Favourite icon
        EXPECTED: - Live icon
        EXPECTED: - Current Score and Match Time
        EXPECTED: - Commentaries updated in Real Time using LiveServe
        EXPECTED: - 'Watch Live' Icon and text (For events with Stream available)
        """
        pass
