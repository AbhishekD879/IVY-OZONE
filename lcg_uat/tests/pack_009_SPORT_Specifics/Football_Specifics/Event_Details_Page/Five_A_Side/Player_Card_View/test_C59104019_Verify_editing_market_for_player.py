import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_prod  # Ladbrokes Only
@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.five_a_side
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@vtest
class Test_C59104019_Verify_editing_market_for_player(BaseFiveASide, BaseSportTest, BaseCashOutTest):
    """
    TR_ID: C59104019
    NAME: Verify editing market for player
    DESCRIPTION: This test case verifies the ability to edit of player's previously selected market on 'Player Card' view on '5-A-Side' tab
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Football event details page that has all 5-A-Side configs
    PRECONDITIONS: 3. Choose on '5-A-Side' tab
    PRECONDITIONS: 4. Click/Tap on 'Build' button
    PRECONDITIONS: 5. Click/Tap '+' (add) button > Select any player
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
        PRECONDITIONS: 1. Event has configured 5-A-Side and BYB markets.
        PRECONDITIONS: 2. 5-A-Side config
        PRECONDITIONS: Navigate to Football event details page that has 5-A-Side data configured.
        PRECONDITIONS: Click/Tap on '5-A-Side' tab.
        PRECONDITIONS: Click/Tap on 'Build' button
        """
        cms_formations = self.cms_config.get_five_a_side_formations()
        if not cms_formations:
            raise CmsClientException('5-A-Side formations list from CMS is empty')
        event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        self.navigate_to_edp(event_id=event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        tab = self.site.sport_event_details.markets_tabs_list.items_names.__contains__('5-A-SIDE')
        self.assertTrue(tab,
                        msg=f'5-A-Side is tab is not present, active tabs are "{self.site.sport_event_details.markets_tabs_list.items_names}"')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')
        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        if tests.settings.backend_env == 'prod':
            wait_for_result(
                lambda: self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.is_displayed(
                    timeout=10) is True,
                timeout=60)
            self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.items_as_ordered_dict
        self.assertTrue(self.pitch_overlay, msg='Players are not displayed on the Pitch View')
        list(self.pitch_overlay.values())[0].icon.click()
        player_name = self.site.sport_event_details.tab_content.players_overlay.players_list.player_names
        self.assertTrue(player_name, msg='Players name is not present in playerListContent')
        self.assertTrue(len(player_name) > 2, msg='Player name list is empty')

    def test_001_verify_player_card_view(self):
        """
        DESCRIPTION: Verify 'Player Card' view
        EXPECTED: * Selected player is displayed with appropriate statistics info for that player (if available)
        EXPECTED: * Drop-down with the list of the markets applicable for the player is displayed
        EXPECTED: * 'Add player' button
        EXPECTED: ![](index.php?/attachments/get/114764015)
        """
        self.site.sport_event_details.tab_content.players_overlay.players_list.items[0].click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')
        market_dropDown = self.site.sport_event_details.tab_content.player_card.market_drop_down
        self.assertTrue(market_dropDown, msg='Drop-down with the list of the markets is not present in player cards')
        add_player = self.site.sport_event_details.tab_content.player_card.add_player_button
        self.assertTrue(add_player, msg='Add a player button is not present in player cards')

    def test_002_clicktap_add_player(self):
        """
        DESCRIPTION: Click/Tap 'Add player'
        EXPECTED: 'Pitch View' section is displayed with the selected player(s)
        """
        self.site.sport_event_details.tab_content.player_card.add_player_button.click()
        actual_selected_player = list(self.pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(actual_selected_player, 'player-icon', msg='Selected player is not appearing in pitch view')
        self.__class__.actual_player_odd = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.player_odds.text

    def test_003_clicktap_on_previously_selected_player(self):
        """
        DESCRIPTION: Click/Tap on previously selected player
        EXPECTED: * 'Player Card' view of previously selected player is displayed with appropriate statistics info for that player (if available)
        EXPECTED: * Drop-down with the list of the markets applicable for the player is displayed (Markets are not limited with current formation and are taken from 'player-statistics?obEventId=978373&playerId=52' request)
        EXPECTED: * 'Update player' button
        EXPECTED: ![](index.php?/attachments/get/114764017)
        """
        list(self.pitch_overlay.values())[0].icon.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                        msg='Player Card is not shown')
        market_dropDown = self.site.sport_event_details.tab_content.player_card.market_drop_down
        self.assertTrue(market_dropDown, msg='Drop-down with the list of the markets is not present in player cards')
        update_player_btn = self.site.sport_event_details.tab_content.player_card.update_player_button
        self.assertTrue(update_player_btn, msg='Update player button is not present in player cards')

    def test_004_clicktap_on_back_button_on_player_card_view(self):
        """
        DESCRIPTION: Click/Tap on 'Back' button on 'Player Card' view
        EXPECTED: * 'Pitch View' section is displayed
        EXPECTED: * Player, player's market and odds remain unchanged
        """
        self.site.sport_event_details.tab_content.player_card.back_button.click()
        actual_selected_player = list(self.pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(actual_selected_player, 'player-icon', msg='Selected player is not appearing in pitch view')
        self.assertFalse(
            self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.place_bet_button.odd_place_bet.is_enabled(),
            msg='Place Bet button is not disabled, but was expected to be disabled')
        expected_player_odd = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.player_odds.text
        self.assertEqual(self.actual_player_odd, expected_player_odd, msg='player odds are changed')

    def test_005_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step #3
        """
        self.test_003_clicktap_on_previously_selected_player()

    def test_006_clicktap_drop_down___select_any_market_from_available(self):
        """
        DESCRIPTION: Click/Tap drop-down -> Select any market from available
        EXPECTED: * Market for player is changed
        EXPECTED: * Market specific options are changed accordingly
        EXPECTED: * Player stats are changed accordingly
        EXPECTED: * Odds are changed accordingly
        """
        self.site.sport_event_details.tab_content.player_card.market_drop_down.click()
        markets_dropdown_list = list(self.site.sport_event_details.tab_content.player_card.items_as_ordered_dict.keys())
        self.site.sport_event_details.tab_content.player_card.market_drop_down.click()
        default_market = self.site.sport_event_details.tab_content.player_card.selected_market.text
        actual_stats = self.site.sport_event_details.tab_content.player_card.stat_value.text
        actual_odds = self.site.sport_event_details.tab_content.player_card.player_odds.text
        for market in markets_dropdown_list:
            self.site.sport_event_details.tab_content.player_card.market_drop_down.click()
            self.site.sport_event_details.tab_content.player_card.items_as_ordered_dict[market].click()
            if market == default_market:
                expected_stats = self.site.sport_event_details.tab_content.player_card.stat_value.text
                self.assertEqual(actual_stats, expected_stats,
                                 msg=f'actual stat value : "{actual_stats}" '
                                     f'is not equal to expected stat value : "{expected_stats}"')
                self.__class__.expected_odds = self.site.sport_event_details.tab_content.player_card.player_odds.text
                self.assertEqual(actual_odds, self.expected_odds,
                                 msg=f'actual odds value : "{actual_odds}" '
                                     f'is not equal to expected odds value : "{self.expected_odds}"')
            else:
                expected_stats = self.site.sport_event_details.tab_content.player_card.stat_value.text
                self.assertNotEqual(actual_stats, expected_stats,
                                    msg=f'actual stat value : "{actual_stats}" '
                                        f'is equal to expected stat value : "{expected_stats}"')
                self.__class__.expected_odds = self.site.sport_event_details.tab_content.player_card.player_odds.text
                self.assertNotEqual(actual_odds, self.expected_odds,
                                    msg=f'actual odds value : "{actual_odds}" '
                                        f'is equal to expected odds value : "{self.expected_odds}"')

    def test_007_repeat_step_6_few_times(self):
        """
        DESCRIPTION: Repeat step #6 few times
        """
        # Covered in step 6

    def test_008_click_update_player(self):
        """
        DESCRIPTION: Click 'Update Player'
        EXPECTED: * 'Pitch View' section is displayed
        EXPECTED: * Player is not changing it's position on the pitch
        EXPECTED: * The last selected market from step #7 is displayed
        EXPECTED: * Changed odds are displayed
        """
        self.site.sport_event_details.tab_content.player_card.update_player_button.click()
        self.assertTrue(self.pitch_overlay, msg='Pitch View section is not displayed')
        actual_selected_player = list(self.pitch_overlay.values())[0].icon.get_attribute('class')
        self.assertEqual(actual_selected_player, 'player-icon', msg='Selected player is not appearing in pitch view')
        actual_player_odd = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field.player_odds.text
        self.assertEqual(actual_player_odd, self.expected_odds,
                         msg=f'actual odds value : "{actual_player_odd}" '
                             f'is not equal to expected odds value : "{self.expected_odds}"')
