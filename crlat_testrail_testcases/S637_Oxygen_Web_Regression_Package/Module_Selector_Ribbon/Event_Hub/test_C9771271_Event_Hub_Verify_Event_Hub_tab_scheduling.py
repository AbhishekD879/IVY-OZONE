import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9771271_Event_Hub_Verify_Event_Hub_tab_scheduling(Common):
    """
    TR_ID: C9771271
    NAME: Event Hub: Verify Event Hub tab scheduling
    DESCRIPTION: This test case verifies Event Hub tab scheduling
    PRECONDITIONS: 1. Event hub is created in CMS > Sport Pages > Event Hubs
    PRECONDITIONS: 2. Event Hub Module ribbon tab is created in CMS > Module ribbon tabs. It is scheduled to be displayed in current time.
    """
    keep_browser_open = True

    def test_001_load_app_and_navigate_to_homepage(self):
        """
        DESCRIPTION: Load app and navigate to homepage
        EXPECTED: Event Hub tab is displayed on FE
        """
        pass

    def test_002_in_cms_set_visible_to_time_for_this_event_hub_module_ribbon_tab_to_few_minutes_in_future(self):
        """
        DESCRIPTION: In CMS set 'Visible to' time for this Event Hub Module ribbon tab to few minutes in future.
        EXPECTED: 
        """
        pass

    def test_003_in_app_wait_for_event_hub_module_ribbon_tab_to_expire(self):
        """
        DESCRIPTION: In app wait for Event Hub Module ribbon tab to expire.
        EXPECTED: Event Hub Module ribbon tab is still displayed.
        """
        pass

    def test_004_refresh_page_and_verify_event_hub_module_ribbon_tab(self):
        """
        DESCRIPTION: Refresh page and verify Event Hub Module ribbon tab.
        EXPECTED: Event Hub Module ribbon tab disappears from FE.
        """
        pass

    def test_005_in_cms_set_visible_from_time_for_this_event_hub_module_ribbon_tab_to_few_minutes_in_future(self):
        """
        DESCRIPTION: In CMS set 'Visible from' time for this Event Hub Module ribbon tab to few minutes in future.
        EXPECTED: 
        """
        pass

    def test_006_load_app_and_wait_for_visible_from_time_to_come(self):
        """
        DESCRIPTION: Load app and wait for 'Visible from' time to come.
        EXPECTED: Event Hub Module ribbon tab is not displayed.
        """
        pass

    def test_007_refresh_page_and_verify_event_hub_module_ribbon_tab(self):
        """
        DESCRIPTION: Refresh page and verify Event Hub Module ribbon tab.
        EXPECTED: Event Hub Module ribbon tab appears on FE.
        """
        pass
