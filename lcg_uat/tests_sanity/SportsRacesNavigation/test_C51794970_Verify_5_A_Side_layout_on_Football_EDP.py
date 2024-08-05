import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name, cleanhtml
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_prod  # Ladbrokes Only
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.sanity
@vtest
class Test_C51794970_Verify_5_A_Side_layout_on_Football_EDP(BaseFiveASide, BaseSportTest, BaseCashOutTest):
    """
    TR_ID: C51794970
    NAME: Verify '5-A-Side' layout on Football EDP
    DESCRIPTION: This test case verifies '5-A-Side' layout on Football EDP
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - '5-A-Side' tab is created in CMS > EDP Markets
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Statistic is mapped for the particular event. Use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91089483#OPTA/BWINScoreboardmappingtoanOBevent-Appendix_A
    PRECONDITIONS: - Player's statisctic takes from local storage 'scoreBoards_dev_prematch_eventId':
    PRECONDITIONS: ![](index.php?/attachments/get/73440082)
    PRECONDITIONS: - Players are taken from Banach provider and received in the following response:
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/players?obEventId=XXXXX
    PRECONDITIONS: where
    PRECONDITIONS: XXXXX - Event ID
    PRECONDITIONS: ![](index.php?/attachments/get/62325587)
    PRECONDITIONS: - The Outfield player's stats label mapping according to stats name from CMS and stats value from OPTA:
    PRECONDITIONS: ![](index.php?/attachments/get/90015196)
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load the app
        DESCRIPTION: Navigate to Football event details page that has all 5-A-Side configs
        """
        self.__class__.cms_formations = self.cms_config.get_five_a_side_formations()
        if not self.cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'***Found Football 5-A-Side event {self.event_name} with id "{self.event_id}"')
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')

    def test_001_verify_5_a_side_tab_displaying(self):
        """
        DESCRIPTION: Verify '5-A-Side' tab displaying
        EXPECTED: * '5-A-Side' tab is present on EDP
        EXPECTED: * 'New' label is displayed on the tab if it's enabled in CMS
        EXPECTED: * '5-A-Side' tab is displayed in the order set in CMS
        """
        tab = self.site.sport_event_details.markets_tabs_list.items_names.__contains__('5-A-SIDE')
        self.assertTrue(tab, msg=f'5-A-Side is tab is not present, active tabs are "{self.site.sport_event_details.markets_tabs_list.items_names}"')

        markets_tabs = self.site.sport_event_details.markets_tabs_list.items_as_ordered_dict
        self.verify_edp_market_tabs_order(edp_market_tabs=markets_tabs.keys())
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')

        new_label_cms = self.cms_config.get_system_configuration_structure()['FiveASide']['newIcon']
        if new_label_cms:
            new_label_ui = self.site.sport_event_details.tab_content.new_label.text
            self.assertEquals(new_label_ui, 'NEW', msg='New label text is not present')

    def test_002_clicktap_on_the_5_a_side_tab(self):
        """
        DESCRIPTION: Click/Tap on the '5-A-Side' tab
        EXPECTED: * '5-A-Side' tab is selected and highlighted
        EXPECTED: * URL ends with event_id/5-a-side
        """
        # Expected-1 is covered in step-1
        current_url = self.device.get_current_url()
        self.assertTrue(current_url.endswith(f'{self.event_id}/5-a-side'),
                        msg=f'Current url "{current_url}" not ends with "{self.event_id}/5-a-side"')

    def test_003_verify_5_a_side_launcher_content(self):
        """
        DESCRIPTION: Verify '5-A-Side' launcher content
        EXPECTED: * '5-A-Side' launcher is present when '5-A-Side' tab is selected
        EXPECTED: * Content of '5-A-Side' tab corresponds to 'five-a-side-launcher' static block in CMS > Static Blocks
        EXPECTED: * Title
        EXPECTED: * Text
        EXPECTED: * Button
        EXPECTED: * 'five-a-side-launcher' response is received from CMS with data set in CMS
        """
        static_block = self.cms_config.get_static_block(uri='five-a-side-launcher')
        cms_title = cleanhtml(static_block['htmlMarkup']).splitlines()[1]
        cms_text = cleanhtml(static_block['htmlMarkup']).splitlines()[2]

        ui_title = self.site.sport_event_details.tab_content.five_a_side_title
        self.assertEquals(cms_title, ui_title, msg=f'Title from UI "{ui_title}" does not match with cms title"{cms_title}"')
        ui_text = self.site.sport_event_details.tab_content.five_a_side_text
        self.assertEquals(cms_text, ui_text, msg=f'Text from UI "{ui_text}" does not match with cms text"{cms_text}"')
        build_button = self.site.sport_event_details.tab_content.team_launcher.build_button.is_displayed()
        self.assertTrue(build_button, msg='Build button is not displayed')

    def test_004_clicktap_on_the_build_team_button(self):
        """
        DESCRIPTION: Click/Tap on the 'Build Team' button
        EXPECTED: * '5-A-Side' overlay is loaded
        EXPECTED: * URL ends with event_id/5-a-side/pitch
        """
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(), msg='Pitch overlay is not shown')
        current_url = self.device.get_current_url()
        self.assertTrue(current_url.endswith(f'{self.event_id}/5-a-side/pitch'),
                        msg=f'Current url "{current_url}" not ends with "{self.event_id}/5-a-side/pitch"')

    def test_005_verify_5_a_side_overlay_content(self):
        """
        DESCRIPTION: Verify '5-A-Side' overlay content
        EXPECTED: * '5-A-Side' header with the following elements:
        EXPECTED: * 'Ladbrokes 5-A-Side' title
        EXPECTED: *'Select a formation and build your team' instruction text
        EXPECTED: * Formation toggles carousel with created formations in CMS
        EXPECTED: * Close 'x' button
        EXPECTED: * '5-A-Side' subheader with the following elements:
        EXPECTED: * Event name
        EXPECTED: * Selected formation (corresponds to value in 'Actual formation' dropdown in CMS e.g. 1-1-2-1)
        EXPECTED: * '5-A-Side' pitch view with the following elements:
        EXPECTED: * ('+') 'Add Player' buttons
        EXPECTED: * Player Information:
        EXPECTED: * Positions (corresponds to entered in CMS 'Position' input field)
        EXPECTED: * Statistics (corresponds to selected in CMS 'Stat' dropdown)
        EXPECTED: * 'Odds/Place Bet' button is disabled by default
        EXPECTED: * Background Pitch Image
        """
        if tests.settings.backend_env == 'prod':
            wait_for_result(lambda: self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.is_displayed(timeout=10) is True,
                            timeout=60)
            self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.click()
        cms_active_formation = self.cms_formations[0]
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        title = self.pitch_overlay.header.title
        self.assertTrue(title,
                        msg=f'Header title "{title}" is not available on UI "{vec.yourcall.FIVE_A_SIDE_DRAWER_TITLE}"')
        instruction = self.pitch_overlay.header.instruction_text
        self.assertEqual(
            instruction, vec.yourcall.SELECT_FORMATION,
            msg=f'Instruction text "{instruction}" is not the same as expected "{vec.yourcall.SELECT_FORMATION}"')
        formation_carousel = self.pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_name, formation_item = next(iter(formation_carousel.items()))
        cms_formation_name = cms_active_formation.get("title").upper()
        self.assertEqual(formation_name, cms_formation_name,
                         msg=f'Formation name "{formation_name}" is not the same as expected '
                             f'from cms "{cms_formation_name}"')
        self.assertTrue(formation_item.has_icon(), msg='Formation icon is not displayed')
        self.assertTrue(self.pitch_overlay.header.has_close_button(), msg='Close "x" button is not displayed')

        event_name = self.pitch_overlay.content.sub_header.event_name
        ss_event_name = self.event_name.upper()
        self.assertEqual(event_name, ss_event_name.split(' (')[0],
                         msg=f'Event name "{event_name}" on sub-header is not the same as expected "{ss_event_name}"')
        formation_value = self.pitch_overlay.content.formation_value
        cms_formation_value = cms_active_formation.get("actualFormation")
        self.assertEqual(formation_value, cms_formation_value,
                         msg=f'Formation "{formation_value}" on sub-header is not the same as expected '
                             f'from cms "{cms_formation_value}"')

        statistics = []
        for stat in self.stat_keys:
            if stat in cms_active_formation.keys():
                statistics.append(cms_active_formation.get(stat).get('title'))
        markets = self.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(markets, msg='Players are not displayed on the Pitch View')
        for market_name, market in markets.items():
            self.assertTrue(market.icon.is_displayed(), msg='Add button is not shown')
            self.assertIn(market_name, statistics,
                          msg=f'Cannot find statistic/market "{market_name}" in "{statistics}"')
        self.assertFalse(self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.place_bet_button.odd_place_bet.is_enabled(),
                         msg='"Odds/Place Bet" button is enabled whereas it should be disabled')

    def test_006_clicktap_on_the_plus_add_player_buttonverify_the_player_list_view_content(self):
        """
        DESCRIPTION: Click/Tap on the ('+') 'Add Player' button.
        DESCRIPTION: Verify the 'Player List' view content.
        EXPECTED: * 'Player List' view is opened
        EXPECTED: * 'Player List' view contains the following elements:
        EXPECTED: * '< Back' button
        EXPECTED: * Title "Add a 'Position name'" below the 'Back' button (e.g 'Add a Cruncher'. Position name sets in the CMS)
        EXPECTED: * Subtitle is the name of the Statistic (e.g. To Win X Tackles, To Make X Passes etc. sets in the CMS)
        EXPECTED: * 'All Players'(selected by default), 'Home', 'Away' buttons. (For all positions except Goalkeeper).
        EXPECTED: * Event name
        EXPECTED: * The list of players that contains:
        EXPECTED: * Crest of the team made up of primary and secondary color set in CMS
        EXPECTED: * Team name
        EXPECTED: * Position playing (If available from Datahub feed) [Goalkeeper -(GK), Defender - (DF), Midfielder - (MF), Forward -(FW)]
        EXPECTED: * Player name
        EXPECTED: * Stats label and value of the player (e.g. 0, 1, N/A, etc.)
        EXPECTED: * Chevron indicating the user can tap on the player - when tapped launch the player card
        """
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(self.pitch_overlay, msg='Players are not displayed on the Pitch View')
        list(self.pitch_overlay.values())[1].icon.click()

        back_button = self.site.sport_event_details.tab_content.players_overlay.back_button
        self.assertTrue(back_button, msg='Back button is not present in playerListContent')

        title = self.site.sport_event_details.tab_content.players_overlay.title
        self.assertTrue(title, msg='Title is not present in playerListContent')

        sub_title = self.site.sport_event_details.tab_content.players_overlay.sub_title
        self.assertTrue(sub_title, msg='Sub-title is not present in playerListContent')

        all_player = self.site.sport_event_details.tab_content.players_overlay.switchers.items_as_ordered_dict['All Players'].is_selected()
        self.assertTrue(all_player, msg='All Players is not selected by default in playerListContent')

        switchers = self.site.sport_event_details.tab_content.players_overlay.switchers
        self.assertTrue(switchers, msg='[All Players, Home, Away] tabs is not present in playerListContent')

        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_name
        self.assertTrue(player_name, msg='Player name is not present in playerListContent')

        stats_label = self.site.sport_event_details.tab_content.players_overlay.players_list.stats_label
        self.assertTrue(stats_label, msg='stats_label is not present in playerListContent')

        team_name = self.site.sport_event_details.tab_content.players_overlay.players_list.team_name
        self.assertTrue(team_name, msg='team_name is not present in playerListContent')

        players = self.site.sport_event_details.tab_content.players_overlay.players_list.items
        for player in players:
            player.click()
            if self.site.sport_event_details.tab_content.wait_for_players_card():
                break
            else:
                five_a_side_dailog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_5ASIDE_PLAYER_NOT_SELECTED, timeout=5)
                five_a_side_dailog.ok_thanks_btn.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(), msg='Player Card is not shown')

    def test_007_select_the_player_by_clickingtapping_on_the_cardverify_the_player_card_view_content(self):
        """
        DESCRIPTION: Select the player by clicking/tapping on the card.
        DESCRIPTION: Verify the 'Player Card' view content.
        EXPECTED: * 'Player Card' view is opened
        EXPECTED: * 'Player Card' view contains the following elements:
        EXPECTED: * '< Back' button
        EXPECTED: * 'Player name' below the 'Back' button
        EXPECTED: * 'Team name'|'Player position' (if received from Data Hub provider)
        EXPECTED: * Selected market (e.g. 'Goals Inside The Box')
        EXPECTED: * 'Player name' + to have + 'Stats value' + 'Stats name'
        EXPECTED: * 'Stats value' (eg. 1+) where default step value is displayed as average stat value with clickable +/- buttons on the sides
        EXPECTED: * List of Player statistics (eg. Goals, Assists, etc.)
            EXPECTED: * 'Odds/Add Player' button at the bottom with dynamic odds
        """
        back_button = self.site.sport_event_details.tab_content.player_card.back_button
        self.assertTrue(back_button, msg='Back button is not present in player cards')

        player_name = self.site.sport_event_details.tab_content.player_card.player_name
        self.assertTrue(player_name, msg='Player name is not present in player cards')

        team_name = self.site.sport_event_details.tab_content.player_card.team_name
        self.assertTrue(team_name, msg='Team name is not present in player cards')

        selected_market = self.site.sport_event_details.tab_content.player_card.selected_market
        self.assertTrue(selected_market, msg='Selected market is not present in player cards')

        stats_value = self.site.sport_event_details.tab_content.player_card.stat_value
        self.assertTrue(stats_value, msg='Stats value is not present in player cards')

        player_list = self.site.sport_event_details.tab_content.player_card.player_list
        self.assertTrue(player_list, msg='Player list is not present in player cards')

        add_player = self.site.sport_event_details.tab_content.player_card.add_player_button
        self.assertTrue(add_player, msg='Add a player button is not present in player cards')

    def test_008_clicktap_on_the_oddsadd_player_buttonverify_the_5_a_side_overlay_content(self):
        """
        DESCRIPTION: Click/Tap on the 'Odds/Add Player' button.
        DESCRIPTION: Verify the '5-A-Side' overlay content.
        EXPECTED: * The player is added and displayed on the corresponding position on the 'Pitch View'
        EXPECTED: * 'Odds/Place Bet' button is disabled
        """
        self.site.sport_event_details.tab_content.player_card.add_player_button.click()
        self.assertTrue(list(self.pitch_overlay.values())[1], msg='Failed to display added Player\'s Name')
        self.assertFalse(self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.place_bet_button.odd_place_bet.is_enabled(),
                         msg='Place Bet button is not disabled, but was expected to be disabled')

    def test_009_add_one_more_playerverify_the_5_a_side_overlay_content(self):
        """
        DESCRIPTION: Add one more Player.
        DESCRIPTION: Verify the '5-A-Side' overlay content.
        EXPECTED: * The players are added and displayed on the corresponding position on the 'Pitch View'
        EXPECTED: * 'Odds/Place Bet' button is active
        """
        list(self.pitch_overlay.values())[0].icon.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_overlay(), msg='Players Overlay is not shown')
        players = self.site.sport_event_details.tab_content.players_overlay.players_list.items
        for player in players:
            player.click()
            if self.site.sport_event_details.tab_content.wait_for_players_card():
                break
            else:
                five_a_side_dailog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_5ASIDE_PLAYER_NOT_SELECTED, timeout=5)
                five_a_side_dailog.ok_thanks_btn.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(), msg='Player Card is not shown')
        self.site.sport_event_details.tab_content.player_card.add_player_button.click()
        self.assertTrue(list(self.pitch_overlay.values())[0], msg='Failed to display added Player\'s Name')
        self.assertTrue(self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.place_bet_button.odd_place_bet.is_enabled(),
                        msg='Place Bet button is not enabled, but was expected to be enabled')
