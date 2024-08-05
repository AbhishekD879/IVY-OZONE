import pytest
from dateutil.parser import parse
from tests.Common import Common
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot settle bets on prod
# @pytest.mark.hl
@pytest.mark.bet_history
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C28147_Verify_Bet_Details_of_Lotto_bets(Common):
    """
    TR_ID: C28147
    NAME: Verify Bet Details of Lotto bets
    PRECONDITIONS: 1. User should be logged in to view their Settled Bets.
    PRECONDITIONS: 2. User should have few pending/win/lose/cancelled bets on Pools i.e. user should place bets on Football Jackpot, which should be settled after that
    PRECONDITIONS: To trigger pending/win/lose/cancelled bets on TST2: http://backoffice-tst2.coral.co.uk/office > Admin> Queries > Lottery bet
    PRECONDITIONS: NOTE: For all configurations on STG2 environment contact UAT team
    """
    keep_browser_open = True
    bet_amount = 0.1

    def verify_bet_status(self, bet_id: str, bet_status: str, page: str):
        """
        Verify bet status badge.
        :param bet_id: specifies bet for which status should be verified
        :param bet_status: specifies expected status
        :param page: specifies page on which bet status should be verified
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if page == 'Settled Bets':
            if self.device_type == 'desktop':
                self.site.open_my_bets_settled_bets()
            tab_content = self.site.bet_history.tab_content
        else:
            tab_content = self.site.account_history.tab_content

        lotto_opened = tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        self.assertTrue(lotto_opened, msg='Lotto tab is not opened')
        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No Lotto bets found')

        lotto_bet = None
        for name, bet in bets.items():
            if bet.bet_receipt_info.bet_id == bet_id:
                lotto_bet = bet
                self.assertEqual(bet.status, bet_status, msg=f'Bet status "{bet.status}" '
                                                             f'is not the same as expected "{bet_status}"')
                break
        self.assertTrue(lotto_bet, msg=f'No bet status "{bet_status}" for bet, current "{lotto_bet}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: User should be logged in to view their Settled Bets.
        DESCRIPTION: User should have few pending/win/lose/cancelled bets on Lotto i.e. user should place bets on Lotto, which should be settled after that
        """
        self.site.login(async_close_dialogs=False)

        self.site.open_sport(name='LOTTO')
        self.site.wait_content_state(state_name='LOTTO')

        self.__class__.lotto_name = self.site.lotto.tab_content.info_panel.lottery_name
        bet_until_time = self.site.lotto.tab_content.info_panel.bet_until_time
        lotto_time = self.get_date_time_formatted_string(time_format='%d.%m %-I:%M %p',
                                                         date_time_obj=parse(bet_until_time))

        self._logger.debug(f'Got formatted date "{lotto_time}" from "{bet_until_time}"')
        tab_content = self.site.lotto.tab_content
        for bet_number in range(8):
            lucky_buttons = tab_content.lucky_buttons.items_as_ordered_dict
            self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
            lucky_buttons['Lucky 5'].click()
            number_selectors = tab_content.number_selectors.items_as_ordered_dict
            self.assertTrue(number_selectors, msg='Number selectors are not found')
            self.__class__.selected_numbers = [number_text.split(' ')[1] for number_text, number in
                                               number_selectors.items()]

            tab_content.bet_amount.value = self.bet_amount
            tab_content.place_bet.click()
            tab_content.confirm_bet.click()
            expected_bet_time = self.get_date_time_formatted_string(time_format=self.time_format_pattern)
            if tests.location == 'IDE':
                utcoffset = -3
            else:
                # for some reasons, there is 61-min difference on CI runs for convert_time_to_local here.
                # it's all ok on ui with no issues.
                # hardcoded it due to no luck during debug and as test was constantly failing for the last year.
                utcoffset = -61
            self.__class__.bet_time = self.convert_time_to_local(date_time_str=expected_bet_time,
                                                                 ui_format_pattern=self.time_format_pattern,
                                                                 ob_format_pattern=self.time_format_pattern,
                                                                 utcoffset=utcoffset)

            self.site.wait_content_state('LottoBetReceipt')

            self.site.lotto_receipt.tab_content.section_list.done_button.click()

        self.site.open_my_bets_open_bets()
        lotto_opened = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        self.assertTrue(lotto_opened, msg='Lotto tab is not opened')
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No Lotto bets found')

        self.__class__.sub_ids = [bet.bet_receipt_info.bet_id for _, bet in bets.items()]

    def test_001_navigate_to_bet_history_tab_on_my_bets_page_for_mobile(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab on 'My Bets' page (for mobile)
        EXPECTED: * 'Settled Bets' page/tab is opened
        EXPECTED: * Pending/win/lose/cancelled/cashed out bet sections are present
        """
        self.site.open_my_bets_settled_bets()

    def test_002_trigger_the_situation_of_winning_a_bet_and_verify_bet_with_status_win_in_bet_history(self):
        """
        DESCRIPTION: Trigger the situation of Winning a bet and verify bet with status 'Win' in Settled Bets
        EXPECTED: Bet with status 'Win' should be present in Settled Bets, bet details are correct
        """
        bet_id = self.sub_ids[0]
        self.ob_config.settle_lotto_bet(bet_sub_id=bet_id, winnings=80)
        self.verify_bet_status(bet_id=bet_id, bet_status=vec.betslip.WON_STAKE, page='Settled Bets')

    def test_003_go_to_lotto_sort_filter_verify_bet_details_and_check_if_bet_details_are_same_as_inob_backofficesystem(self):
        """
        DESCRIPTION: Go to 'Lotto' sort filter -> verify bet details and check if bet details are same as in **OB Backoffice** system
        EXPECTED: Bet details are shown:
        EXPECTED: * Lottery Type in the header of the Individual Lotto Bets
        EXPECTED: * Result : pending/won/lost/cancelled/cashed out
        EXPECTED: * User's picks : X, x, x, x, x (this section must be repeated as many separate draws the user selected for the bet)
        EXPECTED: * Draw Type : e.g. Monday Draw
        EXPECTED: * Draw Date : date of draw
        EXPECTED: * Stake : stake value
        EXPECTED: * Bet placed at : date of lotto bet placement
        EXPECTED: * Bet Receipt #
        EXPECTED: * Stake: stake value
        EXPECTED: * Returns Details : returns value
        """
        lotto_opened = self.site.bet_history.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        self.assertTrue(lotto_opened, msg='Lotto tab is not opened')

        bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict.values()
        self.assertTrue(bets, msg='No Lotto bets found')

        last_bet = list(bets)[0]  # Most recent bet, displayed first on Settled Bets page

        balls = last_bet.balls.items_as_ordered_dict
        self.assertTrue(balls, msg='No balls found')
        balls_numbers = list(balls.keys())
        self.assertListEqual(self.selected_numbers, balls_numbers)

        stake = last_bet.stake.stake_value
        self.assertEqual(float(stake), float(self.bet_amount),
                         msg=f'Stake amount "{stake}" does not match expected bet amount "{self.bet_amount}"')
        bet_receipt = last_bet.bet_receipt_info.bet_receipt.value
        self.assertTrue(bet_receipt, msg='Bet receipt id was not found')
        bet_date = last_bet.bet_receipt_info.date.text
        self.assertTrue(bet_date, msg='Bet date was not found')
        self.assertEqual(bet_date, self.bet_time,
                         msg=f'Incorrect bet placement time is displayed. Actual: "{bet_date}". Expected: "{self.bet_time}"')

    def test_004_trigger_the_situation_of_losing_a_bet_and_verify_bet_with_status_lost_in_bet_history(self):
        """
        DESCRIPTION: Trigger the situation of  Losing a bet and verify bet with  'Lost' in Settled Bets
        EXPECTED: Bet with status 'Lost' should be present in Settled Bets, bet details are correct
        """
        bet_id = self.sub_ids[1]
        self.ob_config.settle_lotto_bet(bet_sub_id=bet_id, winnings=0)
        self.verify_bet_status(bet_id=bet_id, bet_status=vec.betslip.LOST_STAKE, page='Settled Bets')

    def test_005_trigger_the_situation_of_canceling_a_bet_and_verify_bet_with_void_in_bet_history(self):
        """
        DESCRIPTION: Trigger the situation of  Canceling a bet and verify bet with  'Void' in Settled Bets
        EXPECTED: Bet with status 'Void' should be present in Settled Bets, bet details are correct
        """
        bet_id = self.sub_ids[2]
        self.ob_config.settle_lotto_bet(bet_sub_id=bet_id, refund=0.01)
        self.verify_bet_status(bet_id=bet_id, bet_status=vec.betslip.CANCELLED_STAKE, page='Settled Bets')

    def test_006_trigger_the_situation_of_making_a_bet_void_and_verify_bet_with_cancelled_in_bet_history(self):
        """
        DESCRIPTION: Trigger the situation of  making a bet Void and verify bet with  'Void' in Settled Bets
        EXPECTED: Bet with status 'Void' should be present in Settled Bets, bet details are correct
        """
        bet_id = self.sub_ids[3]
        self.ob_config.settle_lotto_bet(bet_sub_id=bet_id, submit_name='CancelBet')
        self.verify_bet_status(bet_id=bet_id, bet_status=vec.betslip.CANCELLED_STAKE, page='Settled Bets')
