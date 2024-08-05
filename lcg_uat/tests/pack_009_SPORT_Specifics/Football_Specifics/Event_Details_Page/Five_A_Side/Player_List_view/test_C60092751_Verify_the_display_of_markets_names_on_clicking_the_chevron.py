import pytest
from tests.base_test import vtest
from time import sleep
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod  # Ladbrokes Only
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C60092751_Verify_the_display_of_markets_names_on_clicking_the_chevron(BaseFiveASide, BaseSportTest, BaseCashOutTest):
    """
    TR_ID: C60092751
    NAME: Verify the display of markets names on clicking the chevron
    DESCRIPTION: Verify on clicking the Chevron all markets names are listed in the dropdown
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: **5-A-Side config:**
        PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
        PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
        PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
        PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
        PRECONDITIONS: - Event is prematch (not live)
        PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
        PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
        """
        cms_formations = self.cms_config.get_five_a_side_formations()
        if not cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)

    def test_001_launch_ladbrokes_app(self):
        """
        DESCRIPTION: Launch Ladbrokes app
        EXPECTED: User should be able launch the application successfully
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_football(self):
        """
        DESCRIPTION: Navigate to Football
        EXPECTED: User should be navigated to Football landing page
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='football')

    def test_003_navigate_to_any_football_event_that_has_5_a_side_available(self):
        """
        DESCRIPTION: Navigate to any football event that has 5-A side available
        EXPECTED: User should be navigated to EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=20)

    def test_004_navigate_to_5_a_side_tab(self):
        """
        DESCRIPTION: Navigate to 5-A Side tab
        EXPECTED: User should be navigated to 5-A Side tab
        """
        tab = self.site.sport_event_details.markets_tabs_list.items_names.__contains__('5-A-SIDE')
        self.assertTrue(tab,
                        msg=f'5-A-Side is tab is not present, active tabs are "{self.site.sport_event_details.markets_tabs_list.items_names}"')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')

    def test_005_click_on_build_a_team(self):
        """
        DESCRIPTION: Click on Build a Team
        EXPECTED: 1: Pitch View should be displayed
        EXPECTED: 2: Balanced formation should be selected by default
        EXPECTED: 3: User should be able to select any formation displayed in the pitch view
        """
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(self.pitch_overlay, msg='Players are not displayed on the Pitch View')
        if self.site.sport_event_details.tab_content.pitch_overlay.has_journey_panel:
            self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.click()
        list(self.pitch_overlay.values())[0].icon.click()
        sleep(2)
        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_names
        self.assertTrue(player_name, msg='Players name is not present in playerListContent')
        self.assertTrue(len(player_name) > 2, msg='Player name list is empty')

    def test_006_click_on_plus_icon_from_any_player_position(self):
        """
        DESCRIPTION: Click on + icon from any player position
        EXPECTED: 1: User should be navigated to select a player page
        EXPECTED: 2: Add a <Position> should be displayed
        EXPECTED: 3: < Back button should be displayed
        EXPECTED: 4: Market name should be displayed in blue with chevron
        """
        position_title = self.site.sport_event_details.tab_content.players_overlay.title.text
        self.assertTrue(position_title, msg=f'"{position_title}" is not displayed')
        self.assertTrue(self.site.sport_event_details.tab_content.players_overlay.back_button.is_displayed(),
                        msg='back button is not displayed')
        self.__class__.default_market = self.site.sport_event_details.tab_content.players_overlay.sub_title.text
        self.assertTrue(self.default_market, msg=f'"{self.default_market}" is not displayed ')

    def test_007_click_on_the_chevron(self):
        """
        DESCRIPTION: Click on the chevron
        EXPECTED: 1: Drop down should be displayed with all market names
        EXPECTED: 2: User should be able to select any market name
        """
        self.site.sport_event_details.tab_content.players_overlay.market_dropdown.click()
        result = self.site.sport_event_details.tab_content.players_overlay.dropdown_menu.text
        menu_items = result.split('\n')
        if len(menu_items) > 1:
            self.site.sport_event_details.tab_content.players_overlay.dropdown_menu.click()
            latest_market = self.site.sport_event_details.tab_content.players_overlay.market_dropdown
            self.assertNotEqual(self.default_market, latest_market, msg='market name is not selected')
        self._logger.info('one market is available for a position')
