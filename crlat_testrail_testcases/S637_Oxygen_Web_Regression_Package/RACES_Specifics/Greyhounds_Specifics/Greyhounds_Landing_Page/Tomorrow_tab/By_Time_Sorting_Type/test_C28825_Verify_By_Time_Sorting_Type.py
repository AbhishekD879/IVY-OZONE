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
class Test_C28825_Verify_By_Time_Sorting_Type(Common):
    """
    TR_ID: C28825
    NAME: Verify 'By Time' Sorting Type
    DESCRIPTION: This test case verifies 'Tomorrow' tab when 'By Time' sorting type is selected
    PRECONDITIONS: 1. In order to get a list with Classes ids use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id =21
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2. To retrieve all event outcomes for class id indentified in step 1 use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/ZZZZ?translationLang=LL?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *Where:*
    PRECONDITIONS: *-* *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *- XX - sport category id*
    PRECONDITIONS: *- ZZZZ is a comma separated list of Class id's(e.g. 97 or 97, 98);*
    PRECONDITIONS: *- YYYY1-MM1-DD1 is tomorrow's date;*
    PRECONDITIONS: *- YYYY2-MM2-YY2 is the day after tomorrow's date;
    PRECONDITIONS: *LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    """
    keep_browser_open = True

    def test_001_tap_tomorrow_tab(self):
        """
        DESCRIPTION: Tap 'TOMORROW' tab
        EXPECTED: 'TOMORROW' tab is opened
        EXPECTED: 'BY MEETING' sorting type is selected by default
        """
        pass

    def test_002_select_by_time_sorting_type(self):
        """
        DESCRIPTION: Select 'BY TIME' sorting type
        EXPECTED: 'BY TIME' sorting type is selected
        """
        pass

    def test_003_check_events_section(self):
        """
        DESCRIPTION: Check Events section
        EXPECTED: 1.  Events Section is displayed
        EXPECTED: 2.  Events section is expanded by default
        """
        pass

    def test_004_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: List of events for tomorrow's date is shown
        """
        pass

    def test_005_check_event_section(self):
        """
        DESCRIPTION: Check event section
        EXPECTED: 1.  Each event is in a separate block
        EXPECTED: 2.  Event name corresponds to the **'name'** attribute from the Site Server response (it includes race local time and event name)
        """
        pass

    def test_006_verify_stream_icon(self):
        """
        DESCRIPTION: Verify 'Stream' icon
        EXPECTED: 1.  Stream icon is displayed under the event name
        EXPECTED: 2.  Event name and Stream icon are aligned
        """
        pass
