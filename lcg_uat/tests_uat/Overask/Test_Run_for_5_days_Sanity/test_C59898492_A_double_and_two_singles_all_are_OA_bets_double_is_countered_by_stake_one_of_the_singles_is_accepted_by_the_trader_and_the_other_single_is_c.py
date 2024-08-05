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
class Test_C59898492_A_double_and_two_singles_all_are_OA_bets_double_is_countered_by_stake_one_of_the_singles_is_accepted_by_the_trader_and_the_other_single_is_countered_by_price(BaseBetSlipTest):
    """
    TR_ID: C59898492
    NAME: A double and two singles all are OA bets, double is countered by stake, one of the singles is accepted by the trader and the other single is countered by price
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

    def test_001_add_two__selections_to_betslip_enter_stake_for_two_singles_and_doubletrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(
            self):
        """
        DESCRIPTION: Add two  selections to Betslip ,Enter stake for two singles and Double
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
        if self.site.wait_logged_out():
            username = tests.settings.betplacement_user
            self.site.login(username)

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.5
        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section, multiples_section = sections.Singles, sections.Multiples
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
            self.enter_stake_amount(stake=stake)
        for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_offer_by_price_for_one_singlestake_for_double_and_accept_the_single(self):
        """
        DESCRIPTION: Counter offer by price for one single,stake for double and accept the single
        EXPECTED: Counter offer shows the double with the stake highlighted, the single countered with price has the price highlighted and the single which was accepted has neither the price nor the stake highlighted
        EXPECTED: All bets have a remove button, even the accepted bet.
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.event_ids)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        flag = False
        data = defaultdict(dict)

        for bet_id, bet_type in bets_details.items():
            if bet_type == 'SGL' and not flag:
                data['bet1']['id'] = bet_id
                data['bet1']['action'] = 'A'
                data['bet1']['bettype'] = bet_type
                flag = True
            elif bet_type == 'SGL' and flag:
                data['bet3']['id'] = bet_id
                data['bet3']['price'] = self.new_price
                data['bet3']['action'] = 'O'
                data['bet3']['bettype'] = bet_type
                data['bet3']['stake'] = self.bet_amount
                data['bet3']['price_changed'] = 'Y'
            elif bet_type == 'DBL':
                data['bet2']['id'] = bet_id
                data['bet2']['action'] = 'O'
                data['bet2']['stake'] = '0.4'
                data['bet2']['bettype'] = bet_type
                data['bet2']['price_changed_1'] = 'N'
                data['bet2']['price_changed_2'] = 'N'
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
        sections = self.get_betslip_sections().Singles
        acpt_stake_name, acpt_stake = list(sections.items())[0]
        ofr_price_stake_name, ofr_price_stake = list(sections.items())[1]
        self.assertTrue(acpt_stake.remove_button.is_displayed(),
                        msg=f'Remove button was not found for stake "{acpt_stake_name}"')
        self.assertTrue(ofr_price_stake.remove_button.is_displayed(),
                        msg=f'Remove button was not found for stake "{ofr_price_stake_name}"')
        stake_color = acpt_stake.offered_price.background_color_value
        self.assertNotEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                            msg=f'Accepted single stake is highlighted in yellow for "{acpt_stake_name}"')
        stake_color = ofr_price_stake.offered_price.background_color_value
        self.assertEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Offered single stake is not highlighted in yellow for "{ofr_price_stake_name}"')

        sections = self.get_betslip_sections(multiples=True).Multiples
        dbl_stake_name, dbl_stake = list(sections.items())[0]
        self.assertTrue(dbl_stake.remove_button.is_displayed(),
                        msg=f'Remove button was not found for stake "{dbl_stake_name}"')
        stake_color = dbl_stake.offered_stake.background_color_value
        self.assertEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified stake is not highlighted in yellow for "{dbl_stake_name}"')

    def test_003_if_user_accepts_the_bet(self):
        """
        DESCRIPTION: If user accepts the bet
        EXPECTED: Bet receipt shown to the customer.
        EXPECTED: Correct potential return should be shown
        EXPECTED: My Bets and Account History will show the bet.
        """
        betslip = self.get_betslip_content()
        est_return_betslip = betslip.total_estimate_returns
        betslip.confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        est_return_betreceipt = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(est_return_betslip, est_return_betreceipt, msg=f'Potential Return on betslip "{est_return_betslip}" '
                                                                        f'is not same as on bet receipt{est_return_betreceipt}')
        self.site.bet_receipt.close_button.click()
        for event_name in self.event_names:
            self.site.open_my_bets_open_bets()
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_in_open_bets=True, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_in_open_bets=True, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
            self.navigate_to_page('bet-history')
            self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_in_open_bets=True, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_in_open_bets=True, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)

    def test_004_if_offer_is_declined_by_user(self):
        """
        DESCRIPTION: If offer is declined by user
        EXPECTED: Then no bet is placed and My Bets and Account History reflect this.
        """
        self.event_ids.clear()
        self.selection_ids.clear()
        self.event_names.clear()
        self.test_001_add_two__selections_to_betslip_enter_stake_for_two_singles_and_doubletrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake()
        self.test_002_counter_offer_by_price_for_one_singlestake_for_double_and_accept_the_single()
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=10)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        for event_name in self.event_names:
            self.site.open_my_bets_open_bets()
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
            self.navigate_to_page('bet-history')
            self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
