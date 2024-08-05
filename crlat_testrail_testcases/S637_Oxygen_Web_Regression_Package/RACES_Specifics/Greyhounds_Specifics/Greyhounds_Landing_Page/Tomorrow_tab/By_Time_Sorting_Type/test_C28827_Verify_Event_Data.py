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
class Test_C28827_Verify_Event_Data(Common):
    """
    TR_ID: C28827
    NAME: Verify Event Data
    DESCRIPTION: This test case verifies whether data about events is displayed correctly
    PRECONDITIONS: To get data about event statuses use the following steps;
    PRECONDITIONS: 1) Retrieve all classes for the category 'Horse racing'.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id = 21
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2. Retrieve all events for class identified in step 1. Use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/ZZZZ?translationLang=LL?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *Where:*
    PRECONDITIONS: *- X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *- XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: *- ZZZZ is a comma separated list of class ids. (e.g. 97 or 97,98);*
    PRECONDITIONS: *- YYYY1-MM1-DD1 is tomorrow's date;*
    PRECONDITIONS: *- YYYY2-MM2-DD2 is the day after tomorrow's date;*
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    """
    keep_browser_open = True

    def test_001_go_to_tomorrow_tab__gt_select_by_time_sorting_type(self):
        """
        DESCRIPTION: Go to 'TOMORROW' tab -&gt; Select 'BY TIME' sorting type
        EXPECTED: 'Events' section is visible
        """
        pass

    def test_002_verify_event_name_and_local_time(self):
        """
        DESCRIPTION: Verify Event name and local time
        EXPECTED: *   Event name corresponds to the **'name' **attribute
        EXPECTED: *   Event name and local time are hyperlinked
        EXPECTED: *   Event name is shown in 'HH:MM EventName' format
        EXPECTED: *   Events with LP prices are displayed in bold if **'priceTypeCodes="LP,"'** attribute is available for **'Win or Each way'** market only
        """
        pass

    def test_003_check_event_name__time_displaying(self):
        """
        DESCRIPTION: Check event name / time displaying
        EXPECTED: Event name/ time are in bold if **'priceTypeCodes="LP, '** attribute is available for **'Win or Each way'** market only
        """
        pass

    def test_004_verify_stream_icon(self):
        """
        DESCRIPTION: Verify 'Stream' icon
        EXPECTED: If event has stream available -&gt; 'Stream' icon will be shown
        """
        pass

    def test_005_tap_event_name(self):
        """
        DESCRIPTION: Tap event name
        EXPECTED: Event landing page is opened
        """
        pass

    def test_006_verify_by_time_sorting_type_when_there_are_no_events_to_show(self):
        """
        DESCRIPTION: Verify 'BY TIME' sorting type when there are no events to show
        EXPECTED: * Events section is not displayed
        EXPECTED: * Message is visible 'No events found'
        """
        pass
