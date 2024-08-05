import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from crlat_siteserve_client.siteserve_client import SiteServeRequests


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.prod #cannot create events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28543_TO_EDIT_Coral_Verify_Scorecast_Section_2_Odds_calculation_button(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C28543
    NAME: TO EDIT [Coral] Verify Scorecast Section 2 ('Odds calculation' button)
    DESCRIPTION: This test scenario verifies cumulative 'Scorecast' odds calculation basing on selected 'First/Last Scorer' and 'Correct Score'.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    DESCRIPTION: TO EDIT http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Scorecasts/<marketId>/<scorerOutcomeId> call with valid ids returns an error
    PRECONDITIONS: In order to run this test scenario select event with market name "First Goal Scorecast"/"Last Goal Scorecast"
    PRECONDITIONS: To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: To get Scorecast prices use Scorecasts Drilldown with the following values :
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Scorecasts/<marketId>/<scorerOutcomeId>
    PRECONDITIONS: *   market id of 'First Goal Scorecast'/'Last Goal Scorecast'
    PRECONDITIONS: *   outcome id of 'First Goalscorer'/'Last Goalscorer
    PRECONDITIONS: *   outcome id of 'Correct Score'
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First Goalscorer"
    PRECONDITIONS: *   PROD: name="First Goal Scorer"
    """
    keep_browser_open = True

    def add_and_verify_scorecast_price_values(self, home_value, away_value, resp_team_name, selected_player):
        self.scorecast.home_team_results_dropdown.select_value(home_value)
        self.scorecast.away_team_results_dropdown.select_value(away_value)
        self.assertTrue(self.scorecast.add_to_betslip.is_enabled(timeout=2),
                        msg='"Odds calculation" button is not active')

        for outcome in self.market_outcomes1:
            if outcome['outcome']['name'] == resp_team_name:
                self.__class__.correct_score_price = outcome['outcome']['children'][0]['price']
                self.assertTrue(self.correct_score_price, msg='"Correct score price" is not received from SiteServer response')
        for outcome in self.market_outcomes2:
            if outcome['outcome']['name'] == f'|{selected_player}|':
                self.__class__.scorer_selection_price = outcome['outcome']['children'][0]['price']
                self.assertTrue(self.scorer_selection_price, msg='"Scorer selection price" is not received from SiteServer response')

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
        # covered in step 003

    def test_003_open_event_detail_page_note_event_id(self):
        """
        DESCRIPTION: Open Event Detail Page, note 'event id'
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *   'Main Markets' collection is selected by default
        """
        self.navigate_to_edp(self.eventID, timeout=30)
        default_collection = self.get_default_tab_name_on_sports_edp(event_id=self.eventID)
        self.assertEqual(self.site.sport_event_details.markets_tabs_list.current, default_collection,
                         msg=f'"{default_collection}" tab is not active by default')

    def test_004_get_siteserver_response_for_noted_event_id_use_first_link_from_preconditions(self):
        """
        DESCRIPTION: Get SiteServer response for noted 'event id' (use first link from preconditions)
        EXPECTED: All necessary information regarding event is received in SS response
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
        EXPECTED: *   Section 2 contains 'Odds calculation' button with appropriate price that depends on selected values in 'Correct Score' drop downs
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets are shown')
        market = self.expected_market_sections.scorecast
        correct_score = self.expected_market_sections.correct_score
        self.__class__.scorecast = markets.get(market)
        self.assertTrue(self.scorecast, msg=f'{market} section is not found')
        self.__class__.correct_score = markets.get(correct_score)
        self.assertTrue(self.correct_score, msg=f'{correct_score} section is not found')
        self.scorecast.expand()
        is_market_section_expanded = self.scorecast.is_expanded()
        self.assertTrue(is_market_section_expanded, msg=f'The section "{self.scorecast.name}" is not expanded')

        self.assertTrue(self.scorecast.home_team_results_dropdown.is_displayed(),
                        msg='Home team result drop-down is not present')
        self.assertTrue(self.scorecast.away_team_results_dropdown.is_displayed(),
                        msg='Away team result drop-down is not present')
        self.assertTrue(self.scorecast.add_to_betslip.is_displayed(), msg='"Add to betslip" button is not present')

    def test_006_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1(self):
        """
        DESCRIPTION: Select 'First Scorer'/'Last Scorer' and '<Home Team>'/'<Away Team>' from section 1
        EXPECTED: * 'First Scorer'/'Last Scorer' and <Home Team>/<Away Team> options are selected
        EXPECTED: * 'market id' of 'First Goal Scorecast'/'Last Goal Scorecast' market is received from SiteServer response
        """
        self.assertTrue(self.scorecast.first_scorer_tab, msg='"First scorer" is not visible')
        self.scorecast.first_scorer_tab.click()
        self.assertTrue(self.scorecast.first_scorer_tab.is_selected(), msg=f'"First scorer" tab is not selected')
        self.scorecast.first_goalscorer_team_button.click()
        self.assertTrue(self.scorecast.first_goalscorer_team_button.is_selected(),
                        msg='"First goal scorer" team button is not selected')
        team_name = self.scorecast.first_goal_scorer_team_attribute_text
        self.__class__.selected_player = self.scorecast.player_scorers_list.selected_item
        resp_team_name = f'|{team_name} 1-0|'

        self.add_and_verify_scorecast_price_values(home_value='1', away_value='0', resp_team_name=resp_team_name,
                                                   selected_player=self.selected_player)

    def test_007_select_first_player_to_scorelast_player_to_score_using_player_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'First Player to Score'/'Last Player to Score' using Player selector (dropdown list)
        EXPECTED: * 'First Player to Score'/'Last Player to Score' value is selected
        EXPECTED: * 'outcome id' is received from SiteServer response
        """
        # covered in step 006

    def test_008_select_some_values_in_correct_score_drop_downs__from_section_2_select_result(self):
        """
        DESCRIPTION: Select some values in 'Correct Score' drop downs  from section 2 (Select Result)
        EXPECTED: * Selected values are displayed in 'Correct Score' drop downs
        EXPECTED: * Use the second link from preconditions (Scorecasts Drilldown) with the following values to get Scorecast prices:
        EXPECTED: **market id** **of 'First Goal Scorecast'/****'Last Goal Scorecast' **(step 6)
        EXPECTED: **outcome id** **of 'First Goalscorer'/****'Last Goalscorer' **(step 7)
        """
        # covered in step 006

    def test_009_from_the_scorecast_response_findcorrect_score_outcome_idstep_7_and_verify_combined_priceodds(self):
        """
        DESCRIPTION: From the scorecast response find 'Correct Score' outcome id** (step 7) and verify combined price/odds
        EXPECTED: Prices in response are displayed in format:
        EXPECTED: **<Correct Score outcome id>** (step 8), <priceNum>,<priceDen>,<priceDec>
        """
        price_list = ['priceNum', 'priceDen', 'priceDec']
        self.correct_score.team_home_scores.select_score_by_text('1')
        sleep(3)
        price_keys = list(self.correct_score_price.keys())
        for odd_name in price_list:
            self.assertIn(odd_name, price_keys,
                          msg=f'odd name "{odd_name}" is not in "{price_keys}"')
        odds_price = self.correct_score.combined_outcome_button.name
        expected_price = self.correct_score_price['priceNum'] + '/' + self.correct_score_price['priceDen']
        self.assertEqual(odds_price, expected_price,
                         msg=f'Actual price "{odds_price}" is not same as expected'
                             f'Expected price "{expected_price}"')

    def test_010_verify_section_2_odds_calculation_button_within_scorecast_market_section(self):
        """
        DESCRIPTION: Verify section 2 ('Odds calculation' button) within Scorecast market section
        EXPECTED: *   Value is changed on 'Odds calculation' button when goals are selected in both dropdowns
        EXPECTED: *   'N/A' value is shown on 'Odds calculation' button if selected combination of outcomes is not valid
        """
        self.scorecast.home_team_results_dropdown.select_value('3')
        self.scorecast.away_team_results_dropdown.select_value('3')
        self.assertFalse(self.scorecast.add_to_betslip.is_enabled(timeout=2, expected_result=False),
                         msg='"Odds calculation" button is active')
        self.assertEqual(self.scorecast.add_to_betslip.name, 'N/A',
                         msg=f'"Add to betslip" button price "{self.scorecast.add_to_betslip.name}" '
                             f'is not the same as expected "N/A" in case of invalid result selection')

    def test_011_verify_whether_value_on_odds_calculation_button_get_from_response_and_this_value_that_is_shown_in_application_on_odds_calculation_button_in_section_2_is_same(self):
        """
        DESCRIPTION: Verify whether value on 'Odds calculation' button get from response and this value that is shown in application on 'Odds calculation' button in section 2 is same
        EXPECTED: * Value on 'Odds calculation' button in application corresponds to **'<priceNum>/<priceDen>' **attributes in fractional format
        EXPECTED: * Value on 'Odds calculation' button in application corresponds to **'<priceDec>' **attribute in decimal format
        """
        odds_price = self.scorecast.add_to_betslip.output_price
        self.assertTrue(odds_price, msg='odd price not displayed')
        self.check_odds_format(odds=odds_price, expected_odds_format="fraction")

    def test_012_clicktap_odds_calculation_button(self):
        """
        DESCRIPTION: Click/Tap 'Odds calculation' button
        EXPECTED: * Combined bet (Scorecast) is successfully added to the betslip
        EXPECTED: * 'Odds calculation' button is selected and has green color
        EXPECTED: * Odds within Betslip is the same as on selected 'Odds calculation' button
        """
        self.scorecast.home_team_results_dropdown.select_value('1')
        self.scorecast.away_team_results_dropdown.select_value('2')
        self.assertTrue(self.scorecast.add_to_betslip.is_enabled(timeout=2),
                        msg='"Odds calculation" button is not active')
        odds_price = self.scorecast.add_to_betslip.output_price
        self.scorecast.add_to_betslip.click()
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel(timeout=60)
            self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(self.scorecast.add_to_betslip.is_selected(), msg='"Odds calculation" button is not selected')
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        section_details = list(singles_section.values())[0]
        self.assertEqual(section_details.odds, odds_price,
                         msg=f'Actual: "{section_details.odds}" odds '
                             f'are not the same as Expected: "{odds_price}"')
