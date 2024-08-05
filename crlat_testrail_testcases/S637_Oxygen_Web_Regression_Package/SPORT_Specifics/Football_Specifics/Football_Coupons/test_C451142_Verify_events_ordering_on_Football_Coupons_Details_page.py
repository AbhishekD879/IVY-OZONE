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
class Test_C451142_Verify_events_ordering_on_Football_Coupons_Details_page(Common):
    """
    TR_ID: C451142
    NAME: Verify events ordering on Football Coupons Details page
    DESCRIPTION: This test case verifies events ordering on Football Coupons Details page
    PRECONDITIONS: 1) 2) In order to get an information about particular coupon use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?simpleFilter=event.startTime:lessThan:2017-07-15T09:01:00.000Z&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.startTime:greaterThanOrEqual:2017-07-09T21:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2017-07-10T09:01:00.000Z&translationLang=en
    PRECONDITIONS: XXX - coupon's id
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
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
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * List of coupons is displayed on the Coupons Landing page
        """
        pass

    def test_004_navigate_to_uk_coupon(self):
        """
        DESCRIPTION: Navigate to UK Coupon
        EXPECTED: * Events for selected coupon are displayed on Coupons Details page
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining accordions are collapsed by default
        """
        pass

    def test_005_verify_competition_accordions_order(self):
        """
        DESCRIPTION: Verify competition accordions order
        EXPECTED: - Accordions are ordered by coupons **classDisplayOrder** and **typeDisplayOrder** in ascending
        EXPECTED: - Alphabetical order in the second instance if display order is the same on type level
        """
        pass

    def test_006_verify_events_order_in_the_accordions(self):
        """
        DESCRIPTION: Verify events order in the accordions
        EXPECTED: Events are ordered in the following way:
        EXPECTED: * startTime - chronological order in the first instance
        EXPECTED: * Event displayOrder in ascending
        EXPECTED: * Alphabetical order in ascending (in case of the same 'startTime')
        """
        pass

    def test_007_repeat_steps_4_6_for_the_next_coupons_odds_on_coupon_european_coupon_euro_elite_coupon_televised_matches_top_leagues_coupon_international_coupon_rest_of_the_world_coupon_goalscorer_coupon(self):
        """
        DESCRIPTION: Repeat steps 4-6 for the next coupons:
        DESCRIPTION: * Odds on Coupon
        DESCRIPTION: * European Coupon
        DESCRIPTION: * Euro Elite Coupon
        DESCRIPTION: * Televised Matches
        DESCRIPTION: * Top Leagues Coupon
        DESCRIPTION: * International Coupon
        DESCRIPTION: * Rest of the World Coupon
        DESCRIPTION: * Goalscorer Coupon
        EXPECTED: 
        """
        pass
