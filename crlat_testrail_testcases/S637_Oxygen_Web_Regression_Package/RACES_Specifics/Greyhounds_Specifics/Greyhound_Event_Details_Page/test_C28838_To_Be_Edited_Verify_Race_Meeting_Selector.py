import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28838_To_Be_Edited_Verify_Race_Meeting_Selector(Common):
    """
    TR_ID: C28838
    NAME: [To Be Edited] Verify Race Meeting Selector
    DESCRIPTION: This test case is for checking of race meeting selector which is displayed on the Greyhound event details page
    PRECONDITIONS: To get data (event start time) about events use the following link:
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1) To get Class IDs use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id =21
    PRECONDITIONS: Greyhound category id = 19
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
    PRECONDITIONS: 3. App is loaded
    """
    keep_browser_open = True

    def test_001_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_002_go_to_the_today_event_details_page(self):
        """
        DESCRIPTION: Go to the today event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_check_meeting_selector(self):
        """
        DESCRIPTION: Check meeting selector
        EXPECTED: **For Mobile&Tablet:**
        EXPECTED: * Race meeting selector is displayed in the [Event Name] + 'Down' arrow part of breadcrumb above the event off times ribbon
        EXPECTED: **For Desktop:**
        EXPECTED: * 'up & down' arrows are changed their location
        EXPECTED: * Widget with list of available meetings is opened right-aligned on the event name level
        """
        pass

    def test_004_check_meeting_name_in_selector(self):
        """
        DESCRIPTION: Check meeting name in selector
        EXPECTED: 1.  Current race meeting name is displayed in race meeting selector
        EXPECTED: 2.  Race meeting name corresponds to the **'typeName'** attribute from the Site Server response
        """
        pass

    def test_005_check_values_in_the_meeting_selector(self):
        """
        DESCRIPTION: Check values in the meeting selector
        EXPECTED: 1.  All race meetings that belong to the 'UK&URE', '%Countries sections%'  'Other International' displayed in corresponding sections
        EXPECTED: 2.  All race today meeting
        EXPECTED: 3.  Groups correspond to the **'typeFlagCodes' **attribute from the Site Server response
        EXPECTED: 4.  Race meetings in selector correspond to the race meetings on Greyhound Racing homepage.
        """
        pass

    def test_006_navigate_between_event_types_using_the_selector(self):
        """
        DESCRIPTION: Navigate between event types using the selector
        EXPECTED: User is redirected to the first available event from the selected event type.
        """
        pass
