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
class Test_C28728_Verify_Landing_pages(Common):
    """
    TR_ID: C28728
    NAME: Verify Landing pages
    DESCRIPTION: This test case verifies Landing pages
    DESCRIPTION: Story related: BMA-2280 Create a Motor Bikes sport within the Application
    PRECONDITIONS: 1. In order to get a list of **Classes IDs **and **Types IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports **Category **ID (Motor Bikes=23)
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

    def test_002_tapmotor_bikes_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Motor Bikes' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: *   Motor Bikes Landing Page is opened
        EXPECTED: *   '**Events**' tab is opened by default
        EXPECTED: *   First **three **sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: **Mobile:**
        EXPECTED: * Motor Bikes Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
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
        EXPECTED: 1.  **(rawlsOffCode == "Y" or (rawlsOffCode == "-" or isStarted==true)) **(for 'Today' tab only for Desktop)
        EXPECTED: 2.  **startTime **- chronological order in the first instance
        EXPECTED: 3.  **Event displayOrder ** in ascending
        EXPECTED: 4.  **Alphabetical order**
        """
        pass

    def test_006_tap_outrights_sectionnote_for_mobile_view_outright_events_are_displayed_in_outrights_section_if_available(self):
        """
        DESCRIPTION: Tap 'Outrights' section
        DESCRIPTION: Note: for Mobile view Outright events are displayed in Outrights section (if available)
        EXPECTED: *  Available '**Outrights**' are displayed
        EXPECTED: *   **All **sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by tapping the section's header
        """
        pass

    def test_007_repeat_step_5(self):
        """
        DESCRIPTION: Repeat step №5
        EXPECTED: The same as on the step №5
        """
        pass