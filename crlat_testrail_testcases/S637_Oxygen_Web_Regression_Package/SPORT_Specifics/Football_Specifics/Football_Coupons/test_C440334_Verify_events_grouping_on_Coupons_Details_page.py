import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C440334_Verify_events_grouping_on_Coupons_Details_page(Common):
    """
    TR_ID: C440334
    NAME: Verify events grouping on Coupons Details page
    DESCRIPTION: This test case verifies events grouping on Coupons Details page
    PRECONDITIONS: 1) In order to get a list of coupons use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon?existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:2017-07-04T21:00:00.000Z&existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:2017-07-05T13:09:30.000Z&existsFilter=coupon:simpleFilter:event.isStarted:isFalse&simpleFilter=coupon.siteChannels:contains:M&existsFilter=coupon:simpleFilter:event.categoryId:intersects:16&existsFilter=coupon:simpleFilter:event.cashoutAvail:equals:Y&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to get an information about particular coupon use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?simpleFilter=event.startTime:lessThan:2017-07-15T09:01:00.000Z&simpleFilter=event.categoryId:intersects:16&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.startTime:greaterThanOrEqual:2017-07-09T21:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2017-07-10T09:01:00.000Z&translationLang=en
    PRECONDITIONS: XXX - coupon's id
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
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
        EXPECTED: * List of coupons is displayed on the Coupons Landing page
        """
        pass

    def test_003_navigate_to_uk_coupon(self):
        """
        DESCRIPTION: Navigate to UK Coupon
        EXPECTED: * Events for selected coupon are displayed on Coupons Details page
        """
        pass

    def test_004_verify_events_displaying(self):
        """
        DESCRIPTION: Verify events displaying
        EXPECTED: * Events are grouped  by **classId** and **typeId**
        EXPECTED: * All Events within accordion are displayed for the next 5 days
        EXPECTED: * Today's events are displayed with time start ( e.g '19:45, Today')
        EXPECTED: * Tomorrow's events are displayed with  time start ( e.g '10:45, 26 Oct')
        EXPECTED: * Future events are displayed with date and time starting ( e.g. '9:45, 29 Oct')
        EXPECTED: * If no events to show, the message **No events found** is displayed
        """
        pass

    def test_005_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * List of coupons is displayed
        """
        pass
