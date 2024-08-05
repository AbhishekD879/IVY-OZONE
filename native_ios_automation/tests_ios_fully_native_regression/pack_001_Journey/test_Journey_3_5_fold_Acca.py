import pytest
from time import sleep
import tests_ios_fully_native_regression as tests
from tests_ios_fully_native_regression.base_test import BaseTest


@pytest.mark.native
class Test_Journey_3_Five_Fold_Acca(BaseTest):
    """
    NAME: Five Fold Acca
    DESCRIPTION: This test case verifies Five Fold Acca Bet Placment
    """

    def test_001_open_app_with_loggedIn_user_and_navigate_to_football(self):
        """
        Action:Open App
        Expected:HomePage Is Open
        Action:Login
        Expected:User Logged In
        Action:Navigate to Football
        Expected:Navigation To Football SLP
        """
        homepage = self.native_app.home_page
        self.assertTrue(homepage, msg="App Not Opened")
        sleep(2)
        if tests.settings.brand != 'bma':
            self.native_app.login(username="testgvcld_RT2JIW")
        else:
            self.native_app.login(username="testgvccl-U3AW6E")
        sleep(5)
        football_item = self.native_app.home_page.menu_carousel.get_on_item_in_scrollable_view(item_name="FOOTBALL")
        football_item.click()
        sleep(10)
        try:
            if self.brand =='bma':
                self.native_app.home_page.close_tutorial.click()
                self.native_app.home_page.cookie_pop_up_close_icon.click()
        except Exception:
            self._logger.info('Cookie popup is not displayed')

    def test_002_add_selection_to_betslip(self):
        """
        Add 5 selections and click Acca Bar
        """
        self.native_app.home_page.add_selections_for_5_fold_acca()
        self.native_app.home_page.betslip.click()
        sleep(10)
        self.native_app.home_page.bet_slip_odds_boost_ok_button.click()
        sleep(2)

    def test_003_place_bet_of_5_fold_acca(self):
        """
        Stake and place bet
        """
        self.native_app.home_page.five_fold_acca_input = ".1"
        self.native_app.home_page.scroll_in_direction(value=500)
        self.native_app.home_page.quick_bet_place_bet.click()
        sleep(5)
