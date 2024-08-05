import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C3009208_CMS_configuration_for_Roulette(Common):
    """
    TR_ID: C3009208
    NAME: CMS configuration for Roulette
    DESCRIPTION: This test case verifies СMS configuration for Roulette
    PRECONDITIONS: * CMS is opened
    PRECONDITIONS: * Roulette feature is turned off in CMS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is not ticked. * The 'SuccessNavigationUrl' is set to 'https://gaming.coral.co.uk', 'timeToRedirect' is set to X seconds.
    PRECONDITIONS: * Roulette promo code is turned off in CMS: System Configuration -> Structure -> Registration -> 'isPromoCodeFieldEnabled'  checkbox is not ticked
    PRECONDITIONS: * Roulette journey can be verified within Local storage and -> attribute for Roulette users = 'OX.rouletteJourney'
    PRECONDITIONS: NOTE: The users will be able to see the dedicated landing page ONCE in a lifetime; upon first app launch - http://promotions.coral.co.uk/lp/shop-games/
    """
    keep_browser_open = True

    def test_001_open_sb_via_specific_url(self):
        """
        DESCRIPTION: Open SB via specific url
        EXPECTED: SB Home page is opened
        """
        pass

    def test_002_tap_join_us_here_button(self):
        """
        DESCRIPTION: Tap 'Join us here' button
        EXPECTED: Registration page is displayed on Step 1
        """
        pass

    def test_003__fill_all_required_data_for_step_1_and_2_tap_next_step(self):
        """
        DESCRIPTION: * Fill all required data for Step 1 and 2
        DESCRIPTION: * Tap 'Next Step'
        EXPECTED: * Registration page is displayed on Step 3
        EXPECTED: * 'Optional Promo code' field is NOT present - after the currency and before deposit limits areas
        """
        pass

    def test_004__go_to_cms_tick_isrouletteenabled_checkbox_tick_ispromocodefieldenabled__checkbox_save_changes(self):
        """
        DESCRIPTION: * Go to CMS
        DESCRIPTION: * Tick 'isRouletteEnabled' checkbox
        DESCRIPTION: * Tick 'isPromoCodeFieldEnabled'  checkbox
        DESCRIPTION: * Save changes
        EXPECTED: RouletteJourney is anabled is CMS
        """
        pass

    def test_005_open_roulette_lp_via_specific_url(self):
        """
        DESCRIPTION: Open Roulette LP via specific url
        EXPECTED: Roulette LP is opened
        """
        pass

    def test_006_tap_join_now_button(self):
        """
        DESCRIPTION: Tap 'Join now' button
        EXPECTED: Registration page is opened
        """
        pass

    def test_007__fill_all_required_data_for_step_1_and_2_tap_next_step(self):
        """
        DESCRIPTION: * Fill all required data for Step 1 and 2
        DESCRIPTION: * Tap 'Next Step'
        EXPECTED: * Registration page is displayed on Step 3
        EXPECTED: * 'Promo code' field is present after the currency and before deposit limits areas
        """
        pass

    def test_008_register_and_make_successful_deposit(self):
        """
        DESCRIPTION: Register and make successful deposit
        EXPECTED: * User redirected to https://gaming.coral.co.uk
        EXPECTED: * Redirection time = X sec, which are set in CMS
        """
        pass
