import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9776270_Verify_Desktop_Mini_games_widget_for_Logged_in_user_with_000_balance(Common):
    """
    TR_ID: C9776270
    NAME: Verify Desktop Mini games widget for Logged in user with 0.00 balance
    DESCRIPTION: This test case verifies Desktop Mini games widget for Logged in user with 0.00 balance
    PRECONDITIONS: 1. Desktop Mini games widget is created and configured in CMS > Widgets
    PRECONDITIONS: 2. Desktop Mini games widget is active in CMS.
    PRECONDITIONS: 3. Login to app as a User with 0.00 balance.
    """
    keep_browser_open = True

    def test_001_click_play_now_on_mini_games_widget(self):
        """
        DESCRIPTION: Click Play Now on Mini games widget
        EXPECTED: 
        """
        pass

    def test_002_select_a_game_to_play_select_real_play_and_click_spin(self):
        """
        DESCRIPTION: Select a game to play, select Real Play and click Spin
        EXPECTED: * 'Insuffficient Balance for the requested Bet...' message displayed
        """
        pass
