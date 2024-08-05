from random import choice
import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from datetime import datetime


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.bet_placement
@pytest.mark.safari
@pytest.mark.sanity
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-31020')
@vtest
class Test_C874321_Place_Lotto_Bet(BaseUserAccountTest):
    """
    TR_ID: C874321
    NAME: Place Lotto Bet
    DESCRIPTION: Bet Placement - Verify that the customer can place a Lotto bet
    """
    bet_amount = 0.55
    keep_browser_open = True
    lotto_tab_draw_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to Oxygen app
        DESCRIPTION: Make sure that there are funds available (if not - top up the account)
        """
        username = tests.settings.betplacement_user
        self.site.login(username=username, async_close_dialogs=False)
        self.site.wait_content_state(state_name='Homepage')
        if self.site.header.user_balance == '':
            self.deposit_with_existing_card_via_cashier(username=username, amount=5)
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_FRAC)
        self.assertTrue(format_changed, msg='Odds format is not changed to fractional')

    def test_001_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to Lotto page
        EXPECTED: Lotto page is loaded
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state('lotto')

    def test_002_click_tap_on_a_random_lottery_49s_german_french_etc(self):
        """
        DESCRIPTION: Click/Tap on a random Lottery (49's/ German/ French etc.)
        EXPECTED: Specific Lottery page is displayed.
        """
        self.__class__.lotto = self.site.lotto
        carousel = self.lotto.lotto_carousel
        self.assertTrue(carousel.is_displayed(), msg='Lottery Selector Carousel isn\'t present on Lotto page')
        lotteries = carousel.items_as_ordered_dict
        self.assertTrue(lotteries, msg='No lotteries found in lotto carousel menu')
        random_lottery = choice(list(lotteries.keys()))
        lottery = lotteries.get(random_lottery)
        self.assertTrue(lottery, msg=f'"{random_lottery}" is not found among lotto carousel menu items')
        carousel.click_item(item_name=lottery.name)
        self.__class__.tab_content = self.lotto.tab_content
        expected_lottery = random_lottery if self.brand == 'ladbrokes' else random_lottery.upper()
        self.assertEqual(lottery.name, expected_lottery,
                         msg=f'Actual lottery name: "{lottery.name}" '
                             f'is not as expected: "{expected_lottery}"')

    def test_003_click_on_lucky_5_button(self):
        """
        DESCRIPTION: Click on Lucky 5 button
        EXPECTED: 5 Random numbers are selected and displayed to the customer
        """
        self.__class__.tab_content = self.site.lotto.tab_content
        lucky_buttons = self.tab_content.lucky_buttons.items_as_ordered_dict
        self.assertTrue(lucky_buttons, msg='Lucky Numbers are not present')
        self.assertIn(vec.lotto.LUCKY_5, lucky_buttons, msg=f'"{vec.lotto.LUCKY_5}" button is not among lucky buttons.')
        lucky_buttons[vec.lotto.LUCKY_5].click()
        number_selectors = wait_for_result(lambda: self.tab_content.number_selectors.items_as_ordered_dict,
                                           name='Number selector list is loaded',
                                           timeout=2,
                                           bypass_exceptions=VoltronException)
        self.assertTrue(number_selectors, msg='Number selectors not found')
        self.__class__.selected_numbers = [number_text.split(' ')[1] for number_text, number in
                                           number_selectors.items() if '-' not in number_text]

    def test_004_add_a_random_stake(self):
        """
        DESCRIPTION: Add a random Stake
        EXPECTED: 1£-10£ - currency sign should be the same as account's currency
        """
        self.tab_content.bet_amount.value = self.bet_amount
        self.__class__.user_currency = self.site.header.user_balance_section.currency_symbol

        lotto_bet_currency = self.tab_content.currency
        self.assertEqual(lotto_bet_currency, self.user_currency,
                         msg=f'Currency on lotto page is not equal to user currency "{self.user_currency}" and is "{lotto_bet_currency}" instead.')

    def test_005_click_on_place_bet_for_xxxx(self):
        """
        DESCRIPTION: Click on "Place Bet for £xx.xx"
        EXPECTED: The button changes it's state form "Place Bet" green button to "Confirm?" orange button
        EXPECTED: Currency sign should be the same as account's currency
        """
        place_bet_btn = self.tab_content.place_bet
        self.assertTrue(place_bet_btn.is_enabled(timeout=10), msg='Place Bet button does not active')
        place_bet_btn.click()
        self.__class__.confirm_bet_button = self.tab_content.confirm_bet
        self.assertTrue(self.tab_content.has_confirm_bet_button(), 'Confirm bet button is not present.')
        confirm_bet_button_text = self.tab_content.confirm_bet_text
        expected_confirm_bet_button_text = vec.lotto.CONFIRM
        self.assertEqual(confirm_bet_button_text, expected_confirm_bet_button_text,
                         msg=f'Confirm bet button text is not "{expected_confirm_bet_button_text}" and is "{confirm_bet_button_text}" instead.')
        confirm_bet_button_color = self.confirm_bet_button.css_property_value('background-color')
        expected_confirm_bet_button_color = 'rgb(245, 107, 35)' if self.is_safari else 'rgba(245, 107, 35, 1)'
        self.assertEqual(confirm_bet_button_color, expected_confirm_bet_button_color,
                         msg=f'Confirm bet button color is not orange "{expected_confirm_bet_button_color}" and is "{confirm_bet_button_color}" instead.')
        self.__class__.lotto_tab_odds = self.tab_content.odd_value
        draw_checkboxes = self.tab_content.draw_checkboxes.items_as_ordered_dict
        self.assertTrue(draw_checkboxes, msg='Draw checkboxes not found')
        self.__class__.lotto_tab_draw_name = next((checkbox.name for _, checkbox in draw_checkboxes.items() if checkbox.value), None)
        if not self.lotto_tab_draw_name:
            # looks like for some reason sometimes first draw checkbox is not selected
            # so let's select it just manually as real user'd like selected it
            list(draw_checkboxes.values())[0].value = True
            self.__class__.lotto_tab_draw_name = next(
                (checkbox.name for _, checkbox in draw_checkboxes.items() if checkbox.value), None)
        self.assertTrue(self.lotto_tab_draw_name,
                        msg=f'There is no selected draw "{self.lotto_tab_draw_name}" in "{draw_checkboxes.keys()}"')

    def test_006_click_on_confirm_button(self):
        """
        DESCRIPTION: Click on "Confirm?" button
        EXPECTED: The bet is successfully placed and bet confirmation is displayed.
        EXPECTED: The currency is the same as account's currency. - verified in next step
        """
        self.confirm_bet_button.click()
        self.site.wait_content_state('LottoBetReceipt')

    def test_007_verify_the_bet_confirmation(self):
        """
        DESCRIPTION: Verify the Bet Confirmation
        EXPECTED: The currency is the same as account's currency.
        EXPECTED: Lottery Name (Draw);
        EXPECTED: Date when the Draw Starts;
        EXPECTED: The bet type is displayed: (e.g: Match 5);
        EXPECTED: Same Selection of numbers is displayed where the bet was placed;
        EXPECTED: Odds are exactly the same as when bet has been placed;
        EXPECTED: Stake is correctly displayed;
        EXPECTED: Total Stake is correctly displayed;
        EXPECTED: Potential Returns is exactly the same as when bet has been placed;
        EXPECTED: Date and time when Bet was placed.
        """
        self.__class__.receipt = self.site.lotto_receipt.tab_content.section_list
        currency = self.receipt.total_stake_currency
        self.assertEqual(currency, self.user_currency,
                         msg=f'Currency on lotto receipt is not equal to user currency "{self.user_currency}" and is "{currency}" instead.')
        self.assertTrue(self.receipt.name, msg='Receipt Name is not shown')
        self.__class__.receipt_event_name = self.receipt.event_name
        self.assertTrue(self.receipt_event_name, msg='Event Name on Receipt is not shown')
        self.assertIn(self.lotto_tab_draw_name, self.receipt_event_name,
                      msg=f'Event Name is not the same as on lotto page "{self.lotto_tab_draw_name}" and is "{self.receipt_event_name}"')
        self.assertTrue(self.receipt.bet_type, msg='Bet Type is not shown')
        self.assertTrue(self.receipt.bet_selections, msg='Bet Selections are not shown')
        numbers_on_receipt = self.receipt.bet_selections.split()
        self.assertEqual(self.selected_numbers, numbers_on_receipt,
                         msg=f'Numbers on bet receipt "{numbers_on_receipt}" are not the ones previously selected "{self.selected_numbers}".')
        odds = self.receipt.bet_odds
        odds_multiplier = odds.split('/')[0]
        self.assertEqual(odds, self.lotto_tab_odds,
                         msg=f'Bet Odds are not the same as on lotto page "{self.lotto_tab_odds}" and are "{odds}" instead.')
        stake = self.receipt.bet_stake_value
        self.assertEqual(stake, self.bet_amount,
                         msg=f'Bet Stake is not the same as "{self.bet_amount}" and equals "{stake}" instead.')
        total_stake = float(self.receipt.total_stake)
        self.assertEqual(total_stake, self.bet_amount,
                         msg=f'Total Stake is not the same as "{self.bet_amount}" and equals "{total_stake}" instead.')
        expected_return = "{0:.2f}".format(self.bet_amount * int(odds_multiplier) + self.bet_amount)
        potential_return = self.receipt.potential_return.replace(',', '')
        self.assertEqual(potential_return, expected_return,
                         msg=f'Potential Returns do not equal "{expected_return}" and are "{potential_return}" instead.')
        self.assertTrue(self.receipt.bet_placed, msg='Bet placed time is not shown')

    def test_008_click_on_done_button(self):
        """
        DESCRIPTION: Click on "Done" button
        EXPECTED: The customer is redirected back to Lotto page
        """
        self.receipt.done_button.click()
        self.site.wait_content_state('lotto')

    def test_009_click_on_my_bets_button_from_the_header_and_navigate_to_open_bets___lotto_page(self):
        """
        DESCRIPTION: Click on My Bets button from the header and navigate to Open Bets -> Lotto page
        EXPECTED: The Lotto page from My Bets -> Open Bets is opened
        """
        self.site.open_my_bets_open_bets()
        lotto_opened = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
        self.assertTrue(lotto_opened, msg='Lotto tab is not opened')

    def test_010_go_to_the_bet_that_was_just_placed_and_verify_that_the_bet_receipt_fields_are_correct(self):
        """
        DESCRIPTION: Go to the bet that was just placed and Verify that the Bet Receipt fields are correct.
        EXPECTED: User's picks : X, x, x, x, x
        EXPECTED: Draw Type : e.g. Monday Draw
        EXPECTED: Draw Date : date of draw
        EXPECTED: Stake: stake value
        EXPECTED: Bet Receipt #
        EXPECTED: Bet placed at : date of lotto bet placement
        """
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No Lotto bets found')
        last_bet_name, last_bet = list(bets.items())[0]
        users_picks = list(last_bet.balls.items_as_ordered_dict)
        self.assertTrue(users_picks, msg='User\'s picks are not found.')
        self.assertEqual(users_picks, self.selected_numbers,
                         msg=f'User\'s picks "{users_picks}" are not the same as previously selected "{self.selected_numbers}".')
        draw_name = last_bet.draw_name
        self.assertEqual(draw_name, self.lotto_tab_draw_name,
                         msg=f'Draw type is not the same as on lotto tab "{self.lotto_tab_draw_name}" and is "{draw_name}" instead.')
        receipt_draw_date = self.receipt_event_name.split(', ')[1]
        date = receipt_draw_date.split()[0]
        time = receipt_draw_date.split()[1]
        am_pm = receipt_draw_date.split()[2].lower()
        receipt_draw_date_modified = date + ' ' + time + ' ' + am_pm
        self._logger.info(f'*** receipt_draw_date_modified "{receipt_draw_date_modified}"')
        my_bets_draw_date = last_bet.date

        # Uncomment assert below once BMA-31020 is fixed.
        # self.assertEqual(receipt_draw_date, my_bets_draw_date,
        #                  msg=f'Draw date does not equal the date from bet receipt "{receipt_draw_date}" and equals "{my_bets_draw_date}" instead.')

        # Workaround for BMA-31020 (reproduced only via Jenkins):
        date = my_bets_draw_date.split()[0]
        time = my_bets_draw_date.split()[1]
        am_pm = my_bets_draw_date.split()[2].lower()
        hours = time.split(':')[0]
        minutes = time.split(':')[1]
        amended_hours = str(int(hours) - 1)  # 1 hour difference adjusted because of different time zone in jenkins.
        if hours == '12' and am_pm == 'am':
            am_pm = 'pm'
        elif hours == '12' and am_pm == 'pm':
            am_pm = 'am'
        my_bet_hr = datetime.strptime(amended_hours, "%H")
        my_bet_amended_hr = my_bet_hr.strftime("%I")
        if my_bet_amended_hr < '10':
            my_bet_amended_hr = my_bet_amended_hr[1:]
        my_bets_draw_date_amended = date + ' ' + my_bet_amended_hr + ':' + minutes + ' ' + am_pm
        possible_dates = [my_bets_draw_date,
                          my_bets_draw_date_amended]
        self._logger.info(f'*** receipt_draw_date "{receipt_draw_date}"')
        self._logger.info(f'*** my_bets_draw_date "{my_bets_draw_date}"')
        self._logger.info(f'*** my_bets_draw_date_amended "{my_bets_draw_date_amended}"')
        self.assertIn(receipt_draw_date_modified, possible_dates,
                      msg=f'Draw date does not equal the date from bet receipt "{receipt_draw_date}" and equals "{my_bets_draw_date}" instead.'
                          f'date = "{date}" '
                          f'time = "{time}" '
                          f'am_pm = "{am_pm}" '
                          f'hours = "{hours}" '
                          f'amended hours = "{amended_hours}", '
                          f'my_bets_draw_date_amended = "{my_bets_draw_date_amended}"')
        # End of workaround

        stake = float(last_bet.stake.stake_value)
        self.assertEqual(stake, self.bet_amount,
                         msg=f'Stake does not equal "{self.bet_amount}" and equals "{stake}" instead')

        self.assertTrue(last_bet.bet_receipt_info.bet_id, msg='Bet receipt ID is not present.')
        self.assertTrue(last_bet.bet_receipt_info.date.name, msg='Placed date is not present.')
