import pytest
import tests
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide
from time import sleep


@pytest.mark.lad_tst2  # Ladbrokes Only
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod  # Cannot change event state in prod
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.desktop
@vtest
class Test_C59549184_Verify_5_A_Side_BYB_tabs_handling_when_user_is_on_EDP_and_event_goes_Live(BaseFiveASide):
    """
    TR_ID: C59549184
    NAME: Verify 5-A-Side/BYB tabs handling when user is on EDP and event goes Live
    DESCRIPTION: This TC verifies that 5-A-Side/BYB tabs disappear and user is redirected to All Markets tab when event goes live
    PRECONDITIONS: 5-A-Side/BYB event
    """
    keep_browser_open = True
    proxy = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if tests.settings.backend_env != 'prod':
            ob_config = cls.get_ob_config()
            ob_config.make_event_live(market_id=cls.market_id, event_id=cls.event_id, is_live=False)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Navigate to Football event details page that has all 5-A-Side configs
        DESCRIPTION: Choose the '5-A-Side' tab
        DESCRIPTION: Click/Tap on the 'Build Team' button on '5-A-Side' launcher
        DESCRIPTION: Login
        EXPECTED: Make sure that '5-A-Side' overlay is opened
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)
        self.__class__.market_id = event_resp[0]['event']['children'][0]['market']['id']

    def test_001_navigate_to_any_tab_except_5_a_sidebyb_edp_of_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to any tab (except 5-A-Side/BYB) EDP of event from preconditions
        EXPECTED: User is on EDP
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')

    def test_002_trigger_push_update_from_ti_event_should_become_live(self):
        """
        DESCRIPTION: Trigger Push update from TI (Event should become Live)
        EXPECTED: - Live Push update is received on UI
        EXPECTED: - 5-A-Side/BYB tabs disappeared from EDP
        """
        self.ob_config.make_event_live(market_id=self.market_id, event_id=self.event_id)
        sleep(3)
        market_tab_list = self.site.sport_event_details.markets_tabs_list.items_names
        tab_name = self.expected_market_tabs.five_a_side
        self.assertFalse(tab_name in market_tab_list, msg=f'"{tab_name}" is still present in "{market_tab_list}"')

    def test_003_update_event_in_ti_make_it_pre_match_again__reload_page_and_navigate_to_5_a_sidebyb_tab(self):
        """
        DESCRIPTION: - Update event in TI (make it pre-match again)
        DESCRIPTION: - Reload page and navigate to 5-A-Side/BYB tab
        EXPECTED: User is on 5-A-Side/BYB tab
        """
        self.ob_config.make_event_live(market_id=self.market_id, event_id=self.event_id, is_live=False)
        self.device.refresh_page()
        sleep(3)
        market_tab_list = self.site.sport_event_details.markets_tabs_list.items_names
        tab_name = self.expected_market_tabs.five_a_side
        self.assertTrue(tab_name in market_tab_list, msg=f'"{tab_name}" is still present in "{market_tab_list}"')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')

    def test_004_trigger_push_update_from_ti_event_should_become_live(self):
        """
        DESCRIPTION: Trigger Push update from TI (Event should become Live)
        EXPECTED: - Live Push update is received on UI
        EXPECTED: - User is redirected to All Markets tab
        EXPECTED: - 5-A-Side/BYB tabs disappeared(not shown on EDP)
        """
        self.ob_config.make_event_live(market_id=self.market_id, event_id=self.event_id)
        sleep(3)
        market_tab_list = self.site.sport_event_details.markets_tabs_list.items_names
        tab_name = self.expected_market_tabs.five_a_side
        self.assertFalse(tab_name in market_tab_list, msg=f'"{tab_name}" is still present in "{market_tab_list}"')

        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.all_markets,
                         msg='User is not redirected to "All Markets" tab')

    def test_005_update_event_in_ti_make_it_pre_match_again__reload_page_and_navigate_to_5_a_sidebyb_tab__add_some_selection_to_byb_dashboard_or_5_a_side_pitch_view(self):
        """
        DESCRIPTION: - Update event in TI (make it pre-match again)
        DESCRIPTION: - Reload page and navigate to 5-A-Side/BYB tab
        DESCRIPTION: - Add some selection to BYB dashboard or 5-A-Side pitch view
        EXPECTED: - User is on 5-A-Side/BYB tab
        EXPECTED: - Selections are added to BYB dashboard/ 5-A-Side pitch view
        """
        self.test_003_update_event_in_ti_make_it_pre_match_again__reload_page_and_navigate_to_5_a_sidebyb_tab()

        self.site.sport_event_details.tab_content.team_launcher.build_button.click()
        self.site.sport_event_details.tab_content.pitch_overlay.journey_panel.close_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_pitch_overlay(),
                        msg='Pitch overlay is not shown')
        self.__class__.expected_players_list = []
        self.__class__.pitch_overlay = self.site.sport_event_details.tab_content.pitch_overlay.content.football_field
        markets = self.pitch_overlay.items_as_ordered_dict
        self.assertTrue(markets, msg='Players are not displayed on the Pitch View')
        player_card_odds = ''
        i = 0
        for market in list(markets.values())[1:3]:
            market.icon.click()
            self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_overlay(),
                            msg='Players Overlay is not shown')
            switchers = self.site.sport_event_details.tab_content.players_overlay.switchers.items_as_ordered_dict
            self.assertTrue(switchers, msg='Cannot find Players switchers on the Players Overlay')
            switchers.get('Home').click()
            self.site.wait_content_state_changed(2)
            players = self.site.sport_event_details.tab_content.players_overlay.players_list.items
            self.assertTrue(players, msg='Players are not displayed on the Players List')
            if players[i].is_enabled():
                players[i].click()
            else:
                players[i + 1].click()
            sleep(3)
            self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                            msg='Player Card is not shown')
            i += 1
            self.assertTrue(self.site.sport_event_details.tab_content.wait_for_players_card(),
                            msg='Player Card is not shown')
            player_card = self.site.sport_event_details.tab_content.player_card
            self.site.wait_content_state_changed(4)
            player_card_odds = player_card.add_player_button.output_price
            player_card.add_player_button.click()
            self.assertTrue(market.added_player_name, msg='Failed to display added Player\'s Name')
            self.expected_players_list.append(f'{market.added_player_name} To Make {market.name}')
        self.__class__.football_field_odds = self.pitch_overlay.place_bet_button.output_price
        self.assertEqual(self.football_field_odds, player_card_odds,
                         msg=f'Odds on the Player Card "{player_card_odds} "is not the same as on the '
                             f'Football Field "{self.football_field_odds}"')

    def test_006_trigger_push_update_from_ti_event_should_become_live(self):
        """
        DESCRIPTION: Trigger Push update from TI (Event should become Live)
        EXPECTED: - Live Push update is received on UI
        EXPECTED: - User is redirected to All Markets tab
        EXPECTED: - 5-A-Side/BYB tabs disappeared(not shown on EDP)
        """
        self.test_004_trigger_push_update_from_ti_event_should_become_live()
