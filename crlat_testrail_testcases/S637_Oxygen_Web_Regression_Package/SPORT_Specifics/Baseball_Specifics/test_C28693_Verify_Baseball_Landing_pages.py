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
class Test_C28693_Verify_Baseball_Landing_pages(Common):
    """
    TR_ID: C28693
    NAME: Verify Baseball Landing pages
    DESCRIPTION: This test case verifies Landing pages
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   [BMA-15231: Changes to behaviour and display of US Sport events][1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-15231
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Baseball=5)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:** Current supported version of OB release can be found in the request by the list of events (Dev tools -> Network -> request URL in the "Headers" section of the request by the list of events)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapbaseball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Baseball' icon on the Sports Menu Ribbon
        EXPECTED: Desktop:
        EXPECTED: * Baseball Landing Page is opened
        EXPECTED: * '**Events**' tab is opened by default
        EXPECTED: * First **three **sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: Mobile:
        EXPECTED: * Baseball Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        pass

    def test_003_verify_accordions_headers_titles(self):
        """
        DESCRIPTION: Verify accordions header's titles
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
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true))** (for 'Today' tab only for desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        pass

    def test_006_verify_displaying_of_team_names_within_the_events(self):
        """
        DESCRIPTION: Verify displaying of team names within the events
        EXPECTED: Team names are shown in the following format:
        EXPECTED: Team1_name Team2_name
        EXPECTED: (2 lines of text), where Team1_name is the name of Away team, and Team2_name is the name of Home team
        """
        pass
