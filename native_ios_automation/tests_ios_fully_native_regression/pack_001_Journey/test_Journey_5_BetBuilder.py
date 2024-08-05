import pytest
import tests_ios_fully_native_regression as tests
from time import sleep
from tests_ios_fully_native_regression.base_test import BaseTest


@pytest.mark.native
class Test_Journey_5_Bet_Builder(BaseTest):
    """
    NAME: Bet Builder
    DESCRIPTION: This test case verifies Bet Placement on Bet Builder
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

    def test_003_navigate_to_Football_SLP(self):
        """
        Click Football from menu carousels
        """
        football_item = self.native_app.home_page.menu_carousel.get_on_item_in_scrollable_view(item_name="FOOTBALL")
        football_item.click()
        sleep(12)
        try:
            if self.brand == 'bma':
                self.native_app.home_page.close_tutorial.click()
                self.native_app.home_page.cookie_pop_up_close_icon.click()
        except Exception:
            self._logger.info('Cookie popup is not displayed')

    def test_004_naviagte_to_EDP_page(self):
        """
        Click on Event
        Click on Bet Builder tab
        """
        self.native_app.home_page.event.click()
        sleep(10)
        self.native_app.home_page.bet_builder_tab.click()
        sleep(10)

    def test_005_add_sections_from_match_betting_total_goals_total_corners(self):
        """
        Add selection from Match Betting, Total Goals and Total Corners
        """
        self.native_app.home_page.match_betting_select_team.click()
        self.native_app.home_page.match_betting_time_period.click()
        self.native_app.home_page.match_betting_add_to_bet_builder.click()
        self.native_app.home_page.total_goals.click()
        self.native_app.home_page.total_goals_select_team.click()
        self.native_app.home_page.total_goals_time_period.click()
        sleep(10)
        self.native_app.home_page.total_goals_goals.click()
        self.native_app.home_page.total_goals_add_to_bet_builder.click()

    def test_006_place_bet(self):
        """
        Click on Place Bet
        Bet Receipt is displayed
        """
        sleep(2)
        self.native_app.home_page.bet_builder_place_bet.click()
        sleep(10)
        self.native_app.home_page.quick_bet_stake_input = ".1"
        self.native_app.home_page.place_bet.click()
        sleep(5)
        self.assertTrue(self.native_app.home_page.bet_receipt, msg='Bet Receipt is not displayed')
