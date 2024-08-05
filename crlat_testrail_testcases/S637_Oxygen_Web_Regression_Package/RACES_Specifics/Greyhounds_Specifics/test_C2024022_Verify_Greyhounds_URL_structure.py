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
class Test_C2024022_Verify_Greyhounds_URL_structure(Common):
    """
    TR_ID: C2024022
    NAME: Verify Greyhounds URL structure
    DESCRIPTION: This test case verifies Greyhounds URL structure
    PRECONDITIONS: * Openbet Systems: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Go to Greyhounds landing page
        EXPECTED: * Greyhounds landing page is opened
        EXPECTED: * Today tab is selected by default
        EXPECTED: * By meeting filter is selected by default
        """
        pass

    def test_003_verify_url_structure(self):
        """
        DESCRIPTION: Verify URL structure
        EXPECTED: URL structure of Event Details page is in the next format:
        EXPECTED: https://{domain}/#/category/{tab}
        EXPECTED: where
        EXPECTED: category - OB category name
        """
        pass

    def test_004_verify_url_structure_format(self):
        """
        DESCRIPTION: Verify URL structure format
        EXPECTED: * All text within URL is in lower case
        EXPECTED: * Space between worlds is replaced by "-" symbol
        EXPECTED: * The next specials characters "%", "-", ":" are replaced by "-" symbol
        """
        pass

    def test_005_select_today_by_time_filter_tomorrow_by_meetingby_time_filter_future_by_meetingby_time_filter_resulttabs_one_by_one_and_repeat_steps_3_4(self):
        """
        DESCRIPTION: Select
        DESCRIPTION: * Today, By Time filter
        DESCRIPTION: * Tomorrow, By meeting/By Time filter
        DESCRIPTION: * Future, By meeting/By Time filter
        DESCRIPTION: * Result
        DESCRIPTION: tabs one by one and repeat steps #3-4
        EXPECTED: 
        """
        pass

    def test_006_go_to_event_details_page_via_next_races_module(self):
        """
        DESCRIPTION: Go to Event Details page via Next Races module
        EXPECTED: Event Details page is opened
        """
        pass

    def test_007_verify_url_structure_of_event_details_page(self):
        """
        DESCRIPTION: Verify URL structure of Event Details page
        EXPECTED: URL structure of Event Details page is in the next format:
        EXPECTED: https://{domain}/#/category/class/type/event/event_id
        EXPECTED: where
        EXPECTED: category - OB category name
        EXPECTED: class - OB class name
        EXPECTED: type - OB type name
        EXPECTED: event_name - OB event name
        EXPECTED: eventID - OB event id
        """
        pass

    def test_008_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_009_go_to_event_details_page_from_today_tab_by_meetingby_time_filter_tomorrow_tab_by_meetingby_time_filter_future_tab_by_meetingby_time_filter_featured_tab_module_with_greyhounds_typeidand_repeat_steps_7_8(self):
        """
        DESCRIPTION: Go to Event Details page from
        DESCRIPTION: * Today tab, By meeting/By Time filter
        DESCRIPTION: * Tomorrow tab, By meeting/By Time filter
        DESCRIPTION: * Future tab, By meeting/By Time filter
        DESCRIPTION: * Featured Tab Module with Greyhounds typeID
        DESCRIPTION: and repeat steps #7-8
        EXPECTED: 
        """
        pass
