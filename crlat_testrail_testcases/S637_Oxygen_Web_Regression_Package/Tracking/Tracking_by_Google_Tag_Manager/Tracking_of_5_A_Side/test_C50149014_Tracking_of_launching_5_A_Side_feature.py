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
class Test_C50149014_Tracking_of_launching_5_A_Side_feature(Common):
    """
    TR_ID: C50149014
    NAME: Tracking of launching 5--A-Side feature
    DESCRIPTION: This test case verifies GA tracking of launching '5-A-Side' feature on the related tab on Football EDP
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to an event details page that has '5-A-Side' tab
    PRECONDITIONS: 3. Click/Tap on '5-A-Side' tab
    PRECONDITIONS: **5-A-Side configuration:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Configure a quick link:**
    PRECONDITIONS: in CMS > sports-pages > homepage > quick links module with the following destination:
    PRECONDITIONS: {domain}/event/football/<class name>/<type name>/<event name>/<event id>/5-a-side/pitch
    PRECONDITIONS: e.g. https://fantom2-excalibur.ladbrokes.com/event/football/english/premier-league/wolverhampton-wanderers-v-leicester/776939/5-a-side/pitch
    """
    keep_browser_open = True

    def test_001_clicktap_on_build_team_button(self):
        """
        DESCRIPTION: Click/Tap on 'Build team' button
        EXPECTED: '5-A-Side' Pitch overlay is loaded
        """
        pass

    def test_002_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: The following parameters and values are present in 'dataLayer' object:
        EXPECTED: * event: "trackEvent"
        EXPECTED: * eventCategory: "5-A-Side"
        EXPECTED: * eventAction: "Build"
        EXPECTED: * eventLabel: "/5-a-side"
        """
        pass

    def test_003_clicktap_on_quick_link_from_pre_condition(self):
        """
        DESCRIPTION: Click/tap on 'Quick link' from pre-condition
        EXPECTED: Corresponding event details page opens with '5-A-Side' Pitch overlay loaded
        """
        pass

    def test_004_type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: Type **'dataLayer'** in browser's console and verify GA tracking record
        EXPECTED: GA Tracking record from step 2 is NOT present
        """
        pass
