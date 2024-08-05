import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C601103_Verify_connection_time_to_3rd_party_domains(Common):
    """
    TR_ID: C601103
    NAME: Verify connection time to 3rd party domains
    DESCRIPTION: This test case verifies connection time to 3rd party domains
    PRECONDITIONS: 1. All cookies and cache are cleared
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 1) For performance verification use Dareboost.com resource. (There is no possibility to check performance for Local env i.e. https://inplay-invictus.coral.co.uk/#/ due to limited access, please use at least https://invictus.coral.co.uk/#/).
    PRECONDITIONS: 2) Check list of available domains within the <head></head> tags using Dev Tools->Elements.
    PRECONDITIONS: List of available domains:
    PRECONDITIONS: * bp.coral.co.uk
    PRECONDITIONS: * www.googletagmanager.com
    PRECONDITIONS: * cdn.evergage.com
    PRECONDITIONS: * connect.facebook.net
    PRECONDITIONS: * www.facebook.com
    PRECONDITIONS: * galainteractive.evergage.com
    PRECONDITIONS: * bam.nr-data.net
    PRECONDITIONS: * js-agent.newrelic.com
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 1) For bp.coral.co.uk then the URL should change per environment e.g bp-tst2.coral.co.uk, bp.stg2.coral.co.uk, etc.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Home page is loaded
        """
        pass

    def test_002_open_dev_tools_and_go_to_network_all(self):
        """
        DESCRIPTION: Open Dev Tools and go to Network->All
        EXPECTED: * Dev Tools is opened
        EXPECTED: * List of responses, domains, etc. are displayed
        """
        pass

    def test_003_select_necessary_domain_ie_googeltagmanagercom_and_choose_timing_tab(self):
        """
        DESCRIPTION: Select necessary domain i.e. <googeltagmanager.com> and choose 'Timing' tab
        EXPECTED: The waterfall graphs are available
        """
        pass

    def test_004_check_dns_lookup_time(self):
        """
        DESCRIPTION: Check 'DNS Lookup' time
        EXPECTED: 'DNS Lookup' time has some value
        """
        pass

    def test_005_check_initial_connection_time(self):
        """
        DESCRIPTION: Check 'Initial connection' time
        EXPECTED: 'Initial connection' time has some value
        """
        pass

    def test_006_repeat_steps_3_5_for_bpcoralcouk_domain(self):
        """
        DESCRIPTION: Repeat steps 3-5 for <bp.coral.co.uk> domain
        EXPECTED: * 'DNS Lookup' time has some value
        EXPECTED: * 'Initial connection' time has some value
        """
        pass

    def test_007_repeat_steps_3_5_for_the_following_domains_cdnevergagecom_galainteractiveevergagecom_bamnr_datanet_js_agentnewreliccom(self):
        """
        DESCRIPTION: Repeat steps 3-5 for the following domains:
        DESCRIPTION: * cdn.evergage.com
        DESCRIPTION: * galainteractive.evergage.com
        DESCRIPTION: * bam.nr-data.net
        DESCRIPTION: * js-agent.newrelic.com
        EXPECTED: * 'DNS Lookup' time is 0ms
        EXPECTED: * 'Initial connection' time is 0ms
        """
        pass

    def test_008_refresh_the_page_and_repeat_steps_3_5_for_googeltagmanagercom_domain(self):
        """
        DESCRIPTION: Refresh the page and repeat steps 3-5 for <googeltagmanager.com> domain
        EXPECTED: * 'DNS Lookup' time has some value
        EXPECTED: * 'Initial connection' time has some value
        """
        pass

    def test_009_refresh_the_page_and_repeat_steps_3_5_for_the_following_domains_bpcoralcouk_cdnevergagecom_galainteractiveevergagecom_bamnr_datanet_js_agentnewreliccom(self):
        """
        DESCRIPTION: Refresh the page and repeat steps 3-5 for the following domains:
        DESCRIPTION: * bp.coral.co.uk
        DESCRIPTION: * cdn.evergage.com
        DESCRIPTION: * galainteractive.evergage.com
        DESCRIPTION: * bam.nr-data.net
        DESCRIPTION: * js-agent.newrelic.com
        EXPECTED: * 'DNS Lookup' time is 0ms
        EXPECTED: * 'Initial connection' time is 0ms
        """
        pass
