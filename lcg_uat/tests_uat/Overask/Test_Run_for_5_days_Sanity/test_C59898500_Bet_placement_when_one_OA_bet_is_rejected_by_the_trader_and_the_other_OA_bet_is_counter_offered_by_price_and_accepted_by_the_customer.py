import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from collections import defaultdict
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898500_Bet_placement_when_one_OA_bet_is_rejected_by_the_trader_and_the_other_OA_bet_is_counter_offered_by_price_and_accepted_by_the_customer(BaseBetSlipTest):
    """
    TR_ID: C59898500
    NAME: Bet placement when one OA bet is rejected by the trader and the other OA bet is counter offered by price and accepted by the customer.
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1
    suggested_max_bet = 0.25
    prices = {0: '1/12'}
    new_price = '1/6'
    event_ids = []
    selection_ids = []
    event_names = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        for i in range(2):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices, max_bet=self.max_bet)
            self.event_ids.append(event_params.event_id)
            self.selection_ids.append(list(event_params.selection_ids.values())[0])
            self.event_names.append(event_params.ss_response['event']['name'])
        if self.site.wait_logged_out():
            self.__class__.username = tests.settings.betplacement_user
            self.site.login(self.username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_two_selection_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two selection to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=2)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_if_trader_rejects_one_oa_bet_and_the_other_oa_bet_is_counter_offered_by_price(self):
        """
        DESCRIPTION: If trader rejects one OA bet and the other OA bet is counter offered by price
        EXPECTED: The counter offer should show the bet that was not accepted with a 'trader did not accept...' message.
        EXPECTED: The other offer should have the price highlighted and show updated potential returns.
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.event_ids)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        flag = False
        data = defaultdict(dict)
        for bet_id, bet_type in bets_details.items():
            if bet_type == 'SGL' and not flag:
                data['bet1']['id'] = bet_id
                data['bet1']['action'] = 'D'
                data['bet1']['bettype'] = bet_type
                flag = True
            elif bet_type == 'SGL' and flag:
                data['bet2']['id'] = bet_id
                data['bet2']['price'] = self.new_price
                data['bet2']['action'] = 'O'
                data['bet2']['bettype'] = bet_type
                data['bet2']['stake'] = self.bet_amount
                data['bet2']['price_changed'] = 'Y'
        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)
        sections = self.get_betslip_sections(multiples=True).Singles
        event_2_price = list(sections.values())[1].offered_price
        odd_value = event_2_price.text.strip(' x')
        odd_value_color = event_2_price.background_color_value
        self.assertEqual(odd_value, self.new_price,
                         msg=f'Actual price :{odd_value} is not same as'
                             f'Expected price :{self.new_price}')
        self.assertEqual(odd_value_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR, msg=f'Modified price for stake is not highlighted in yellow')
        overask_warning_message = sections.overask_trader_offer.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
        self.__class__.actual_stake = self.get_betslip_content().total_stake
        expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=expected_return, bet_amount=self.actual_stake, odds=self.new_price)

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt.
        EXPECTED: Balance should be updated correctly
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.device.refresh_page()
        expected_user_balance = self.user_balance - float(self.actual_stake)
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0])
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_name=self.event_names[0])

    def test_004_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.event_ids.clear()
        self.event_names.clear()
        self.selection_ids.clear()
        self.test_000_preconditions()
        self.test_001_add_two_selection_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_if_trader_rejects_one_oa_bet_and_the_other_oa_bet_is_counter_offered_by_price()
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[0],
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[0],
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
