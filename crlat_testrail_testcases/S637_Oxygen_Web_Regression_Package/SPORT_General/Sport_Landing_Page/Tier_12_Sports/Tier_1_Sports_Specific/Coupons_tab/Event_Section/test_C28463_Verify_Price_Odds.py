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
class Test_C28463_Verify_Price_Odds(Common):
    """
    TR_ID: C28463
    NAME: Verify Price/Odds
    DESCRIPTION: This test case verifies Price/Odds buttons of event.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 1. In order to get a list with **Coupon IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: 2. For each Coupon retrieve a list of **Events and Outcomes**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/XX.XX/CouponToOutcomeForCoupon/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - **Coupon **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * For DESKTOP: 'Price/Odds' button size depends on screen resolution (see https://ladbrokescoral.testrail.com/index.php?/cases/view/1474609 test case).
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sports> Landing page
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

    def test_004_go_to_event_section(self):
        """
        DESCRIPTION: Go to Event section
        EXPECTED: 
        """
        pass

    def test_005_verify_data_of_priceodds_for_verified_event_in_fraction_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified event in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   'Price/Odds'  are disabled if **eventStatusCode="S"**
        """
        pass

    def test_006_verify_priceodds_button_for_1_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 1-Way Market
        EXPECTED: Price/Odds button is displayed next to the Event name according to market
        """
        pass

    def test_007_verify_priceodds_button_for_2_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 2-Way Market
        EXPECTED: Two selections are shown in one row below the Event name according to the Market
        EXPECTED: *   For markets with outcomes Yes/No - 'Yes'/'No' labels are present within price/odds buttons with corresponding values
        EXPECTED: *   For markets with outcomes Over/Under- 'Over'/'Under' labels are present within price/odds buttons with corresponding values
        """
        pass

    def test_008_verify_priceodds_button_for_3_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 3-Way Market
        EXPECTED: For 3-way market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home 'Win'
        EXPECTED: *   outcomeMeaningMinorCode="D" is a 'Draw'
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away 'Win'
        """
        pass

    def test_009_add_selection_to_the_betslip_from_sport_landing_page(self):
        """
        DESCRIPTION: Add selection to the Betslip from <Sport> Landing Page
        EXPECTED: Bet indicator displays 1.
        """
        pass

    def test_010_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        pass

    def test_011_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass
