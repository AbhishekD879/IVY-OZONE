import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2377307_Verify_Shop_Promotions_when_there_is_no_active_benefits(Common):
    """
    TR_ID: C2377307
    NAME: Verify Shop Promotions when there is no active benefits
    DESCRIPTION: This test case verifies Connect (Shop) Promotions tab without promotions.
    PRECONDITIONS: Make sure In-Shop Promotions feature is turned on in CMS: System configuration -> Connect -> promotions
    PRECONDITIONS: Proceed to CMS: https://CMS_ENDPOINT/keystone
    PRECONDITIONS: Make sure there are no active promotions with category 'Connect Promotion'
    """
    keep_browser_open = True

    def test_001_tap_promotions_item_on_sports_menu_ribbon___shop_exclusive_tab(self):
        """
        DESCRIPTION: Tap Promotions item on Sports Menu Ribbon -> 'Shop Exclusive' tab
        EXPECTED: 'Shop Exclusive' tab is opened
        """
        pass

    def test_002_verify_page_content(self):
        """
        DESCRIPTION: Verify page content
        EXPECTED: There are no active promotions.
        EXPECTED: Text 'No active Promotions at the moment' is displayed.
        """
        pass
