from random import choice

import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import tests
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.bet_placement
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.ob_smoke
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29588_Lottery_Place_Straight_Bet(BaseBetSlipTest):
    """
    TR_ID: C29588
    NAME: Place straight bets
    DESCRIPTION: This Test Case verifies placing straight bets on Lotteries.
    DESCRIPTION: **Jira Ticket: **
    DESCRIPTION: BMA-5831 Lottery - Place straight bets
    DESCRIPTION: BMA-7590 - Lotto Bet Receipt
    PRECONDITIONS: 1. Launch Invictus application
    PRECONDITIONS: To get a list of lotteries and draws use following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Lottery/X.XX/LotteryToDraw/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: **To verify data on Bet Receipt page: **
    """
    keep_browser_open = True
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Launch application and login
        EXPECTED: Site is launched
        EXPECTED: User is logged in to the site
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_001_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page
        EXPECTED: *   'Lotto' page is opened.
        EXPECTED: *   Stake entry box is disabled until at least one ball will be selected.
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state('lotto')
        self.__class__.lotto = self.site.lotto.tab_content
        self.assertFalse(self.lotto.bet_amount.is_enabled(expected_result=False),
                         msg='Stake entry box is enabled')
        lottery_name = self.lotto.info_panel.lottery_name
        self.__class__.lotto_name = lottery_name.title() if self.brand == 'ladbrokes' else lottery_name.upper()

    def test_002_select_any_numbers_using_select_numbers_pop_up_and_tap_done_button(self):
        """
        DESCRIPTION: Select any numbers using Select Numbers pop-up and tap 'Done' button
        EXPECTED: *   Selected numbers are displayed in number line in increasing order
        EXPECTED: *   Odds Section is displayed in one row with Straight Bet. By default if no numbers selected, the Odds value is equal to 'priceNum'/'priceDen' attribute values according to the attribute 'numberPicks=5' from SiteServer.
        EXPECTED: *   Value about Single Straight Bet is displayed before Stake entry box as '1x'.
        EXPECTED: *   Stake entry box is available to enter the bet amount. Default value within Stake entry box is "0.00" and has right alignment within field. Currency sign has left alignment.
        """
        number_selections = list(self.lotto.number_selectors.items_as_ordered_dict.values())
        self.assertTrue(number_selections, msg='Lotto number selectors is not present')
        number_selections[0].click()

        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW)
        self.assertTrue(choose_lucky_num_dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW}" dialog is not shown')
        numbers = choose_lucky_num_dialog.items_as_ordered_dict
        self.assertTrue(numbers, msg='No Lucky numbers present on dialog')
        for _, number in list(numbers.items())[:2]:
            number.click()

        choose_lucky_num_dialog.done_button.click()
        self.assertTrue(choose_lucky_num_dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW}" dialog is not closed')
        self.assertTrue(self.lotto.bet_amount.is_enabled(expected_result=True),
                        msg='Stake entry box is disabled')

    def test_003_tap_on_stake_entry_box(self):
        """
        DESCRIPTION: Tap on Stake entry box
        EXPECTED: Keypad is opened.
        """
        self.lotto.bet_amount.click()

    def test_004_enter_different_data_into_stake_entry_box_eg_numbers_special_characters_letters(self):
        """
        DESCRIPTION: Enter different data into Stake entry box (e.g. numbers, special characters, letters)
        EXPECTED: *   Only entered numbers are displayed within the Stake field.
        EXPECTED: *   It is impossible to enter letters (nothing happen while entering them).
        EXPECTED: *   It is impossible to enter special characters (nothing happen while entering them).
        EXPECTED: *   XXX,XXX,XXX,XXX.XX is the max value limitations for Stake field.
        EXPECTED: *   It is impossible to enter more than 12 digits and 2 decimals in Stake field.
        """
        self.lotto.bet_amount.value = "abc"
        self.assertEqual(self.lotto.bet_amount.value, '', msg='Letters added to stake box')
        self.lotto.bet_amount.value = "!£$%"
        self.assertEqual(self.lotto.bet_amount.value, '', msg='Special characters added to stake box')
        self.lotto.bet_amount.value = '999999999999.99'
        self.assertEqual(self.lotto.bet_amount.value, '999999999999.99',
                         msg='Max stake value exceeded')
        self.lotto.bet_amount.clear()
        result = wait_for_result(lambda: self.lotto.bet_amount.value == '',
                                 name=f'Empty input field',
                                 timeout=3)
        self.assertTrue(result, msg='Input field is not cleared')

    def test_005_verify_place_bet_for_button(self):
        """
        DESCRIPTION: Verify 'Place Bet for' button
        EXPECTED: *   'Place Bet for' button should be automaticaly update with the Total Stake of the bet entered into Stake entry box.
        EXPECTED: *   Appropriate currency symbol sould be displayed within 'Place Bet for' button.
        """
        self.lotto.bet_amount.value = self.bet_amount
        self.assertTrue(self.lotto.place_bet.is_enabled(),
                        msg='"Place Bet" button is disabled')
        input_text = self.lotto.bet_amount.value
        btn_text = self.lotto.place_bet.name.lstrip()
        self.assertTrue(input_text in btn_text,
                        msg=f'Bet amount on "Place bet btn" "{btn_text}" is not the same as entered one "{input_text}"')

    def test_006_tap_on_place_bet_for_button(self):
        """
        DESCRIPTION: Tap on 'Place Bet for' button
        EXPECTED: *   'Place Bet for' button label is changed to 'Confirm Bet?'.
        EXPECTED: *   'Place Bet for' button's color is changed to amber.
        """
        self.lotto.place_bet.click()
        self.assertTrue(self.lotto.confirm_bet.is_enabled(),
                        msg='"Place Bet" button is disabled')

    def test_007_tap_on_anywhere_within_the_page_except_confirm_button(self):
        """
        DESCRIPTION: Tap on anywhere within the page except 'Confirm?' button
        EXPECTED: *   'Confirm Bet?' button label is changed back to 'Place Bet for'.
        EXPECTED: *   'Confirm Bet?' button's color is changed back to green.
        """
        self.lotto.bet_amount.click()
        self.assertTrue(self.lotto.place_bet.is_enabled(), msg='"Place Bet" button is disabled')

    def test_008_repeat_step_6(self):
        """
        DESCRIPTION: Repeat step #6
        """
        self.lotto.place_bet.click()
        self.assertTrue(self.lotto.confirm_bet.is_enabled(),
                        msg='"Place Bet" button is disabled')

    def test_009_tap_on_confirm_bet_button(self):
        """
        DESCRIPTION: Tap on 'Confirm Bet?' button
        EXPECTED: 1.  Stake is placed successfully.
        EXPECTED: 2.  Bet Receipt is displayed with following items:
        EXPECTED: *   the Lottery product - e.g. 49's 6 Ball (note this is the Lotto product and the variation depending on selecting woth or without the bonus ball - 6 Ball or 7 Ball)
        EXPECTED: *    List of selected draws with Draw date and time (in one line for each draw). Time = 'drawAtTime' from SSResponse
        EXPECTED: *   Bet Type: e.g. "Match (3)" or "All Trebles"
        EXPECTED: *   Bet Selections: e.g. 1,2,3
        EXPECTED: *   Bet Odds: e.g. 600/1 or 601.0 (make sure you handle decimal and fractional)
        EXPECTED: *   Stake: e.g. £1.00 x 1
        EXPECTED: *   Separator
        EXPECTED: *   Total Stake
        EXPECTED: *   Potential return
        EXPECTED: *   Bet Placed: time and date of bet placement
        """
        self.lotto.confirm_bet.click()
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

    def test_010_verify_bet_selections_order(self):
        """
        DESCRIPTION: Verify bet selections order
        EXPECTED: Selected numbers are displayed in ascending
        """
        receipt = self.site.lotto_receipt.tab_content.section_list
        self.assertTrue(receipt.bet_selections, msg='Bet Selections are not shown')
        self.site.lotto_receipt.tab_content.section_list.done_button.click()

    def test_011_select_any_other_lottery_and_repeat_steps_2_9(self):
        """
        DESCRIPTION: Select any other Lottery and repeat steps #2-9
        """
        all_lottery = self.site.lotto.lotto_carousel.items_as_ordered_dict
        name = self.lotto_name.lower() if '49' in self.lotto_name and self.brand == 'ladbrokes' else self.lotto_name
        all_lottery.pop(name)
        if all_lottery:
            other_lottery = choice(list(all_lottery.values()))
            other_lottery.click()
            self.test_002_select_any_numbers_using_select_numbers_pop_up_and_tap_done_button()
            self.test_003_tap_on_stake_entry_box()
            self.test_004_enter_different_data_into_stake_entry_box_eg_numbers_special_characters_letters()
            self.test_005_verify_place_bet_for_button()
            self.test_006_tap_on_place_bet_for_button()
            self.test_007_tap_on_anywhere_within_the_page_except_confirm_button()
            self.test_008_repeat_step_6()
            self.test_009_tap_on_confirm_bet_button()
        else:
            self._logger.info('Just 1 lottery is available')
