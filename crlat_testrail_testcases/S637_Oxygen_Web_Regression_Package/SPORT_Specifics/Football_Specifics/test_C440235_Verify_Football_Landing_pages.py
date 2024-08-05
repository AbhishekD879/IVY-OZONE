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
class Test_C440235_Verify_Football_Landing_pages(Common):
    """
    TR_ID: C440235
    NAME: Verify Football Landing pages
    DESCRIPTION: This test case verifies Football Landing pages
    PRECONDITIONS: Preconditions
    PRECONDITIONS: 1) In order to get a list with Regions (Classes IDs) and Leagues (Types IDs) use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: XX - sports Category ID (Football=16)
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID (Football=16)
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: * 'Matches'  page is opened by default
        EXPECTED: * First three sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: * The section header titles are in the following format and correponds to the attributes:
        EXPECTED: * className (sport name is not displayed) + "" - "" + typeName
        """
        pass

    def test_004_verify_leagues_sections_order(self):
        """
        DESCRIPTION: Verify Leagues sections order
        EXPECTED: Leagues sections are ordered by:
        EXPECTED: * Class displayOrder in ascending order where minus ordinals are displayed first
        EXPECTED: * Type displayOrder in ascending order
        """
        pass

    def test_005_verify_events_order_in_the_league_section(self):
        """
        DESCRIPTION: Verify events order in the League section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: * (rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) (for 'Today' tab only for Desktop)
        EXPECTED: * startTime - chronological order in the first instance
        EXPECTED: * Event displayOrder  in ascending
        EXPECTED: * Alphabetical order
        """
        pass

    def test_006_go_to_outrights_events_page(self):
        """
        DESCRIPTION: Go to 'Outrights' Events page
        EXPECTED: * 'Outrights' Events page is opened
        EXPECTED: * All sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by tapping the section's header
        """
        pass

    def test_007_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps №3-5
        EXPECTED: The same as on the steps №3-5
        """
        pass
