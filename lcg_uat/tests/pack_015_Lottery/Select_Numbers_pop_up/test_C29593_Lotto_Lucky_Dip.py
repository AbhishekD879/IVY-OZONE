import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_placement
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.login
@vtest
class Test_C29593_Lotto_Lucky_Dip(BaseBetSlipTest):
    """
    TR_ID: C29593
    NAME: Verify Lotto betting using "Lucky dip" functionality
    DESCRIPTION: This test case verifies Lucky Dip buttons displaying and functionality
    """
    keep_browser_open = True
    selected_numbers = []
    bet_amount = 0.1

    def test_000_login(self):
        """
        DESCRIPTION: Login as user that have enough money to place bet
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_001_open_lotto(self):
        """
        DESCRIPTION: Go to Lotto
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state('lotto')
        self._logger.info('*** Current Lotto is: "%s"' % self.site.lotto.tab_content.info_panel.lottery_name)

    def test_002_choose_number(self):
        """
        DESCRIPTION: Select lucky numbers using "Lucky Dip" functionality
        """
        lucky_buttons = list(self.site.lotto.tab_content.lucky_buttons.items_as_ordered_dict.values())
        self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
        lucky_buttons[0].click()
        for name, item in self.site.lotto.tab_content.number_selectors.items_as_ordered_dict.items():
            self._logger.debug('*** Text on button is: "%s"' % name)
            if '-' not in name:
                self.__class__.selected_numbers.append(name)
        self.assertTrue(self.selected_numbers, msg='No selected numbers are found')
        self._logger.debug('*** Selected numbers are: "%s"' '", "'.join(self.selected_numbers))

    def test_003_verify_pop_up(self):
        """
        DESCRIPTION: Verify that previously selected numbers are active on 'Choose Your Lucky Numbers Below' dialog
        """
        number_selections = list(self.site.lotto.tab_content.number_selectors.items_as_ordered_dict.values())
        self.assertTrue(number_selections, msg='Lotto number selectors is not present')
        number_selections[-1].click()
        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW, timeout=5)
        self.assertTrue(choose_lucky_num_dialog, msg='"Choose Your Lucky Numbers Below" pop up is not found')
        lotto_selections = choose_lucky_num_dialog.items_as_ordered_dict
        self.assertTrue(lotto_selections, msg=f'There is no lotto buttons')
        available_selections = len(lotto_selections)
        self._logger.debug('Number of available selections is: %s' % available_selections)

        for item in self.selected_numbers:
            item = item.split(' ')[1]
            self._logger.info('*** Number is is: "%s"' % item)
            self.assertTrue(lotto_selections[item].is_selected())
        choose_lucky_num_dialog.done_button.click()
        choose_lucky_num_dialog.wait_dialog_closed()

    def test_004_make_a_bet(self):
        """
        DESCRIPTION: Make a bet
        """
        lotto_tab_content = self.site.lotto.tab_content
        lotto_tab_content.bet_amount.value = self.bet_amount
        self.assertTrue(lotto_tab_content.place_bet.is_enabled(timeout=2), msg='"Place Bet" button is disabled')
        input_text = lotto_tab_content.bet_amount.value
        btn_text = lotto_tab_content.place_bet.name.lstrip()
        self.assertTrue(input_text in btn_text,
                        msg=f'Bet amount on "Place bet" button "{btn_text}" is not the same as entered "{input_text}"')
        lotto_tab_content.place_bet.click()
        lotto_tab_content.confirm_bet.click()

    def test_005_verify_receipt(self):
        """
        DESCRIPTION: Verify Receipt
        """
        receipt = self.site.lotto_receipt.tab_content.section_list
        self.assertTrue(receipt.name, msg='Receipt Name is not shown')
        self.assertTrue(receipt.event_name, msg='Event Name is not shown')
        self.assertTrue(receipt.bet_type, msg='Bet Type is not shown')
        self.assertTrue(receipt.bet_selections, msg='Bet Selections are not shown')
        self.assertTrue(receipt.bet_odds, msg='Bet Odds are not shown')
        self.assertTrue(receipt.bet_stake, msg='Bet Stake is not shown')
        self.assertTrue(receipt.total_stake, msg='Total Stake is not shown')
        self.assertTrue(receipt.potential_return, msg='Potential Return is not shown')
        self.assertTrue(receipt.bet_placed, msg='Bet placed time is not shown')

        self.site.lotto_receipt.tab_content.section_list.done_button.click()
