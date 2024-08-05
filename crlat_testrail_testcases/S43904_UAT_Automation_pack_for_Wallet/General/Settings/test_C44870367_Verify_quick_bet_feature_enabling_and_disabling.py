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
class Test_C44870367_Verify_quick_bet_feature_enabling_and_disabling(Common):
    """
    TR_ID: C44870367
    NAME: Verify quick bet feature enabling and disabling
    DESCRIPTION: Note: Quick Bet will not be displayed for Football -> Coupons page. It is disabled by default as per requirement.
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_navigate_to_betting_settings_from_the_my_accountright_menu__settings__betting_settings(self):
        """
        DESCRIPTION: Navigate to Betting Settings from the My Account/Right menu > Settings > Betting settings
        EXPECTED: 1. Settings page is displayed.
        EXPECTED: 2. Quick bet is enabled by default.
        """
        pass

    def test_002_disable_quick_bet_click_on_back_and_close_the_my_account_menu_select_any_selection_on_home_page_and_verify(self):
        """
        DESCRIPTION: Disable Quick Bet. Click on Back and close the My Account menu. Select any selection on Home page and verify.
        EXPECTED: 1. The selection is added directly to the bet slip, i.e. the bet slip counter displays the value as 1.
        EXPECTED: 2. Quick Bet is not displayed.
        """
        pass

    def test_003_navigate_to_settings_from_the_my_accountright_menu_and_enable_quick_bet_click_on_back_and_close_the_my_account_menu_select_any_selection_on_home_page_and_verify(self):
        """
        DESCRIPTION: Navigate to Settings from the My Account/Right menu and enable Quick Bet. Click on Back and close the My Account menu. Select any selection on Home page and verify.
        EXPECTED: 1. Quick Bet is displayed with the selection details.
        EXPECTED: 2. The selection should added to the bet slip, i.e. the bet slip counter displays the value as 1.
        """
        pass
