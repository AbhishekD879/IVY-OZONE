import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C18019842_LADBROKES_Verify_Scorecast_Section_Odds_calculation_button(Common):
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

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing Page
        EXPECTED: Football Landing Page is opened
        """
        pass

    def test_003_open_event_detail_page_note_event_id(self):
        """
        DESCRIPTION: Open Event Detail Page, note 'event id'
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *  'All Markets' collection is selected by default
        """
        pass

    def test_004_get_siteserver_response_for_noted_event_id_use_the_link_from_preconditions(self):
        """
        DESCRIPTION: Get SiteServer response for noted 'event id' (use the link from preconditions)
        EXPECTED: All necessary information regarding the event is received in SS response
        """
        pass

    def test_005_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: *   Scorecast market section is opened
        EXPECTED: *   Section 2 contains 'Odds calculation' button with an appropriate price that depends on selected values in 'Correct Score' dropdowns
        """
        pass

    def test_006_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1select_first_player_to_scorelast_player_to_score_using_player_selector_dropdown_listselect_some_valueseg_1_0_win_in_correct_score_drop_downs__from_section_2_select_result(self):
        """
        DESCRIPTION: Select 'First Scorer'/'Last Scorer' and '<Home Team>'/'<Away Team>' from section 1
        DESCRIPTION: Select 'First Player to Score'/'Last Player to Score' using Player selector (dropdown list)
        DESCRIPTION: Select some values(e.g. 1-0 "Win") in 'Correct Score' drop downs  from section 2 (Select Result)
        EXPECTED: * 'First Scorer'/'Last Scorer' and <Home Team>/<Away Team> options are selected
        EXPECTED: * 'First Player to Score'/'Last Player to Score' value is selected
        EXPECTED: * Selected values are displayed in 'Correct Score' dropdowns
        EXPECTED: * 'outcome ids with prices' are received from SiteServer response
        """
        pass

    def test_007_calculate_correct_score_and_scorerplayer_selection_price_values_using_instructionuse_a_lookup_table_to_get_the_scorecast_price(self):
        """
        DESCRIPTION: Calculate 'Correct score' and 'Scorer(player) selection price' values using instruction
        DESCRIPTION: Use a lookup table to get the scorecast price
        EXPECTED: * "Correct Score" and "Scorer(player) selection price" are calculated
        EXPECTED: * "Scorecast price" is found in the lookup table and it is the same as displayed on UI
        """
        pass

    def test_008_repeat_steps_6_7_for_drawlose_scores(self):
        """
        DESCRIPTION: Repeat steps 6-7 for Draw/Lose scores
        EXPECTED: * Selected values are displayed in 'Correct Score' dropdowns
        EXPECTED: * "Correct Score" and "Scorer(player) selection price" are calculated
        EXPECTED: * "Scorecast price" is found in the lookup table and it is the same as displayed on UI
        """
        pass

    def test_009_verify_section_2_odds_calculation_button_within_scorecast_market_section(self):
        """
        DESCRIPTION: Verify section 2 ('Odds calculation' button) within Scorecast market section
        EXPECTED: *   Value is changed on 'Odds calculation' button when goals are selected in both dropdowns
        EXPECTED: *   'N/A' value is shown on 'Odds calculation' button if the selected combination of outcomes is not valid
        """
        pass

    def test_010_clicktap_odds_calculation_button(self):
        """
        DESCRIPTION: Click/Tap 'Odds calculation' button
        EXPECTED: * Combined bet (Scorecast) is successfully added to the betslip
        EXPECTED: * 'Odds calculation' button is selected and has green color
        EXPECTED: * Odds within Betslip is the same as on selected 'Odds calculation' button
        """
        pass
