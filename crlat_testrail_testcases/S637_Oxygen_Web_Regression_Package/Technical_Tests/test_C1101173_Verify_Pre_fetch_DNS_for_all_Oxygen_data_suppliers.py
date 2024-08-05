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
class Test_C1101173_Verify_Pre_fetch_DNS_for_all_Oxygen_data_suppliers(Common):
    """
    TR_ID: C1101173
    NAME: Verify Pre-fetch DNS for all Oxygen data suppliers
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_open_developer_tools___elements(self):
        """
        DESCRIPTION: Open Developer tools -> Elements
        EXPECTED: 
        """
        pass

    def test_003_expand_head(self):
        """
        DESCRIPTION: Expand <head>
        EXPECTED: 
        """
        pass

    def test_004_verify_pre_fetch_dns_for_all_oxygen_data_suppliers(self):
        """
        DESCRIPTION: Verify Pre-fetch DNS for all Oxygen data suppliers
        EXPECTED: The following data suppliers are listed:
        EXPECTED: https://img.coral.co.uk
        EXPECTED: https://backoffice-tst2.coral.co.uk
        EXPECTED: https://bp-tst2.coral.co.uk
        EXPECTED: https://www.googletagmanager.com
        EXPECTED: https://connect.facebook.net
        EXPECTED: https://www.facebook.com
        EXPECTED: https://bam.nr-data.net
        EXPECTED: https://js-agent.newrelic.com
        EXPECTED: https://static.goqubit.com
        EXPECTED: https://www.google-analytics.com
        EXPECTED: https://ec2-35-177-34-113.eu-west-2.compute.amazonaws.com
        EXPECTED: https://banners-cms-assets.coral.co.uk
        EXPECTED: https://spark-br-stg2.symphony-solutions.eu/api
        """
        pass
