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
class Test_C2377243_Verify_Shop_Exclusive_tab_view_and_content(Common):
    """
    TR_ID: C2377243
    NAME: Verify 'Shop Exclusive' tab view and content
    DESCRIPTION: This test case verifies view of 'Connect Exclusive' tab
    PRECONDITIONS: Make sure In-Shop Promotions feature is turned on in CMS: System configuration -> Connect -> promotions
    PRECONDITIONS: A user is logged in
    PRECONDITIONS: CMS: https://CMS_ENDPOINT/keystone/ -> Pick 'sportsbook' brand from the drop-down -> 'Promotions'  :
    PRECONDITIONS: Active promotions are created with current validity period and Category equal 'Connect Promotions'
    """
    keep_browser_open = True

    def test_001_header_ribbon_menu___promotions___shop_exclusive_tab(self):
        """
        DESCRIPTION: Header ribbon menu -> Promotions -> 'Shop Exclusive' tab
        EXPECTED: Tab contains:
        EXPECTED: * List of promotions with category 'Connect Promotions'
        """
        pass

    def test_002_verify_the_list_of_benefits(self):
        """
        DESCRIPTION: Verify the list of benefits
        EXPECTED: * Only benefits with the category 'Connect Promotions' (set in CMS) are displayed
        EXPECTED: * Benefits are sorted accordingly to sort order in CMS
        EXPECTED: * Only banners with current validity time and category equal to 'Connect Promotions' are displayed
        """
        pass
