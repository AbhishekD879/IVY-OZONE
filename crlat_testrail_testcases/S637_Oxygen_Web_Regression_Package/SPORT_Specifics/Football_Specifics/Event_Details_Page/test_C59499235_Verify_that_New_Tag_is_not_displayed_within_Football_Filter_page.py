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
class Test_C59499235_Verify_that_New_Tag_is_not_displayed_within_Football_Filter_page(Common):
    """
    TR_ID: C59499235
    NAME: Verify that New Tag is not displayed within Football Filter page
    DESCRIPTION: Test case verify if "New" tag isn't displayed on Football Coupon/Accas page.
    DESCRIPTION: **NOTE:** Will be implemented for Ladbrokes after OX 108
    PRECONDITIONS: User is logged into Oxygen application.
    PRECONDITIONS: At least one coupon exist in application.
    """
    keep_browser_open = True

    def test_001_open_football_page_and_go_to_couponsaccas_tab_choose_any_of_existing_coupons(self):
        """
        DESCRIPTION: Open Football page and go to Coupons/Accas tab. Choose any of existing coupons.
        EXPECTED: Coupons detail page is displayed.
        """
        pass

    def test_002_verify_if_new_tag_isnt_displayed_next_to_any_of_coupons(self):
        """
        DESCRIPTION: Verify if "New" tag isn't displayed next to any of coupons
        EXPECTED: Tag "New" isn't displayed next to any of coupons
        """
        pass
