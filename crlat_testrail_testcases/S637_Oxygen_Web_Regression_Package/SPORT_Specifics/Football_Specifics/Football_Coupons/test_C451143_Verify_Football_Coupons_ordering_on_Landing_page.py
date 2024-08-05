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
class Test_C451143_Verify_Football_Coupons_ordering_on_Landing_page(Common):
    """
    TR_ID: C451143
    NAME: Verify Football Coupons ordering on Landing page
    DESCRIPTION: This test case verifies Football Coupons ordering on Landing page
    PRECONDITIONS: **CMS Configuration:**
    PRECONDITIONS: Football Coupon ->Coupon Segments -> Create New Segment -> Featured coupon section
    PRECONDITIONS: NOTE:  **Popular coupon** section contains all the rest of available coupons EXCEPT coupons are present in *Featured section*
    PRECONDITIONS: 1) In order to get a list of coupons use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon?existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:2017-07-04T21:00:00.000Z&existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:2017-07-05T13:09:30.000Z&existsFilter=coupon:simpleFilter:event.isStarted:isFalse&simpleFilter=coupon.siteChannels:contains:M&existsFilter=coupon:simpleFilter:event.categoryId:intersects:16&existsFilter=coupon:simpleFilter:event.cashoutAvail:equals:Y&translationLang=en
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
        EXPECTED: * **Featured Coupons**(CMS configurable) and **Popular Coupons**(all the rest of available coupons) sections are shown on the Coupons Landing page
        EXPECTED: * List of coupons is displayed on the Coupons Landing page according to related section
        """
        pass

    def test_003_verify_coupons_order(self):
        """
        DESCRIPTION: Verify coupons order
        EXPECTED: **Featured Coupons** are ordered according to CMS config
        EXPECTED: **Popular Coupons** are ordered by **'displayOrder'** in ascending
        """
        pass
