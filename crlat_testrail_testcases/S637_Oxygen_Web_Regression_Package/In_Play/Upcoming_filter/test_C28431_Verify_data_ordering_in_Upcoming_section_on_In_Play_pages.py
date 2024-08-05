import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C28431_Verify_data_ordering_in_Upcoming_section_on_In_Play_pages(Common):
    """
    TR_ID: C28431
    NAME: Verify data ordering in 'Upcoming' section on 'In-Play' pages
    DESCRIPTION: This test case verifies  'Upcoming' filter on 'In-Play Sports' page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1. Load Oxygen application
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for Mobile/Tablet) or Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header' (**Desktop**) and choose 'Watch Live' tab and choose 'Upcoming' switcher (**Desktop**)
    PRECONDITIONS: 3. Make sure that Upcoming events are present in 'Upcoming' section (**Mobile/Tablet**) or when 'Upcoming' switcher is selected (** Desktop**)
    PRECONDITIONS: Note:
    PRECONDITIONS: * In order to get a list with Regions (Classes IDs) and Leagues (Types IDs) use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: * http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: * To verify category/class/type ordering check received data using Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORTS::XX::UPCOMING_EVENT"
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: ![](index.php?/attachments/get/40723)
    """
    keep_browser_open = True

    def test_001_verify_category_title_on_the_first_level_accordion_within_upcoming_section(self):
        """
        DESCRIPTION: Verify <Category> title on the first level accordion within 'Upcoming' section
        EXPECTED: 'Sport' name is displayed at the <Category> accordion within 'Upcoming' section
        """
        pass

    def test_002_verify_category_accordions_order(self):
        """
        DESCRIPTION: Verify <Category> accordions order
        EXPECTED: <Category> accordions are ordered by:
        EXPECTED: * Category 'displayOrder' in ascending where minus ordinals are displayed first
        """
        pass

    def test_003_verify_type_title_on_accordionsodds_headers_within_upcoming_section(self):
        """
        DESCRIPTION: Verify <Type> title on accordions/odds headers within 'Upcoming' section
        EXPECTED: The accordion header titles are in the following format and correspond to the following attributes:
        EXPECTED: **Mobile/Tablet:**
        EXPECTED: 'Type Name'
        EXPECTED: **Desktop:**
        EXPECTED: *   'Category Name' - 'Type Name' if section is named Category Name + Type Name on Pre-Match pages
        EXPECTED: *   'Class Name' - 'Type Name' if section is named Class Name (sport name should not be displayed) + Type Name on Pre-Match pages
        EXPECTED: 'CASH OUT' label is shown next to Event type name if at least one of it's events has cashoutAvail="Y
        """
        pass

    def test_004_verify_type_accordionsodds_headers_order(self):
        """
        DESCRIPTION: Verify <Type> accordions/odds headers order
        EXPECTED: <Type> accordions/odds headers are ordered by:
        EXPECTED: * Class 'displayOrder' in ascending where minus ordinals are displayed first
        EXPECTED: * Type 'displayOrder' in ascending where minus ordinals are displayed first
        """
        pass

    def test_005_verify_events_order_within_the_type_accordionsodds_headers(self):
        """
        DESCRIPTION: Verify events order within the <Type> accordions/odds headers
        EXPECTED: Events are ordered in the following way:
        EXPECTED: *  'startTime' - chronological order in the first instance
        EXPECTED: *  Event 'displayOrder'  in ascending
        EXPECTED: *  Alphabetical order
        """
        pass

    def test_006_repeat_steps_1_5_on_home_page__in_play_tab_mobiletablet(self):
        """
        DESCRIPTION: Repeat steps 1-5 on:
        DESCRIPTION: * Home page > 'In-Play' tab **Mobile/Tablet**
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_3_5_on_sports_landing_page__in_play_tab_in_play_page__sport_tab(self):
        """
        DESCRIPTION: Repeat steps 3-5 on:
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * 'In-Play' page > 'Sport' tab
        EXPECTED: 
        """
        pass
