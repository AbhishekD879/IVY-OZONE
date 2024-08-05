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
class Test_C2605913_Verify_Correct_Score_Coupon_live_updating(Common):
    """
    TR_ID: C2605913
    NAME: Verify Correct Score Coupon live updating
    DESCRIPTION: 
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 1. Coupon contains ONLY Correct Score markets
    PRECONDITIONS: 2. Coupon is added to Football > Coupons / ACCAS > Some particular section.
    PRECONDITIONS: 3. Correct Score Coupon is opened
    """
    keep_browser_open = True

    def test_001_using_the_ob_remove_some_event_from_the_couponrefresh_the_correct_score_coupon_detailsverify_event_disappears_in_the_coupon_page(self):
        """
        DESCRIPTION: Using the OB remove some Event from the coupon
        DESCRIPTION: Refresh the Correct Score coupon details.
        DESCRIPTION: Verify event disappears in the Coupon page.
        EXPECTED: Event disappears from the list of events after page refresh
        """
        pass

    def test_002_finishresult_the_event_from_the_correct_score_couponrefresh_the_correct_score_coupon_detailsverify_events_displaying_in_the_coupon_details_page(self):
        """
        DESCRIPTION: Finish/result the event from the Correct score coupon.
        DESCRIPTION: Refresh the Correct Score coupon details.
        DESCRIPTION: Verify event's displaying in the Coupon details page
        EXPECTED: * [displayed:"N"] or [isresulted:"Y"] attributes are received in LIVE SERV push/WS
        EXPECTED: * Event disappears on front end
        """
        pass

    def test_003_using_the_ob_suspend_some_event_from_the_coupon(self):
        """
        DESCRIPTION: Using the OB suspend some Event from the coupon
        EXPECTED: * Event remains in the list
        EXPECTED: * Score switchers disappear
        EXPECTED: * Price button get disabled
        """
        pass

    def test_004_using_the_ob_add_some_event_to_the_couponrefresh_the_correct_score_coupon_detailsverify_event_appears_in_the_coupon_page(self):
        """
        DESCRIPTION: Using the OB add some Event to the coupon.
        DESCRIPTION: Refresh the Correct Score coupon details.
        DESCRIPTION: Verify event appears in the Coupon page.
        EXPECTED: Event appears within the list after page refresh
        """
        pass

    def test_005_change_the_selection_price_in_ob_check_if_the_price_gets_changed_in_the_application_increase_price_decrease_price(self):
        """
        DESCRIPTION: Change the selection price in OB, check if the price gets changed in the application
        DESCRIPTION: * Increase price
        DESCRIPTION: * Decrease price
        EXPECTED: * Price gets changed
        EXPECTED: * Price button colour is changed appropriately
        """
        pass
