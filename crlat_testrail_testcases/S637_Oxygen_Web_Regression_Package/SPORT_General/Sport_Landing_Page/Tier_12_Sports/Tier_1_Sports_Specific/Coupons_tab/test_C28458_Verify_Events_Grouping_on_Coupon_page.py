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
class Test_C28458_Verify_Events_Grouping_on_Coupon_page(Common):
    """
    TR_ID: C28458
    NAME: Verify Events Grouping on Coupon page
    DESCRIPTION: This test case verifies events grouping on Coupon page.
    PRECONDITIONS: 1. In order to get a list with **Coupon IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: 2. For each Coupon retrieve a list of **Events and Outcomes**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?translationLang=LL
    PRECONDITIONS: *   XXX is the **Coupon **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: NOTE: within coupon all events suppose to have the same market
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

    def test_004_verify_sections_collapsingexpanding(self):
        """
        DESCRIPTION: Verify section's collapsing/expanding
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: *   The first 5 events loads within 1 second after clicking on the section and incrementally render more events when user scrolls down
        """
        pass

    def test_005_verify_cash_out_label(self):
        """
        DESCRIPTION: Verify 'Cash out' label
        EXPECTED: If any event within the coupon has cashoutAvail="Y" on type level, 'CASH OUT' label is shown next to the Coupon name
        """
        pass

    def test_006_go_to_sections(self):
        """
        DESCRIPTION: Go to sections
        EXPECTED: Events are grouped by **'coupon i****d'**
        """
        pass

    def test_007_verify_page_when_there_are_no_events_to_show(self):
        """
        DESCRIPTION: Verify page when there are no events to show
        EXPECTED: Message is visible **'No events found'**
        """
        pass
