import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide


@pytest.mark.lad_tst2  # Ladbrokes Only
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.event_details
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.banach
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.cms
@vtest
class Test_C47660680_Verify_5_A_Side_Launcher_and_URL_structure(BaseFiveASide):
    """
    TR_ID: C47660680
    NAME: Verify 5-A-Side Launcher and URL structure
    DESCRIPTION: This test case verifies pitch overlay launching and URL structure.
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> Five_A_Side
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Be aware that the '5-A-Side' tab should be switched off in case Static Block is disabled because it's part of the path for reaching the '5-A-Side' overlay.
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Select the '5-A-Side' tab
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with 5-A-Side
        DESCRIPTION: Navigate to Football event details page that has all 5-A-Side configs
        DESCRIPTION: Choose the '5-A-Side' tab
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        self._logger.info(f'***Found Football 5-A-Side event with id "{self.event_id}"')
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'"{self.expected_market_tabs.five_a_side}" is not active tab after click, '
                             f'active tab is "{current_tab}"')

    def test_001_verify_url_structure_when_5_a_side_tab_is_selected(self):
        """
        DESCRIPTION: Verify URL Structure when '5-A-Side' tab is selected
        EXPECTED: URL ends with event_id/5-a-side
        """
        current_url = self.device.get_current_url()
        self.assertTrue(current_url.endswith(f'{self.event_id}/5-a-side'),
                        msg=f'Current url "{current_url}" not ends with "{self.event_id}/5-a-side"')

    def test_002_click_tap_on_build_a_team_button_cms_configurable(self):
        """
        DESCRIPTION: Click/Tap on 'Build A Team' button (CMS configurable)
        EXPECTED: '5-A-Side' overlay is loaded
        """
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')

    def test_003_verify_url_structure(self):
        """
        DESCRIPTION: Verify URL Structure
        EXPECTED: URL ends with event_id/5-a-side/pitch
        """
        self.__class__.current_url = self.device.get_current_url()
        self.assertTrue(self.current_url.endswith(f'{self.event_id}/5-a-side/pitch'),
                        msg=f'Current url "{self.current_url}" not ends with "{self.event_id}/5-a-side/pitch"')

    def test_004_copy_url_open_a_new_browser_tab_and_paste_url(self):
        """
        DESCRIPTION: * Copy URL.
        DESCRIPTION: * Open a new browser tab and paste URL.
        EXPECTED: * Corresponding event details page is loaded
        EXPECTED: * '5-A-Side' overlay is launched
        """
        self.device.open_new_tab()
        self.device.navigate_to(url=self.current_url)
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
