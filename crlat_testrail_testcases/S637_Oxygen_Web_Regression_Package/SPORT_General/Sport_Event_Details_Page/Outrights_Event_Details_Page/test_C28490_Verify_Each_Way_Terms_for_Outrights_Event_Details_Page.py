import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28490_Verify_Each_Way_Terms_for_Outrights_Event_Details_Page(Common):
    """
    TR_ID: C28490
    NAME: Verify Each Way Terms for 'Outrights' Event Details Page
    DESCRIPTION: This test case verifies market terms for 'Outrights' event details page
    PRECONDITIONS: Outright event has market with Each Way terms available:
    PRECONDITIONS: attribute **'isEachWayAvailable'**='true' is present on the market level
    """
    keep_browser_open = True

    def test_001_open_outright_details_page(self):
        """
        DESCRIPTION: Open Outright Details page
        EXPECTED: Outright Details page is opened
        """
        pass

    def test_002_verify_market_with_each_way_terms_available(self):
        """
        DESCRIPTION: Verify market with Each Way terms available
        EXPECTED: Each Way Terms are displayed at the top of market section
        """
        pass

    def test_003_verify_terms_correctness(self):
        """
        DESCRIPTION: Verify terms correctness
        EXPECTED: Terms attributes correspond to the **'eachWayFactorNum'**, **'eachWayFactorDen'** and** 'eachWayPlaces'** attributes from the Site Server
        """
        pass

    def test_004_check_terms_format(self):
        """
        DESCRIPTION: Check terms format
        EXPECTED: Terms are displayed in the following format:
        EXPECTED: ***" Each Way: x/y odds - Places z,j,k"***
        EXPECTED: where:
        EXPECTED: x = eachWayFactorNum
        EXPECTED: y= eachWayFactorDen
        EXPECTED: z,j,k = eachWayPlaces
        """
        pass

    def test_005_verify_outright_event_with_market_whichdoesnthave_terms_availableattributeiseachwayavailabletrue_is_absent_on_site_server(self):
        """
        DESCRIPTION: Verify Outright event with market which doesn't have terms available:
        DESCRIPTION: Attribute** 'isEachWayAvailable'**='true' is absent on Site Server
        EXPECTED: Terms are not displayed for this market
        """
        pass
