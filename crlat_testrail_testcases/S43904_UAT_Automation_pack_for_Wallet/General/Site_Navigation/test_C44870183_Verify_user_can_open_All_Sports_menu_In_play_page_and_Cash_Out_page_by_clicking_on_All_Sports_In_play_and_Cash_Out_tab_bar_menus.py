import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C44870183_Verify_user_can_open_All_Sports_menu_In_play_page_and_Cash_Out_page_by_clicking_on_All_Sports_In_play_and_Cash_Out_tab_bar_menus(Common):
    """
    TR_ID: C44870183
    NAME: Verify user can open 'All Sports' menu , 'In-play' page and 'Cash Out' page by clicking on  'All Sports' , 'In-play' and 'Cash Out' tab bar menus.
    DESCRIPTION: 
    PRECONDITIONS: BETA App should be loaded.
    """
    keep_browser_open = True

    def test_001_tap_on_menu_from_bottom_menu_bar(self):
        """
        DESCRIPTION: Tap on 'Menu' from bottom menu bar
        EXPECTED: 'All Sports' opens with 'Top Sports' followed by  'A-Z Sports' Sections. User  should be able to tap on any of the menu items and corresponding page should load.
        """
        pass

    def test_002_while_on_all_sports_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'All Sports' page tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        pass

    def test_003_tap_on_in_play_from_bottom_menu_bar(self):
        """
        DESCRIPTION: Tap on 'In-Play' from bottom menu bar
        EXPECTED: 'In-Play' page is loaded and all the events which are live should appear followed by Upcoming events. User should be able to switch between sports from the sub header by tapping on corresponding sport icon. User should be able to see list of Live events for which streaming is available by tapping on 'Watch Live' icon.
        """
        pass

    def test_004_while_on_in_play_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'In Play' page tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        pass

    def test_005_tap_on_cash_out_from_bottom_menu_bar_for_a_logged_out_user(self):
        """
        DESCRIPTION: Tap on 'CASH OUT' from bottom menu bar for a Logged out user
        EXPECTED: 'My Bets' page should open with 'CASH OUT' tab expanded by default. 'Please log in to see your cash out bets' will appear along with 'Login' tab.
        """
        pass

    def test_006_while_on_my_bets_page_tap_on_open_bets_for_a_logged_out_user(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'OPEN BETS' for a logged out user
        EXPECTED: 'Please log in to see your open bets' message is seen along with 'Log in' tab.
        """
        pass

    def test_007_while_on_my_bets_page_tap_on_settled_bets_for_a_logged_out_user(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'SETTLED BETS' for a logged out user
        EXPECTED: 'Please log in to see your settled bets' message is seen along with 'Log in' tab.
        """
        pass

    def test_008_tap_on_cash_out_from_bottom_menu_bar_for_a_logged_in_user(self):
        """
        DESCRIPTION: Tap on 'CASH OUT' from bottom menu bar for a Logged in user
        EXPECTED: 'My Bets' page should open with 'CASH OUT' tab expanded by default. The current cash out bets of the user will be displayed with the latest bet placed at the top.
        """
        pass

    def test_009_while_on_my_bets_page_tap_on_open_bets_for_a_logged_in_user(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'OPEN BETS' for a logged in user
        EXPECTED: The current open bets of the user will be displayed with the latest bet placed at the top. User should be able to switch between Sports / Lotto / Pools under OPEN BETS tab
        """
        pass

    def test_010_while_on_my_bets_page_tap_on_settled_bets_for_a_logged_in_user(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'SETTLED BETS' for a logged in user
        EXPECTED: all the settled bets of the user for the set period of time should be displayed.User should be able to switch between Sports / Lotto / Pools under OPEN BETS tab. User should be able to set From and To dates to view all the settled bets between that period.
        """
        pass

    def test_011_while_on_my_bets_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on My Bets Page, tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        pass
