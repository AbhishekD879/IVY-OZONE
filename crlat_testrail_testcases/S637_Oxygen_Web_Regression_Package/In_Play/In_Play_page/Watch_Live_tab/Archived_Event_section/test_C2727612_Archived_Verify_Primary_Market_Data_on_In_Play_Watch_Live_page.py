import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C2727612_Archived_Verify_Primary_Market_Data_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727612
    NAME: [Archived] Verify Primary Market Data on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies Primary Market Data on 'In-Play Watch Live' page.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load Oxygen application
    PRECONDITIONS: 3. Load application and navigate to In-Play - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: 4. Navigate to <Sport> event section when 'Live Now' switcher is selected
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_verify_sport_event_with_available_selections(self):
        """
        DESCRIPTION: Verify <Sport> event with available selections
        EXPECTED: Only selections that belong to the Market with the following attributes are shown on In-Play Landing page:
        EXPECTED: *   Market's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Attribute 'isMarketBetInRun="true"' is present
        EXPECTED: *   All selections in such market have 'outcomeMeaningMajorCode="MR"/"HH"'
        EXPECTED: *   All selections in such market have attribute 'siteChannels' contains 'M'
        EXPECTED: If event has several markets that contain the above attributes - selections from the market **with the lowest 'displayOrder'** are shown on In-Play Landing page
        """
        pass

    def test_002_navigate_to_event_section_whenupcomingswitcher_is_selected(self):
        """
        DESCRIPTION: Navigate to event section when 'Upcoming' switcher is selected
        EXPECTED: The list of pre-match events is displayed on the page
        """
        pass

    def test_003_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step #1
        EXPECTED: 
        """
        pass
