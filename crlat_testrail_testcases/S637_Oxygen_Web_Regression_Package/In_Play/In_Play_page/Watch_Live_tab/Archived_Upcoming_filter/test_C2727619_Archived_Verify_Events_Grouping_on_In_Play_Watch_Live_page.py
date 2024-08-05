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
class Test_C2727619_Archived_Verify_Events_Grouping_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727619
    NAME: [Archived] Verify Events Grouping on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies events grouping on 'In-Play Watch Live' page.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: 3. Choose 'Upcoming' switcher
    PRECONDITIONS: In order to get a list with Classes IDs and Types IDs for particular Category use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports Category ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: For each Type retrieve a list of Event IDs:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXX?translationLang=LL
    PRECONDITIONS: *   XXX -  is a comma separated list of **Type **ID's;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    """
    keep_browser_open = True

    def test_001_verify_upcoming_view(self):
        """
        DESCRIPTION: Verify 'Upcoming' view
        EXPECTED: *   Sections with Sports' names are visible
        EXPECTED: *   Events are grouped by 'categoryId'
        EXPECTED: *  All sections are collapsed by default for **Mobile**
        EXPECTED: *  The first section is expanded for **Desktop**
        EXPECTED: *   It is possible to collapse/expand all of the accordions by clicking the accordion's header
        """
        pass

    def test_002_verify_sport_section(self):
        """
        DESCRIPTION: Verify '<Sport>' section
        EXPECTED: *   Section consists of the list of Leagues/Competitions
        EXPECTED: *   Events are grouped by 'typeId' within '<Sport>' section
        EXPECTED: *   Accordions expanded by default correspond to 'competitionsCount' value within System_configuration section in CMS
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the accordion's header
        """
        pass
