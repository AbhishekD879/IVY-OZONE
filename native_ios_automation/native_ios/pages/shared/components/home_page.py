from time import sleep
import tests_ios_fully_native_regression as tests
from appium.webdriver.common.touch_action import TouchAction

from native_ios.pages.shared import get_driver
from native_ios.pages.shared.components.base import IOSNativeBase
from native_ios.pages.shared.components.login import Login
from native_ios.pages.shared.components.menu_carousel import MenuCarousel


class NativeHomePage(IOSNativeBase):
    _home_button = 'id=home'
    _logo = 'id=logo'
    _login_button = 'xpath=//android.view.View[@content-desc="LOG IN"]'
    _racing_card_item = 'xpath=//*[@name="Coral"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeOther'
    # 'xpath=//*[@name="Ladbrokes"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[3]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther[2]'
    _login_popup = 'xpath=//android.view.View[@resource-id="cdk-overlay-0"]'
    _menu_carousel = 'xpath=//android.view.View[@resource-id="page-content"]/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.ListView'
    _bet_buttons = 'xpath=//android.widget.Button[contains(@resource-id, "bet-")]'
    _quick_bet_stake_input = 'xpath=//*[@id="stake-input"] | //android.widget.EditText[@resource-id="stake-input"]'
    _quick_bet_add_to_betslip = 'xpath=//android.widget.Button[@text="ADD TO BETSLIP"]'
    _betslip_btn = 'xpath=//android.widget.TextView[@text="BETSLIP"]'
    _5_fold_acca = 'xpath=//android.widget.TextView[contains(@text,"5 Fold Acca")]/following-sibling::android.view.View//android.widget.EditText'
    _quick_bet_place_bet = 'xpath=//android.widget.Button[@text="PLACE BET"] | //android.widget.Button[@text="ACCEPT AND PLACE BET"]'
    _next_races_uk_irish_filter = 'xpath=//android.widget.TextView[@text="International"] | //android.widget.TextView[@text="UK & Irish"]'
    # _next_races_uk_irish_filter = 'xpath=//android.widget.TextView[@text="UK & Irish"]'
    # _bet_receipt = 'xpath=//android.widget.TextView[@text="Bet Receipt"]'
    _bet_receipt = 'xpath=//*[@class="qb-receipt"]'
    _my_bets = 'xpath=//android.view.View[@content-desc="MY BETS"]'
    _cash_out = 'xpath=//android.widget.Button[contains(@text, "CASH OUT")]'
    _cash_out_successful_message = 'xpath=//android.widget.TextView[@text="Cash Out Successful"]'
    _cookie_pop_up_close_icon = 'xpath=//android.widget.Button[@resource-id="kplDeferButton"]'
    _close_tutorial = 'xpath=//android.widget.Button[@text="Close tutorial"]'
    _timeline_tutorial_overlay = 'xpath=//android.widget.Button[@text="OK, THANKS!"]'
    _quick_bet_receipt_close_button = 'xpath=//android.widget.TextView[@text="Bet Receipt"]/following-sibling::android.view.View'
    #_event = 'xpath=//android.widget.TextView[@text="TOMORROW"]/parent::android.view.View/following-sibling::android.view.View/android.widget.TextView'
    _event = 'xpath=//android.widget.TextView[@text="CHANGE"]/../../../../following-sibling::android.view.View/android.view.View[2]/android.view.View[2]'
    _bet_builder_tab = 'xpath=//android.widget.TextView[@text="BET BUILDER"] | //android.widget.TextView[@text="BUILD YOUR BET"]'
    _total_goals = 'xpath=//android.widget.TextView[@text="Total Goals"] | //android.widget.TextView[@text="TOTAL GOALS"]'
    _total_corners = 'xpath=//android.widget.TextView[@text="Total Corners"] | //android.widget.TextView[@text="TOTAL CORNERS"]'
    _match_betting_select_team = 'xpath=//android.widget.TextView[@text="Match Betting"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Select Team"]/following-sibling::android.view.View | //android.widget.TextView[@text="MATCH BETTING"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Select Team"]/following-sibling::android.view.View'
    _match_betting_time_period = 'xpath=//android.widget.TextView[@text="Match Betting"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Time Period"]/following-sibling::android.view.View | //android.widget.TextView[@text="MATCH BETTING"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Time Period"]/following-sibling::android.view.View'
    _match_betting_add_to_bet_builder = 'xpath=//android.widget.TextView[@text="Match Betting"]/parent::android.view.View/parent::android.view.View//android.widget.Button[@text="ADD TO BET BUILDER"] | //android.widget.TextView[@text="MATCH BETTING"]/parent::android.view.View/parent::android.view.View//android.widget.Button[@text="ADD TO BET BUILDER"]'
    _total_goals_select_team = 'xpath=//android.widget.TextView[@text="Total Goals"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Select Team"]/following-sibling::android.view.View | //android.widget.TextView[@text="TOTAL GOALS"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Select Team"]/following-sibling::android.view.View'
    _total_goals_time_period = 'xpath=//android.widget.TextView[@text="Total Goals"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Time Period"]/following-sibling::android.view.View | //android.widget.TextView[@text="TOTAL GOALS"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Time Period"]/following-sibling::android.view.View'
    _total_goals_goals = 'xpath=//android.widget.TextView[@text="Total Goals"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Goals"]/following-sibling::android.widget.Button | //android.widget.TextView[@text="TOTAL GOALS"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Goals"]/following-sibling::android.widget.Button'
    _total_goals_add_to_bet_builder = 'xpath=//android.widget.TextView[@text="Total Goals"]/parent::android.view.View/parent::android.view.View//android.widget.Button[@text="ADD TO BET BUILDER"] | //android.widget.TextView[@text="TOTAL GOALS"]/parent::android.view.View/parent::android.view.View//android.widget.Button[@text="ADD TO BET BUILDER"]'
    _total_corners_select_team = 'xpath=//android.widget.TextView[@text="Total Corners"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Select Team"]/following-sibling::android.view.View | //android.widget.TextView[@text="TOTAL CORNERS"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Select Team"]/following-sibling::android.view.View'
    _total_corners_time_period = 'xpath=//android.widget.TextView[@text="Total Corners"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Time Period"]/following-sibling::android.view.View | //android.widget.TextView[@text="TOTAL CORNERS"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Time Period"]/following-sibling::android.view.View'
    _total_corners_corners = 'xpath=//android.widget.TextView[@text="Total Corners"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Corners"]/following-sibling::android.widget.Button | //android.widget.TextView[@text="TOTAL CORNERS"]/parent::android.view.View/parent::android.view.View//android.widget.TextView[@text="Corners"]/following-sibling::android.widget.Button'
    _total_corners_add_to_bet_builder = 'xpath=//android.widget.TextView[@text="Total Corners"]/parent::android.view.View/parent::android.view.View//android.widget.Button[@text="ADD TO BET BUILDER"] | //android.widget.TextView[@text="TOTAL CORNERS"]/parent::android.view.View/parent::android.view.View//android.widget.Button[@text="ADD TO BET BUILDER"]'
    _bet_builder_place_bet = 'xpath=//android.widget.TextView[contains(@text, "PLACE BET")]'
    _my_bets_footer = 'xpath=//a[@id="My Bets"]'
    _place_bet = 'xpath=//*[@class="qb-right-cta-btn"]'
    _accrodian_expanded = 'xpath=//android.widget.TextView[@text="CHANGE"]/parent::android.view.View/parent::android.view.View/parent::android.view.View/parent::android.view.View/following-sibling::android.view.View[1]/android.view.View/android.view.View'
    _accrodian = 'xpath=//android.widget.TextView[@text="CHANGE"]/parent::android.view.View/parent::android.view.View/parent::android.view.View/parent::android.view.View/following-sibling::android.view.View[1]'
    _accrodian_bet_button = 'xpath=//android.widget.TextView[@text="CHANGE"]/parent::android.view.View/parent::android.view.View/parent::android.view.View/parent::android.view.View/following-sibling::android.view.View[1]/android.view.View/android.view.View//android.widget.Button[contains(@resource-id, "bet-")]'
    #_accrodian_bet_button = 'xpath=//android.widget.TextView/../following-sibling::android.view.View//android.widget.Button[contains(@resource-id, "bet-")]'
    _bet_slip_odds_boost_ok_button = 'xpath=//*[text()="Ok"]'
    _module_ribbon = 'xpath=//android.view.View[@resource-id="module-ribbon"]'

    @property
    def home_button(self):
        return IOSNativeBase(selector=self._home_button)

    @property
    def login_button(self):
        return IOSNativeBase(selector=self._login_button)

    @property
    def five_fold_acca_input(self):
        return IOSNativeBase(selector=self._5_fold_acca, timeout=5)

    @five_fold_acca_input.setter
    def five_fold_acca_input(self, val=0.1):
        self.scroll_to_ele(selector=self._5_fold_acca, uiautomatorclassname='android.widget.TextView', text='Total Stake')
        self.five_fold_acca_input._we.send_keys(val)

    @property
    def betslip(self):
        return IOSNativeBase(selector=self._betslip_btn, timeout=5)

    @property
    def logo(self):
        return IOSNativeBase(selector=self._logo)

    @property
    def login_popup(self):
        return Login(selector=self._login_popup, timeout=0)

    @property
    def menu_carousel(self):
        return MenuCarousel(selector=self._menu_carousel, timeout=5)

    @property
    def bet_buttons(self):
        self.scroll_in_direction(value=100)
        elements = self._find_elements_by_selector(selector=self._bet_buttons)
        buttons = []
        for el in elements:
            buttons.append(IOSNativeBase(web_element=el, timeout=10))
        return buttons[::-1]

    @property
    def quick_bet_stake_input(self):
        return IOSNativeBase(selector=self._quick_bet_stake_input, timeout=5, context=self._webview)

    @quick_bet_stake_input.setter
    def quick_bet_stake_input(self, value=0.1):
        self.quick_bet_stake_input.click()
        # self.quick_bet_stake_input.clear()
        # self.quick_bet_stake_input._we.send_keys(value)
        self._driver.execute_script(f"arguments[0].value = '{value}'; arguments[0].dispatchEvent(new Event('change'));",
                                    self.quick_bet_stake_input._we)
        # self.switch_to_context(self._webview)
        # self._driver.execute_script(f"arguments[0].value={value}", self.quick_bet_stake_input._we)
        # self._driver.execute_script(f"arguments[0].dispatchEvent(new Event('change'));")

    @property
    def quick_bet_add_to_betslip(self):
        return IOSNativeBase(selector=self._quick_bet_add_to_betslip, timeout=5)

    @property
    def quick_bet_place_bet(self):
        return IOSNativeBase(selector=self._quick_bet_place_bet, timeout=5)

    @property
    def next_races_uk_irish_filter(self):
        return IOSNativeBase(selector=self._next_races_uk_irish_filter, timeout=5)
        sleep(5)

    def accept_and_place_bet(self):
        sleep(5)
        action = TouchAction(get_driver())
        action.tap(None, x=1040, y=2955).perform()

    @property
    def bet_receipt(self):
        return IOSNativeBase(selector=self._bet_receipt, context=self._webview)

    @property
    def my_bets(self):
        return IOSNativeBase(selector=self._my_bets)

    @property
    def cash_out(self):
        return IOSNativeBase(selector=self._cash_out)

    @property
    def cash_out_successful(self):
        return IOSNativeBase(selector=self._cash_out_successful_message)

    @property
    def cookie_pop_up_close_icon(self):
        return IOSNativeBase(selector=self._cookie_pop_up_close_icon)

    @property
    def close_tutorial(self):
        return IOSNativeBase(selector=self._close_tutorial)

    @property
    def timeline_tutorial_overlay(self):
        return IOSNativeBase(selector=self._timeline_tutorial_overlay,timeout=5)

    @property
    def quick_bet_receipt_close_button(self):
        return IOSNativeBase(selector=self._quick_bet_receipt_close_button)

    @property
    def event(self):
        self.scroll_to_ele(selector=self._event, uiautomatorclassname='android.widget.TextView', text='CHANGE')
        return IOSNativeBase(selector=self._event)

    @property
    def bet_builder_tab(self):
        return IOSNativeBase(selector=self._bet_builder_tab)

    @property
    def match_betting_select_team(self):
        self.scroll_to_ele(selector=self._match_betting_select_team, uiautomatorclassname='android.widget.TextView',
                           text='Select Team')
        return IOSNativeBase(selector=self._match_betting_select_team)

    @property
    def match_betting_time_period(self):
        self.scroll_to_ele(selector=self._match_betting_time_period, uiautomatorclassname='android.widget.TextView',
                           text='Time Period')
        return IOSNativeBase(selector=self._match_betting_time_period)

    @property
    def match_betting_add_to_bet_builder(self):
        return IOSNativeBase(selector=self._match_betting_add_to_bet_builder)

    @property
    def total_goals(self):
        total_goals = 'Total Goals'.upper() if tests.settings.brand == 'bma' else 'Total Goals'
        self.scroll_to_ele(selector=self._total_goals, uiautomatorclassname='android.widget.TextView',
                           text=total_goals)
        return IOSNativeBase(selector=self._total_goals)

    @property
    def total_goals_select_team(self):
        self.scroll_to_ele(selector=self._total_goals_select_team, uiautomatorclassname='android.widget.TextView',
                           text='Select Team')
        return IOSNativeBase(selector=self._total_goals_select_team)

    @property
    def total_goals_time_period(self):
        self.scroll_to_ele(selector=self._total_goals_time_period, uiautomatorclassname='android.widget.TextView',
                           text='Time Period')
        return IOSNativeBase(selector=self._total_goals_time_period)

    @property
    def total_goals_goals(self):
        self.scroll_to_ele(selector=self._total_goals_goals, uiautomatorclassname='android.widget.TextView',
                           text='Goals')
        return IOSNativeBase(selector=self._total_goals_goals)

    @property
    def total_goals_add_to_bet_builder(self):
        self.scroll_to_ele(selector=self._total_goals_add_to_bet_builder,
                           uiautomatorclassname='android.widget.Button',
                           text='ADD TO BET BUILDER')
        return IOSNativeBase(selector=self._total_goals_add_to_bet_builder)

    @property
    def total_corners(self):
        total_corners = 'Total Corners'.upper() if tests.settings.brand == 'bma' else 'Total Corners'
        self.scroll_to_ele(selector=self._total_corners, uiautomatorclassname='android.widget.TextView',
                           text=total_corners)
        return IOSNativeBase(selector=self._total_corners)

    @property
    def total_corners_select_team(self):
        self.scroll_to_ele(selector=self._total_corners_select_team, uiautomatorclassname='android.widget.TextView',
                           text='Select Team')
        return IOSNativeBase(selector=self._total_corners_select_team)

    @property
    def total_corners_time_period(self):
        self.scroll_to_ele(selector=self._total_corners_time_period, uiautomatorclassname='android.widget.TextView',
                           text='Time Period')
        return IOSNativeBase(selector=self._total_corners_time_period)

    @property
    def total_corners_corners(self):
        self.scroll_to_ele(selector=self._total_corners_time_period, uiautomatorclassname='android.widget.TextView',
                           text='Corners')
        return IOSNativeBase(selector=self._total_corners_corners)

    @property
    def total_corners_add_to_bet_builder(self):
        self.scroll_to_ele(selector=self._total_corners_add_to_bet_builder,
                           uiautomatorclassname='android.widget.Button',
                           text='ADD TO BET BUILDER')
        return IOSNativeBase(selector=self._total_corners_add_to_bet_builder)

    @property
    def bet_builder_place_bet(self):
        return IOSNativeBase(selector=self._bet_builder_place_bet)

    @property
    def place_bet(self):
        return IOSNativeBase(selector=self._place_bet, context=self._webview)

    @property
    def my_bets_footer_item(self):
        return IOSNativeBase(selector=self._my_bets_footer, context=self._webview)

    def add_selections_for_5_fold_acca(self):
        self.scroll_to_ele(selector=self._accrodian_bet_button,
                           uiautomatorclassname='android.widget.TextView',
                           text='CHANGE')
        for i in range(1, 4):
            if not self._find_element_by_selector(selector=self._accrodian_expanded):
                IOSNativeBase(selector=self._accrodian).click()
            bet_buttons = self._find_elements_by_selector(selector=self._accrodian_bet_button)
            odds = []
            for index, bet_button in enumerate(bet_buttons):
                if index % 2 == 0:
                    odds.append(IOSNativeBase(web_element=bet_button, timeout=10))
            if i == 1:
                odds.pop().click()
                self.quick_bet_add_to_betslip.click()
            screen_size = self._driver.get_window_rect()
            y = screen_size['height']
            for j in range(0, len(odds)):
                y_coordinate = odds[j]._we.location['y']
                if y_coordinate > y-y // 4:
                    self.scroll_in_direction(value=50)
                if y_coordinate < y // 3:
                    self.scroll_in_direction(value=-400)
                odds[j].click()
            self.scroll_in_direction(value=400)

    @property
    def bet_slip_odds_boost_ok_button(self):
        return IOSNativeBase(selector=self._bet_slip_odds_boost_ok_button, context=self._webview)

    @property
    def module_ribbon(self):
        return IOSNativeBase(selector=self._module_ribbon)






