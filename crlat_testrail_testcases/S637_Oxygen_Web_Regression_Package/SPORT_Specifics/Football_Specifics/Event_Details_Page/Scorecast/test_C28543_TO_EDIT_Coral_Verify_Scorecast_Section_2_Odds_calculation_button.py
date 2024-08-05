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
class Test_C28543_TO_EDIT_Coral_Verify_Scorecast_Section_2_Odds_calculation_button(Common):
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
        EXPECTED: *   'Main Markets' collection is selected by default
        """
        pass

    def test_004_get_siteserver_response_for_noted_event_id_use_first_link_from_preconditions(self):
        """
        DESCRIPTION: Get SiteServer response for noted 'event id' (use first link from preconditions)
        EXPECTED: All necessary information regarding event is received in SS response
        """
        pass

    def test_005_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: *   Scorecast market section is opened
        EXPECTED: *   Section 2 contains 'Odds calculation' button with appropriate price that depends on selected values in 'Correct Score' drop downs
        """
        pass

    def test_006_select_first_scorerlast_scorer_and_home_teamaway_team_from_section_1(self):
        """
        DESCRIPTION: Select 'First Scorer'/'Last Scorer' and '<Home Team>'/'<Away Team>' from section 1
        EXPECTED: * 'First Scorer'/'Last Scorer' and <Home Team>/<Away Team> options are selected
        EXPECTED: * 'market id' of 'First Goal Scorecast'/'Last Goal Scorecast' market is received from SiteServer response
        """
        pass

    def test_007_select_first_player_to_scorelast_player_to_score_using_player_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'First Player to Score'/'Last Player to Score' using Player selector (dropdown list)
        EXPECTED: * 'First Player to Score'/'Last Player to Score' value is selected
        EXPECTED: * 'outcome id' is received from SiteServer response
        """
        pass

    def test_008_select_some_values_in_correct_score_drop_downs__from_section_2_select_result(self):
        """
        DESCRIPTION: Select some values in 'Correct Score' drop downs  from section 2 (Select Result)
        EXPECTED: * Selected values are displayed in 'Correct Score' drop downs
        EXPECTED: * Use the second link from preconditions (Scorecasts Drilldown) with the following values to get Scorecast prices:
        EXPECTED: **market id** **of 'First Goal Scorecast'/****'Last Goal Scorecast' **(step 6)
        EXPECTED: **outcome id** **of 'First Goalscorer'/****'Last Goalscorer' **(step 7)
        """
        pass

    def test_009_from_the_scorecast_response_findcorrect_score_outcome_idstep_7_and_verify_combined_priceodds(self):
        """
        DESCRIPTION: From the scorecast response find 'Correct Score' outcome id** (step 7) and verify combined price/odds
        EXPECTED: Prices in response are displayed in format:
        EXPECTED: **<Correct Score outcome id>** (step 8), <priceNum>,<priceDen>,<priceDec>
        """
        pass

    def test_010_verify_section_2_odds_calculation_button_within_scorecast_market_section(self):
        """
        DESCRIPTION: Verify section 2 ('Odds calculation' button) within Scorecast market section
        EXPECTED: *   Value is changed on 'Odds calculation' button when goals are selected in both dropdowns
        EXPECTED: *   'N/A' value is shown on 'Odds calculation' button if selected combination of outcomes is not valid
        """
        pass

    def test_011_verify_whether_value_on_odds_calculation_button_get_from_response_and_this_value_that_is_shown_in_application_on_odds_calculation_button_in_section_2_is_same(self):
        """
        DESCRIPTION: Verify whether value on 'Odds calculation' button get from response and this value that is shown in application on 'Odds calculation' button in section 2 is same
        EXPECTED: * Value on 'Odds calculation' button in application corresponds to **'<priceNum>/<priceDen>' **attributes in fractional format
        EXPECTED: * Value on 'Odds calculation' button in application corresponds to **'<priceDec>' **attribute in decimal format
        """
        pass

    def test_012_clicktap_odds_calculation_button(self):
        """
        DESCRIPTION: Click/Tap 'Odds calculation' button
        EXPECTED: * Combined bet (Scorecast) is successfully added to the betslip
        EXPECTED: * 'Odds calculation' button is selected and has green color
        EXPECTED: * Odds within Betslip is the same as on selected 'Odds calculation' button
        """
        pass
