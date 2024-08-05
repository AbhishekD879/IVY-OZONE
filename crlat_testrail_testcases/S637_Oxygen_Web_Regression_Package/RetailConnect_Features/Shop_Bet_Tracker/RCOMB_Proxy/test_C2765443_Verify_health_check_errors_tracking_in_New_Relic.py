import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2765443_Verify_health_check_errors_tracking_in_New_Relic(Common):
    """
    TR_ID: C2765443
    NAME: Verify health-check errors tracking in New Relic
    DESCRIPTION: This test case verify health-check errors tracking in New Relic
    DESCRIPTION: JIRA ticket:
    DESCRIPTION: HMN-3192 Add health-check errors to newrelic for rcomb proxy app
    PRECONDITIONS: Find New Relic  credentials here: https://confluence.egalacoral.com/display/SPI/Environments+for+managing+test+data
    PRECONDITIONS: Direct link to Error analytics (for dev app):
    PRECONDITIONS: https://rpm.newrelic.com/accounts/1641266/applications/58225161/filterable_errors#/table?top_facet=transactionUiName&primary_facet=error.class&barchart=barchart&filters=%5B%7B%22key%22%3A%22error.class%22%2C%22value%22%3A%22HealthCheckError-betTracker%22%2C%22like%22%3Afalse%7D%5D&_k=1vn0q3
    PRECONDITIONS: Assistance of developer could be required to make some server down so corresponding error will appear in 'Error analytics'
    """
    keep_browser_open = True

    def test_001_load_new_relic___application___cr_spt_rbpp_mbfe_dev0___events___error_analytics(self):
        """
        DESCRIPTION: Load New relic -> Application -> CR-SPT-RBPP-MBFE-DEV0 -> Events -> Error analytics
        EXPECTED: Error analytics is opened
        """
        pass

    def test_002_make_one_of_externals_servers_down_e_g_auditlog(self):
        """
        DESCRIPTION: Make one of externals servers down (e. g.: AuditLog)
        EXPECTED: * HealthCheckError-AuditLog error appears in 'Error traces' table
        EXPECTED: (errors checking is occurring every 40 sec)
        """
        pass

    def test_003_make_another_externals_servers_down(self):
        """
        DESCRIPTION: Make another externals servers down
        EXPECTED: * HealthCheckError-ServiceName error appears in 'Error traces' table
        EXPECTED: (errors checking is occurring every 40 sec)
        """
        pass
