import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726259_Event_Hub_Verify_Modules_Publish_Timing(Common):
    """
    TR_ID: C9726259
    NAME: Event Hub: Verify Modules Publish Timing
    DESCRIPTION: This test case verifies Modules Publish Timing on Event Hub tab.
    PRECONDITIONS: 1) At least 1 Event Hub is created in CMS
    PRECONDITIONS: 2)
    PRECONDITIONS: *   Publish Timing corresponds to values set in 'Visible from', 'Visible to' fields in CMS
    PRECONDITIONS: ('displayFrom', 'displayTo' attributes)
    PRECONDITIONS: *   It is possible to set time and dates manually or with buttons 'Today' (set current day's date) and 'Tomorrow' (set the next day's date)
    PRECONDITIONS: 3) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_setvisible_from_visible_to_fields_in_cms_for_verified_module_from_the_past(self):
        """
        DESCRIPTION: Set 'Visible from', 'Visible to' fields in CMS  for verified Module from the Past
        EXPECTED: Verified Module is not shown on the Event Hub tab
        """
        pass

    def test_002_setvisible_from_visible_to_fields_in_cms_for_verified_module_from_the_future(self):
        """
        DESCRIPTION: Set 'Visible from', 'Visible to' fields in CMS  for verified Module from the Future
        EXPECTED: Verified Module is not shown on the Event Hub tab
        """
        pass

    def test_003_setvisible_from_visible_to_fields_in_cms_for_verified_module_with_current_day_within_this_time_interval(self):
        """
        DESCRIPTION: Set 'Visible from', 'Visible to' fields in CMS  for verified Module with **current day** within this time interval
        EXPECTED: Verified Module is shown on the Event Hub tab
        """
        pass

    def test_004_set_visible_from_in_x_minutes_from_now_and_verify_it_on_front_end(self):
        """
        DESCRIPTION: Set 'Visible from' in x minutes from now and verify it on front end
        EXPECTED: Module will appear on front end in x minutes
        """
        pass

    def test_005_set_visible_from_in_the_past_visible_to_x_minutes_in_future_and_verify_it_on_front_end(self):
        """
        DESCRIPTION: Set 'Visible from' in the past, 'Visible to' x minutes in future and verify it on front end
        EXPECTED: Module will disappear from front end in x minutes
        """
        pass
