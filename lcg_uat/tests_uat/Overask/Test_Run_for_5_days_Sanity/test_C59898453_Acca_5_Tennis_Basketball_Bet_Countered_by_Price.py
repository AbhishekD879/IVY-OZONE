import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.uat
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.acca
@vtest
class Test_C59898453_Acca_5_Tennis_Basketball_Bet_Countered_by_Price(BaseBetSlipTest):
    """
    TR_ID: C59898453
    NAME: Acca 5 Tennis/Basketball Bet Countered by Price
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_mult_bet = 0.35
    max_bet = 0.25
    prices = [{'odds_home': '1/5', 'odds_away': '1/6'},
              {'odds_home': '1/10', 'odds_away': '1/6'},
              {'odds_home': '1/15', 'odds_away': '1/6'},
              {'odds_home': '1/20', 'odds_away': '1/6'},
              {'odds_home': '1/25', 'odds_away': '1/6'}]
    new_prices = ['1/7', '1/9']
    selection_ids = []
    event_names = []

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        for i in range(0, 5):
            event_params = self.ob_config.\
                add_tennis_event_to_autotest_trophy(lp=self.prices[i], max_mult_bet=self.max_mult_bet, max_bet=self.max_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_names.append(event_params.ss_response['event']['name'])
        if self.site.wait_logged_out():
            self.__class__.username = tests.settings.betplacement_user
            self.site.login(self.username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_five_selections_from_tennisbasketball_sport_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add five selections from Tennis/Basketball sport to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 5
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_by_price_for_one_of_the_selection_in_ob_ti_tool(self, new_price=None):
        """
        DESCRIPTION: Counter by Price for one of the selection in OB TI tool
        EXPECTED: Counter offer with the new price highlighted and updated potential returns shown to the customer on FE
        """
        if not new_price:
            new_price = self.new_prices[0]
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.\
            offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                  betslip_id=betslip_id, max_bet=self.max_bet,
                                  price_1=new_price, price_2=self.prices[1]['odds_home'],
                                  price_3=self.prices[2]['odds_home'])
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask panel is not closed')

        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

        self.__class__.sections = self.get_betslip_sections(multiples=True).Multiples
        stakes = list(self.sections.overask_trader_offer.items_as_ordered_dict.values())[0].stake_odds
        actual_price = stakes.value
        odd_color = stakes.value_color
        self.assertEqual(odd_color,
                         vec.colors.OVERASK_MODIFIED_PRICE_COLOR, msg=f'Modified price for stake is not highlighted in yellow')

        self.assertEqual(actual_price, new_price,
                         msg=f'Actual price :{actual_price} is not same as'
                             f'Expected price :{new_price}')
        expected_return = self.get_betslip_content().total_estimate_returns
        self.prices[0]['odds_home'] = new_price
        combined_odd = self.calculate_combined_odd(prices_list=self.prices)
        self.verify_estimated_returns(est_returns=expected_return, odds=combined_odd, bet_amount=self.max_bet)

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: Balance should be updated correctly
        """
        actual_stake = self.sections.overask_trader_offer.stake_content.stake_value.value.strip('£')
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.device.refresh_page()
        expected_user_balance = self.user_balance - float(actual_stake)
        self.verify_user_balance(expected_user_balance=expected_user_balance)

    def test_004_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.BET_TYPES.ACC5, event_name=self.event_names[0])
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.BET_TYPES.ACC5, event_name=self.event_names[0])

    def test_005_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        self.selection_ids.clear()
        self.event_names.clear()
        self.test_000_preconditions()
        self.test_001_add_five_selections_from_tennisbasketball_sport_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_counter_by_price_for_one_of_the_selection_in_ob_ti_tool(new_price=self.new_prices[1])
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[1], bet_in_open_bets=False, bet_type=vec.bet_history.BET_TYPES.ACC5)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[1], bet_in_open_bets=False, bet_type=vec.bet_history.BET_TYPES.ACC5)
