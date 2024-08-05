import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C9701552_Verify_Surface_Bet_module_ordering_among_other_modules(Common):
    """
    TR_ID: C9701552
    NAME: Verify Surface Bet module ordering among other modules
    DESCRIPTION: Test case verifies possibility to order Surface Bet module among other modules
    PRECONDITIONS: 1. There is at least one Surface Bet added to the SLP/Homepage in CMS.
    PRECONDITIONS: 2. There are other modules active and configured in CMS for this homepage/SLP
    PRECONDITIONS: 3. Open this SLP/Homepage in Oxygen application.
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_verify_the_order_of_the_surface_bet_module_is_as_per_order_in_the_cms(self):
        """
        DESCRIPTION: Verify the order of the Surface Bet module is as per order in the CMS
        EXPECTED: The order is as defined in CMS
        """
        pass

    def test_002_change_the_order_in_the_cmsin_the_application_refresh_the_page_and_verify_the_order_is_updated(self):
        """
        DESCRIPTION: Change the order in the CMS.
        DESCRIPTION: In the application refresh the page and verify the order is updated
        EXPECTED: The order is updated and is as defined in the CMS
        """
        pass
