import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C49498684_5_A_Side_tab_availability_based_on_Player_Bets_market_data(Common):
    """
    TR_ID: C49498684
    NAME: '5-A-Side' tab availability based on 'Player Bets' market data
    DESCRIPTION: This test case verifies '5-A-Side' tab availability based on 'Player Bets' market data
    DESCRIPTION: Autotest: [C58833971]
    DESCRIPTION: Autotest: [C58833972]
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request  to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: **Note 1:**
    PRECONDITIONS: To verify whether Player Bets market is provided by Banach, check **hasPlayerProps** property in https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/{event_id} response
    PRECONDITIONS: ![](index.php?/attachments/get/60196803)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page with **hasPlayerProps: true** in .../events/{event_id}
    PRECONDITIONS: **Note 2:**
    PRECONDITIONS: Banach have made a change that they will only send 'HasPlayerProps:true' message when the original player prop markets are available. This means that when Goals and Cards are the only markets that are available (this will happen often as these become available far earlier than the others) then the message will not be sent and we will not display the 5-A-Side tab.
    """
    keep_browser_open = True

    def test_001_verify_5_a_side_tab_availability(self):
        """
        DESCRIPTION: Verify '5-A-Side' tab availability
        EXPECTED: '5-A-Side' tab is displayed on event details page
        """
        pass

    def test_002_navigate_to_football_event_details_page_with_hasplayerprops_falsenote_can_be_triggered_using_charles_tool_edit_hasplayerprops_from_true_to_false_in_eventsevent_id_response(self):
        """
        DESCRIPTION: Navigate to Football event details page with **hasPlayerProps: false**
        DESCRIPTION: NOTE! Can be triggered, using Charles tool: edit **hasPlayerProps** from 'true' to 'false in '.../events/{event_id} 'response
        EXPECTED: 
        """
        pass

    def test_003_verify_5_a_side_tab_availability(self):
        """
        DESCRIPTION: Verify '5-A-Side' tab availability
        EXPECTED: '5-A-Side' tab is NOT displayed on event details page
        """
        pass
