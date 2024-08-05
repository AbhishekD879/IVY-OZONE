import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C59206235_Verify_Chess_landing_page(Common):
    """
    TR_ID: C59206235
    NAME: Verify Chess landing page
    DESCRIPTION: This test case verifies Chess Landing pages
    PRECONDITIONS: Note:
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: * XX - sports **Category **ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: * Chess category id = 132
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: * XXX - the event ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    PRECONDITIONS: Steps:
    PRECONDITIONS: 1. Load the app
    """
    keep_browser_open = True

    def test_001_navigate_to_chess_landing_page(self):
        """
        DESCRIPTION: Navigate to Chess Landing page
        EXPECTED: **Desktop:**
        EXPECTED: * Table Tennis Landing Page is opened
        EXPECTED: * **Matches** -> **Today** tab is opened by default
        EXPECTED: * 'Enhanced Multiples' carousel is displayed above the tabs (if events are available)
        EXPECTED: * First **three** sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: **Mobile:**
        EXPECTED: * **Matches** tab is opened by default
        EXPECTED: * 'Enhanced Multiples' accordion is displayed at the top of 'Type' accordions (if events are available)
        """
        pass

    def test_002_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: The section header titles are in the following format and corresponds to the attributes:
        EXPECTED: categoryName + "** -** " + **typeName**
        """
        pass

    def test_003_verify_competitions_sections_order(self):
        """
        DESCRIPTION: Verify competitions sections order
        EXPECTED: Sections are ordered by displayOrder of each Type in ascending order
        """
        pass

    def test_004_verify_events_order_in_the_particular_type_section(self):
        """
        DESCRIPTION: Verify events order in the particular type section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: * (rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) (for 'Today' tab only for Desktop)
        EXPECTED: * startTime - chronological order in the first instance
        EXPECTED: * Event displayOrder in ascending order
        EXPECTED: * Alphabetical order
        """
        pass

    def test_005_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap **Outrights** tab
        EXPECTED: * **Outrights** tab is opened
        EXPECTED: * All sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by tapping the section's header
        EXPECTED: * Sections are ordered by displayOrder in ascending order
        """
        pass

    def test_006_tap_in_play_tab_desktop_only(self):
        """
        DESCRIPTION: Tap **In-Play** tab (Desktop only)
        EXPECTED: * 'Live now' and 'Upcoming' tabs are displayed
        EXPECTED: * 'Live now' tab is displayed by default if live events are available (if no - 'Upcoming' tab is opened)
        EXPECTED: * Live events on 'Live now' tab are displayed with related startTime and 'isOff = Yes' parameters
        """
        pass

    def test_007_tap_tomorrow_tab_desktop_only(self):
        """
        DESCRIPTION: Tap **Tomorrow** tab (Desktop only)
        EXPECTED: * **Tomorrow** tab is opened
        EXPECTED: * First **three** sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: * Types sections and events inside them are order same way as on Today tab
        EXPECTED: * Events within a tab have next day start time
        """
        pass

    def test_008_tap_future_tab_desktop_only(self):
        """
        DESCRIPTION: Tap 'Future' tab (Desktop only)
        EXPECTED: * **Future* tab is opened
        EXPECTED: * First **three** sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: * Types sections and events inside them are order same way as on Today tab
        EXPECTED: * Events within a tab have 2+ days start time from current date
        """
        pass
