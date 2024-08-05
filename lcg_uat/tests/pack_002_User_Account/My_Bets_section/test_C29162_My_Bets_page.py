import pytest
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C29162_My_Bets_page(Common):
    """
    TR_ID: C29162
    NAME: My Bets page
    DESCRIPTION: This test case verifies My Bets page
    DESCRIPTION: Design:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f0e0920f1230172b7f095
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f22d544fe0d63959b3162
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.login()
        self.site.wait_content_state('HomePage')

    def test_002_tap_my_bets_button(self):
        """
        DESCRIPTION: Tap 'My bets' button
        EXPECTED: * Page with header 'My Bets' and Back button is opened
        EXPECTED: * 'Cash Out'(if available), 'Open Bets' and 'Settled bets' tabs are present
        EXPECTED: * 'Open bets' tab is selected by default - Available from OX99
        """
        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                self.site.header.right_menu_button.avatar_icon.click()
                self.site.right_menu.click_item(vec.bet_history.TAB_TITLE)
                self.assertTrue(self.site.has_back_button, msg='Back button is not displayed')
                actual_my_bets_tabs = self.site.open_bets.tabs_menu.current
            else:
                self.site.open_my_bets()
                self.site.open_my_bets_open_bets()
                actual_my_bets_tabs = self.site.betslip.tabs_menu.current
            self.assertEqual(actual_my_bets_tabs, vec.bet_history.OPEN_BETS_TAB_NAME,
                             msg=f'Actual text: "{actual_my_bets_tabs}" is not as'
                                 f'Expected text: "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
        else:
            if self.device_type == 'mobile':
                self.site.header.my_bets.click()
                self.assertTrue(self.site.has_back_button, msg='Back button is not displayed')
                actual_my_bets_tabs = self.site.open_bets.tabs_menu.current
                self.assertEqual(actual_my_bets_tabs, vec.bet_history.OPEN_BETS_TAB_NAME,
                                 msg=f'Actual text: "{actual_my_bets_tabs}" is not as'
                                     f'Expected text: "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
            else:
                self.site.open_my_bets()
                actual_my_bets_tabs = self.site.cashout.tab_content.grouping_buttons.current
                self.assertEqual(actual_my_bets_tabs, vec.bet_history.CASH_OUT_TAB_NAME,
                                 msg=f'Actual text: "{actual_my_bets_tabs}" is not as'
                                     f'Expected text: "{vec.bet_history.CASH_OUT_TAB_NAME}"')

    def test_003_navigate_through_tabs(self):
        """
        DESCRIPTION: Navigate through tabs
        EXPECTED: 'Cash Out(if available)', 'Open Bets' and 'Settled bets' tabs are opened, information is displayed correctly.
        """
        self.site.open_my_bets_open_bets()
        result = wait_for_result(lambda: self.site.open_bets.tab_content.grouping_buttons.current == vec.bma.SPORTS,
                                 name=f'"{vec.bma.SPORTS}" to became active',
                                 timeout=2)
        self.assertTrue(result, msg=f'{vec.bma.SPORTS} sorting type is not selected by default')
        self.site.open_my_bets_settled_bets()
        result = wait_for_result(lambda: self.site.bet_history.tab_content.grouping_buttons.current == vec.bma.SPORTS,
                                 name=f'"{vec.bma.SPORTS}" to became active',
                                 timeout=2)
        self.assertTrue(result, msg=f'{vec.bma.SPORTS} sorting type is not selected by default')
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            cash_out_bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
            if len(cash_out_bets) > 0:
                self.assertTrue(cash_out_bets, msg='Cashout tab has no bets to display.')
            else:
                cash_out_text = self.site.cashout.tab_content.accordions_list.no_bets_text
                self.assertEqual(cash_out_text, vec.bet_history.NO_CASHOUT_BETS,
                                 msg=f'Actual text: "{cash_out_text}" is not equal with the'
                                     f'Expected text: "{vec.bet_history.NO_CASHOUT_BETS}"')

    def test_004_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User gets back to page he/she navigated from
        """
        if self.device == 'mobile':
            self.site.back_button.click()
            actual_my_bets_tabs = self.site.open_bets.tabs_menu.current
            self.assertEqual(actual_my_bets_tabs, vec.bet_history.OPEN_BETS_TAB_NAME,
                             msg=f'Actual text: "{actual_my_bets_tabs}" is not as'
                                 f'Expected text: "{vec.bet_history.OPEN_BETS_TAB_NAME}"')
