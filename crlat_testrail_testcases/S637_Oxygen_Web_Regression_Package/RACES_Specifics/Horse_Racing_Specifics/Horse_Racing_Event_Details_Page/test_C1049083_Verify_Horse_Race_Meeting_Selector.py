import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1049083_Verify_Horse_Race_Meeting_Selector(Common):
    """
    TR_ID: C1049083
    NAME: Verify Horse Race Meeting Selector
    DESCRIPTION: This test case is for checking of race meeting selector which is displayed on the Horse Racing event details page
    DESCRIPTION: Applies to mobile, tablet & desktop
    DESCRIPTION: AUTOTEST: [C1501908]
    PRECONDITIONS: To get data (event start time) about events use the following link:
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id =21
    PRECONDITIONS: 2) To get all 'Events' for the classes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: Where
    PRECONDITIONS: *YYYY - a comma separated values of class ID's (e.g. 97 or 97, 98)*
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: - '**typeName' **to check race meetings name;
    PRECONDITIONS: - **'typeFlagCodes'** to verify a race group
    PRECONDITIONS: *   'UK' or 'IE' parameter, this event should be included in the group 'UK & IRE'
    PRECONDITIONS: *   'ZA'  - South Africa; 'AE' - UAE; 'CL' - Chile; 'IN' - India; 'AU' - Australia; 'US' - US; 'FR' - France
    PRECONDITIONS: *   'INT' parameter, this event should be included to the "Other International" group
    PRECONDITIONS: *   'VR' parameter, this event should be included in the 'VR' group ('Ladbrokes/Coral Legends' sections)
    PRECONDITIONS: User has Horse Racing Event Details Page opened
    """
    keep_browser_open = True

    def test_001_check_meeting_selector(self):
        """
        DESCRIPTION: Check 'Meeting' selector
        EXPECTED: **For Mobile&Tablet:**
        EXPECTED: *'Down' arrow is available right next to '[Event Name]'/'Next Races'  in breadcrumbs
        EXPECTED: **For Desktop**:
        EXPECTED: *'Meetings' link and 'up & down' arrows are shown right-aligned on the event name level
        """
        pass

    def test_002_mobiletablet_tap_on_the_part_of_breadcrumb_event_namenext_races_plusdown_arrow_in_the_page_subheaderdesktop_click_on_the_meeting_link_and_up__down_arrows(self):
        """
        DESCRIPTION: **Mobile&Tablet:** Tap on the part of breadcrumb: '[Event Name]'/'Next Races' +'Down' arrow in the page subheader
        DESCRIPTION: **Desktop:** Click on the 'Meeting' link and 'up & down' arrows
        EXPECTED: **For Mobile&Tablet:**
        EXPECTED: * 'Down' arrow is switched to 'Up' arrow
        EXPECTED: *  An overlay is slides from the bottom with list of available meetings
        EXPECTED: **For Desktop:**
        EXPECTED: * 'up & down' arrows are changed their location
        EXPECTED: * Widget with list of available meetings is opened right-aligned on the event name level
        """
        pass

    def test_003_check_the_list_of_meetings(self):
        """
        DESCRIPTION: Check the list of meetings
        EXPECTED: The following data are present:
        EXPECTED: * 'OFFERS AND FEATURED RACES' section with only 1 option available
        EXPECTED: - Extra Place Races
        EXPECTED: * All race meetings that belong to the 'UK&URE', '%Countries sections%'  'Other International', 'Virtual', 'Next Races', and Enhanced Multiples;
        EXPECTED: * Sub Regions as per below order:
        EXPECTED: UK + Ireland
        EXPECTED: France
        EXPECTED: UAE
        EXPECTED: South Africa
        EXPECTED: India
        EXPECTED: USA
        EXPECTED: Australia
        EXPECTED: Other International
        EXPECTED: Virtual
        EXPECTED: * Groups correspond to the **'typeFlagCodes' **attribute from the Site Server response
        EXPECTED: * The list of available meetings displays data only on the same day as the selected event. (e.g. If user selects today race event that the list of meetings available for today only is displayed)
        """
        pass

    def test_004_mobiletablet_tap_on_x_button_in_the_overlay_headerdesktop_click_on_the_meeting_link_and_up__down_arrows(self):
        """
        DESCRIPTION: **Mobile&Tablet:** Tap on 'X' button in the overlay header.
        DESCRIPTION: **Desktop:** Click on the 'Meeting' link and 'up & down' arrows
        EXPECTED: **For mobile&tablet:**
        EXPECTED: * Overlay with list of meetings is closed
        EXPECTED: **For desktop:**
        EXPECTED: * Widget with list of meetings is closed
        """
        pass

    def test_005_mobiletablet_click_on_the_meeting_link_in_the_menudesktop_click_on_the_meeting_link_and_up__down_arrows_navigate_between_event_types_using_the_selector(self):
        """
        DESCRIPTION: **Mobile&Tablet:** Click on the 'Meeting' link in the Menu
        DESCRIPTION: **Desktop:** Click on the 'Meeting' link and 'up & down' arrows
        DESCRIPTION: > Navigate between event types using the selector
        EXPECTED: User is redirected to the first available event from the selected event type.
        """
        pass

    def test_006_scroll_updown_event_details_page(self):
        """
        DESCRIPTION: Scroll up/down event details page
        EXPECTED: Meeting header is anchored to the top of the screen
        """
        pass
