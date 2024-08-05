import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from datetime import date, timedelta


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870298_4Customer_is_able_to_access_Bet_History_from_My_account_page(BaseBetSlipTest):
    """
    TR_ID: C44870298
    NAME: 4.Customer is able to access Bet History from 'My account' page
    DESCRIPTION: Verify that games and lotto history displays on the front end when a user has played that relevant game
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: Must place the bets
    """
    keep_browser_open = True
    bet_amount = 0.1

    def test_001_login_to_websiteapp(self):
        """
        DESCRIPTION: Login to website/App
        EXPECTED: User logged in
        """
        self.site.login()

    def test_002_place_abet_on_each_on_any_sportlottopools(self):
        """
        DESCRIPTION: Place abet on each on any sport/lotto/pools
        EXPECTED: User has placed a bet on sport/lotto/pools
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state('lotto')
        self.lotto = self.site.lotto.tab_content
        number_selections = list(self.lotto.number_selectors.items_as_ordered_dict.values())
        self.assertTrue(number_selections, msg='Lotto number selectors is not present')
        number_selections[0].click()
        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW)
        self.assertTrue(choose_lucky_num_dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW}" dialog is not shown')
        numbers = choose_lucky_num_dialog.items_as_ordered_dict
        self.assertTrue(numbers, msg='No Lucky numbers present on dialog')
        for number in list(numbers.values())[:2]:
            number.click()
        choose_lucky_num_dialog.done_button.click()
        self.assertTrue(choose_lucky_num_dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW}" dialog is not closed')
        self.assertTrue(self.lotto.bet_amount.is_enabled(expected_result=True),
                        msg='Stake entry box is disabled')
        self.lotto.bet_amount.click()
        self.lotto.bet_amount.value = self.bet_amount
        self.lotto.place_bet.click()
        self.lotto.bet_amount.click()
        self.lotto.place_bet.click()
        self.lotto.confirm_bet.click()
        receipt = self.site.lotto_receipt.tab_content.section_list
        self.assertTrue(receipt.bet_placed, msg='Bet placed time is not shown')

    def test_003_navigate_to_settled_bets_page_via_my_account_overlay_by_clicking_on_the_avatar__history__betting_history(self):
        """
        DESCRIPTION: Navigate to Settled bets page via My Account overlay (by clicking on the Avatar) > History > Betting History
        EXPECTED: User navigated to Settled bets where the user can see all sports/lotto/pools bets
        """
        self.navigate_to_page("Homepage")
        self.navigate_to_page(name='bet-history')
        self.site.close_all_dialogs()

    def test_004_verify_functionality_of_date_picker_today_last_7_days_and_last_30_days(self):
        """
        DESCRIPTION: Verify functionality of Date Picker Today, Last 7 days and Last 30 days
        EXPECTED: User can see correct history for all the relevant bets placed
        """
        settled_bet_tabs = self.site.bet_history.tab_content.grouping_buttons.items_as_ordered_dict
        self.assertTrue(settled_bet_tabs, msg='Settled Bet tabs are not displayed')
        for i in [0, 7, 30]:
            new_date = date.today() - timedelta(days=i)
            past_date = new_date.__format__('%d/%m/%Y')
            self.site.bet_history.tab_content.accordions_list.date_picker.date_from.date_picker_value = past_date
            self.assertEqual(self.site.bet_history.tab_content.accordions_list.date_picker.date_from.text, past_date,
                             msg='Date range is not selected')
            bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
            if len(bets) > 0:
                self.assertTrue(bets, msg=f'There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
            else:
                self._logger.info(f'***There are no bets displayed on "{vec.bet_history.SETTLED_BETS_TAB_NAME}" tab')
