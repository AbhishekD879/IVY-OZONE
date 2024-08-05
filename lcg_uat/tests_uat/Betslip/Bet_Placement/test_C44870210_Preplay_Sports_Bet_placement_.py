import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from collections import OrderedDict
from random import sample
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.p1
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870210_Preplay_Sports_Bet_placement_(BaseCashOutTest):
    """
    TR_ID: C44870210
    NAME: Preplay Sports Bet placement "
    DESCRIPTION: this test case verify - Customer places single, double and complex bets on football, Cricket, Basketball sports verify Accumulator bets,YAN,PAT,TRX,CAN etc complex bet types
    PRECONDITIONS: UserName: goldenbuild1   Password: Password1
    """
    keep_browser_open = True

    def get_selection_detail(self, event):
        if tests.settings.backend_env == 'prod':
            selection_details = OrderedDict()
            selection_details.update({'event_name': event['event']['name']})
            selection_details.update({'market_name': event['event']['children'][0]['market']['templateMarketName']})
            outcomes = event['event']['children'][0]['market']['children']
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        else:
            selection_details = OrderedDict()
            selection_details.update({'event_name': f'{event.team1} v {event.team2}'})
            selection_details.update({'market_name': self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')})
            selection_ids = event.selection_ids
        if list(selection_ids.keys())[0] == 'Draw':
            selection_details.update({'selection_names': list(selection_ids.keys())[1]})
            selection_details.update({'selection_ids': list(selection_ids.values())[1]})
        else:
            selection_details.update({'selection_names': list(selection_ids.keys())[0]})
            selection_details.update({'selection_ids': list(selection_ids.values())[0]})
        return selection_details

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: HomePage opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_make_sure_the_user_is_logged_into_their_account(self):
        """
        DESCRIPTION: Make sure the user is logged into their account
        EXPECTED: User logged in
        """
        self.site.login()

    def test_003_the_users_account_balance_is_sufficient_to_cover_a_bet_stake(self):
        """
        DESCRIPTION: The User's account balance is sufficient to cover a bet stake
        EXPECTED: Header balance displayed sufficient balance
        """
        self.__class__.balance = self.site.header.user_balance
        self.assertGreaterEqual(self.balance, self.bet_amount, msg=f'{self.balance} not greater than or equal to {self.bet_amount}')

    def test_004_go_to_football_preplay_event_make_a_selection_and_add_to_betslip(self, number_of_events=1):
        """
        DESCRIPTION: Go to football preplay event, make a selection and add to betslip
        EXPECTED: Selection added to betslip
        """
        self.__class__.all_selection_details = OrderedDict()
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True, in_play_event=False)
            events = sample(events, k=number_of_events)
            self.assertEquals(len(events), number_of_events, msg=f'Expected number of events: {number_of_events} '
                                                                 f'actual number of events: {len(events)}')
            all_selections = []
            for event in events:
                selection_detail = self.get_selection_detail(event)
                all_selections.append(selection_detail)
            for k in selection_detail.keys():
                self.all_selection_details[k] = list(all_selection_details[k] for all_selection_details in all_selections)
            self.open_betslip_with_selections(selection_ids=self.all_selection_details['selection_ids'])
        else:
            events = self.create_several_autotest_premier_league_football_events(number_of_events=number_of_events)
            self.assertEquals(len(events), number_of_events, msg=f'Expected number of events: {number_of_events} '
                                                                 f'actual number of events: {len(events)}')
            all_selections = []
            for event in events:
                selection_detail = self.get_selection_detail(event)
                all_selections.append(selection_detail)
            for k in selection_detail.keys():
                self.all_selection_details[k] = list(
                    all_selection_details[k] for all_selection_details in all_selections)
            self.open_betslip_with_selections(selection_ids=self.all_selection_details['selection_ids'])

    def test_005_verify_selection_details_in_betslip(self, bet_type=None):
        """
        DESCRIPTION: Verify Selection details in betslip
        EXPECTED: Event Name
        EXPECTED: Market Name
        EXPECTED: Event time
        EXPECTED: Odds
        EXPECTED: Sake box
        EXPECTED: Potential retus etc are displayed in betslip
        """
        section = self.get_betslip_sections().Singles
        for i in range(self.betslip_counter):
            selection_name, self.__class__.stake = list(section.items())[i]
            self.assertIn(selection_name, self.all_selection_details['selection_names'][i], msg=f'Expected selection {self.all_selection_details["selection_names"][i]} actual selection in betslip {selection_name}')
            self.assertTrue(self.stake.amount_form.is_displayed(), msg='stake box is not displayed')
            self.assertIn(self.stake.event_name, self.all_selection_details['event_name'][i], msg=f'Expected event {self.all_selection_details["event_name"][i]} actual event in betslip {self.stake.event_name}')
            self.assertTrue(self.stake.market_name == self.all_selection_details['market_name'][i] or
                            self.stake.market_name == 'Match Result', msg=f'Expected Market '
                                                                          f'{self.all_selection_details["market_name"][i]} or Match Result, actual market {self.stake.market_name}')
            self.assertTrue(self.stake.odds, msg='Odd is not displayed')
        if bet_type == vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE or bet_type == vec.bet_history._bet_types_ACC4:
            sections = self.get_betslip_sections(multiples=True)
            multiples_section = sections.Multiples
            stake_name, self.__class__.stake = list(multiples_section.items())[0]
            self.assertTrue(self.stake.odds, msg='Odd is not displayed for multiple bet')
            self.assertTrue(self.stake.amount_form.is_displayed(), msg='stake box is not displayed')
        self.assertTrue(self.get_betslip_content().total_stake, msg='Total stake is not present')
        self.assertTrue(self.get_betslip_content().total_estimate_returns, msg='Total estimated return is not present')

    def test_006_verify_bet_receipt_displaying_after_clickingtapping_the_place_bet_button_and_verify_bet_is_placed_successfully(
            self, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, expected_betslip_counter_value=0):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Place Bet' button and verify Bet is placed successfully
        EXPECTED: Bet is placed successfully
        EXPECTED: User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: Bet Slip is replaced with a Bet Receipt view
        """
        balance = self.site.header.user_balance
        self.__class__.expected_betslip_counter_value = expected_betslip_counter_value
        if bet_type == vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE:
            bet_info = self.place_and_validate_single_bet()
        if bet_type == vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE or bet_type == vec.bet_history._bet_types_ACC4:
            bet_info = self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        receipt_header = self.site.bet_receipt.receipt_header
        self.assertTrue(receipt_header.is_displayed(timeout=15),
                        msg='Receipt header is not displayed')
        receipt_footer = self.site.bet_receipt.footer
        self.assertTrue(receipt_footer.is_displayed(timeout=5),
                        msg='Receipt footer is not displayed')
        self.assertEqual(receipt_header.bet_placed_text, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{receipt_header.bet_placed_text}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        self.assertTrue(receipt_footer.has_reuse_selections_button(),
                        msg=f'"{receipt_footer.reuse_selection_button.name}" is not displayed')
        self.assertTrue(receipt_footer.has_done_button(),
                        msg=f'"{receipt_footer.done_button.name}" is not displayed')
        self.assertTrue(self.site.header.user_balance, msg='User Balance is not available')
        current_balance = self.site.header.user_balance
        expected_current_balance = balance - bet_info['total_stake']
        self.assertEqual(round(expected_current_balance, 2), current_balance,
                         msg=f'Expected balance: {round(expected_current_balance, 2)} actual balance: {current_balance}')

    def test_007_verify_bet_receipt_layout(self):
        """
        DESCRIPTION: Verify Bet Receipt layout
        EXPECTED: Bet Receipt header and subheader
        EXPECTED: Card with selections information
        EXPECTED: 'Reuse Selections' and 'Go Betting' buttons
        """
        #  This step is covered in scope of test_006

    def test_008_verify_bet_receipt_header(self):
        """
        DESCRIPTION: Verify Bet Receipt header
        EXPECTED: Bet Receipt header contains the following elements:
        EXPECTED: * 'X' button
        EXPECTED: * 'Bet Receipt' title
        EXPECTED: * 'User Balance' button
        """
        if self.device_type == 'mobile':
            self.assertEqual(self.site.bet_receipt.bet_receipt_header_name, vec.betslip.BET_RECEIPT,
                             msg=f'Page title "{self.site.bet_receipt.bet_receipt_header_name}" is '
                                 f'not the same as expected "{vec.betslip.BET_RECEIPT}"')
            self.assertTrue(self.site.bet_receipt.close_button, msg='X button is not available')

    def test_009_repeat_steps_4_to_8_for_different_sports_and_multiple__complex_bet(self):
        """
        DESCRIPTION: Repeat steps #4 to #8 for different sports and Multiple & complex bet
        EXPECTED:
        """
        bet_types = {vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE: 2, vec.bet_history._bet_types_ACC4: 4}
        for bet_type in range(len(bet_types)):
            self.test_003_the_users_account_balance_is_sufficient_to_cover_a_bet_stake()
            self.test_004_go_to_football_preplay_event_make_a_selection_and_add_to_betslip(number_of_events=list(bet_types.values())[bet_type])
            self.test_005_verify_selection_details_in_betslip(bet_type=list(bet_types.keys())[bet_type])
            self.test_006_verify_bet_receipt_displaying_after_clickingtapping_the_place_bet_button_and_verify_bet_is_placed_successfully(bet_type=list(bet_types.keys())[bet_type])
            self.test_007_verify_bet_receipt_layout()
            self.test_008_verify_bet_receipt_header()
