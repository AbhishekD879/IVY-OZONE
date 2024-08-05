import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.helpers import cleanhtml
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_prod  # Ladbrokes Only
@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C58996617_Verify_Remove_Selection_functionality_on_a_pitch_view_on_5_A_Side_tab(BaseFiveASide, BaseSportTest,
                                                                                           BaseCashOutTest):
    """
    TR_ID: C58996617
    NAME: Verify 'Remove Selection' functionality on a pitch view on '5-A-Side' tab
    DESCRIPTION: This test case verified 'Remove Selection' functionality on a pitch view on '5-A-Side' tab on Football EDP.
    PRECONDITIONS: 1. Event has configured 5-A-Side and BYB markets.
    PRECONDITIONS: 2. 5-A-Side config:
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (TI) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Opta statistics is mapped to the event (ask Natalia Shalay to help)
    PRECONDITIONS: - Formations are created and set up in CMS/BYB/5 A Side
    PRECONDITIONS: - Event is prematch (not live)
    """
    keep_browser_open = True
    proxy = None
    default_player_name = 'Keeper'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Event has configured 5-A-Side and BYB markets.
        PRECONDITIONS: 2. 5-A-Side config
        """
        self.__class__.cms_formations = self.cms_config.get_five_a_side_formations()
        if not self.cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: Application is opened.
        """
        self.navigate_to_page('Homepage')
        self.assertTrue(self.site.wait_content_state('homepage'), msg='User has not re-directed to homepage')

    def test_002_navigate_to_football_event_details_page_that_has_5_a_side_data_configured(self):
        """
        DESCRIPTION: Navigate to Football event details page that has 5-A-Side data configured.
        EXPECTED: Football EDP is opened.
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')

    def test_003_clicktap_on_5_a_side_tab(self):
        """
        DESCRIPTION: Click/Tap on '5-A-Side' tab.
        EXPECTED: '5-A-Side' tab with appropriate data is shown.
        """
        tab = self.site.sport_event_details.markets_tabs_list.items_names.__contains__('5-A-SIDE')
        self.assertTrue(tab,
                        msg=f'5-A-Side is tab is not present, active tabs are "{self.site.sport_event_details.markets_tabs_list.items_names}"')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')

        new_label_cms = self.cms_config.get_system_configuration_structure()['FiveASide']['newIcon']
        if new_label_cms:
            new_label_ui = self.site.sport_event_details.tab_content.new_label.text
            self.assertEquals(new_label_ui, 'NEW', msg='New label text is not present')
        static_block = self.cms_config.get_static_block(uri='five-a-side-launcher')
        cms_title = cleanhtml(static_block['htmlMarkup']).splitlines()[1]
        cms_text = cleanhtml(static_block['htmlMarkup']).splitlines()[2]

        ui_title = self.site.sport_event_details.tab_content.five_a_side_title
        self.assertEquals(cms_title, ui_title,
                          msg=f'Title from UI "{ui_title}" does not match with cms title"{cms_title}"')
        ui_text = self.site.sport_event_details.tab_content.five_a_side_text
        self.assertEquals(cms_text, ui_text, msg=f'Text from UI "{ui_text}" does not match with cms text"{cms_text}"')
        build_button = self.site.sport_event_details.tab_content.team_launcher.build_button.is_displayed()
        self.assertTrue(build_button, msg='Build button is not displayed')

    def test_004_clicktap_build_your_team_button_ladbrokes_build_button_coral(self):
        """
        DESCRIPTION: Click/Tap 'Build Your Team' button (Ladbrokes) 'Build' button (Coral).
        EXPECTED: Pitch view with created formations is shown.
        """
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        if tests.settings.backend_env == 'prod':
            wait_for_result(
                lambda: self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.is_displayed(
                    timeout=10) is True,
                timeout=60)
            self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.click()

        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
        current_url = self.device.get_current_url()
        self.assertTrue(current_url.endswith(f'{self.event_id}/5-a-side/pitch'),
                        msg=f'Current url "{current_url}" not ends with "{self.event_id}/5-a-side/pitch"')

        cms_active_formation = self.cms_formations[0]
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        formation_carousel = self.pitch_overlay.content.formation_carousel.items_as_ordered_dict
        self.assertTrue(formation_carousel, msg='Formation toggles carousel is not displayed')
        formation_name, formation_item = next(iter(formation_carousel.items()))
        cms_formation_name = cms_active_formation.get("title").upper()
        self.assertEqual(formation_name, cms_formation_name,
                         msg=f'Formation name "{formation_name}" is not the same as expected '
                             f'from cms "{cms_formation_name}"')

    def test_005_clicktap_on_plus_button_for_any_position_on_any_formation(self):
        """
        DESCRIPTION: Click/Tap on '+' button for any position on any formation.
        EXPECTED: The list of players is shown for both teams for the opened market.
        """
        team_name_pitchview = self.pitch_overlay.content.sub_header.event_name.split(' V ')
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(self.pitch_overlay, msg='Players are not displayed on the Pitch View')
        list(self.pitch_overlay.values())[0].icon.click()

        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_names
        self.assertTrue(player_name, msg='Players name is not present in playerListContent')
        self.assertTrue(len(player_name) > 2, msg='Player name list is empty')

        self.assertTrue(self.site.sport_event_details.tab_content.players_overlay.players_list.team_names,
                        msg='team_name is not present in playerListContent')
        team_name = [team_names.text.split('(')[0] for team_names in
                     self.site.sport_event_details.tab_content.players_overlay.players_list.team_names]
        self.assertEqual(sorted(set(team_name)), sorted(team_name_pitchview),
                         msg=f'team name in player list "{team_name}", is not matching with team name in pitch view "{team_name_pitchview}"')

    def test_006_clicktap_on_some_player_and_then_clicktap_add_player_button(self):
        """
        DESCRIPTION: Click/Tap on some player and then click/tap 'Add Player' button.
        EXPECTED: Selected Player is shown on the position, opened `C17727964` the previous step.
        """
        self.site.sport_event_details.tab_content.players_overlay.players_list.items[0].click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')
        self.site.sport_event_details.tab_content.player_card.add_player_button.click()
        actual_selected_player = list(self.pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(actual_selected_player, 'player-icon', msg='Selected player is not appearing in pitch view')

    def test_007_clicktap_on_just_filled_position(self):
        """
        DESCRIPTION: Click/Tap on just filled position.
        EXPECTED: 'Edit Player' card/overlay is shown with 'Remove Selection' button and other info.
        """
        list(self.pitch_overlay.values())[0].icon.click()
        self.assertTrue(self.site.sport_event_details.tab_content.player_card.remove_selection.is_displayed(),
                        msg='Remove selection link is not present in Player card view')
        update_player = self.site.sport_event_details.tab_content.player_card.add_player_button.name.split('\n')[2].__contains__('UPDATE PLAYER')
        self.assertTrue(update_player, msg='Update player button is not present in edit player mode')

    def test_008_clicktap_remove_selection_button(self):
        """
        DESCRIPTION: Click/Tap 'Remove Selection' button.
        EXPECTED: 'Remove Player' pop-up appeared with 'Are you sure you want to remove this player from your team? message and 'Cancel'/'Remove' buttons.
        """
        self.site.sport_event_details.tab_content.player_card.remove_selection.click()
        self.__class__.remove_player_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_PLAYER,
                                                                        timeout=40)
        self.assertTrue(self.remove_player_dialog,
                        msg='Remove Player dailog is not shown, after clicking on removing selection in player card view')
        self.assertEqual(vec.five_a_side.REMOVE_PLAYER, self.remove_player_dialog.pop_up_text,
                         msg=f'Actual text "{self.remove_player_dialog.pop_up_text}" is not matching with expected text "{vec.five_a_side.REMOVE_PLAYER}"')
        self.assertTrue(self.remove_player_dialog.remove_player.is_displayed(),
                        msg='Remove player button is not present on Remove player dailog box')
        self.assertTrue(self.remove_player_dialog.cancel.is_displayed(),
                        msg='Cancel button is not present on Remove player dailog box')

    def test_009_clicktap_cancel_button(self):
        """
        DESCRIPTION: Click/Tap 'Cancel' button
        EXPECTED: 'Remove Player' pop-up is closed and user stays on 'Edit Player' card/overlay.
        """
        self.remove_player_dialog.cancel.click()
        self.assertFalse(self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_PLAYER, timeout=5),
                         msg='Remove player dialog is not closed upon clicking on cancel button')
        self.assertTrue(self.site.sport_event_details.tab_content.player_card.remove_selection.is_displayed(),
                        msg='Remove selection link is not present in Player card view')
        update_player = self.site.sport_event_details.tab_content.player_card.add_player_button.name.split('\n')[2].__contains__('UPDATE PLAYER')
        self.assertTrue(update_player, msg='Update player button is not present in edit player mode')

    def test_010_clicktap_remove_selection_button_and_then_confirm_removal_action(self):
        """
        DESCRIPTION: Click/Tap 'Remove Selection' button and then confirm removal action.
        EXPECTED: Pitch view is loaded and the removed player is not displayed on it.
        EXPECTED: Odds are updated accordingly to not include removed Player.
        """
        self.site.sport_event_details.tab_content.player_card.remove_selection.click()
        remove_player_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_PLAYER, timeout=40)
        self.assertTrue(self.remove_player_dialog, msg='Remove Player dailog is not shown, after clicking on removing selection in player card view')
        remove_player_dialog.remove_player.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
        selected_player = list(self.pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(selected_player, 'player-icon not-selected-player-icon',
                         msg='Selected player is appearing in pitch view, after removing selection')
        odd_value = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.place_bet_button.odd_place_bet.text.split('\n')[0]
        self.assertEquals(odd_value, '-/-',
                          msg=f'odd value is not correct, expected "-/-", and actual value is "{odd_value}"')
        player_name = list(self.pitch_overlay.values())[0].added_player_name
        self.assertEquals(player_name, self.default_player_name, msg='Player is not removed from pitch view')
