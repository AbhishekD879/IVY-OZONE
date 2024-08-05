import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C874354_Navigation_All_Sports(Common):
    """
    TR_ID: C874354
    NAME: Navigation All Sports
    DESCRIPTION: AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=735046&group_order=asc
    DESCRIPTION: Verify that all sports are listed on "All Sports" page in alphabetical order
    DESCRIPTION: **NOTE:**
    DESCRIPTION: * Also, displaying of a Sport in 'A-Z Competitions' & 'Top Sports' sections based on availability of OB events
    DESCRIPTION: * To check whether events are available for a CategoryId:
    DESCRIPTION: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Event/?simpleFilter=event.categoryId:equals:{ID}&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.suspendAtTime:greaterThanOrEqual:YYYY-MM-DDTHH:MM:00.000&includeUndisplayed=false
    DESCRIPTION: * Displaying of a Sport depends on "hasEvents"="true/false" parameter received in "initial-data" response > sportCategories
    DESCRIPTION: AUTOMATED [C47071798] [C47855353]
    PRECONDITIONS: 1. Oxygen application is loaded ->'Sports' page is opened
    PRECONDITIONS: 2. Verify the 'Left Navigation' menu (A-Z Sports)(For Desktop)
    PRECONDITIONS: 3. Tap on 'All Spots' Button -> A-Z Sports is opened (For Mobile/Tablet)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. Sport Category is configured in CMS: Sports Pages > Sport Categories with:
    PRECONDITIONS: - Open Bet 'CategoryId' (e.g. 'Football' with 'CategoryId'=16) if events are available for a Category in Open Bet
    PRECONDITIONS: - Open Bet 'CategoryId' (e.g. 'Darts' with 'CategoryId'=13) if events are NOT available for a Category in Open Bet
    PRECONDITIONS: - Non Open Bet 'CategoryId' e.g. Player Bets
    PRECONDITIONS: 2. 'Top Sports' are configured in CMS for some Sports e.g. Football, Horse Racing, Greyhounds:
    PRECONDITIONS: Sports Pages > Sport Categories > <Sport> -> 'General Sport Configuration' ->'Is Top Sport' check box is checked
    PRECONDITIONS: 3. 'A-Z Sports' is configured in CMS for some Sports e.g. Basketball, Football, Greyhounds, Horse Racing etc
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> -> 'General Sport Configuration' -> 'Show in AZ' check box is checked)
    PRECONDITIONS: 4. Make sure Connect section in A-Z is turned on in CMS: System configuration -> Connect -> menu
    """
    keep_browser_open = True

    def test_001_verify_page_header_and_back_button_mobiletablet(self):
        """
        DESCRIPTION: Verify page header and Back button (Mobile/Tablet)
        EXPECTED: * Page header is 'All Sports'
        EXPECTED: * Tap on Back button gets user back to previous page
        """
        pass

    def test_002_verify_top_sports_section_mobiletablet(self):
        """
        DESCRIPTION: Verify 'Top Sports' section (Mobile/Tablet)
        EXPECTED: * Section is displayed only if Top Sports are configured in CMS
        EXPECTED: * Sports are displayed in a list view
        EXPECTED: * No icon is displayed next to a Sport name
        EXPECTED: * Only Sports with the CMS setting 'is Top Sport?' are shown in this section
        EXPECTED: * Top Sports are ordered like configured in CMS (configurations made by dragging)
        """
        pass

    def test_003_verify_a_z_section(self):
        """
        DESCRIPTION: Verify 'A-Z' section
        EXPECTED: * Title is 'A-Z'
        EXPECTED: * Sports are displayed in a list view
        EXPECTED: * There are Sport name and icon
        EXPECTED: * Only Sports with the CMS setting 'Show in A-Z' are shown in this section
        EXPECTED: * All sports are shown in alphabetical A-Z order
        """
        pass

    def test_004_verify_connect_section_mobiletablet(self):
        """
        DESCRIPTION: Verify 'Connect' section (Mobile/Tablet)
        EXPECTED: * There is the section 'Connect' at the bottom of the page
        EXPECTED: * The name of the section is 'Connect'
        EXPECTED: * Section contains list of items (that corresponds to CMS configurations) (one exception: 'User connect online' item is shown only for Logged in In-Shop user)
        EXPECTED: * 'Connect' section's items are ordered as configured in CMS:
        EXPECTED: Menu -> Connect menu
        EXPECTED: (configurations made by dragging)
        """
        pass

    def test_005_verify_sport_availability_in_a_z_categories_section_that_has_events_from_preconditions_1_eg_football(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section that has events (from Preconditions 1 e.g. Football)
        EXPECTED: Sport e.g. Football is available in 'A-Z Categories' section
        """
        pass

    def test_006_verify_sport_availability_in_a_z_categories_section_that_has_no_events_from_preconditions_2_eg_darts(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section that has no events (from Preconditions 2 e.g. Darts)
        EXPECTED: Sport e.g. Darts is NOT available in 'A-Z Categories' section (Not applicable for Desktop - all categories will be displayed)
        """
        pass

    def test_007_verify_sport_availability_in_a_z_categories_section_with_non_ob_categoryid_from_preconditions_3_eg_player_bets(self):
        """
        DESCRIPTION: Verify Sport availability in 'A-Z Categories' section with non OB 'CategoryId' (from Preconditions 3 e.g. Player Bets)
        EXPECTED: Sport e.g. Player Bets is available in 'A-Z Categories' section
        """
        pass

    def test_008_repeat_steps_5_7_for_sports_in_top_sports_section(self):
        """
        DESCRIPTION: Repeat steps 5-7 for sports in 'Top Sports' section
        EXPECTED: Results are the same
        """
        pass
