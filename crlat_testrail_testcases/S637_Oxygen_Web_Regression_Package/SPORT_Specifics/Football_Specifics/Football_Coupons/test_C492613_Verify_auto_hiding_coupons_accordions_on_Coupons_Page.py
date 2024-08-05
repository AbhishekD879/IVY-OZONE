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
class Test_C492613_Verify_auto_hiding_coupons_accordions_on_Coupons_Page(Common):
    """
    TR_ID: C492613
    NAME: Verify auto hiding coupons accordions on Coupons Page
    DESCRIPTION: This Test Case verified auto hiding coupons accordions on Coupons Page
    DESCRIPTION: ﻿JIRA Tickets:
    DESCRIPTION: BMA-21405 UX Football Pages - Auto hide coupons accordions when no events are available
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

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        pass

    def test_003_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: * 'Coupons' tab is selected and highlighted
        EXPECTED: * List of coupons is displayed on the Coupons Landing page
        EXPECTED: * It is possible to navigate on Coupons Details page by tapping a row from the list
        """
        pass

    def test_004_undisplay_all_events_in_any_of_coupon_group(self):
        """
        DESCRIPTION: Undisplay all events in any of Coupon group
        EXPECTED: All events are undisplayed
        """
        pass

    def test_005_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: The Coupon accordion is no longer shown in the list
        """
        pass

    def test_006_result_all_events_in_any_of_coupon_group(self):
        """
        DESCRIPTION: Result all events in any of Coupon group
        EXPECTED: All events are resulted
        """
        pass

    def test_007_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: Coupon accordion is no longer shown in the list
        """
        pass

    def test_008_undisplay_half_of_the_events_in_any_of_coupon_group_and_result_the_rest_events(self):
        """
        DESCRIPTION: Undisplay half of the events in any of Coupon group and result the rest events
        EXPECTED: Events are undisplayed/resulted
        """
        pass

    def test_009_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: Coupon accordion is no longer shown in the list
        """
        pass
