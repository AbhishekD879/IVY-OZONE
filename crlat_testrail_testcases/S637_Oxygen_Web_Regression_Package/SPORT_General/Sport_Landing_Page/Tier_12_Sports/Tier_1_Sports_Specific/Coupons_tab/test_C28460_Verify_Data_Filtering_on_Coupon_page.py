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
class Test_C28460_Verify_Data_Filtering_on_Coupon_page(Common):
    """
    TR_ID: C28460
    NAME: Verify Data Filtering on Coupon page
    DESCRIPTION: 
    PRECONDITIONS: 1. In order to get a list with **Coupon IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: 2. For each Coupon retrieve a list of **Events and Outcomes**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?translationLang=LL
    PRECONDITIONS: *   XXX is the **Coupon **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing Page
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_clicktap_coupons_tab(self):
        """
        DESCRIPTION: Click/Tap 'Coupons' tab
        EXPECTED: 'Coupons' tab is opened
        """
        pass

    def test_004_verify_list_of_present_coupons_on_the_tab(self):
        """
        DESCRIPTION: Verify list of present Coupons on the tab
        EXPECTED: All associated coupons for the category of <Sport> <categoryId ="XX"> or <'classSortCode="YY"'> are shown
        EXPECTED: where YY - SortCode for particular Sport e.g. Football "FB"
        """
        pass

    def test_005_verify_list_of_present_events_within_coupons(self):
        """
        DESCRIPTION: Verify list of present events within Coupons
        EXPECTED: *   Events within selected coupon type are present
        EXPECTED: *   Events with attributes: **rawIsOffCode="-" isStarted="true" **OR **rawIsOffCode="Y"**  are not shown
        """
        pass

    def test_006_verify_event_start_datetime(self):
        """
        DESCRIPTION: Verify event start date/time
        EXPECTED: *   It is displayed below the event name
        EXPECTED: *   Event start date corresponds to '**startTime**' attribute
        EXPECTED: *   Today's events are displayed with only time ( e.g '9:45 PM') and following events are displayed with date and time ( e.g. '26 Oct 9:45 PM'). **12 hours AM/PM'** format
        """
        pass
