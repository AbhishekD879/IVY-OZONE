import pytest
import re

import tests
import voltron.environments.constants as vec
from datetime import datetime
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C29215_Verify_Open_Bets_tab_for_Lottery(Common):
    """
    TR_ID: C29215
    NAME: Verify Open Bets tab for Lottery
    """
    keep_browser_open = True
    bet_amount = 0.1
    selected_numbers = None
    lotto_name = None
    draw_name = None
    lotto_time = None
    time_format_pattern = '%H:%M - %d %b'
    expected_bet_time = None

    def get_lotto_bet(self, draw_name, lotto_time=None):
        expected_bet_name = f'{draw_name} {lotto_time}' if lotto_time else f'{draw_name}'
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No Lotto bets found')
        bet = next(((bet_name, bet) for (bet_name, bet) in bets.items() if expected_bet_name in bet_name), ('', None))
        self.assertTrue(all(bet), msg=f'Bet "{expected_bet_name}" was not found')
        return bet

    def test_001_place_lotto_bet(self):
        """
        DESCRIPTION: Login as user that have enough money to place bet
        DESCRIPTION: Navigate to Lotto page
        DESCRIPTION: Select your numbers
        DESCRIPTION: Make a bet
        """
        self.site.login(async_close_dialogs=False)
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state(state_name='Lotto')

        lucky_buttons = self.site.lotto.tab_content.lucky_buttons.items_as_ordered_dict
        self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
        lucky_buttons['Lucky 5'].click()
        number_selectors = self.site.lotto.tab_content.number_selectors.items_as_ordered_dict
        self.assertTrue(number_selectors, msg='Number selectors are not found')
        self.__class__.selected_numbers = [number_text.split(' ')[1] for number_text, number in number_selectors.items()]

        lotto_tab_content = self.site.lotto.tab_content
        lotto_tab_content.bet_amount.value = self.bet_amount
        lotto_tab_content.place_bet.click()
        lotto_tab_content.confirm_bet.click()
        expected_bet_time = self.get_date_time_formatted_string(time_format=self.time_format_pattern)
        self.site.wait_content_state('LottoBetReceipt')

        if tests.location == 'IDE':
            utcoffset = -24
        else:
            # for some reasons, there is 61-min difference on CI runs for convert_time_to_local here.
            # it's all ok on ui with no issues.
            # hardcoded it due to no luck during debug and as test was constantly failing for the last year.
            utcoffset = -1
        self.__class__.expected_bet_date = self.convert_time_to_local(date_time_str=expected_bet_time,
                                                                      ui_format_pattern=self.time_format_pattern,
                                                                      ob_format_pattern=self.time_format_pattern,
                                                                      utcoffset=utcoffset)

        event_name = self.site.lotto_receipt.tab_content.section_list.event_name
        draw_name_match = re.match(r'^([\w \|]+).', event_name)
        self.assertTrue(draw_name_match, msg='Cannot get draw type from "%s"' % event_name)
        self.__class__.draw_name = draw_name_match.group(1)

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: 'My Bets' page/'Bet Slip' widget is opened
        EXPECTED: 'Open Bets' tab is shown next to 'Cash Out' tab
        """
        self.site.open_my_bets_open_bets()

    def test_003_navigate_to_lotto_filter_and_check_content_within_it(self):
        """
        DESCRIPTION: Navigate to 'Lotto' filter and check content within it
        EXPECTED: All '**Pending bets**' sections are displayed chronologically (**'settled=N'** attribute is set for all displayed bets (from response select 'Network' tab-> 'All' filter -> choose the last request that appears after bet line expanding ->'Preview' tab))
        """
        name = vec.lotto.LOTTO if self.brand == 'ladbrokes' else vec.lotto.LOTTO.upper()
        lotto_opened = self.site.open_bets.tab_content.grouping_buttons.click_button(name)
        self.assertTrue(lotto_opened, msg='Lotto tab is not opened')

        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        ui_bet_times = bet_times = [bet.date for bet_name, bet in bets.items()]
        bet_times.sort(key=lambda date: datetime.strptime(date, '%d.%m %I:%M %p'), reverse=True)
        self.assertListEqual(ui_bet_times, bet_times,
                             msg=f'sections on ui: "{ui_bet_times}" are not displayed chronologically: "{bet_times}"')

    def test_004_verify_information_in_bet(self):
        """
        DESCRIPTION: Verify information in bet section header
        DESCRIPTION: Verify bet details and check if bet details are same as in **OpenBet** system
        EXPECTED: Following information is displayed in bet section header:
        EXPECTED: *   Lottery name
        EXPECTED: Bet details are shown:
        EXPECTED: **User's pick** s : X, x, x, x, x
        EXPECTED: **Draw Type** : e.g. Monday Draw
        EXPECTED: **Draw Date** : date of draw
        EXPECTED: **Stake**: stake value
        EXPECTED: **Bet Receipt #**
        EXPECTED: **Bet placed at** : date of lotto bet placement
        """
        bet_name, bet = self.get_lotto_bet(draw_name=self.draw_name)
        balls = bet.balls.items_as_ordered_dict
        self.assertTrue(balls, msg='No balls found')
        balls_numbers = list(balls.keys())
        self.assertListEqual(self.selected_numbers, balls_numbers)
        stake = bet.stake.stake_value
        self.assertEqual(float(stake), float(self.bet_amount),
                         msg='Stake amount "%s" does not match expected bet amount "%s"' % (stake, self.bet_amount))
        bet_receipt = bet.bet_receipt_info.bet_receipt.value
        self.assertTrue(bet_receipt, msg='Betreceipt id was not found')
        bet_date = bet.bet_receipt_info.date.text
        self.assertTrue(bet_date, msg='Bet date was not found')

        self.assertEqual(bet_date, self.expected_bet_date,
                         msg=f'Bet date "{bet_date}" is not the same as expected "{self.expected_bet_date}"')
