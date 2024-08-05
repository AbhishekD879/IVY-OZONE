import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C543391_TO_EDIT_Reloading_landing_page_content_after_inactivity_period(Common):
    """
    TR_ID: C543391
    NAME: [TO EDIT] Reloading landing page content after inactivity period
    DESCRIPTION: This test case verifies reloading landing page content after inactivity period
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to any sport landing page
        EXPECTED: 
        """
        pass

    def test_002_lock_devices_for_more_than_1_minute(self):
        """
        DESCRIPTION: Lock devices for more than 1 minute
        EXPECTED: 
        """
        pass

    def test_003_trigger_changes_in_backoffice_for_some_event_suspension_price_or_start_timedate_change_etc(self):
        """
        DESCRIPTION: Trigger changes in backoffice for some event (suspension, price or start time/date change etc.)
        EXPECTED: 
        """
        pass

    def test_004_unlock_device(self):
        """
        DESCRIPTION: Unlock device
        EXPECTED: * Page content is reloaded
        EXPECTED: * Changes are shown on front end
        """
        pass

    def test_005_loose_internet_for_more_than_1_minute(self):
        """
        DESCRIPTION: Loose internet for more than 1 minute
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps #3-4
        EXPECTED: 
        """
        pass

    def test_007_lock_device_for_less_than_1_minute(self):
        """
        DESCRIPTION: Lock device for less than 1 minute
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps #3-4
        EXPECTED: * Page content is NOT reloaded
        EXPECTED: * Changes are NOT shown on front end
        """
        pass

    def test_009_loose_internet_for_less_than_1_minute(self):
        """
        DESCRIPTION: Loose internet for less than 1 minute
        EXPECTED: 
        """
        pass

    def test_010_repeat_step_8(self):
        """
        DESCRIPTION: Repeat step #8
        EXPECTED: 
        """
        pass
