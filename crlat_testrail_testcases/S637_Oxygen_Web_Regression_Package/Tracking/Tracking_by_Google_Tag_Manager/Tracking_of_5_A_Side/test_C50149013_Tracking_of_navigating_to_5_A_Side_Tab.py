import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.5_a_side
@vtest
class Test_C50149013_Tracking_of_navigating_to_5_A_Side_Tab(Common):
    """
    TR_ID: C50149013
    NAME: Tracking of navigating to 5-A-Side Tab
    DESCRIPTION: This test case verifies GA tracking of the navigation to 5-A-Side Tab on Football EDP
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to an event details page that has '5-A-Side' tab
    PRECONDITIONS: **5-A-Side configuration:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True

    def test_001_clicktap_on_5_a_side_tab_on_edp(self):
        """
        DESCRIPTION: Click/Tap on '5-A-Side' tab on EDP
        EXPECTED: '5-A-Side' tab is selected
        """
        pass

    def test_002_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * event: "content-view"
        EXPECTED: * screen_name: <URL PATH>
        EXPECTED: where <URL PATH> is **/event/football/<class name>/<type name>/<event name>/<event id>/5-a-side**
        """
        pass

    def test_003_navigate_to_the_5_a_side_tab_via_direct_link_or_from_quick_links_etc(self):
        """
        DESCRIPTION: Navigate to the '5-A-Side' tab via direct link or from quick links, etc.
        EXPECTED: '5-A-Side' tab is selected
        """
        pass

    def test_004_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * event: "content-view"
        EXPECTED: * screen_name: <URL PATH>
        EXPECTED: where <URL PATH> is **/event/football/<class name>/<league name>/<event name>/<event id>/5-a-side**
        """
        pass
