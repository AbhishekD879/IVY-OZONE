import pytest
from time import sleep
from tests_ios_fully_native_regression.base_test import BaseTest
import tests_ios_fully_native_regression as tests


@pytest.mark.native
class Test_Journey_4_In_Play_Football(BaseTest):
    """
    NAME: Open App And Login
    DESCRIPTION: This test case verifies bet placement on inplay event
    """

    def test_001_open_app(self):
        """
        Open The Native App
        """
        homepage = self.native_app.home_page
        self.assertTrue(homepage, msg="App Not Opened")

    def test_002_click_on_login(self):
        """
        Open Inplay From Menu Carousel
        """
        if tests.settings.brand != 'bma':
            self.native_app.login(username="testgvcld_RT2JIW")
        else:
            self.native_app.login(username="testgvccl-U3AW6E")
        inplay = self.native_app.home_page.menu_carousel.get_on_item_in_scrollable_view("IN-PLAY")
        inplay.click()
        self.native_app.home_page.capture_screenshot()
        sleep(10)

    def test_003_Add_Inplay_selection(self):
        """
        Enter Credentials
        """
        buttons = self.native_app.home_page.bet_buttons
        curr_btn = buttons.pop()
        while curr_btn.text == "SUSP":
            curr_btn = buttons.pop()
        curr_btn.click()
        self.native_app.home_page.quick_bet_stake_input = "0.1"
        self.native_app.home_page.quick_bet_place_bet.click()
        try:
            self.native_app.home_page.quick_bet_receipt_close_button
        except Exception:
            self.native_app.home_page.quick_bet_place_bet.click()
        self.assertTrue(self.native_app.home_page.quick_bet_receipt_close_button, msg="quick bet receipt not shown")
