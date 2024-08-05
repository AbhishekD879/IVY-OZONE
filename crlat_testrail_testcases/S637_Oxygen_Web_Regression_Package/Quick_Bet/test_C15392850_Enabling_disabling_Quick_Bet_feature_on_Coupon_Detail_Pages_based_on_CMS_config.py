import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C15392850_Enabling_disabling_Quick_Bet_feature_on_Coupon_Detail_Pages_based_on_CMS_config(Common):
    """
    TR_ID: C15392850
    NAME: Enabling/disabling Quick Bet feature on Coupon Detail Pages based on CMS config
    DESCRIPTION: This Test Case verifies 'Block Quick Bet' feature on Coupon Detail Pages (ACCA page for Ladbrokes) across the App.
    PRECONDITIONS: **CMS config:**
    PRECONDITIONS: - quick bet should be enabled in CMS > system configuration > structure > quickBet > EnableQuickBet
    PRECONDITIONS: - 'blockOnCouponDetailsPage' should be enabled (checked) in CMS > system configuration > structure > quickBet.
    PRECONDITIONS: CMS links and credentials: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Quick bet should be enabled in User account menu > Settings
    PRECONDITIONS: 1. Log in
    PRECONDITIONS: 2. Navigate to any sport landing page e.g. Football > 'Coupons' tab (Coral) / 'ACCAS' tab (Ladbrokes)
    PRECONDITIONS: 3. Tap on any Coupon > Coupon details page is opened
    """
    keep_browser_open = True

    def test_001_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Quick Bet is NOT invoked
        """
        pass

    def test_002_navigate_to_homepage__coupons_tab__coupon_details_page(self):
        """
        DESCRIPTION: Navigate to Homepage > Coupons tab > Coupon details page
        EXPECTED: 
        """
        pass

    def test_003_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: * Selection is added to Betslip
        EXPECTED: * Quick Bet is NOT invoked
        """
        pass

    def test_004_disable_uncheck_blockoncoupondetailspage_in_cms__system_configuration__structure__quickbet(self):
        """
        DESCRIPTION: Disable (uncheck) 'blockOnCouponDetailsPage' in CMS > system configuration > structure > quickBet
        EXPECTED: 
        """
        pass

    def test_005_on_fe_reload_any_coupon_details_page(self):
        """
        DESCRIPTION: On FE reload any Coupon details page
        EXPECTED: 
        """
        pass

    def test_006_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: * Quick Bet is invoked
        EXPECTED: * Selection is added to Quick Bet
        """
        pass

    def test_007_navigate_to_homepage__coupons_tab__coupon_details_page(self):
        """
        DESCRIPTION: Navigate to Homepage > Coupons tab > Coupon details page
        EXPECTED: 
        """
        pass

    def test_008_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: * Quick Bet is invoked
        EXPECTED: * Selection is added to Quick Bet
        """
        pass

    def test_009_repeat_all_steps_for_logged_out_user(self):
        """
        DESCRIPTION: Repeat all steps for logged out user
        EXPECTED: 
        """
        pass
