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
class Test_C489765_Verify_Change_coupon_Selector_functionality(Common):
    """
    TR_ID: C489765
    NAME: Verify 'Change coupon' Selector functionality
    DESCRIPTION: This test case verifies  'Change coupon' Selector functionality for Coral: Desktop and Mobile, **for Ladbrokes:** Desktop only.
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

    def test_001_load_oxygen_application_and_go_to_football___coupons_landing_page(self):
        """
        DESCRIPTION: Load Oxygen application and go to Football -> Coupons landing page
        EXPECTED: List of all available coupons is displayed on the page
        """
        pass

    def test_002_select_coupon_from_the_list_and_tap_its_name(self):
        """
        DESCRIPTION: Select coupon from the list and tap its name
        EXPECTED: Selected Coupon details page is opened
        """
        pass

    def test_003_verify__change_coupon_selector_displaying_in_the_coupons_details_page(self):
        """
        DESCRIPTION: Verify  'Change coupon' Selector displaying in the Coupon's Details page
        EXPECTED: 'Change coupon' Selector is displayed at the right side of Coupons sub-header
        """
        pass

    def test_004_tap_change_coupon_selector_link_and_verify_selector_content_and_animation(self):
        """
        DESCRIPTION: Tap 'Change coupon' Selector link and verify selector content and animation
        EXPECTED: * List of all available coupons received in response from OB is displayed
        EXPECTED: * the coupon list drop overlay cascades down the page
        EXPECTED: * white background must be visible hiding the content of the background page
        """
        pass

    def test_005_select_coupon_from_the_coupon_selector_and_tap_it(self):
        """
        DESCRIPTION: Select Coupon from the Coupon Selector and tap it
        EXPECTED: * Coupon Selector is automatically closed
        EXPECTED: * List of events for selected coupon is displayed for the chosen Coupon
        EXPECTED: * Selected coupon name is displayed in the sub header
        """
        pass

    def test_006_repeat_step_5_for_all_available_in_the_selector_coupons(self):
        """
        DESCRIPTION: Repeat step 5 for all available in the Selector Coupons
        EXPECTED: 
        """
        pass
