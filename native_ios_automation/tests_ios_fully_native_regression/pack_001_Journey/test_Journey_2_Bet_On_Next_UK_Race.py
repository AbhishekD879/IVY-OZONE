import pytest
import tests_ios_fully_native_regression as tests
from time import sleep
from tests_ios_fully_native_regression.base_test import BaseTest


@pytest.mark.native
class Test_Journey_2_Bet_On_Next_UK_Race(BaseTest):
    """
    NAME: Bet on Next UK Race
    DESCRIPTION: This test case verifies Bet Placement on Next UK Race
    """
    def test_001_open_app(self):
        """
        Open The Native App
        """
        homepage = self.native_app.home_page
        self.assertTrue(homepage, msg="App not opened")

    def test_002_login_into_app(self):
        """
        Click on Login CTA
        Enter Credentials
        Click On Login Button to Confirm Login
        """
        if tests.settings.brand != 'bma':
            self.native_app.login(username="testgvcld_RT2JIW")
        else:
            self.native_app.login(username="testgvccl-U3AW6E")
        sleep(5)

    def test_003_naviagte_to_Horse_Racing_sport(self):
        """
        Click Horse Racing sport on Sport Ribbon tab
        """
        horse_racing_item = self.native_app.home_page.menu_carousel.get_on_item_in_scrollable_view(item_name="HORSE RACING")
        horse_racing_item.click()
        sleep(15)
        if self.brand =='bma':
            self.native_app.home_page.cookie_pop_up_close_icon.click()

    def test_004_place_bet_on_next_uk_race(self):
        """
        Click on UK & Irish filter under Next Races
        Click on odds button
        Place bet
        """
        self.native_app.home_page.next_races_uk_irish_filter.click()
        sleep(2)
        self.native_app.home_page.scroll_in_direction(value=200)
        odds_button = self.native_app.home_page.bet_buttons[-1]
        odds_button.click()
        sleep(5)
        self.native_app.home_page.quick_bet_stake_input = ".1"
        self.native_app.home_page.place_bet.click()

    def test_005_verify_bet_receipt(self):
        """
        Bet Receipt is displayed
        """
        sleep(5)
        self.assertTrue(self.native_app.home_page.bet_receipt, msg='Bet Receipt is not displayed')
