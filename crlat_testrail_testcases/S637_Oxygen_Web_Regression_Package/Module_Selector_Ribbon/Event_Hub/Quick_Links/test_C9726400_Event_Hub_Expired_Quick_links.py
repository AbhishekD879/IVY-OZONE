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
class Test_C9726400_Event_Hub_Expired_Quick_links(Common):
    """
    TR_ID: C9726400
    NAME: Event Hub: Expired Quick links
    DESCRIPTION: This test case verifies expiration of Quick links on Event Hub
    PRECONDITIONS: 1. Go to CMS -> Sport Pages->Event Hub -> Quick Links and configure a Quick link for Event Hub with Validity period End Date=current time +10 minutes. - (<Quick Link1>)
    PRECONDITIONS: 2. There should be no other active Quick links for Event Hub expect <Quick Link1>.
    PRECONDITIONS: 3. Go to Oxygen app and navigate to Event hub tab.
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True

    def test_001_verify_displaying_if_configured_quick_link_is_not_displayed_on_event_hub_tab(self):
        """
        DESCRIPTION: Verify displaying if configured Quick link is not displayed on Event Hub tab.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick link is displayed.
        """
        pass

    def test_002_go_to_cms__gt_sport_pages_gtevent_hub__gt_quick_links_and_create_the_second_active_quick_link_with_validity_period_end_datecurrent_time_plus20_minutes_ltquick_link2gt(self):
        """
        DESCRIPTION: Go to CMS -&gt; Sport Pages-&gt;Event Hub -&gt; Quick Links and create the second active Quick link with Validity period End Date=current time +20 minutes. (&lt;Quick Link2&gt;)
        EXPECTED: 
        """
        pass

    def test_003_go_to_oxygen_app_and_navigate_to_event_hub_tabverify_that_configured_quick_links_are_displayed_on_event_hub(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event Hub tab.
        DESCRIPTION: Verify that configured Quick links are displayed on Event Hub.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick Links are displayed.
        """
        pass

    def test_004_wait_forltquick_link1gt_to_get_expired_in_10_minutes(self):
        """
        DESCRIPTION: Wait for&lt;Quick Link1&gt; to get expired (in 10 minutes)
        EXPECTED: 
        """
        pass

    def test_005_go_to_oxygen_app_and_navigate_to_event_hub_tabverify_that_configured_ltquick_link1gt_is_not_displayed_on_event_hub(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event Hub tab.
        DESCRIPTION: Verify that configured &lt;Quick Link1&gt; is not displayed on Event hub.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * &lt;Quick Link1&gt; is not displayed.
        EXPECTED: * &lt;Quick Link2&gt; is displayed
        """
        pass

    def test_006_wait_for_ltquick_link2gt_to_get_expired_in_20_minutes(self):
        """
        DESCRIPTION: Wait for &lt;Quick Link2&gt; to get expired (in 20 minutes)
        EXPECTED: 
        """
        pass

    def test_007_go_to_oxygen_app_and_navigate_to_event_hub_tabverify_that_configured_ltquick_link2gt_is_not_displayed_on_event_hub(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event Hub tab.
        DESCRIPTION: Verify that configured &lt;Quick Link2&gt; is not displayed on Event Hub
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * No Quick links are displayed.
        """
        pass
