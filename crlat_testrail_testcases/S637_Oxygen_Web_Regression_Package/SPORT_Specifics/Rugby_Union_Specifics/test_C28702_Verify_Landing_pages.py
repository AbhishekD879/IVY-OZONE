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
class Test_C28702_Verify_Landing_pages(Common):
    """
    TR_ID: C28702
    NAME: Verify Landing pages
    DESCRIPTION: This test case verifies Landing pages
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Rugby Union category id = 31
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
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

    def test_002_taprugby_union_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Rugby Union' icon on the sports menu ribbon
        EXPECTED: *   Rugby Union Landing Page is opened
        EXPECTED: *   '**Matches**'->''**Today**' tab is opened by default (for desktop)/ 'Matches' tab is opened (for mobile)
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: The section header titles are in the following format and correponds to the attributes:
        EXPECTED: **categoryName** + "** -** " + **typeName**
        """
        pass

    def test_004_verify_competitions_sections_order(self):
        """
        DESCRIPTION: Verify Competitions sections order
        EXPECTED: Competitions sections are ordered by:
        EXPECTED: **Type displayOrder **in ascending order
        """
        pass

    def test_005_verify_events_order_in_the_competitions_section(self):
        """
        DESCRIPTION: Verify events order in the Competitions section
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) **(for 'Today' tab only for desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        pass

    def test_006_tap_tomorrow_tab_for_desktop_only(self):
        """
        DESCRIPTION: Tap **'Tomorrow' **tab (for desktop only)
        EXPECTED: *   '**Tomorrow**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_007_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps №5-6
        """
        pass

    def test_008_tap_future_tab__for_desktop_only(self):
        """
        DESCRIPTION: Tap **'Future'** tab ( for desktop only)
        EXPECTED: *   '**Future**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_009_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps steps №5-6
        """
        pass

    def test_010_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap** 'Outrights'** tab
        EXPECTED: *   '**Outrights**' tab is opened
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        pass

    def test_011_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps №5-6
        EXPECTED: The same as on the steps №5-6
        """
        pass
