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
class Test_C28545_Scorecast_market_section_in_case_suspensions_occurrence(Common):
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

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapltfootballgt_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '&lt;Football&gt;' icon on the Sports Menu Ribbon
        EXPECTED: *   &lt;Football&gt; Landing Page is opened
        EXPECTED: *   'Matches' tab is selected by default
        """
        pass

    def test_003_go_to_football_event_details_page_of_suspended_eventwith_attributeeventstatuscodes(self):
        """
        DESCRIPTION: Go to Football Event Details page of suspended event
        DESCRIPTION: (with attribute **eventStatusCode="S")**
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *   FOR CORAL: 'Main Markets' collection is selected by default
        EXPECTED: *   FOR LADBROKES: 'All Markets' collection is selected by default
        """
        pass

    def test_004_verify_scorecast_market_section_of_event_with_attributeeventstatuscodes(self):
        """
        DESCRIPTION: Verify Scorecast market section of event with attribute **eventStatusCode="S"**
        EXPECTED: * 'Odds calculation' button is greyed out
        EXPECTED: * There is no opportunity to add selection to the Betslip
        """
        pass

    def test_005_go_to_other_football_event_details_page__gt_verify_first_scorer_option_of_scorecast_market_section_in_case_of_suspension(self):
        """
        DESCRIPTION: Go to other Football Event Details Page -&gt; Verify 'First Scorer' option of Scorecast market section in case of suspension
        EXPECTED: *   If **one of (both)** 'First Goalscorer'/'First Goal Scorecast' markets are with attribute **marketStatusCode="S", **option is greyed out
        EXPECTED: *   Market is disabled and it's imposible to make a bet
        EXPECTED: *   The other option ('Last Scorer') is available.
        """
        pass

    def test_006_go_to_other_football_event_details_page__gtverify_last_scorer_option_of_scorecast_market_section_in_case_of_suspension(self):
        """
        DESCRIPTION: Go to other Football Event Details Page -&gt; Verify 'Last Scorer' option of Scorecast market section in case of suspension
        EXPECTED: *   If **one of (both)** Last Goalscorer/Last Goal Scorecast markets are with attribute **marketStatusCode="S", **option is greyed out
        EXPECTED: *   Market is disabled and it's imposible to make a bet
        EXPECTED: *   The other one ('First Scorer') is available.
        """
        pass

    def test_007_go_to_other_football_event_details_page__gt_verify_scorecast_market_section_in_case_of_suspension_of_both_options_first_scorerlast_scorer(self):
        """
        DESCRIPTION: Go to other Football Event Details Page -&gt; Verify Scorecast market section in case of suspension of both options ('First Scorer'/'Last Scorer')
        EXPECTED: *   If **one of (both)** (First Goalscorer and Last Goalscorer) / (First Goal Scorecast/Last Goal Scorecast) markets are with attribute **marketStatusCode="S", **option is greyed out
        EXPECTED: *   Scorecast section is all grey out colored
        EXPECTED: *   Markets and controls within are disabled and it's impossible to make a bet
        """
        pass

    def test_008_go_to_other_football_event_details_page__gt_verify_scorecast_market_section_when_correct_score_market_is_with_attribute_marketstatuscodes(self):
        """
        DESCRIPTION: Go to other Football Event Details Page -&gt; Verify Scorecast market section when Correct Score Market is with attribute  **marketStatusCode="S"**
        EXPECTED: *   Scorecast section is all grey out colored
        EXPECTED: *   Markets and controls within are disabled and it's impossible to make a bet
        """
        pass

    def test_009_go_to_other_football_event_details_page__gtverify_outcome_of_scorecast_market_section_with_attribute_outcomestatuscodes_in_scorercorrect_score_drop_down(self):
        """
        DESCRIPTION: Go to other Football Event Details Page -&gt; Verify outcome of Scorecast market section with attribute **outcomeStatusCode="S" **in Scorer/Correct Score drop-down
        EXPECTED: Outcome is removed from drop-down
        """
        pass

    def test_010_navigate_to_all_markets_collection_coral(self):
        """
        DESCRIPTION: Navigate to 'All Markets' collection (CORAL)
        EXPECTED: 'All Markets' collection is selected
        """
        pass

    def test_011_repeat_steps_3_9_for_all_markets_collection(self):
        """
        DESCRIPTION: Repeat steps 3-9 for 'All Markets' collection
        EXPECTED: 
        """
        pass
