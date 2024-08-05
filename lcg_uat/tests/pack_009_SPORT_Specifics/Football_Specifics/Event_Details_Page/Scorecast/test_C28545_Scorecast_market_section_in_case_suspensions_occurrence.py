import pytest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Event need to suspend
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28545_Scorecast_market_section_in_case_suspensions_occurrence(BaseSportTest):
    """
    TR_ID: C28545
    NAME: Scorecast market section in case suspensions occurrence
    DESCRIPTION: This test case verifies Scorecast market section behavior on suspensions occurrence
    PRECONDITIONS: To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Note:
    PRECONDITIONS: *   In case of disabling 'First Scorer' option '**First Goalscorer' and 'First Goal Scorecast' **markets should be checked on SS
    PRECONDITIONS: *   In case of disabling 'Last Scorer' option '**Last Goalscorer' and 'Last Goal Scorecast' **markets should be checked on SS
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First Goalscorer"
    PRECONDITIONS: *   PROD: name="First Goal Scorer"
    """
    keep_browser_open = True

    def get_market_data(self, event_id):

        self.navigate_to_edp(event_id, timeout=30)
        self.site.wait_content_state_changed(timeout=15)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets are shown')
        market = self.expected_market_sections.scorecast
        self.__class__.scorecast = markets.get(market)
        self.assertTrue(self.scorecast, msg=f'{market} section is not found')

    def verify_market_suspension(self):

        try:
            self.scorecast.last_goalscorer_team_button.click()
        except Exception:
            pass
        self.assertFalse(self.scorecast.last_goalscorer_team_button.is_selected(),
                         msg='Last scorer team button is  selected')
        odds_price = self.scorecast.add_to_betslip
        self.assertFalse(odds_price.is_enabled(expected_result=False, timeout=5, poll_interval=1),
                         msg='Bet button is not disabled, but was expected to be disabled')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with Scorecast market
        EXPECTED: Event is created
        """
        event_1 = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
        self.__class__.eventID_1 = event_1.event_id
        market_ids_dict = self.ob_config.market_ids[self.eventID_1]
        self.__class__.first_goalscorer_market = market_ids_dict['first_goalscorer']
        self.__class__.last_goalscorer_market = market_ids_dict['last_goalscorer']
        self.__class__.correct_score_market = market_ids_dict['correct_score']
        self.__class__.selection_id = event_1.selection_ids['first_goalscorer']['Player 2']

        if self.site.brand == 'bma':

            event_2 = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
            self.__class__.eventID_2 = event_2.event_id
            market_ids_dict = self.ob_config.market_ids[self.eventID_2]
            self.__class__.first_goalscorer_market_2 = market_ids_dict['first_goalscorer']
            self.__class__.last_goalscorer_market_2 = market_ids_dict['last_goalscorer']
            self.__class__.correct_score_market_2 = market_ids_dict['correct_score']
            self.__class__.selection_id_2 = event_2.selection_ids['first_goalscorer']['Player 2']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Football>' icon on the Sports Menu Ribbon
        EXPECTED: *   <Football> Landing Page is opened
        EXPECTED: *   'Matches' tab is selected by default
        """
        # step 003 is having navigation through direct url , skipping this step
        pass

    def test_003_go_to_football_event_details_page_of_suspended_eventwith_attributeeventstatuscodes(self):
        """
        DESCRIPTION: Go to Football Event Details page of suspended event
        DESCRIPTION: (with attribute **eventStatusCode="S")**
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *   FOR CORAL: 'Main Markets' collection is selected by default
        EXPECTED: *   FOR LADBROKES: 'All Markets' collection is selected by default
        """
        self.ob_config.change_event_state(event_id=self.eventID_1, displayed=True, active=False)
        self.navigate_to_edp(self.eventID_1, timeout=30)
        default_collection = self.get_default_tab_name_on_sports_edp(event_id=self.eventID_1)
        self.assertEqual(self.site.sport_event_details.markets_tabs_list.current, default_collection,
                         msg=f'"{default_collection}" tab is not active by default')

    def test_004_verify_scorecast_market_section_of_event_with_attributeeventstatuscodes(self, event_id=None):
        """
        DESCRIPTION: Verify Scorecast market section of event with attribute **eventStatusCode="S"**
        EXPECTED: * 'Odds calculation' button is greyed out
        EXPECTED: * There is no opportunity to add selection to the Betslip
        """
        event_id = self.eventID_1 if event_id == None else event_id
        self.get_market_data(event_id)
        self.verify_market_suspension()
        self.ob_config.change_event_state(event_id=event_id, displayed=True, active=True)

    def test_005_go_to_other_football_event_details_page___verify_first_scorer_option_of_scorecast_market_section_in_case_of_suspension(
            self, event_id=None, first_goalscorer_market=None):
        """
        DESCRIPTION: Go to other Football Event Details Page -> Verify 'First Scorer' option of Scorecast market section in case of suspension
        EXPECTED: *   If **one of (both)** 'First Goalscorer'/'First Goal Scorecast' markets are with attribute **marketStatusCode="S", **option is greyed out
        EXPECTED: *   Market is disabled and it's imposible to make a bet
        EXPECTED: *   The other option ('Last Scorer') is available.
        """
        event_id = self.eventID_1 if event_id == None else event_id
        first_goalscorer_market=self.first_goalscorer_market  if first_goalscorer_market==None else first_goalscorer_market

        self.ob_config.change_market_state(event_id, first_goalscorer_market, displayed=True)
        self.get_market_data(event_id)
        self.verify_market_suspension()
        self.scorecast.last_scorer_tab.click()
        self.assertTrue(self.scorecast.last_scorer_tab.is_selected(), msg='Last scorer tab is not selected')
        self.scorecast.home_team_results_dropdown.select_value('2')
        odds_price = self.scorecast.add_to_betslip
        self.assertTrue(odds_price.is_enabled(expected_result=True, timeout=5, poll_interval=1),
                        msg='Bet button is disabled, but was expected to be enabled')
        self.ob_config.change_market_state(event_id, first_goalscorer_market, displayed=True, active=True)

    def test_006_go_to_other_football_event_details_page__verify_last_scorer_option_of_scorecast_market_section_in_case_of_suspension(
            self, event_id=None, first_goalscorer_market=None, last_goalscorer_market=None):
        """
        DESCRIPTION: Go to other Football Event Details Page -> Verify 'Last Scorer' option of Scorecast market section in case of suspension
        EXPECTED: *   If **one of (both)** Last Goalscorer/Last Goal Scorecast markets are with attribute **marketStatusCode="S", **option is greyed out
        EXPECTED: *   Market is disabled and it's imposible to make a bet
        EXPECTED: *   The other one ('First Scorer') is available.
        """
        event_id = self.eventID_1 if event_id == None else event_id
        first_goalscorer_market = self.first_goalscorer_market if first_goalscorer_market == None else first_goalscorer_market
        last_goalscorer_market = self.last_goalscorer_market if last_goalscorer_market == None else last_goalscorer_market
        self.ob_config.change_market_state(event_id, last_goalscorer_market, displayed=True)
        self.get_market_data(event_id)
        self.scorecast.last_scorer_tab.click()
        self.assertTrue(self.scorecast.last_scorer_tab.is_selected(), msg='Last scorer tab is not selected')
        self.verify_market_suspension()
        self.scorecast.first_scorer_tab.click()
        self.assertTrue(self.scorecast.first_scorer_tab.is_selected(), msg='Last scorer tab is not selected')
        self.scorecast.home_team_results_dropdown.select_value('2')
        odds_price = self.scorecast.add_to_betslip
        self.assertTrue(odds_price.is_enabled(expected_result=True, timeout=5, poll_interval=1),
                        msg='Bet button is disabled, but was expected to be enabled')
        self.ob_config.change_market_state(event_id, first_goalscorer_market, displayed=True, active=True)

    def test_007_go_to_other_football_event_details_page___verify_scorecast_market_section_in_case_of_suspension_of_both_options_first_scorerlast_scorer(
            self, event_id=None, first_goalscorer_market=None, last_goalscorer_market=None, selection_id=None):
        """
        DESCRIPTION: Go to other Football Event Details Page -> Verify Scorecast market section in case of suspension of both options ('First Scorer'/'Last Scorer')
        EXPECTED: *   If **one of (both)** (First Goalscorer and Last Goalscorer) / (First Goal Scorecast/Last Goal Scorecast) markets are with attribute **marketStatusCode="S", **option is greyed out
        EXPECTED: *   Scorecast section is all grey out colored
        EXPECTED: *   Markets and controls within are disabled and it's impossible to make a bet
        """
        event_id = self.eventID_1 if event_id == None else event_id
        first_goalscorer_market = self.first_goalscorer_market if first_goalscorer_market == None else first_goalscorer_market
        last_goalscorer_market = self.last_goalscorer_market if last_goalscorer_market == None else last_goalscorer_market
        selection_id = self.selection_id if selection_id == None else selection_id
        self.ob_config.change_market_state(event_id, first_goalscorer_market, displayed=True)
        self.get_market_data(event_id)
        self.verify_market_suspension()
        self.scorecast.home_team_results_dropdown.select_value('2')
        odds_price = self.scorecast.add_to_betslip
        self.assertFalse(odds_price.is_enabled(expected_result=True, timeout=5, poll_interval=1),
                         msg='Bet button is enabled, but was expected to be disabled')
        self.ob_config.change_market_state(event_id, first_goalscorer_market, displayed=True, active=True)
        self.ob_config.change_market_state(event_id, last_goalscorer_market, displayed=True, active=True)

        # Selection suspension
        self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=False)
        self.get_market_data(event_id)
        self.scorecast.last_goalscorer_team_button.click()
        self.scorecast.first_goalscorer_team_button.click()
        players = self.scorecast.player_scorers_list.available_options
        self.assertNotIn('Player 2', players,
                         msg=f'Player list in UI "{players}" and expected Players2 is present which should not present')

    def test_008_go_to_other_football_event_details_page___verify_scorecast_market_section_when_correct_score_market_is_with_attribute_marketstatuscodes(
            self, event_id=None,correct_score_market=None):
        """
        DESCRIPTION: Go to other Football Event Details Page -> Verify Scorecast market section when Correct Score Market is with attribute  **marketStatusCode="S"**
        EXPECTED: *   Scorecast section is all grey out colored
        EXPECTED: *   Markets and controls within are disabled and it's impossible to make a bet
        """
        event_id = self.eventID_1 if event_id == None else event_id
        correct_score_market = self.correct_score_market if correct_score_market == None else correct_score_market
        self.ob_config.change_market_state(event_id, correct_score_market, displayed=True)
        self.get_market_data(event_id)
        self.scorecast.home_team_results_dropdown.select_value('2')
        odds_price = self.scorecast.add_to_betslip
        self.assertFalse(odds_price.is_enabled(expected_result=False, timeout=5, poll_interval=1),
                         msg='Bet button is enabled, but was expected to be disabled')

    def test_009_go_to_other_football_event_details_page__verify_outcome_of_scorecast_market_section_with_attribute_outcomestatuscodes_in_scorercorrect_score_drop_down(
            self):
        """
        DESCRIPTION: Go to other Football Event Details Page -> Verify outcome of Scorecast market section with attribute **outcomeStatusCode="S" **in Scorer/Correct Score drop-down
        EXPECTED: Outcome is removed from drop-down
        """
        # Covered in step-7

    def test_010_navigate_to_all_markets_collection_coral(self):
        """
        DESCRIPTION: Navigate to 'All Markets' collection (CORAL)
        EXPECTED: 'All Markets' collection is selected
        """
        if self.site.brand == 'bma':
            self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.expected_market_tabs.all_markets)
            current_tab = self.site.sport_event_details.markets_tabs_list.current
            self.assertEqual(current_tab, self.expected_market_tabs.all_markets,
                             msg='All Markets is not active tab after click, active tab is %s' % current_tab)
            self.ob_config.change_event_state(event_id=self.eventID_2, displayed=True, active=False)
            self.navigate_to_edp(self.eventID_2, timeout=30)
            self.test_004_verify_scorecast_market_section_of_event_with_attributeeventstatuscodes(event_id=self.eventID_2)
            self.test_005_go_to_other_football_event_details_page___verify_first_scorer_option_of_scorecast_market_section_in_case_of_suspension(
                event_id=self.eventID_2, first_goalscorer_market=self.first_goalscorer_market_2)
            self.test_006_go_to_other_football_event_details_page__verify_last_scorer_option_of_scorecast_market_section_in_case_of_suspension(
                event_id=self.eventID_2, first_goalscorer_market=self.first_goalscorer_market_2, last_goalscorer_market=self.last_goalscorer_market_2)
            self.test_007_go_to_other_football_event_details_page___verify_scorecast_market_section_in_case_of_suspension_of_both_options_first_scorerlast_scorer(
                event_id=self.eventID_2, first_goalscorer_market=self.first_goalscorer_market_2, last_goalscorer_market=self.last_goalscorer_market_2, selection_id=self.selection_id_2)
            self.test_008_go_to_other_football_event_details_page___verify_scorecast_market_section_when_correct_score_market_is_with_attribute_marketstatuscodes(
                event_id=self.eventID_2, correct_score_market=self.correct_score_market_2)

    def test_011_repeat_steps_3_9_for_all_markets_collection(self):
        """
        DESCRIPTION: Repeat steps 3-9 for 'All Markets' collection
        EXPECTED:
        """
        # Covered in step-10
        pass
