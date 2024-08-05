import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C440338_Verify_Coupons_Details_page(Common):
    """
    TR_ID: C440338
    NAME: Verify Coupons Details page
    DESCRIPTION: This test case verifies Coupons Details page
    PRECONDITIONS: 1) In order to get an information about particular coupon use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?simpleFilter=event.startTime:lessThan:2017-07-15T09:01:00.000Z&simpleFilter=event.categoryId:intersects:16&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.startTime:greaterThanOrEqual:2017-07-09T21:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2017-07-10T09:01:00.000Z&translationLang=en
    PRECONDITIONS: XXX - coupon's id
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: Load Oxygen application - Homepage is opened
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    """
    keep_browser_open = True

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        pass

    def test_002_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: * 'Coupons' tab is selected and highlighted
        EXPECTED: * Coupons Landing page is loaded
        """
        pass

    def test_003_navigate_to_coupon_details_page(self):
        """
        DESCRIPTION: Navigate to Coupon Details page
        EXPECTED: Coupon Details page is loaded
        """
        pass

    def test_004_verify_url_when_navigating_to_coupon_details_page(self):
        """
        DESCRIPTION: Verify URL when navigating to Coupon Details page
        EXPECTED: https://{websitename}.coral.co.uk/coupons/football/couponname/id is displayed in URL for selected coupon
        EXPECTED: https://{websitename}.ladbrokes.com/coupons/football/couponname/id
        """
        pass

    def test_005_verify_coupons_header(self):
        """
        DESCRIPTION: Verify Coupons header
        EXPECTED: The following elements are present on Coupons header:
        EXPECTED: * 'Back' button
        EXPECTED: * 'Coupons' inscription
        EXPECTED: * 'Bet Filter' for Coral
        """
        pass

    def test_006_verify_coupons_sub_header(self):
        """
        DESCRIPTION: Verify Coupons sub-header
        EXPECTED: * Coupons sub-header is located below Coupons header
        EXPECTED: * "Name of selected coupon" is displayed at the left side of Coupons sub-header
        EXPECTED: * "Change Coupon" link and image is displayed at the right side of Coupons sub-header
        """
        pass

    def test_007_verify_coupons_market_selector_section(self):
        """
        DESCRIPTION: Verify Coupons Market selector section
        EXPECTED: * Coupons Market selector section is below Coupons sub-header
        EXPECTED: * "Name of selected market" is displayed at the left side
        EXPECTED: * "Change Market" label is displayed at the right side of Coupons Market selector section
        """
        pass

    def test_008_verify_coupons_page_content(self):
        """
        DESCRIPTION: Verify Coupons page content
        EXPECTED: * Events for appropriate coupon are displayed on Coupons Details page
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the accordions by tapping the accordion's header
        EXPECTED: * If no events to show, the message '**No events found**' is displayed
        """
        pass

    def test_009_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * List of coupons is displayed
        """
        pass

    def test_010_repeat_steps_4_10_for_another_one_coupon(self):
        """
        DESCRIPTION: Repeat steps 4-10 for another one coupon
        EXPECTED: 
        """
        pass
