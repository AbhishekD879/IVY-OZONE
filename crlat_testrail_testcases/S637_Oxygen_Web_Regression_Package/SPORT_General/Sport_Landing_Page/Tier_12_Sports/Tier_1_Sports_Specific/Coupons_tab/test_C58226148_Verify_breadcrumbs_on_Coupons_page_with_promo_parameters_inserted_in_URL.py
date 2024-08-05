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
class Test_C58226148_Verify_breadcrumbs_on_Coupons_page_with_promo_parameters_inserted_in_URL(Common):
    """
    TR_ID: C58226148
    NAME: Verify breadcrumbs on Coupons page with promo parameters inserted in URL
    DESCRIPTION: This test case verifies breadcrumbs on Coupons page with additional promo parameters inserted in URL
    PRECONDITIONS: Prod incident related: https://jira.egalacoral.com/browse/BMA-49477
    PRECONDITIONS: - User is on Football landing page
    PRECONDITIONS: - Additional promo parameters to be used for coupons: '/coupons?utm=coupon_campaign&vip=true'
    """
    keep_browser_open = True

    def test_001_navigate_to_coupons_page(self):
        """
        DESCRIPTION: Navigate to Coupons page
        EXPECTED: Coupons page is loaded
        """
        pass

    def test_002_insert_into_page_url_the_campaign_promo_parameter_from_preconditions_press_enter(self):
        """
        DESCRIPTION: Insert into page url the campaign promo parameter from preconditions, press enter
        EXPECTED: Page is refreshed with the updated url
        """
        pass

    def test_003_check_the_breadcrumbs_on_coupons_page(self):
        """
        DESCRIPTION: Check the breadcrumbs on Coupons page
        EXPECTED: Breadcrumbs look like 'Home->Football->Coupons'
        EXPECTED: ![](index.php?/attachments/get/101256740)
        EXPECTED: ![](index.php?/attachments/get/101256741)
        """
        pass

    def test_004_navigate_to_other_pages_across_the_app_and_check_all_other_breadcrumbs_look_not_affected(self):
        """
        DESCRIPTION: Navigate to other pages across the app and check all other breadcrumbs look not affected
        EXPECTED: All breadcrumbs are not affected
        """
        pass
