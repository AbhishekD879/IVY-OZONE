import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import tests
from crlat_siteserve_client.siteserve_client import SiteServeRequests


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod # cannot have access to prod OB
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.scorecast
@vtest
class Test_C18019842_LADBROKES_Verify_Scorecast_Section__Odds_calculation_button(BaseBetSlipTest):
    """
    TR_ID: C18019842
    NAME: [LADBROKES] Verify Scorecast Section  ('Odds calculation' button)
    DESCRIPTION: This test scenario verifies 'Scorecast' odds calculation basing on selected 'First/Last Scorer' and 'Correct Score'.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: The instruction "How to create Scorecast market and calculate odds prices for them" (Ladbrokes section)- https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+create+Scorecast+market+and+calculate+odds+prices+for+them
    PRECONDITIONS: To find the scorecast price on Ladbrokes environment need to use a lookup table - https://jira.egalacoral.com/secure/attachment/1216091/scorecast-lookup-table.json.
    PRECONDITIONS: In order to run this test scenario select event with Scorecast market
    PRECONDITIONS: To get information for an event use the following url (SS response):
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForEvent/EventID?
    """
    keep_browser_open = True

    def add_and_verify_scorecast_price_values(self, home_value, away_value, resp_team_name, selected_player):
        self.scorecast.home_team_results_dropdown.select_value(home_value)
        self.scorecast.away_team_results_dropdown.select_value(away_value)
        self.assertTrue(self.scorecast.add_to_betslip.is_enabled(timeout=2),
                        msg='"Odds calculation" button is not active')

        for outcome in self.market_outcomes1:
            if outcome['outcome']['name'] == resp_team_name:
                correct_score_price = outcome['outcome']['children'][0]['price']
                self.assertTrue(correct_score_price, msg='"Correct score price" is not received from SiteServer response')
        for outcome in self.market_outcomes2:
            if outcome['outcome']['name'] == f'|{selected_player}|':
                scorer_selection_price = outcome['outcome']['children'][0]['price']
                self.assertTrue(scorer_selection_price, msg='"Scorer selection price" is not received from SiteServer response')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with Scorecast market
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
        self.__class__.eventID = event_params.event_id
        market_ids_dict = self.ob_config.market_ids[self.eventID]
        self.__class__.marketIDs = [market_ids_dict[market_name] for market_name in
                                    ['correct_score', 'first_goalscorer'] if market_name in market_ids_dict]

        self.__class__.ss_req_football = SiteServeRequests(env=tests.settings.backend_env,
                                                           brand=self.brand,
                                                           category_id=self.ob_config.backend.ti.football.category_id)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing Page
        EXPECTED: Football Landing Page is opened
        """
        # step 003 is having navigation through direct url , skipping this step
        pass

    def test_003_open_event_detail_page_note_event_id(self):
        """
        DESCRIPTION: Open Event Detail Page, note 'event id'
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *  'All Markets' collection is selected by default
        """
        self.navigate_to_edp(self.eventID, timeout=30)
        default_collection = self.get_default_tab_name_on_sports_edp(event_id=self.eventID)
        self.assertEqual(self.site.sport_event_details.markets_tabs_list.current, default_collection,
                         msg=f'"{default_collection}" tab is not active by default')

    def test_004_get_site_server_response_for_noted_event_id_use_the_link_from_preconditions(self):
        """
        DESCRIPTION: Get SiteServer response for noted 'event id' (use the link from preconditions)
        EXPECTED: All necessary information regarding the event is received in SS response
        """
        self.__class__.event_resp = self.ss_req_football.ss_event_to_outcome_for_event(event_id=self.eventID)
        self.assertTrue(self.event_resp, msg='"EventToOutcomeForEvent" response is not received from site server')
        ss_event_markets = self.event_resp[0]['event']['children']
        for market in ss_event_markets:
            if market['market']['id'] == self.marketIDs[0]:
                self.__class__.market_outcomes1 = market['market']['children']

            if market['market']['id'] == self.marketIDs[1]:
                self.__class__.market_outcomes2 = market['market']['children']

    def test_005_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: *   Scorecast market section is opened
        EXPECTED: *   Section 2 contains 'Odds calculation' button with an appropriate price that depends on selected values in 'Correct Score' dropdowns
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets are shown')
        market = self.expected_market_sections.scorecast
        self.__class__.scorecast = markets.get(market)
        self.assertTrue(self.scorecast, msg=f'{market} section is not found')
        self.scorecast.expand()
        is_market_section_expanded = self.scorecast.is_expanded()
        self.assertTrue(is_market_section_expanded, msg=f'The section "{self.scorecast.name}" is not expanded')

        self.assertTrue(self.scorecast.home_team_results_dropdown.is_displayed(), msg='Home team result drop-down is not present')
        self.assertTrue(self.scorecast.away_team_results_dropdown.is_displayed(), msg='Away team result drop-down is not present')
        self.assertTrue(self.scorecast.add_to_betslip.is_displayed(), msg='"Add to betslip" button is not present')

    def test_006_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1(self):
        """
        DESCRIPTION: Select 'First Scorer'/'Last Scorer' and '<Home Team>'/'<Away Team>' from section 1
        DESCRIPTION: Select 'First Player to Score'/'Last Player to Score' using Player selector (dropdown list)
        DESCRIPTION: Select some values(e.g. 1-0 "Win") in 'Correct Score' drop downs  from section 2 (Select Result)
        EXPECTED: * 'First Scorer'/'Last Scorer' and <Home Team>/<Away Team> options are selected
        EXPECTED: * 'First Player to Score'/'Last Player to Score' value is selected
        EXPECTED: * Selected values are displayed in 'Correct Score' drop downs
        EXPECTED: * 'outcome ids with prices' are received from SiteServer response
        """
        self.assertTrue(self.scorecast.first_scorer_tab, msg='"First scorer" is not visible')
        self.scorecast.first_scorer_tab.click()
        self.assertTrue(self.scorecast.first_scorer_tab.is_selected(), msg=f'"First scorer" tab is not selected')
        self.scorecast.first_goalscorer_team_button.click()
        self.assertTrue(self.scorecast.first_goalscorer_team_button.is_selected(), msg='"First goal scorer" team button is not selected')
        team_name = self.scorecast.first_goal_scorer_team_attribute_text
        self.__class__.selected_player = self.scorecast.player_scorers_list.selected_item
        resp_team_name = f'|{team_name} 1-0|'

        self.add_and_verify_scorecast_price_values(home_value='1', away_value='0', resp_team_name=resp_team_name, selected_player=self.selected_player)

    def test_007_calculate_correct_score_and_scorerplayer_selection_price_values_using_instructionuse_a_lookup_table_to_get_the_scorecast_price(self):
        """
        DESCRIPTION: Calculate 'Correct score' and 'Scorer(player) selection price' values using instruction
        DESCRIPTION: Use a lookup table to get the scorecast price
        EXPECTED: * "Correct Score" and "Scorer(player) selection price" are calculated
        EXPECTED: * "Scorecast price" is found in the lookup table and it is the same as displayed on UI
        """
        self.__class__.expected_scorecast_price = '8/1'
        odds_price = self.scorecast.add_to_betslip.output_price
        self.assertEqual(odds_price, self.expected_scorecast_price, msg=f'Actual "{odds_price}" and expected "{self.expected_scorecast_price}" scorecast price is not equal')

    def test_008_repeat_steps_6_7_for_drawlose_scores(self):
        """
        DESCRIPTION: Repeat steps 6-7 for Draw/Lose scores
        EXPECTED: * Selected values are displayed in 'Correct Score' dropdowns
        EXPECTED: * "Correct Score" and "Scorer(player) selection price" are calculated
        EXPECTED: * "Scorecast price" is found in the lookup table and it is the same as displayed on UI
        """
        resp_team_name = '|Draw 1-1|'
        self.add_and_verify_scorecast_price_values(home_value='1', away_value='1', resp_team_name=resp_team_name,
                                                   selected_player=self.selected_player)
        odds_price = self.scorecast.add_to_betslip.output_price
        self.assertEqual(odds_price, self.expected_scorecast_price,
                         msg=f'Actual "{odds_price}" and expected "{self.expected_scorecast_price}" scorecast price is not equal')

        self.scorecast.last_goalscorer_team_button.click()
        self.assertTrue(self.scorecast.last_goalscorer_team_button.is_selected(),
                        msg='Last scorer team button is not selected')
        team_name = self.scorecast.first_goal_scorer_team_attribute_text
        selected_player = self.scorecast.player_scorers_list.selected_item
        resp_team_name = f'|{team_name} 1-0|'
        self.add_and_verify_scorecast_price_values(home_value='0', away_value='1', resp_team_name=resp_team_name,
                                                   selected_player=selected_player)
        odds_price = self.scorecast.add_to_betslip.output_price
        self.assertEqual(odds_price, self.expected_scorecast_price,
                         msg=f'Actual "{odds_price}" and expected "{self.expected_scorecast_price}" scorecast price is not equal')

    def test_009_verify_section_2_odds_calculation_button_within_scorecast_market_section(self):
        """
        DESCRIPTION: Verify section 2 ('Odds calculation' button) within Scorecast market section
        EXPECTED: *   Value is changed on 'Odds calculation' button when goals are selected in both dropdowns
        EXPECTED: *   'N/A' value is shown on 'Odds calculation' button if the selected combination of outcomes is not valid
        """
        self.scorecast.home_team_results_dropdown.select_value('1')
        self.scorecast.away_team_results_dropdown.select_value('0')
        self.assertFalse(self.scorecast.add_to_betslip.is_enabled(timeout=2, expected_result=False), msg='"Odds calculation" button is active')
        self.assertEqual(self.scorecast.add_to_betslip.name, 'N/A',
                         msg=f'"Add to betslip" button price "{self.scorecast.add_to_betslip.name}" '
                         f'is not the same as expected "N/A" in case of invalid result selection')

    def test_010_click_tap_odds_calculation_button(self):
        """
        DESCRIPTION: Click/Tap 'Odds calculation' button
        EXPECTED: * Combined bet (Scorecast) is successfully added to the betslip
        EXPECTED: * 'Odds calculation' button is selected and has green color
        EXPECTED: * Odds within Betslip is the same as on selected 'Odds calculation' button
        """
        self.scorecast.home_team_results_dropdown.select_value('0')
        self.scorecast.away_team_results_dropdown.select_value('1')
        self.assertTrue(self.scorecast.add_to_betslip.is_enabled(timeout=2),
                        msg='"Odds calculation" button is not active')
        odds_price = self.scorecast.add_to_betslip.output_price
        self.scorecast.add_to_betslip.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(self.scorecast.add_to_betslip.is_selected(), msg='"Odds calculation" button is not selected')
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        section_details = list(singles_section.values())[0]
        self.assertEqual(section_details.odds, odds_price,
                         msg=f'Actual: "{section_details.odds}" odds '
                         f'are not the same as Expected: "{odds_price}"')
