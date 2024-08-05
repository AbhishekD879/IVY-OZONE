import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28241_CMS_Control_for_Hourly_Alerts(Common):
    """
    TR_ID: C28241
    NAME: CMS Control for Hourly Alerts
    DESCRIPTION: This test case verifies Hourly alerts displaying depending on appropriate CMS setting value
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: BMA-6871 LCCP Improvements: Current Hourly Notification - CMS Control
    PRECONDITIONS: 1.  User should be logged in
    PRECONDITIONS: 2.  User Session limit should be Not defined
    PRECONDITIONS: 3.  CMS: https://CMS\_ENDPOINT/keystone/ (check CMS\_ENDPOINT via devlog function)
    """
    keep_browser_open = True

    def test_001_go_to_cms___system_configuration_section___lccp_section(self):
        """
        DESCRIPTION: Go to CMS -> System Configuration section -> 'LCCP' section
        EXPECTED: 1.* 'Display Hourly Alerts' (*hourlyAlerts*)* option is added
        EXPECTED: 2. It is possible to enable/disable option
        """
        pass

    def test_002_enable_display_hourly_alerts_optionload_application_and_verifyhourly_alert_displaying_after_60_min_will_be_elapsed(self):
        """
        DESCRIPTION: Enable '*Display Hourly Alerts*' option
        DESCRIPTION: Load application and verify Hourly Alert displaying after 60 min will be elapsed
        EXPECTED: Hourly Alert is displayed after 60 min elapsed
        """
        pass

    def test_003_disable_display_hourly_alerts_optionload_application_and_verifyhourly_alert_displaying_after_60_min_will_be_elapsed(self):
        """
        DESCRIPTION: Disable '*Display Hourly Alerts*' option.
        DESCRIPTION: Load application and verify Hourly Alert displaying after 60 min will be elapsed
        EXPECTED: Hourly Alert is NOT displayed after 60 min elapsed
        """
        pass
