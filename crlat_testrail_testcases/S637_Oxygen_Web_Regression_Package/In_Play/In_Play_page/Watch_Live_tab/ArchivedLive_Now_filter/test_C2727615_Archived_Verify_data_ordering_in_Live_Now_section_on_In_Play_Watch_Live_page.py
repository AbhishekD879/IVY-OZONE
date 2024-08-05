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
class Test_C2727615_Archived_Verify_data_ordering_in_Live_Now_section_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727615
    NAME: [Archived] Verify data ordering in  'Live Now' section on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies data ordering in  'Live Now' section on 'In-Play Watch Live' page
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbontion
    PRECONDITIONS: In order to get a list with Regions (Classes IDs) and Leagues (Types IDs) use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    """
    keep_browser_open = True

    def test_001_verify_first_level_accordions_title_within_live_now_page(self):
        """
        DESCRIPTION: Verify first level accordion's title within 'Live Now' page
        EXPECTED: First level accordions within 'Live Now' page are titled in the format:
        EXPECTED: <Sport Name>
        """
        pass

    def test_002_verify_second_level_accordions_title_within_each_sport_accordion(self):
        """
        DESCRIPTION: Verify second level accordion's title within each <Sport> accordion
        EXPECTED: The second level accordion's titles are in the following format and correspond to the following attributes:
        EXPECTED: *   'Type Name' if section is named Category Name + Type Name on Pre-Match pages
        EXPECTED: *   'Class Name' - 'Type Name' if section is named Class Name (sport name should not be displayed) + Type Name on Pre-Match pages
        """
        pass

    def test_003_verify_sport_accordions_order(self):
        """
        DESCRIPTION: Verify <Sport> accordions order
        EXPECTED: <Sport> accordions are ordered by Category 'displayOrder' in ascending
        """
        pass

    def test_004_verify_leaguecompetition_accordions_order_in_sport_accordion(self):
        """
        DESCRIPTION: Verify <League/Competition> accordions order in <Sport> accordion
        EXPECTED: <League/Competition> accordions are ordered by:
        EXPECTED: 1.  Class 'displayOrder' in ascending where minus ordinals are displayed first
        EXPECTED: 2.  Type 'displayOrder' in ascending
        """
        pass

    def test_005_verify_events_order_in_the_leaguecompetitionaccordion(self):
        """
        DESCRIPTION: Verify events order in the <League/Competition> accordion
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  'startTime' - chronological order in the first instance
        EXPECTED: 2.  Event 'displayOrder' in ascending
        EXPECTED: 3.  Alphabetical order
        """
        pass
