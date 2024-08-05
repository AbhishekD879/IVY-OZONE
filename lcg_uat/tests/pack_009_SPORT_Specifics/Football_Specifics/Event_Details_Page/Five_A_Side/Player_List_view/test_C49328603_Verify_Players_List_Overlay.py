import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.helpers import normalize_name, cleanhtml
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
class Test_C49328603_Verify_Players_List_Overlay(BaseFiveASide, BaseSportTest, BaseCashOutTest):
    """
    TR_ID: C49328603
    NAME: Verify Players List Overlay
    DESCRIPTION: This test case verifies Players List Overlay.
    PRECONDITIONS: Feature epic: https://jira.egalacoral.com/browse/BMA-49261
    PRECONDITIONS: Feature invision: https://projects.invisionapp.com/share/ASHWPQ0DB8K#/screens/397567275
    PRECONDITIONS: Designs: https://app.zeplin.io/project/5e0a3b413cbeb61b6eb8f5c9/dashboard
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - User is on Football event EDP, '5 A Side' sub tab (event type described above)
    PRECONDITIONS: - Player data and statisctic takes from local storage 'scoreBoards_dev_prematch_eventId'(receivs from Bnah) and from response 'players?obEventId=773006'
    PRECONDITIONS: ![](index.php?/attachments/get/61571599)
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load the app
        DESCRIPTION: Navigate to Football event details page that has all 5-A-Side configs
        """
        cms_formations = self.cms_config.get_five_a_side_formations()
        if not cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'***Found Football 5-A-Side event {event_name} with id "{event_id}"')
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails', timeout=30)

    def test_001_select_a_player_position_from_a_pitch_overlay(self):
        """
        DESCRIPTION: Select a Player position from a pitch overlay
        EXPECTED: Player List View is displayed.
        """
        tab = self.site.sport_event_details.markets_tabs_list.items_names.__contains__('5-A-SIDE')
        self.assertTrue(tab,
                        msg=f'5-A-Side is tab is not present, active tabs are "{self.site.sport_event_details.markets_tabs_list.items_names}"')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(self.pitch_overlay, msg='Players are not displayed on the Pitch View')
        list(self.pitch_overlay.values())[1].icon.click()
        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_names
        self.assertTrue(player_name, msg='Players name is not present in playerListContent')
        self.assertTrue(len(player_name) > 2, msg='Player name list is empty')

    def test_002_verify_player_list_view_overlay_content(self):
        """
        DESCRIPTION: Verify Player List View overlay content.
        EXPECTED: Player List View overlay should contain:
        EXPECTED: - '<Back' Button.
        EXPECTED: - Title "Add a 'Position name'" below the 'Back' button (e.g 'Add a Cruncher'. Position name sets in the CMS)
        EXPECTED: - SubTitle is the name of the Statistic (e.g. To Win X Tackles, To Make X Passes etc. sets in the CMS)
        EXPECTED: - Buttons 'All Players'(selected by default), 'Home', 'Away'.(For all positions except Goalkeeper).
        EXPECTED: - Event Name.
        EXPECTED: - The list of players.
        EXPECTED: ![](index.php?/attachments/get/59126054)
        EXPECTED: ![](index.php?/attachments/get/59126055)
        """
        position_title = self.site.sport_event_details.tab_content.players_overlay.title.text
        self.assertTrue(position_title, msg=f'"{position_title}" is not displayed')
        self.assertTrue(self.site.sport_event_details.tab_content.players_overlay.back_button.is_displayed(), msg='back button is not displayed')
        sub_title = self.site.sport_event_details.tab_content.players_overlay.sub_title.text
        self.assertTrue(sub_title, msg=f'"sub title" is not displayed ')
        players_list = self.site.sport_event_details.tab_content.players_overlay.players_list.items_as_ordered_dict
        self.assertTrue(players_list, msg="The list of players not displayed")

        all_player = self.site.sport_event_details.tab_content.players_overlay.switchers.items_as_ordered_dict['All Players'].is_selected()
        self.assertTrue(all_player, msg='All Players is not selected by default in playerListContent')

        switchers = self.site.sport_event_details.tab_content.players_overlay.switchers
        self.assertTrue(switchers, msg='[All Players, Home, Away] tabs is not present in playerListContent')

    def test_003_lick_on_the_home__away_button_for_all_positions_except_goalkeeper(self):
        """
        DESCRIPTION: Сlick on the Home / Away button. (For all positions except Goalkeeper)
        EXPECTED: A list of players from the selected team is displayed (Home or Away) with corresponding chevrons.
        """
        self.site.sport_event_details.tab_content.players_overlay.switchers.items_as_ordered_dict['Home'].click()
        players_list = self.site.sport_event_details.tab_content.players_overlay.players_list.items_as_ordered_dict
        self.assertTrue(players_list, msg="The list of players not displayed")

    def test_004_lick_on_the_all_players_button_for_all_positions_except_goalkeeper(self):
        """
        DESCRIPTION: Сlick on the 'All Players' button. (For all positions except Goalkeeper)
        EXPECTED: A list of players from both teams is displayed (Home and Away).
        """
        self.site.sport_event_details.tab_content.players_overlay.switchers.items_as_ordered_dict['All Players'].click()
        players_list = self.site.sport_event_details.tab_content.players_overlay.players_list.items_as_ordered_dict
        self.assertTrue(players_list, msg="The list of players not displayed")

    def test_005_verify_a_player_card_content(self):
        """
        DESCRIPTION: Verify a player card content.
        EXPECTED: Player card should contain such details:
        EXPECTED: - Name of a player.
        EXPECTED: - Team name.
        EXPECTED: - Crest of the team made up of primary and secondary color set in CMS.
        EXPECTED: - Position playing (If received from Opta) [Goalkeeper -(GK), Defender - (DF), Midfielder - (MF), Forward -()].
        EXPECTED: - Stats of the player (If received from Opta).
        EXPECTED: - Chevron indicating the user can tap on the player - when tapped launch the player card.
        """
        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_name
        self.assertTrue(player_name, msg='Player name is not present in playerListContent')

        stats_label = self.site.sport_event_details.tab_content.players_overlay.players_list.stats_label
        self.assertTrue(stats_label, msg='stats_label is not present in playerListContent')

        team_name = self.site.sport_event_details.tab_content.players_overlay.players_list.team_name
        self.assertTrue(team_name, msg='team_name is not present in playerListContent')

    def test_006_click_on_the_back_button(self):
        """
        DESCRIPTION: Click on the 'Back' button.
        EXPECTED: User is returned to the pitch view.
        """
        self.site.sport_event_details.tab_content.players_overlay.back_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')

    def test_007_return_to_the_player_list_view_overlay_and_click_on_one_of_players_card(self):
        """
        DESCRIPTION: Return to the Player List View overlay and click on one of players card.
        EXPECTED: User is redirected to the 'Player card' of the selected player.
        """
        list(self.pitch_overlay.values())[1].icon.click()
        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_names
        self.assertTrue(player_name, msg='Players name is not present in playerListContent')
        self.assertTrue(len(player_name) > 2, msg='Player name list is empty')
