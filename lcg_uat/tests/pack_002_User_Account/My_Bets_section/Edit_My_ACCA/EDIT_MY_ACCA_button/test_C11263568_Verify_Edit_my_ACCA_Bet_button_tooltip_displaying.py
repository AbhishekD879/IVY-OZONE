import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  cannot suspend events in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.desktop
@vtest
class Test_C11263568_Verify_Edit_my_ACCA_Bet_button_tooltip_displaying(BaseCashOutTest):
    """
    TR_ID: C11263568
    NAME: Verify 'Edit my ACCA/Bet' button tooltip displaying
    DESCRIPTION: Test case verified Edit my Acca tooltip appearing on Open Bets/Cash Out
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place a few Acca bets
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    """
    keep_browser_open = True
    selection_ids = []
    event_names = []
    event_ids = []

    def get_bet_with_my_acca_edit(self, open_bets=True):
        """
        Get bet with My ACCA edit functionality
        """
        if open_bets:
            if self.device_type == 'mobile':
                self.site.open_my_bets_open_bets()
            else:
                self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
            self.site.wait_content_state('open-bets')
            _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE, event_names=self.event_names, number_of_bets=1)
        else:
            if self.device_type == 'mobile':
                self.site.open_my_bets_cashout()
            else:
                self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.CASH_OUT_TAB_NAME).click()
            _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE, event_names=self.event_names,
                number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event_names}"')
        return bet

    def navigate_to_mybets(self):
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2])
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6])
        self.site.wait_content_state_changed()
        actual_history_menu = list(self.site.right_menu.items_as_ordered_dict)
        self.assertEqual(actual_history_menu, vec.bma.HISTORY_MENU_ITEMS,
                         msg=f'Actual items: "{actual_history_menu}" are not equal with the'
                             f'Expected items: "{vec.bma.HISTORY_MENU_ITEMS}"')
        self.site.right_menu.click_item(vec.bma.HISTORY_MENU_ITEMS[0])
        self.site.wait_content_state('bet-history')
        self.site.wait_content_state_changed()

    def test_000_preconditions(self):
        """
        Description: Enable My ACCA feature toggle in CMS
        Description: CMS -> System Configuration -> Structure -> EMA -> Enabled
        Description: Login into App
        Description: Place a few Acca bets
        """
        if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)
        for i in range(0, 3):
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.event_ids.append(event.event_id)
            self.event_names.append(event.ss_response['event']['name'])
            self.selection_ids.append(list(event.selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)
        self.open_betslip_with_selections(self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.navigate_to_mybets()

    def test_001_navigate_to_open_bets_pageverify_the_tooltip_is_shown_below_the_edit_my_accabet_button_if_visit_open_bets_page_after_the_login(self):
        """
        DESCRIPTION: Navigate to Open Bets page
        DESCRIPTION: Verify the tooltip is shown below the Edit my Acca/Bet button if visit Open Bets page after the login
        EXPECTED: Tooltip with text 'Now you can remove selections from your acca to keep your bet alive' is shown below the first "Edit my Acca/Bet" button
        """
        self.__class__.bet = self.get_bet_with_my_acca_edit(open_bets=True)
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is displayed')
        self.assertTrue(self.bet.has_acca_tooltip(), msg='acca tooltip is not present')
        self.assertEquals(self.bet.acca_tooltip_text.text, vec.app.TOOLTIP.edit_my_acca,
                          msg=f'Acca tooltip text "{self.bet.acca_tooltip_text.text}" is not the same as expected "{vec.app.TOOLTIP.edit_my_acca}"')

    def test_002_tap_the_screen_verify_the_tooltip_disappears(self):
        """
        DESCRIPTION: Tap the screen. Verify the tooltip disappears
        EXPECTED: Tooltip disappears
        """
        self.bet.stake.click()
        self.assertFalse(self.bet.has_acca_tooltip(expected_result=False), msg='acca tooltip is present')

    def test_003_refresh_the_page_verify_the_tooltip_isnt_shown(self):
        """
        DESCRIPTION: Refresh the page. Verify the tooltip isn't shown
        EXPECTED: Tooltip isn't shown
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state_changed()
        self.assertFalse(self.bet.has_acca_tooltip(expected_result=False), msg='acca tooltip is present')

    def test_004_suspend_one_of_the_events_from_the_accarelogin_and_verify_the_tooltip_is_not_shown(self):
        """
        DESCRIPTION: Suspend one of the events from the acca.
        DESCRIPTION: Relogin and verify the tooltip is not shown.
        EXPECTED: Tooltip isn't shown if the Edit Acca button is disabled.
        """
        self.ob_config.change_event_state(event_id=self.event_ids[0], displayed=True, active=False)
        sleep(2)
        self.site.logout()
        self.site.wait_content_state('homepage')
        self.site.login(self.username)
        self.navigate_to_mybets()
        bet = self.get_bet_with_my_acca_edit(open_bets=True)
        self.assertFalse(bet.edit_my_acca_button.is_enabled(expected_result=False),
                         msg=f'"{vec.EMA.EDIT_MY_BET}" button is enabled')
        self.assertFalse(bet.has_acca_tooltip(expected_result=False), msg='acca tooltip is present')

    def test_005_navigate_to_cash_out_pagerelogin_and_verify_the_tooltip_is_shown_below_the_edit_my_accabet_button_if_visit_cash_out_page_after_the_login(self):
        """
        DESCRIPTION: Navigate to Cash Out page
        DESCRIPTION: Relogin and verify the tooltip is shown below the Edit my Acca/Bet button if visit Cash Out page after the login
        EXPECTED: Tooltip with text 'Now you can remove selections from your acca to keep your bet alive' is shown below the first "Edit my Acca/Bet" button
        EXPECTED: OX 105:
        EXPECTED: Tooltip is not shown - rest of the steps should be removed and are not relevant
        """
        if self.brand == 'bma':
            self.site.logout()
            self.site.wait_content_state('homepage')
            self.site.login(self.username)
            self.navigate_to_mybets()
            bet = self.get_bet_with_my_acca_edit(open_bets=False)
            self.assertFalse(bet.edit_my_acca_button.is_enabled(expected_result=False),
                             msg=f'"{vec.EMA.EDIT_MY_BET}" button is enabled')
            self.assertFalse(bet.has_acca_tooltip(expected_result=False), msg='acca tooltip is present')

    def test_006_tap_the_screen_verify_the_tooltip_disappears(self):
        """
        DESCRIPTION: Tap the screen. Verify the tooltip disappears
        EXPECTED: Tooltip disappears
        """
        # step not applicable

    def test_007_refresh_the_page_verify_the_tooltip_isnt_shown(self):
        """
        DESCRIPTION: Refresh the page. Verify the tooltip isn't shown
        EXPECTED: Tooltip isn't shown
        """
        # step not applicable

    def test_008_suspend_one_of_the_events_from_the_accarelogin_and_verify_the_tooltip_is_not_shown(self):
        """
        DESCRIPTION: Suspend one of the events from the acca.
        DESCRIPTION: Relogin and verify the tooltip is not shown.
        EXPECTED: Tooltip isn't shown if the Edit Acca button is disabled.
        """
        # step not applicable
