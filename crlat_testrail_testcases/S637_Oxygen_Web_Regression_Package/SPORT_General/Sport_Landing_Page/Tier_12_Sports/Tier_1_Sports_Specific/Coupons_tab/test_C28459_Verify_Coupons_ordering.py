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
class Test_C28459_Verify_Coupons_ordering(Common):
    """
    TR_ID: C28459
    NAME: Verify Coupons ordering
    DESCRIPTION: This test case verifies events sorting on the Coupons tab.
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

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_003_tap_coupons_tab(self):
        """
        DESCRIPTION: Tap 'Coupons' tab
        EXPECTED: 'Coupons' tab is opened
        """
        pass

    def test_004_verify_section_header_title(self):
        """
        DESCRIPTION: Verify section header title
        EXPECTED: The section header title should be in the format:
        EXPECTED: '<Coupon Name>' and correpond to the attribute **'name' **of coupon
        """
        pass

    def test_005_verify_sections_order(self):
        """
        DESCRIPTION: Verify sections order
        EXPECTED: Sections are ordered by coupons **'displayOrder' **in ascending
        """
        pass

    def test_006_verify_events_order_in_the_sections(self):
        """
        DESCRIPTION: Verify events order in the sections
        EXPECTED: *   Events are ordered by event's '**typeDisplayOrder'** in ascending
        EXPECTED: *   Events are ordered by** 'startTime' **in ascending (in case of the same 'typedisplayOrder')
        EXPECTED: *   Events are ordered alphabetically in ascending (in case of the same 'startTime')
        """
        pass
