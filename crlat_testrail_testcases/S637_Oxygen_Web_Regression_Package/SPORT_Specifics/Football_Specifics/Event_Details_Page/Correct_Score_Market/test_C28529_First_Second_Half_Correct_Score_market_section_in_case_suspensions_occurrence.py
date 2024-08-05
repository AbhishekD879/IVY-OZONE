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
class Test_C28529_First_Second_Half_Correct_Score_market_section_in_case_suspensions_occurrence(Common):
    """
    TR_ID: C28529
    NAME: First/Second Half Correct Score market section in case suspensions occurrence
    DESCRIPTION: This test case verifies First Half Correct Score/ Second Half Correct Score /Correct Score markets sections behavior on suspensions occurrence
    DESCRIPTION: **Jira ticket:** BMA-3861
    PRECONDITIONS: To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapltfootballgt_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '&lt;Football&gt;' icon on the Sports Menu Ribbon
        EXPECTED: *   &lt;Football&gt; Landing Page is opened
        EXPECTED: *   'Leagues & Competitions' sorting type is selected by default
        """
        pass

    def test_003_go_to_football_event_details_page_of_suspended_eventwith_attributeeventstatuscodes(self):
        """
        DESCRIPTION: Go to Football Event Details page of suspended event
        DESCRIPTION: (with attribute **eventStatusCode="S")**
        EXPECTED: *   Football Event Details page is opened
        EXPECTED: *   'Main Markets' collection is selected by default
        """
        pass

    def test_004_verify_correct_score_marketof_suspended_event(self):
        """
        DESCRIPTION: Verify Correct Score market of suspended event
        EXPECTED: *   'Add to Betslip N/A' disabled button is shown
        EXPECTED: *   Selections and controls within are disabled and it's impossible to make a bet
        """
        pass

    def test_005_go_to_other_football_event_details_page(self):
        """
        DESCRIPTION: Go to other Football Event Details Page
        EXPECTED: 
        """
        pass

    def test_006_verify_correct_score_section_in_case_of_market_suspension(self):
        """
        DESCRIPTION: Verify Correct Score section in case of market suspension
        EXPECTED: *   If Correct Score market** **are with attribute **marketStatusCode="S",  **Market is disabled and it's imposible to make a bet
        EXPECTED: *   'Add to Betslip N/A' disabled button is shown
        EXPECTED: *   Selections and controls within are disabled and it's impossible to make a bet
        """
        pass

    def test_007_go_to_other_football_event_details_page(self):
        """
        DESCRIPTION: Go to other Football Event Details Page
        EXPECTED: 
        """
        pass

    def test_008_verify_outcome_of_correct_score_market_section_with_attribute_outcomestatuscodes(self):
        """
        DESCRIPTION: Verify outcome of Correct Score market section with attribute **outcomeStatusCode="S" **
        EXPECTED: *   Selection is disabled with prices
        EXPECTED: *   The rest event's selections are enabled with prices
        """
        pass

    def test_009_repeat_steps_3_8_for_first_half_correct_score_market_section(self):
        """
        DESCRIPTION: Repeat steps 3-8 for First Half Correct Score market section
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_3_8_for_second_half_correct_score_section(self):
        """
        DESCRIPTION: Repeat steps 3-8 for Second Half Correct Score section
        EXPECTED: 
        """
        pass
