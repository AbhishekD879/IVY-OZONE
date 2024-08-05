import pytest
import tests
from voltron.environments import constants as vec
from collections import defaultdict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898455_Double_and_Singles_on_Football_Countered_by_Stake_for_Double_and_a_Price_for_one_of_the_Singles_and_user_removes_the_counter_single_and_places_the_bet(BaseBetSlipTest):
    """
    TR_ID: C59898455
    NAME: Double and Singles on Football Countered by Stake for Double and a Price for one of the Singles and user removes the counter single and places the bet
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.5
    prices = [{0: '1/5', 1: '1/3', 2: '1/4'},
              {0: '1/4', 1: '1/6', 2: '1/7'}]
    new_price = '1/2'
    new_stake = '0.7'
    eventIDs = []
    selectionIDs = []
    event_names = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        for i in range(0, 2):
            event = self.ob_config.add_autotest_premier_league_football_event(default_market_name='|Draw No Bet|',
                                                                              lp=self.prices[i], max_bet=self.max_bet)
            self.eventIDs.append(event.event_id)
            self.selectionIDs.append(event.selection_ids[event.team1])
            self.event_names.append(f'{event.team1} v {event.team2}')
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_add_two_selections_from_football_sport_to_betslip(self):
        """
        DESCRIPTION: Add two selections from Football sport to Betslip
        EXPECTED: Selections are added to betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.__class__.bet_amount = self.max_bet + 0.5
        self.open_betslip_with_selections(selection_ids=self.selectionIDs)

    def test_002_enter_stake_for_both_singles_and_doublestrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Enter stake for both singles and doubles
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section, multiples_section = sections.Singles, sections.Multiples
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
            self.enter_stake_amount(stake=stake)
        for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        self.__class__.initial_est_returns = self.site.betslip.total_estimate_returns
        bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_003_counter_by_stake_for_double_and_a_price_for_one_of_the_singles(self):
        """
        DESCRIPTION: Counter by Stake for Double and a Price for one of the Singles
        EXPECTED: Customer should be shown a counter offer with the stake for the double highlighted and the price of the single being highlighted.
        EXPECTED: Updated potential returns should be shown to the customer on FE
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.eventIDs)
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
                data['bet2']['stake'] = self.new_stake
                data['bet2']['bettype'] = bet_type
                data['bet2']['price_changed_1'] = 'N'
                data['bet2']['price_changed_2'] = 'N'
        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)
        overask_trader_message = wait_for_result(lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=10)
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=10)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain "{cms_overask_expires_message}" from CMS')

        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section, multiples_section = sections.Singles, sections.Multiples

        ofr_price_stake_name, self.__class__.ofr_price_stake = list(singles_section.items())[1]
        stake_color = self.ofr_price_stake.offered_price.background_color_value
        self.assertEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg='Counter offer by price for the single with a price of "{ofr_price_stake_name}" '
                             'is not highlighted in yellow')

        dbl_stake_name, dbl_stake = list(multiples_section.items())[0]
        stake_color = dbl_stake.offered_stake.background_color_value
        self.assertEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg='Counter offer by stake for the double with a stake of "{dbl_stake_name}" '
                             'is not highlighted in yellow')

        updated_est_returns = self.site.betslip.total_estimate_returns
        self.assertNotEqual(updated_est_returns, self.initial_est_returns,
                            msg='Updated potential returns is not shown on FE')

    def test_004_if__user_removes_the_counter_single_and_places_the_bet(self):
        """
        DESCRIPTION: If  user removes the counter single and places the bet
        EXPECTED: User should be able to remove the countered single and place the bet for double and one single.
        EXPECTED: The bet receipt should only show the double and one single and so should My Bets and Account History.
        """
        sections = self.get_betslip_sections().Singles
        stake = list(sections.values())[1]
        stake.select()
        self.site.wait_content_state_changed()
        self.assertTrue(stake.undo_button.is_displayed(),
                        msg=f'"{vec.betslip.OVERASK_ELEMENTS.undo}" button is not displayed for the bet "{self.event_names[0]}"')
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        single_section = bet_receipt_sections.get(vec.betslip.SINGLE).items_as_ordered_dict
        len_of_expected_singles = 1
        self.assertEqual(len(single_section), len_of_expected_singles,
                         msg=f'Length of singles section "{len(single_section)}" '
                             f'is not same as Expected length of singles "{len_of_expected_singles}"')
        double_section = bet_receipt_sections.get(vec.betslip.DBL).items_as_ordered_dict
        len_of_expected_doubles = 2
        self.assertEqual(len(double_section), len_of_expected_doubles,
                         msg=f'Length of double section "{len(double_section)}" '
                             f'is not same as Expected length of double section items "{len_of_expected_doubles}"')
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_names[0], bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        for event_name in self.event_names:
            self.verify_bet_in_open_bets(event_name=event_name, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_names[0], bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        for event_name in self.event_names:
            self.verify_bet_in_open_bets(event_name=event_name, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
