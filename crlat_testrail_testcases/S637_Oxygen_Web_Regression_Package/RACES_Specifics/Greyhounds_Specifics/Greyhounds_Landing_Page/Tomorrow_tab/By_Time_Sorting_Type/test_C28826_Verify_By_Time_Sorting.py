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
class Test_C28826_Verify_By_Time_Sorting(Common):
    """
    TR_ID: C28826
    NAME: Verify 'By Time' Sorting
    DESCRIPTION: This test case verifies 'By Time' sorting of events
    PRECONDITIONS: 1. In order to get a list with Classes ids use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id =21
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2. To retrieve all event outcomes for class id identified in step 1 use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/ZZZZ?translationLang=LL?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *Where:*
    PRECONDITIONS: *- X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *- XX - sport category id*
    PRECONDITIONS: *- ZZZZ is a comma separated list of Class id's(e.g. 97 or 97, 98);*
    PRECONDITIONS: *- YYYY1-MM1-DD1 is tomorrow's date;*
    PRECONDITIONS: *- YYYY2-MM2-YY2 is the day after tomorrow's date;*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: see **'name' **attribute in order to check a name and local time
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    """
    keep_browser_open = True

    def test_001_go_to_tomorrow_tab___select_by_time_sorting_type(self):
        """
        DESCRIPTION: Go to 'TOMORROW' tab -> Select 'BY TIME' sorting type
        EXPECTED: - 'BY TIME' sorting type is opened
        EXPECTED: - 'Events' section is visible
        EXPECTED: - 'Next Races' section is visible
        """
        pass

    def test_002_check_events_section(self):
        """
        DESCRIPTION: Check 'Events' section
        EXPECTED: - Section header is entitled 'Events'
        EXPECTED: - 'Events' section is expanded by default
        EXPECTED: - It is possible to collapse/expand the 'Events' section
        """
        pass

    def test_003_check_next_races_section(self):
        """
        DESCRIPTION: Check 'Next races' section
        EXPECTED: Section header is entitled 'Next races'
        EXPECTED: **FOR Mobile** 'NEXT RACES' section is displayed and expanded by default
        EXPECTED: **FOR Desktop** 'Next Races' widget is displayed and expanded by default
        EXPECTED: It is possible to collapse/expand the 'Next races' sections
        """
        pass

    def test_004_verify_by_time_sorting(self):
        """
        DESCRIPTION: Verify 'BY TIME' sorting
        EXPECTED: Events are sorted in the following order:
        EXPECTED: 1)** **chronologically **by race** **local time** order in the first instance
        EXPECTED: 2) alphabetically by **name** in ascending order if event start times are the same
        """
        pass
