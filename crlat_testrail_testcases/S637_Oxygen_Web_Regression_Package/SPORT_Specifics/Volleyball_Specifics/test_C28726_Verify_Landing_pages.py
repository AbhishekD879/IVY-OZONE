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
class Test_C28726_Verify_Landing_pages(Common):
    """
    TR_ID: C28726
    NAME: Verify Landing pages
    DESCRIPTION: This test case verifies Landing pages
    PRECONDITIONS: 1) In order to get a list with **Regions **(**Classes IDs) **and **Leagues (Types IDs) **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Vollyeball=36)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID (Volleyball=36)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapvolleyball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Volleyball' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: *   '**Matches**'->''**Today**' tab is opened by default
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: **Mobile:**
        EXPECTED: *   '**Matches** tab is opened by default
        EXPECTED: * In-Play module is displayed at the top if available
        EXPECTED: * Upcoming module is displayed below (with Market selector)
        """
        pass

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: The section header titles are in the following format and correponds to the attributes:
        EXPECTED: **className** (sport name is not displayed) + ""** -** "" + t**ypeName**
        """
        pass

    def test_004_verify_leagues_sections_order(self):
        """
        DESCRIPTION: Verify Leagues sections order
        EXPECTED: Leagues sections are ordered by:
        EXPECTED: 1.  Class **displayOrder **in ascending order where minus ordinals are displayed first
        EXPECTED: 2.  Type **displayOrder **in ascending order
        """
        pass

    def test_005_verify_events_order_in_the_league_section(self):
        """
        DESCRIPTION: Verify events order in the League section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true))** (for 'Today' tab only for Desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        pass

    def test_006_tap_tomorrow_tab_desktop(self):
        """
        DESCRIPTION: Tap '**Tomorrow**' tab (Desktop)
        EXPECTED: *   'Tomorrow' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_007_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps №3-5
        EXPECTED: The same as on the steps №3-5
        """
        pass

    def test_008_tap_future_tab_desktop(self):
        """
        DESCRIPTION: Tap '**Future**' tab (Desktop)
        EXPECTED: *   'Future' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_009_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps №3-5
        EXPECTED: The same as on the steps №3-5
        """
        pass

    def test_010_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap '**Outrights**' tab
        EXPECTED: *   'Outrights' tab is opened
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        pass

    def test_011_repeat_steps_3_5(self):
        """
        DESCRIPTION: Repeat steps №3-5
        EXPECTED: The same as on the steps №3-5
        """
        pass
