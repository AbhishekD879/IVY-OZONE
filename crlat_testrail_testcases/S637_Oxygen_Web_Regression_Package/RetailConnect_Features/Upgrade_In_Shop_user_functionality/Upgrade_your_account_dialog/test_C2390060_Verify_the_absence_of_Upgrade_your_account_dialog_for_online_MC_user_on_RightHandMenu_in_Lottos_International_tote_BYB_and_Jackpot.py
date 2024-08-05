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
class Test_C2390060_Verify_the_absence_of_Upgrade_your_account_dialog_for_online_MC_user_on_RightHandMenu_in_Lottos_International_tote_BYB_and_Jackpot(Common):
    """
    TR_ID: C2390060
    NAME: Verify the absence of 'Upgrade your account' dialog for online/MC user on RightHandMenu, in Lottos, International tote, BYB  and Jackpot
    DESCRIPTION: This test case verifies the absence of pop-up upgrade dialog for online/MC users after tapping Deposit/Withdraw/Cancel Withdrawal/My account items on RightHandMenu, Lottos, International tote, BYB, Player Bets, and Jackpot
    DESCRIPTION: multi-channel user: bluerabbit/ password (?)
    DESCRIPTION: testgvcld_yest0 / qwerty123 (beta-sports.ladbrokes.com)
    PRECONDITIONS: Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    """
    keep_browser_open = True

    def test_001_log_in_an_online_user(self):
        """
        DESCRIPTION: Log in an online user
        EXPECTED: The user is successfully logged in
        """
        pass

    def test_002_open_righthandmenu_my_account__open_following_menu_items_one_by_onedepositwithdrawcancel_withdrawalmy_account_items(self):
        """
        DESCRIPTION: Open RightHandMenu (My Account) ->
        DESCRIPTION: Open following menu items (one by one):
        DESCRIPTION: **Deposit/Withdraw/Cancel Withdrawal/My account** items
        EXPECTED: * Deposit/Withdraw/Cancel Withdrawal/My account item is opened
        EXPECTED: * No upgrade pop-up dialog is opened
        """
        pass

    def test_003_close_rhm_with_the_close_button(self):
        """
        DESCRIPTION: Close RHM with the Close button
        EXPECTED: RHM is closed successfully
        """
        pass

    def test_004_tapclick_lotto_on_the_ribbon_header_menu(self):
        """
        DESCRIPTION: Tap/click **Lotto** on the ribbon header menu
        EXPECTED: The Lotto page is open
        """
        pass

    def test_005_tap_lucky_5_button___enter_some_number_in_the__box_and_tap_place_bet_for__amount_of_money_button(self):
        """
        DESCRIPTION: Tap 'Lucky 5' button -> Enter some number in the £ box and tap 'Place bet for £ {amount of money}' button
        EXPECTED: The 'Place bet...' button changed to red 'Confirm?' button
        """
        pass

    def test_006_tapclick_confirm_button(self):
        """
        DESCRIPTION: Tap/click 'Confirm?' button
        EXPECTED: Bet Receipt is open
        """
        pass

    def test_007_tapclick_coralladbrokes_logo(self):
        """
        DESCRIPTION: Tap/click Coral/Ladbrokes logo
        EXPECTED: Homepage is open
        """
        pass

    def test_008_tapclick_international_tote_on_the_ribbon_header_menu(self):
        """
        DESCRIPTION: Tap/click **International Tote** on the ribbon header menu
        EXPECTED: International Tote page is open
        """
        pass

    def test_009_tapclick_any_upcoming_event___enter_some_number_in_the_box_with_currency_sign_and_tap_bet_now_button_do_not_place_tote_bets_on_prod(self):
        """
        DESCRIPTION: Tap/click any upcoming event -> Enter some number in the box with currency sign and tap 'Bet now' button (DO NOT PLACE TOTE BETS ON PROD!)
        EXPECTED: Bet Receipt is open
        """
        pass

    def test_010_tapclick_coralladbrokes_logo(self):
        """
        DESCRIPTION: Tap/click Coral/Ladbrokes logo
        EXPECTED: Homepage is open
        """
        pass

    def test_011_tapclick_football_on_the_ribbon_header_menu___jackpot_tab___lucky_dip_button___bet_now_button(self):
        """
        DESCRIPTION: Tap/click Football on the ribbon header menu -> **Jackpot** tab -> 'Lucky Dip' button -> 'Bet now' button
        EXPECTED: Bet Receipt with games and selections is displayed
        """
        pass

    def test_012_tapclick_coralladbrokes_logo(self):
        """
        DESCRIPTION: Tap/click Coral/Ladbrokes logo
        EXPECTED: Homepage is open
        """
        pass

    def test_013_tapclick_byb_on_tabs_ribbon___select_any_event___select_markets___place_bet___fill_in_stake_field___place_bet(self):
        """
        DESCRIPTION: Tap/click **BYB** on tabs ribbon -> Select any event -> Select markets -> Place bet -> Fill in 'Stake' field -> Place bet
        EXPECTED: Bet receipt is displayed
        """
        pass

    def test_014_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out
        """
        pass

    def test_015_log_in_to_the_sb_app_as_an_multi_channel_user_with_username_and_password(self):
        """
        DESCRIPTION: Log in to the SB app as an multi-channel user (with username and password)
        EXPECTED: The user is successfully logged in
        """
        pass

    def test_016_repeat_steps_2__16(self):
        """
        DESCRIPTION: Repeat steps #2 -#16
        EXPECTED: 
        """
        pass
