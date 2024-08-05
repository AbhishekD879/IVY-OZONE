import voltron.environments.constants as vec
import tests
import pytest
from tests.base_test import vtest
from collections import defaultdict
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.overask
@vtest
class Test_C59898493_2_single_OA_bets__counter_offer_returned_for_both_and_the_user_removes_one_and_the_accepts_the_other(BaseBetSlipTest):
    """
    TR_ID: C59898493
    NAME: 2 single OA bets - counter offer returned for both and the user removes one and the accepts the other.
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.3
    max_mult_bet = 0.5
    prices = [{0: '1/12', 1: '1/10', 2: '1/9'},
              {0: '1/13', 1: '1/11', 2: '1/11'}]
    new_price = '1.5'
    selection_ids = []
    event_ids = []
    event_names = []

    def test_001_add_two_single_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two single selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(
                default_market_name='|Draw No Bet|', lp=self.prices[i],
                max_bet=self.max_bet,
                max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)
            self.event_names.append(f'{event_params.team1} v {event_params.team2}')

        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.5
        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section = sections.Singles
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
            self.enter_stake_amount(stake=stake)
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_offer_by_price_for_both_singles(self):
        """
        DESCRIPTION: Counter offer by price for both singles
        EXPECTED: Counter offer with the new prices highlighted and updated potential returns shown to the customer
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.event_ids)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        flag = False
        data = defaultdict(dict)

        for bet_id, bet_type in bets_details.items():
            if not flag:
                data['bet1']['id'] = bet_id
                data['bet1']['price'] = self.new_price
                data['bet1']['action'] = 'O'
                data['bet1']['bettype'] = bet_type
                data['bet1']['stake'] = self.bet_amount
                data['bet1']['price_changed'] = 'Y'
                flag = True
            else:
                data['bet2']['id'] = bet_id
                data['bet2']['price'] = self.new_price
                data['bet2']['action'] = 'O'
                data['bet2']['bettype'] = bet_type
                data['bet2']['stake'] = self.bet_amount
                data['bet2']['price_changed'] = 'Y'
        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=10)
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=10)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain "{cms_overask_expires_message}" from CMS')
        expected_est_return = 2 * float(self.new_price) * float(self.bet_amount)

        self.__class__.sections = self.get_betslip_sections().Singles
        for stake_name, stake in self.sections.items():
            self.assertTrue(stake.remove_button.is_displayed(),
                            msg=f'Remove button was not found for stake "{stake_name}"')
            stake_color = stake.offered_price.background_color_value
            self.assertEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                             msg=f'Offered single stake is not highlighted in yellow for "{stake_name}"')

        est_return_betslip = self.get_betslip_content().total_estimate_returns
        self.assertEqual(expected_est_return, float(est_return_betslip), msg=f'Actual potential returns "{expected_est_return}" '
                                                                             f'is not matching with potential returns "{est_return_betslip}" shown on betslip')

    def test_003_verify_remove_button(self):
        """
        DESCRIPTION: Verify Remove button
        EXPECTED: User should be able to remove one of the singles and then accept the offer for the other single.
        EXPECTED: Bet receipt, My Bets and Account History should only show the bet accepted by the user.
        """
        stake = list(self.sections.values())[0]
        stake.select()
        self.site.wait_content_state_changed()
        self.assertTrue(stake.undo_button.is_displayed(), msg=f'Undo button is not displayed for the bet "{self.event_names[0]}"')
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[0],
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.verify_bet_in_open_bets(event_name=self.event_names[1],
                                     bet_in_open_bets=True, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[0],
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.verify_bet_in_open_bets(event_name=self.event_names[1],
                                     bet_in_open_bets=True, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
