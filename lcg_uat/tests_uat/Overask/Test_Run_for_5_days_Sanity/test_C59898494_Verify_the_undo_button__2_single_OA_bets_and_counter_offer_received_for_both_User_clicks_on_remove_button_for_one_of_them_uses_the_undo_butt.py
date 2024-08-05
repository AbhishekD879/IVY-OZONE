import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from collections import defaultdict
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898494_Verify_the_undo_button__2_single_OA_bets_and_counter_offer_received_for_both_User_clicks_on_remove_button_for_one_of_them_uses_the_undo_button_to_undo_his_her_actions_and_then_accepts_the_offer(BaseBetSlipTest):
    """
    TR_ID: C59898494
    NAME: Verify the undo button - 2 single OA bets and counter offer received for both. User clicks on remove button for one of them, uses the undo button to undo his/her actions and then accepts the offer
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.3
    max_mult_bet = 0.4
    prices = [{0: '1/12', 1: '1/10', 2: '1/9'},
              {0: '1/13', 1: '1/11', 2: '1/11'}]
    new_price = '1.5'
    selection_ids = []
    event_ids = []
    event_names = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        Expected: Created events
        """
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(
                default_market_name='|Draw No Bet|', lp=self.prices[i],
                max_bet=self.max_bet,
                max_mult_bet=self.max_mult_bet)
            self.event_names.append(f'{event_params.team1} v {event_params.team2}')
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(self.eventID)
        username = tests.settings.betplacement_user
        self.site.login(username)

    def test_001_add_two_single__selections__to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two single  selections  to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
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
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_counter_offer_by_price_for_both_singles(self):
        """
        DESCRIPTION: Counter offer by price for both singles
        EXPECTED: Counter offer with the new prices highlighted and updated potential returns shown  to the customer
        """
        bets_details = \
            self.bet_intercept.find_bets_for_review(events_id=self.event_ids)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        flag = False
        data = defaultdict(dict)

        for bet_id, bet_type in bets_details.items():
            if bet_type == 'SGL' and not flag:
                data['bet1']['id'] = bet_id
                data['bet1']['price'] = self.new_price
                data['bet1']['action'] = 'O'
                data['bet1']['bettype'] = bet_type
                data['bet1']['stake'] = self.bet_amount
                data['bet1']['price_changed'] = 'Y'
                flag = True
            elif bet_type == 'SGL' and flag:
                data['bet2']['id'] = bet_id
                data['bet2']['price'] = self.new_price
                data['bet2']['action'] = 'O'
                data['bet2']['bettype'] = bet_type
                data['bet2']['stake'] = self.bet_amount
                data['bet2']['price_changed'] = 'Y'

        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)
        self.site.wait_content_state_changed()
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=15)
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=10)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain "{cms_overask_expires_message}" from CMS')

    def test_003_verify_undo_button(self):
        """
        DESCRIPTION: Verify Undo button
        EXPECTED: Counter offer should show the remove button and then when clicked for one selection, should show the undo button.
        EXPECTED: Clicking on undo will put the counter offer back into its original state and clicking on the accept button should successfully place both bets.
        EXPECTED: The bet receipt, My Bets and Account History should show both bets in My Bets and Account History.
        """
        place_bet_button = self.get_betslip_content().confirm_overask_offer_button
        singles_section = self.get_betslip_sections().Singles
        ofr_price_stake_name, ofr_price_stake = list(singles_section.items())[0]
        self.assertTrue(ofr_price_stake.has_remove_button(),
                        msg=f'Remove button was not found for stake "{ofr_price_stake_name}"')
        ofr_price_stake.select()
        self.site.wait_content_state_changed()
        self.assertTrue(ofr_price_stake.undo_button.is_displayed(),
                        msg=f'Undo button was not found for stake "{ofr_price_stake_name}"')
        ofr_price_stake.undo_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(ofr_price_stake.is_displayed(), msg='selection 1 is not restored')
        self.assertTrue(ofr_price_stake.has_remove_button(), msg=f'Remove button is not present for "{ofr_price_stake_name}"')
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')
        place_bet_button.click()

        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        for event_name in self.event_names:
            self.site.open_my_bets_open_bets()
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
            self.navigate_to_page('bet-history')
            self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
            self.verify_bet_in_open_bets(event_name=event_name,
                                         bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
