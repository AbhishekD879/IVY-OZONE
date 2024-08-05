import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C2727614_Archived_Verify_number_of_available_markets_Markets_link_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727614
    NAME: [Archived] Verify  '+<number of available markets> Markets'  link on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies '+<number of available markets> Markets' link on 'In-Play Watch Live' page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy).
    PRECONDITIONS: 2. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: 3. Go to Event section when 'Live Now' switcher is selected
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: '+<number of available markets> Markets'  link is NOT shown for Outrights/Race events
    """
    keep_browser_open = True

    def test_001_verify_plusnumber_of_available_markets_markets__link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '+<number of available markets> Markets'  link for event with several markets
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: '<number of available markets> MORE' is shown below odds buttons
        EXPECTED: **For Desktop:**
        EXPECTED: '+<number of available markets> Markets' is shown next to odds buttons
        """
        pass

    def test_002_verify_number_of_extra_markets(self):
        """
        DESCRIPTION: Verify number of extra markets
        EXPECTED: *   For 'Upcoming' events number of markets correspond to:
        EXPECTED: 'Number of all markets - 1'
        EXPECTED: *   For 'Live Now' events number of markets correspond to:
        EXPECTED: 'Number of markets with 'isMarketBetInRun="true" attribute - 1'
        """
        pass

    def test_003_clicktap_plusnumber_of_available_markets_markets_link(self):
        """
        DESCRIPTION: Click/Tap '+<number of available markets> Markets' link
        EXPECTED: '+<number of available markets> Markets' link leads to the Event Details page
        """
        pass

    def test_004_verify_plusnumber_of_available_markets_markets_link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Verify '+<number of available markets> Markets' link for event with ONLY one market
        EXPECTED: '+<number of available markets> Markets' link is not shown on the Event section
        """
        pass

    def test_005_go_to_event_section_whenupcomingfilter_is_selected(self):
        """
        DESCRIPTION: Go to Event section when 'Upcoming' filter is selected
        EXPECTED: The list of pre-match events is displayed on the page
        """
        pass

    def test_006_repeat_steps_1_5(self):
        """
        DESCRIPTION: Repeat steps #1-5
        EXPECTED: 
        """
        pass
