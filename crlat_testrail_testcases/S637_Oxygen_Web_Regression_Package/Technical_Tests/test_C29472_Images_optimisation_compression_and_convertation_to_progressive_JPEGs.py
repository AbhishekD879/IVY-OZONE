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
class Test_C29472_Images_optimisation_compression_and_convertation_to_progressive_JPEGs(Common):
    """
    TR_ID: C29472
    NAME: Images optimisation, compression and convertation to progressive JPEGs
    DESCRIPTION: This test case verifies Images optimisation, compression and convertation to progressive JPEGs
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-10596 Some JPEG banner images are still not optimised, compressed and converted to Progressive JPEG’s
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_openhttpswwwwebpagetestorg_and_enter_application_url_on_the_homepage(self):
        """
        DESCRIPTION: Open https://www.webpagetest.org/ and enter application URL on the Homepage
        EXPECTED: 
        """
        pass

    def test_002_perform_testing_and_check_results___performance_review(self):
        """
        DESCRIPTION: Perform testing and check Results -> Performance review
        EXPECTED: *   Compresse Images = 100/100
        EXPECTED: *   Use Progressive JPEGs = 100/100
        """
        pass
