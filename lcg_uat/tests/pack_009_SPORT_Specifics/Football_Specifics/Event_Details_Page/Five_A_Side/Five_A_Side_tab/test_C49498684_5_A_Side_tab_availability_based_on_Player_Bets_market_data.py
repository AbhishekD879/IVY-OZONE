import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.helpers import normalize_name


@pytest.mark.lad_tst2  # Ladbrokes only
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.event_details
@pytest.mark.login
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.banach
@pytest.mark.desktop
@vtest
class Test_C49498684_5_A_Side_tab_availability_based_on_Player_Bets_market_data(BaseFiveASide):
    """
    TR_ID: C49498684
    NAME: '5-A-Side' tab availability based on 'Player Bets' market data
    DESCRIPTION: This test case verifies '5-A-Side' tab availability based on 'Player Bets' market data
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request  to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: **Note 1:**
    PRECONDITIONS: To verify whether Player Bets market is provided by Banach, check **hasPlayerProps** property in https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/{event_id} response
    PRECONDITIONS: ![](index.php?/attachments/get/60196803)
    PRECONDITIONS: **Note 2:**
    PRECONDITIONS: Banach have made a change that they will only send 'HasPlayerProps:true' message when the original player prop markets are available. This means that when Goals and Cards are the only markets that are available (this will happen often as these become available far earlier than the others) then the message will not be sent and we will not display the 5-A-Side tab.
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Load the app
        DESCRIPTION: 2. Navigate to Football event details page with **hasPlayerProps: true** in .../events/{event_id}
        """
        self.__class__.event_id_with_5_a_side = self.get_ob_event_with_byb_market(five_a_side=True)
        self.__class__.event_id_without_5_a_side = self.get_ob_event_with_byb_market(five_a_side=False)
        event_ids = [self.event_id_with_5_a_side, self.event_id_without_5_a_side]
        for event_id in event_ids:
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
            event_name = normalize_name(event_resp[0]['event']['name'])
            self._logger.info(f'***Found Football event "{event_id}" "{event_name}"')

        self.navigate_to_edp(event_id=self.event_id_with_5_a_side, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')

    def test_001_verify_5_a_side_tab_availability(self):
        """
        DESCRIPTION: Verify '5-A-Side' tab availability
        EXPECTED: '5-A-Side' tab is displayed on event details page
        """
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.five_a_side),
                        msg=f'"{self.expected_market_tabs.five_a_side}" tab is not active')

    def test_002_navigate_to_football_event_details_page_with_hasplayerprops_false(self):
        """
        DESCRIPTION: Navigate to Football event details page with **hasPlayerProps: false**
        DESCRIPTION: NOTE! Can be triggered, using Charles tool: edit **hasPlayerProps** from 'true' to 'false in '.../events/{event_id} 'response
        """
        self.navigate_to_edp(event_id=self.event_id_without_5_a_side, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')

    def test_003_verify_5_a_side_tab_availability(self):
        """
        DESCRIPTION: Verify '5-A-Side' tab availability
        EXPECTED: '5-A-Side' tab is NOT displayed on event details page
        """
        available_market_tabs = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
        self.assertTrue(available_market_tabs, msg='Market tabs are not available')
        self.assertNotIn(self.expected_market_tabs.five_a_side, available_market_tabs.keys(),
                         msg=f'"{self.expected_market_tabs.five_a_side}" tab is present among '
                             f'market tabs "{available_market_tabs.keys()}"')
