import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.reg165_fix
@vtest
class Test_C2604447_Betslip_Widget_Display_on_Desktop(BaseBetSlipTest):
    """
    TR_ID: C2604447
    VOL_ID: C9697596
    NAME: Betslip Widget Display on Desktop
    DESCRIPTION: This test case verifies view of BetSlip widget displaying with no added selections on Desktop version
    PRECONDITIONS: Desktop
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify CashOut tab configuration in CMS
        """
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        self.__class__.is_cashout_tab_enabled = cashout_cms.get('isCashOutTabEnabled')

    def test_001_load_oxygen_app_on_desktop_device(self):
        """
        DESCRIPTION: Load Oxygen app on desktop device
        EXPECTED: - Homepage is opened
        EXPECTED: -  Bet Slip widget is located at the top of last column
        EXPECTED: -  Bet Slip widget contains:
        EXPECTED: * 'BETSLIP' header
        EXPECTED: * Tabs: 'BETSLIP' (selected by default); 'MY BETS'
        EXPECTED: * Message "Your betslip is empty" at the top
        EXPECTED: * and for CORAL message below "Please add one or more selections to place a bet" displayed within Betslip content area
        """
        self.__class__.betslip_widget_name = self.cms_config.constants.BETSLIP_WIDGET_NAME
        self.assertEquals(self.betslip_widget_name, self.site.right_column.items_names[0],
                          msg=f'"{self.betslip_widget_name}" widget is not located at the top of right column')

        self.__class__.betslip_widget = self.site.right_column.bet_slip_widget

        actual_tab_menu = self.get_betslip_content().betslip_tabs.items_names
        for tab in self.required_bet_slip_tabs:
            self.assertTrue(tab in actual_tab_menu,
                            msg=f'"{tab}" tab was not found in right column of "{self.betslip_widget_name}" widget section')

        bet_slip_tab = self.required_bet_slip_tabs[0]
        actual_selected_tab = self.get_betslip_content().name
        self.assertEquals(bet_slip_tab, actual_selected_tab,
                          msg=f'"{bet_slip_tab}" tab is not selected by default, instead "{actual_selected_tab}" is')

        actual_message = self.get_betslip_content().no_selections_title
        self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual title message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

        if self.brand != 'ladbrokes':
            actual_message = self.get_betslip_content().no_selections_message
            self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_MSG,
                             msg=f'Actual body message "{actual_message}" != Expected "{vec.betslip.NO_SELECTIONS_MSG}"')

    def test_002_tap_my_bets_tab(self):
        """
        DESCRIPTION: Tap 'MY BETS' tab
        EXPECTED: New tabs are visible:
        EXPECTED: * 'CASH OUT' (selected by default)
        EXPECTED: * 'OPEN BETS'
        EXPECTED: * 'SETTLED BETS'
        EXPECTED: ** Coral only
        EXPECTED: * 'SHOP BETS'
        """
        self.site.open_my_bets()
        tabs = self.site.betslip.tabs_menu.items_names
        self.assertTrue(tabs, msg='Tabs are not found')
        expected_tabs = [vec.bet_history.CASH_OUT_TAB_NAME,
                         vec.bet_history.OPEN_BETS_TAB_NAME,
                         vec.bet_history.SETTLED_BETS_TAB_NAME,
                         vec.bet_history.IN_SHOP_BETS_TAB_NAME]
        for tab in tabs:
            self.assertIn(tab, expected_tabs,
                          msg=f'Tab "{tab}" is not found in "{expected_tabs}"')

        if self.is_cashout_tab_enabled:
            self.site.betslip.tabs_menu.items_as_ordered_dict.get(vec.bet_history.CASH_OUT_TAB_NAME).click()
            self.assertTrue(self.site.betslip.tabs_menu.items_as_ordered_dict.get(vec.bet_history.CASH_OUT_TAB_NAME).is_selected(),
                            msg=f'Tab "{vec.bet_history.CASH_OUT_TAB_NAME}" is not selected by default')
        else:
            self.assertTrue(
                self.site.betslip.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).is_selected(),
                msg=f'Tab "{vec.bet_history.OPEN_BETS_TAB_NAME}" is not selected by default')

        self.__class__.widget_tabs = self.site.betslip.tabs_menu.items_as_ordered_dict

    def test_003_tap_cash_out_tab(self):
        """
        DESCRIPTION: Tap 'CASH OUT' tab
        EXPECTED: 'CASH OUT' tab is displayed
        EXPECTED: **Coral**
        EXPECTED: "Please log in to see your cash out bets." message is displayed
        EXPECTED: 'Log In' button is displayed under the message
        EXPECTED: **Ladbrokes**
        EXPECTED: "Your cash out bets will appear here, Please login to view." message is displayed
        """
        if self.is_cashout_tab_enabled:
            self.widget_tabs.get(vec.bet_history.CASH_OUT_TAB_NAME).click()
            current_text = self.site.cashout.tab_content.please_login_text
            self.assertEqual(current_text, vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE,
                             msg=f'Actual message "{current_text}" != Expected "{vec.bet_history.CASHOUT_PLEASE_LOGIN_MESSAGE}"')
            if self.brand != 'ladbrokes':
                self.assertTrue(self.site.cashout.tab_content.has_login_button(),
                                msg=f'Tab "{vec.bet_history.CASH_OUT_TAB_NAME}" does not contain "Log In" button')

    def test_004_tap_open_bets_out_tab(self):
        """
        DESCRIPTION: Tap 'OPEN BETS' tab
        EXPECTED: 'OPEN BETS' tab is displayed
        EXPECTED: **Coral**
        EXPECTED: "Please log in to see your open bets." message is displayed
        EXPECTED: 'Log In' button is displayed under the message
        EXPECTED: **Ladbrokes**
        EXPECTED: "Your open bets will appear here, Please login to view." message is displayed
        """
        self.widget_tabs.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        current_text = self.site.open_bets.tab_content.please_login_text
        self.assertEqual(current_text, vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual message "{current_text}" != Expected "{vec.bet_history.OPEN_BETS_PLEASE_LOGIN_MESSAGE}"')
        if self.brand != 'ladbrokes':
            self.assertTrue(self.site.open_bets.tab_content.has_login_button(),
                            msg=f'Tab "{vec.bet_history.OPEN_BETS_TAB_NAME}" does not contain "Log In" button')

    def test_005_tap_settled_bets_out_tab(self):
        """
        DESCRIPTION: Tap 'SETTLED BETS' tab
        EXPECTED: 'SETTLED BETS' tab is displayed
        EXPECTED: **Coral**
        EXPECTED: "Please log in to see your settled bets." message is displayed
        EXPECTED: 'Log In' button is displayed under the message
        EXPECTED: **Ladbrokes**
        EXPECTED: "Your settled bets will appear here, Please login to view." message is displayed
        """
        self.widget_tabs.get(vec.bet_history.SETTLED_BETS_TAB_NAME).click()
        current_text = self.site.bet_history.tab_content.please_login_text
        self.assertEqual(current_text, vec.bet_history.SETTLED_BETS_PLEASE_LOGIN_MESSAGE,
                         msg=f'Actual message "{current_text}" != Expected "{vec.bet_history.SETTLED_BETS_PLEASE_LOGIN_MESSAGE}"')
        if self.brand != 'ladbrokes':
            self.assertTrue(self.site.bet_history.tab_content.has_login_button(),
                            msg=f'Tab "{vec.bet_history.SETTLED_BETS_TAB_NAME}" does not contain "Log In" button')
