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
class Test_C28980_Verify_By_Meetings_Sorting_Type___To_be_archived(Common):
    """
    TR_ID: C28980
    NAME: Verify 'By Meetings' Sorting Type  -  To be archived
    DESCRIPTION: This test case verifies 'By Meetings' sorting of events
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_from_the_sports_menu_ribbon_tap_greyhounds_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon tap 'Greyhounds' icon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_tap_result_tab(self):
        """
        DESCRIPTION: Tap 'Result' tab
        EXPECTED: *   'Result' tab is opened
        EXPECTED: *   'By Latest Results' sorting type is selected by default
        """
        pass

    def test_004_select_by_meetings_sorting_type(self):
        """
        DESCRIPTION: Select** 'By Meetings'** sorting type
        EXPECTED: *   'By Meetings' sorting type is opened
        EXPECTED: *   A list of Results sections is shown
        """
        pass

    def test_005_verify_results_sections(self):
        """
        DESCRIPTION: Verify Results sections
        EXPECTED: *   All Result's sections are collapsed be default
        EXPECTED: *   Result section is expandable / collapsible
        """
        pass

    def test_006_verify_results_section_header(self):
        """
        DESCRIPTION: Verify Result's section header
        EXPECTED: Header consists of Event Type Name ('**typeName' **attribute from the event level)
        """
        pass

    def test_007_verify_start_date_for_each_event_within_one_event_type(self):
        """
        DESCRIPTION: Verify start date for each event within one event type
        EXPECTED: *   Event start time is shown under each Result's section
        EXPECTED: *   Event start time corresponds to the '**startTime'** attribute (NOTE, user localization is taken into consideration)
        EXPECTED: *   Event time is shown in the format:
        EXPECTED: **Today. MM:HH**
        """
        pass
