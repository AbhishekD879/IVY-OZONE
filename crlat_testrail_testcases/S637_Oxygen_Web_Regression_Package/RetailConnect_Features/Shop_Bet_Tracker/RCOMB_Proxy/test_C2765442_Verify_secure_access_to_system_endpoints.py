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
class Test_C2765442_Verify_secure_access_to_system_endpoints(Common):
    """
    TR_ID: C2765442
    NAME: Verify secure access to system endpoints
    DESCRIPTION: This test case verify that only authorized users have access to system endpoints
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: HMN-3227 Proxy: Secure access to system endpoints
    PRECONDITIONS: https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html
    PRECONDITIONS: Endpoints with 'Sensitive Default' = 'true' are available only with username/password
    PRECONDITIONS: For dev environment https://coral-retail-bpp-dev.symphony-solutions.eu/****:
    PRECONDITIONS: * security.user.name=manager
    PRECONDITIONS: * security.user.password=M@nager
    PRECONDITIONS: Other environments:
    PRECONDITIONS: * https://retail-bpp-tst2.coral.co.uk/****
    PRECONDITIONS: * https://retail-bpp-stg.coral.co.uk/****
    PRECONDITIONS: * https://retail-bpp.coral.co.uk/****
    PRECONDITIONS: **TIP:**
    PRECONDITIONS: **Before loading next endpoint close the browser and open it again so that CTA appears every time (in other case after valid credentials have been applied for one endpoint they won't be required while loading another endpoint) and make sure your browser doesn't remember the password**
    """
    keep_browser_open = True

    def test_001_load__httpscoral_retail_bpp_devsymphony_solutionseuautoconfigin_the_browser(self):
        """
        DESCRIPTION: Load  https://coral-retail-bpp-dev.symphony-solutions.eu/autoconfig
        DESCRIPTION: in the browser
        EXPECTED: * CTA requires entering of username and password
        EXPECTED: * After submitting correct credentials (from precondition) endpoints data are loaded
        """
        pass

    def test_002_load__httpscoral_retail_bpp_devsymphony_solutionseubeansin_the_browser(self):
        """
        DESCRIPTION: Load  https://coral-retail-bpp-dev.symphony-solutions.eu/beans
        DESCRIPTION: in the browser
        EXPECTED: * CTA requires entering of username and password
        EXPECTED: * After submitting correct credentials (from precondition) endpoints data are loaded
        """
        pass

    def test_003_repeat_previous_step_for_following_endpoints_httpscoral_retail_bpp_devsymphony_solutionseuconfigprops_httpscoral_retail_bpp_devsymphony_solutionseudump_httpscoral_retail_bpp_devsymphony_solutionseuenv_httpscoral_retail_bpp_devsymphony_solutionseumetrics_httpscoral_retail_bpp_devsymphony_solutionseumappings_httpscoral_retail_bpp_devsymphony_solutionseutrace(self):
        """
        DESCRIPTION: Repeat previous step for following endpoints:
        DESCRIPTION: * https://coral-retail-bpp-dev.symphony-solutions.eu/configprops
        DESCRIPTION: * https://coral-retail-bpp-dev.symphony-solutions.eu/dump
        DESCRIPTION: * https://coral-retail-bpp-dev.symphony-solutions.eu/env
        DESCRIPTION: * https://coral-retail-bpp-dev.symphony-solutions.eu/metrics
        DESCRIPTION: * https://coral-retail-bpp-dev.symphony-solutions.eu/mappings
        DESCRIPTION: * https://coral-retail-bpp-dev.symphony-solutions.eu/trace
        EXPECTED: * CTA requires entering of username and password
        EXPECTED: * After submitting correct credentials (from precondition) endpoints data are loaded
        """
        pass

    def test_004_repeat_previous_step_for_following_endpoints_httpscoral_retail_bpp_devsymphony_solutionseuhealth_httpscoral_retail_bpp_devsymphony_solutionseuinfo(self):
        """
        DESCRIPTION: Repeat previous step for following endpoints:
        DESCRIPTION: * https://coral-retail-bpp-dev.symphony-solutions.eu/health
        DESCRIPTION: * https://coral-retail-bpp-dev.symphony-solutions.eu/info
        EXPECTED: *  Endpoints data are loaded successfully, entering credentials is not required
        """
        pass
