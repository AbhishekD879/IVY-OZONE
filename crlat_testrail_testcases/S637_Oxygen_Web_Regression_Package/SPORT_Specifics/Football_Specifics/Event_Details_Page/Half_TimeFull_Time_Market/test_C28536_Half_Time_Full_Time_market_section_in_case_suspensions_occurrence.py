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
class Test_C28536_Half_Time_Full_Time_market_section_in_case_suspensions_occurrence(Common):
    """
    TR_ID: C28536
    NAME: Half Time/Full Time market section in case suspensions occurrence
    DESCRIPTION: This test case verifies Half Time/Full Time market section behavior on suspensions occurrence
    DESCRIPTION: **Jira ticket:** BMA-3863
    DESCRIPTION: [TO EDIT] Looks like the following is not up to date relating to this market
    DESCRIPTION: - market sections
    DESCRIPTION: - 'Show All' section
    PRECONDITIONS: To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
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

    def test_004_verify_half_timefull_time_marketof_suspended_event(self):
        """
        DESCRIPTION: Verify Half Time/Full Time market of suspended event
        EXPECTED: *   [TO EDIT] Half Time/Full Time market sections are all greyed out
        EXPECTED: *   [TO EDIT] Disabled odds/price buttons are displayed on outcomes on 'Show All' section
        EXPECTED: *   Selections and controls within are disabled and it's impossible to make a bet
        """
        pass

    def test_005_go_to_other_football_event_details_page(self):
        """
        DESCRIPTION: Go to other Football Event Details Page
        EXPECTED: 
        """
        pass

    def test_006_verify_half_timefull_time_market_section_in_case_of_suspension(self):
        """
        DESCRIPTION: Verify 'Half Time/Full Time market section in case of suspension
        EXPECTED: *   If** **'Half Time/Full Time market** **are with attribute **marketStatusCode="S",  **Market is disabled and it's imposible to make a bet
        EXPECTED: *   [TO EDIT] Half Time/Full Time market sections are all greyed out
        EXPECTED: *   [TO EDIT] Disabled odds/price buttons are displayed on 'Show All' section
        """
        pass

    def test_007_go_to_other_football_event_details_page(self):
        """
        DESCRIPTION: Go to other Football Event Details Page
        EXPECTED: 
        """
        pass

    def test_008_verify_outcome_of_half_timefull_time_market_section_with_attribute_outcomestatuscodes(self):
        """
        DESCRIPTION: Verify outcome of Half Time/Full Time market section with attribute **outcomeStatusCode="S" **
        EXPECTED: *   Selection odds/price button is disabled
        EXPECTED: *   It's impossible to place a bet for this selection
        EXPECTED: *   The rest event's selections are enabled with prices
        """
        pass
