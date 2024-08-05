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
class Test_C28661_Verify_Tennis_Landing_pages(Common):
    """
    TR_ID: C28661
    NAME: Verify Tennis Landing pages
    DESCRIPTION: This test case verifies Tennis Landing pages
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C9690158](https://ladbrokescoral.testrail.com/index.php?/cases/view/9690158)
    DESCRIPTION: Desktop - [C9697897](https://ladbrokescoral.testrail.com/index.php?/cases/view/9697897)
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Tennis=34)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
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

    def test_002_taptennis_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Tennis' icon on the Sports Menu Ribbon
        EXPECTED: *   Tennis Landing Page is opened
        EXPECTED: *   '**Matches**'->'**Today**' tab is opened by default (for desktop)/ '**Matches** tab is opened by default (for mobile)
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_003_verify_section_headers_titles(self):
        """
        DESCRIPTION: Verify section header's titles
        EXPECTED: The section header titles are in the following format and correponds to the attributes:
        EXPECTED: **Category Name** + "** -** " + **Type Name**
        """
        pass

    def test_004_verify_competitions_sections_order(self):
        """
        DESCRIPTION: Verify Competitions sections order
        EXPECTED: Competitions sections are ordered by:
        EXPECTED: **Type displayOrder **in ascending order
        """
        pass

    def test_005_verify_events_order(self):
        """
        DESCRIPTION: Verify events order
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) **(for 'Today' tab only, for desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        pass

    def test_006_verify_displaying_of_team_names_within_the_events(self):
        """
        DESCRIPTION: Verify displaying of team names within the events
        EXPECTED: Team names are shown in the following format:
        EXPECTED: *  Team1_name
        EXPECTED: *  Team2_name
        EXPECTED: (2 lines of text), where Team1_name is the name of Away team, and Team2_name is the name of Home team
        """
        pass

    def test_007_tap_matches_tomorrow_tab_for_desktop_onle(self):
        """
        DESCRIPTION: Tap 'Matches'->'Tomorrow' tab (for desktop onle)
        EXPECTED: *   '**Tomorrow**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_008_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: The same as on the steps №4-5
        """
        pass

    def test_009_tap_matches_future_tab_for_destop_only(self):
        """
        DESCRIPTION: Tap 'Matches'->'Future' tab (for destop only)
        EXPECTED: *   '**Future**' tab is opened
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        """
        pass

    def test_010_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: The same as on the steps steps №4-5
        """
        pass

    def test_011_tap_outrights_tab(self):
        """
        DESCRIPTION: Tap 'Outrights' tab
        EXPECTED: *   '**Outrights**' tab is opened
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        pass

    def test_012_repeat_steps_4_5(self):
        """
        DESCRIPTION: Repeat steps №4-5
        EXPECTED: The same as on the steps №4-5
        """
        pass
