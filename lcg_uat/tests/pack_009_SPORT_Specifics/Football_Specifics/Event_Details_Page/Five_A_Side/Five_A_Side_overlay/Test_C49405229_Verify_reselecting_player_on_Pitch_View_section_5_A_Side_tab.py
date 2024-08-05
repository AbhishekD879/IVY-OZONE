import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
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
class Test_C49405229_Verify_reselecting_player_on_Pitch_View_section_5_A_Side_tab(BaseFiveASide, BaseSportTest,
                                                                                  BaseCashOutTest):
    """
    TR_ID: C49405229
    NAME: Verify reselecting player on 'Pitch View' section ( '5-A-Side' tab)
    DESCRIPTION: This test case verifies the ability to reselect previously chosen players on 'Pitch View' section on '5-A-Side' tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose on '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click/Tap '+' (add) button > Select any player > Click/Tap 'Add player'
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
        PRECONDITIONS: 3. Choose on '5-A-Side' tab
        PRECONDITIONS: 4. Click/Tap on 'Build' button
        PRECONDITIONS: 5. Click/Tap '+' (add) button > Select any player > Click/Tap 'Add player'
        """
        self.__class__.cms_formations = self.cms_config.get_five_a_side_formations()
        if not self.cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)

        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')

        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')

        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        wait_for_result(
            lambda: self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.is_displayed(
                timeout=10) is True,
            timeout=60)
        self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.click()

        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(self.pitch_overlay, msg='Players are not displayed on the Pitch View')

        list(self.pitch_overlay.values())[0].icon.click()
        self.site.sport_event_details.tab_content.players_overlay.players_list.items[0].click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')

        self.site.sport_event_details.tab_content.player_card.add_player_button.click()

    def test_001_verify_selected_players_on_pitch_view_section(self):
        """
        DESCRIPTION: Verify selected player(s) on 'Pitch View' section
        EXPECTED: 'Pitch View' section is displayed with the selected player(s)
        """
        actual_selected_player = list(self.pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(actual_selected_player, 'player-icon', msg='Selected player is not appearing in pitch view')
        self.__class__.actual_player_odd = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.player_odds.text

    def test_002_clicktap_on_any_previously_selected_player(self):
        """
        DESCRIPTION: Click/Tap on any previously selected player
        EXPECTED: 'Player Card' view of previously selected player is displayed with appropriate statistics info for that player (if available):
        EXPECTED: ![](index.php?/attachments/get/113306236)
        """
        list(self.pitch_overlay.values())[0].icon.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')

    def test_003_clicktap_on_back_button_on_player_card_view(self):
        """
        DESCRIPTION: Click/Tap on 'Back' button on 'Player Card' view
        EXPECTED: * 'Pitch View' section is displayed
        EXPECTED: * Player and odds remain unchanged
        """
        self.site.sport_event_details.tab_content.player_card.back_button.click()

        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        self.assertTrue(pitch_overlay, msg='Pitch View is not displayed')

        actual_selected_player = list(self.pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(actual_selected_player, 'player-icon', msg='Selected player is not appearing in pitch view')
        self.assertFalse(
            self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.place_bet_button.odd_place_bet.is_enabled(),
            msg='Place Bet button is not disabled, but was expected to be disabled')
        expected_player_odd = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.player_odds.text
        self.assertEqual(self.actual_player_odd, expected_player_odd, msg='player odds are changed')

    def test_004_clicktap_on_plus_add_button_for_any_position(self):
        """
        DESCRIPTION: Click/Tap on '+' (add) button for any position
        EXPECTED: 'Player List' view is displayed
        """
        list(self.pitch_overlay.values())[1].icon.click()
        self.assertTrue(self.site.sport_event_details.tab_content.players_overlay.players_list,
                        msg='Player List view is not displayed')

    def test_005_select_any_player_from_the_list(self):
        """
        DESCRIPTION: Select any player from the list
        EXPECTED: 'Player Card' view is displayed
        """
        self.site.sport_event_details.tab_content.players_overlay.players_list.items[1].click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')

    def test_006__clicktap_on_back_button_on_player_card_view_clicktap_on_back_button_on_player_list_view(self):
        """
        DESCRIPTION: * Click/Tap on 'Back' button on 'Player Card' view
        DESCRIPTION: * Click/Tap on 'Back' button on 'Player List' view
        EXPECTED: * 'Pitch View' section is displayed
        EXPECTED: * Player is not added to the position; '+' button to add a player is displayed
        EXPECTED: * Odds remain unchanged
        """
        self.site.sport_event_details.tab_content.player_card.back_button.click()
        self.site.sport_event_details.tab_content.players_overlay.back_button.click()

        pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay
        self.assertTrue(pitch_overlay, msg='Players are not displayed on the Pitch View')

        actual_selected_player = list(self.pitch_overlay.values())[1].icon.get_attribute('class')
        self.assertNotEqual(actual_selected_player, 'player-icon', msg='Selected player is appearing in pitch view')

        expected_player_odd = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.player_odds.text
        self.assertEqual(self.actual_player_odd, expected_player_odd, msg='player odds are changed')
