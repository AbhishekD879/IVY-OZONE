import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C16268964_Vanilla_Accessing_Log_In_popup(Common):
    """
    TR_ID: C16268964
    NAME: [Vanilla] Accessing Log In popup
    DESCRIPTION: This test case verifies accessing Log In popup from different places of the application
    DESCRIPTION: AUTOTESTS:
    DESCRIPTION: Mobile [C9698473]
    DESCRIPTION: Desktop [C9698093]
    DESCRIPTION: *Automation notes*
    DESCRIPTION: Test case should be updated for ladbrokes wallet as there's no Log In button on all of those pages, or should be marked as Vanilla Coral only, also some steps are coral related only (like favourites feature). Current autotest status to execute - Coral only.
    PRECONDITIONS: Home page (with Vanilla) is opened
    PRECONDITIONS: User is logged out
    PRECONDITIONS: NOTICE: Test Steps where is figuring "Widget", is related ONLY for Desktop - right side vertical panel where mini-Games and betslip are placed;
    """
    keep_browser_open = True

    def test_001_open_homepage(self):
        """
        DESCRIPTION: Open 'Homepage'
        EXPECTED: 'Log In' button is present on the header
        """
        pass

    def test_002_clicktap_the_log_in_button(self):
        """
        DESCRIPTION: Click/Tap the 'Log in' button
        EXPECTED: 'Log in' pop-up is displayed
        EXPECTED: ![](index.php?/attachments/get/34254)
        """
        pass

    def test_003_open_cash_out_page_cashout(self):
        """
        DESCRIPTION: Open 'Cash Out' page (/cashout)
        EXPECTED: 'Log In' button is present on the page
        EXPECTED: ![](index.php?/attachments/get/34255)
        """
        pass

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_005_open_cash_out_tab_in_the_widget___desktop_only(self):
        """
        DESCRIPTION: Open 'Cash Out' tab in the widget - Desktop only;
        EXPECTED: 'Log In' button is present in the widget
        """
        pass

    def test_006_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_007_open_open_bets_page_open_bets(self):
        """
        DESCRIPTION: Open 'Open Bets' page (/open-bets)
        EXPECTED: 'Log In' button is present on the page
        """
        pass

    def test_008_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_009_open_open_bets_page_in_the_widget___desktop_only(self):
        """
        DESCRIPTION: Open 'Open Bets' page in the widget - Desktop only;
        EXPECTED: 'Log In' button is present in the widget
        """
        pass

    def test_010_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_011_open_settled_bets_page_bet_history(self):
        """
        DESCRIPTION: Open 'Settled Bets' page (/bet-history)
        EXPECTED: 'Log In' button is present on the page
        """
        pass

    def test_012_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_013_open_settled_bets_page_in_the_widget___desktop_only(self):
        """
        DESCRIPTION: Open 'Settled Bets' page in the widget - Desktop only;
        EXPECTED: 'Log In' button is present in the widget
        """
        pass

    def test_014_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_015_open_shop_bets_page_in_shop_bets(self):
        """
        DESCRIPTION: Open 'Shop Bets' page (/in-shop-bets)
        EXPECTED: 'Log In' button is present on the page
        """
        pass

    def test_016_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_017_open_favourites_page_favourites(self):
        """
        DESCRIPTION: Open 'Favourites' page (/favourites)
        EXPECTED: 'Log In' button is present on the page
        """
        pass

    def test_018_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_019_open_favourites_widget___desktop_only(self):
        """
        DESCRIPTION: Open 'Favourites' widget - Desktop only;
        EXPECTED: 'Log In' button is present in the widget
        """
        pass

    def test_020_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_021_tap_on_star_icon_under_any_event_eg_in_in_play_page(self):
        """
        DESCRIPTION: Tap on star icon under any event (e.g. in In-play page)
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_022_enter_any_valid_username_and_password_click_log_in_button(self):
        """
        DESCRIPTION: Enter any valid username and password. Click Log in button.
        EXPECTED: User is logged in and stays at the same page
        """
        pass
