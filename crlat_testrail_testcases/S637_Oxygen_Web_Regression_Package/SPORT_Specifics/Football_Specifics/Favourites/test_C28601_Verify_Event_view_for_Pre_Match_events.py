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
class Test_C28601_Verify_Event_view_for_Pre_Match_events(Common):
    """
    TR_ID: C28601
    NAME: Verify Event view for Pre-Match events
    DESCRIPTION: This Test Case verified Event view for Pre-Match events on Favourites page/widget
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_add_football_pre_match_event_to_favourites(self):
        """
        DESCRIPTION: Add Football Pre-Match event to Favourites
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_favourite_matches_matcheswidget(self):
        """
        DESCRIPTION: Navigate to 'Favourite Matches' matches/widget
        EXPECTED: 
        """
        pass

    def test_003_verify_event_view_for_pre_match_event(self):
        """
        DESCRIPTION: Verify Event view for Pre-Match event
        EXPECTED: Pre-Match event contains:
        EXPECTED: - Fixture header (Home, Draw, Away)
        EXPECTED: - Primary Market Price/Odds buttons
        EXPECTED: - Event name
        EXPECTED: - Event time
        EXPECTED: - "+x Markets" link
        EXPECTED: - Favourite icon
        EXPECTED: - 'Watch Live' Icon and text (For events with Stream available)
        EXPECTED: - Signposting icons (if they are available)
        EXPECTED: All data is correct and corresponds to added event info
        """
        pass
