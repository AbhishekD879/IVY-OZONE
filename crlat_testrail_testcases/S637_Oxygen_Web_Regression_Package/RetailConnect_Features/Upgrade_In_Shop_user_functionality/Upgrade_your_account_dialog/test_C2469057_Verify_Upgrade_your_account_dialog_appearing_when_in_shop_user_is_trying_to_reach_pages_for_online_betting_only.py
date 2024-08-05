import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2469057_Verify_Upgrade_your_account_dialog_appearing_when_in_shop_user_is_trying_to_reach_pages_for_online_betting_only(Common):
    """
    TR_ID: C2469057
    NAME: Verify 'Upgrade your account' dialog appearing when in-shop user is trying to reach pages for online betting only
    DESCRIPTION: This test case verifies displaying the upgrade pop-up when an in-shop user clicks on some items (Deposit, Withdraw etc.) in My Account menu, 'Place Bet' in football, in Lottos, in International tote etc.
    PRECONDITIONS: * Load the app
    PRECONDITIONS: * Log in with in-shop user
    PRECONDITIONS: * Close the upgrade dialog
    """
    keep_browser_open = True

    def test_001_tapclick_deposit_item(self):
        """
        DESCRIPTION: Tap/click **Deposit** item
        EXPECTED: The upgrade page appears
        """
        pass

    def test_002_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass

    def test_003_tapclick_withdraw_item(self):
        """
        DESCRIPTION: Tap/click **Withdraw** item
        EXPECTED: The upgrade dialog appears
        """
        pass

    def test_004_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass

    def test_005_tapclick_cancel_withdrawal_item(self):
        """
        DESCRIPTION: Tap/click **Cancel Withdrawal** item
        EXPECTED: The upgrade dialog appears
        """
        pass

    def test_006_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass

    def test_007_tapclick_my_account__connect__upgrade(self):
        """
        DESCRIPTION: Tap/click **My Account** > **Connect** > **Upgrade**
        EXPECTED: The upgrade dialog appears
        """
        pass

    def test_008_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass

    def test_009_tapclick_lotto_on_the_ribbon_header_menu(self):
        """
        DESCRIPTION: Tap/click **Lotto** on the ribbon header menu
        EXPECTED: The Lotto page is open
        """
        pass

    def test_010_tap_lucky_5_button___enter_some_number_in_the__box_and_tap_place_bet_for__amount_of_money_button(self):
        """
        DESCRIPTION: Tap 'Lucky 5' button -> Enter some number in the £ box and tap 'Place bet for £ {amount of money}' button
        EXPECTED: The upgrade dialog appears
        """
        pass

    def test_011_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass

    def test_012_tapclick_coral_logo(self):
        """
        DESCRIPTION: Tap/click Coral logo
        EXPECTED: Homepage is open
        """
        pass

    def test_013_tapclick_international_tote_on_the_ribbon_header_menu(self):
        """
        DESCRIPTION: Tap/click **International Tote** on the ribbon header menu
        EXPECTED: International Tote page is open
        """
        pass

    def test_014_tapclick_any_upcoming_event___enter_some_number_in_the_box_with_currency_sign_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap/click any upcoming event -> Enter some number in the box with currency sign and tap 'Bet now' button
        EXPECTED: The upgrade dialog appears
        """
        pass

    def test_015_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass

    def test_016_tapclick_player_bets_on_the_ribbon_header_menu(self):
        """
        DESCRIPTION: Tap/click **Player Bets** on the ribbon header menu
        EXPECTED: Player Bets page is open
        """
        pass

    def test_017_select_player_statistic___add_to_the_betslip(self):
        """
        DESCRIPTION: Select Player, Statistic -> Add to the betslip
        EXPECTED: Betslip is open
        """
        pass

    def test_018_type_figures_in_stake_boxes(self):
        """
        DESCRIPTION: Type figures in stake boxes
        EXPECTED: 'Bet now' button became active
        """
        pass

    def test_019_tapclick_bet_now_button(self):
        """
        DESCRIPTION: Tap/click 'Bet now' button
        EXPECTED: The upgrade dialog appears
        """
        pass

    def test_020_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass

    def test_021_tapclick_football_on_the_ribbon_header_menu(self):
        """
        DESCRIPTION: Tap/click Football on the ribbon header menu
        EXPECTED: Football page is open
        """
        pass

    def test_022_tapclick_jackpot_tab(self):
        """
        DESCRIPTION: Tap/click **Jackpot** tab
        EXPECTED: Jackpot tab is open
        """
        pass

    def test_023_tapclick_lucky_dip_button____bet_now_button(self):
        """
        DESCRIPTION: Tap/click 'Lucky Dip' button  -> 'Bet now' button
        EXPECTED: The upgrade dialog appears
        """
        pass

    def test_024_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass

    def test_025_tapclick_byb_on_tabs_ribbon___select_any_event___select_markets(self):
        """
        DESCRIPTION: Tap/click **BYB** on tabs ribbon -> Select any event -> Select markets
        EXPECTED: Build Your Bet Betslip is opened
        """
        pass

    def test_026_tapclick_place_bet_button(self):
        """
        DESCRIPTION: Tap/click 'Place bet' button
        EXPECTED: The upgrade dialog appears
        """
        pass

    def test_027_tapclick_close_button_x(self):
        """
        DESCRIPTION: Tap/click close button (X)
        EXPECTED: * The upgrade pop-up dialog is closed
        """
        pass
