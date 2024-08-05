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
class Test_C2380385_Verify_Shop_Exclusive_promotions_details(Common):
    """
    TR_ID: C2380385
    NAME: Verify 'Shop Exclusive' promotions details
    DESCRIPTION: This test case verifies 'Connect Exclusive' tab details
    PRECONDITIONS: Make sure In-Shop Promotions feature is turned on in CMS: System configuration -> Connect -> promotions
    PRECONDITIONS: CMS:
    PRECONDITIONS: https://CMS_ENDPOINT/keystone/ -> Pick 'sportsbook' brand from the drop-down -> 'Promotions'  :
    PRECONDITIONS: Active promotions are created with current validity period and Category equal 'Connect promotions'
    PRECONDITIONS: 'Shop Exclusive' tab should be opened (Header ribbon menu -> Promotions -> 'Shop Exclusive' tab)
    """
    keep_browser_open = True

    def test_001_verify_promotion_view(self):
        """
        DESCRIPTION: Verify promotion view
        EXPECTED: List of CMS configurable promotion content:
        EXPECTED: * Banner
        EXPECTED: * Promotion title (White text on a blue area)
        EXPECTED: * Short Description (Grey text on a grey area)
        EXPECTED: * green 'More info' button on a grey area
        """
        pass

    def test_002_tapclick_more_info_button_on_any_promotion(self):
        """
        DESCRIPTION: Tap/Click 'More info' button on any promotion
        EXPECTED: Promotion page is opened
        """
        pass

    def test_003_verify_the_promotion_details_page(self):
        """
        DESCRIPTION: Verify the promotion details page
        EXPECTED: * Promotion title
        EXPECTED: * Banner (according to CMS configuration)
        EXPECTED: * Description (according to CMS configuration)
        EXPECTED: * 'T&C's' section (according to CMS configuration)
        """
        pass
