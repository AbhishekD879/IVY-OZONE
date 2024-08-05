import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C25088267_Verify_that_Show_More_CTA_is_not_shown_when_number_of_selections_is_less_than_specified_in_CMS(Common):
    """
    TR_ID: C25088267
    NAME: Verify that Show More CTA is not shown when number of selections is less than specified in CMS
    DESCRIPTION: This test case verifies that 'Show More' CTA is not shown if the number of selections available in the Outrights market is less than the number specified in CMS
    PRECONDITIONS: * The app is installed and launched
    PRECONDITIONS: * Outrights market is created in CMS as featured module
    PRECONDITIONS: * The number of selections to be expanded is specified in CMS
    PRECONDITIONS: * Outright market has fewer selections configured than the number of selections specified in CMS
    """
    keep_browser_open = True

    def test_001__open_homepage_swipe_down_the_outrights_market(self):
        """
        DESCRIPTION: * Open Homepage
        DESCRIPTION: * Swipe down the Outrights market
        EXPECTED: * 'Show More' CTA is not shown as the number of selections is less than the number specified in CMS
        """
        pass
