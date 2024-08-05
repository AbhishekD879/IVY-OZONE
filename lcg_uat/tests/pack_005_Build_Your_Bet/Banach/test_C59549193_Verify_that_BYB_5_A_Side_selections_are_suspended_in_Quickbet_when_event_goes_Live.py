import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Event_Details_Page.Five_A_Side.five_a_side import BaseFiveASide


@pytest.mark.lad_tst2  # Ladbrokes Only
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod  # Cannot change event state in prod
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.desktop
@vtest
class Test_C59549193_Verify_that_BYB_5_A_Side_selections_are_suspended_in_Quickbet_when_event_goes_Live(BaseFiveASide):
    """
    TR_ID: C59549193
    NAME: Verify that BYB/5-A-Side selections are suspended in Quickbet when event goes Live
    DESCRIPTION: This TC verifies that:
    DESCRIPTION: - BYB/5-A-Side selections in Quickbet become suspended when event goes live
    DESCRIPTION: - User is redirected to All markets tab when they close Quickbet
    DESCRIPTION: - 5-A-Side/BYB tabs are not shown
    PRECONDITIONS: User is on EDP page, 5-A-Side/BYB tab
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
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market(five_a_side=True)
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id)
        self.__class__.market_id = event_resp[0]['event']['children'][0]['market']['id']

    def test_001_add_some_selections_and_click_place_bet(self):
        """
        DESCRIPTION: Add some selections and click Place Bet
        EXPECTED: Quickbet is shown with the selections
        """
        self.site.login()
        self.navigate_to_edp(event_id=self.event_id, sport_name='football')
        self.site.wait_content_state(state_name='EventDetails')
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.five_a_side)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.five_a_side,
                         msg=f'5-A-Side is not active tab after click, active tab is "{current_tab}"')

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
        self.pitch_overlay.place_bet_button.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='5-A-Side Betslip is not shown')

    def test_002_trigger_push_update_from_ti_event_should_become_live___set_event_start_time__current_time_and_flag_is_off__yes(self):
        """
        DESCRIPTION: Trigger push update from TI (event should become Live - set event start time = current time and flag is off = yes)
        EXPECTED: - started: "Y" is received in push update
        EXPECTED: - Selections in quickbet are suspended
        EXPECTED: - Relevant message is displayed
        EXPECTED: - User cannot place bet
        EXPECTED: ![](index.php?/attachments/get/118215617)
        """
        self.ob_config.make_event_live(market_id=self.market_id, event_id=self.event_id)
        sleep(5)
        self.__class__.byb_betslip_panel = self.site.byb_betslip_panel
        self.assertTrue(self.byb_betslip_panel.is_displayed(), msg='5-A-Side BetSlip is not shown')

        actual_message = self.byb_betslip_panel.info_panels_text[0]
        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.event_suspended
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')

        place_bet_button = self.byb_betslip_panel.place_bet
        self.assertFalse(place_bet_button.is_enabled(expected_result=False), msg='Place bet button is not disabled')

        self.assertFalse(self.byb_betslip_panel.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add to Betslip button is not disabled')

    def test_003_close_quickbet(self):
        """
        DESCRIPTION: Close Quickbet
        EXPECTED: - User is redirected to All markets tab
        EXPECTED: - 5-A-Side/BYB tabs are not shown
        """
        self.byb_betslip_panel.header.close_button.click()
        market_tab_list = self.site.sport_event_details.markets_tabs_list.items_names
        tab_name = self.expected_market_tabs.five_a_side
        self.assertFalse(tab_name in market_tab_list, msg=f'"{tab_name}" is still present in "{market_tab_list}"')
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.expected_market_tabs.all_markets,
                         msg='User is not redirected to "All Markets" tab')
